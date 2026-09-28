from __future__ import annotations
from ..catalog import live_or_static_catalog, examples, business_glossary, security_policy
from ..vector_store import SchemaVectorStore
from ..database import sample_distinct
from ..config import settings

_store: SchemaVectorStore | None = None

def get_store():
    global _store
    if _store is None:
        _store = SchemaVectorStore()
        if _store.tables.count() == 0 or _store.columns.count() == 0:
            _store.index_catalog(live_or_static_catalog(), examples())
    return _store

def include_join_tables(selected, catalog):
    """Include intermediate tables only for unique shortest verified join paths."""
    from collections import deque
    from itertools import combinations
    graph = {table: set() for table in catalog['tables']}
    for rel in catalog.get('relationships', []):
        a, b = rel['from_table'], rel['to_table']
        if a in graph and b in graph:
            graph[a].add(b)
            graph[b].add(a)
    result = list(selected)
    for source, target in combinations(selected, 2):
        queue = deque([source])
        distances, ways, parent = {source: 0}, {source: 1}, {}
        while queue:
            current = queue.popleft()
            for neighbor in sorted(graph[current]):
                distance = distances[current] + 1
                if neighbor not in distances:
                    distances[neighbor] = distance
                    ways[neighbor] = ways[current]
                    parent[neighbor] = current
                    queue.append(neighbor)
                elif distances[neighbor] == distance:
                    ways[neighbor] += ways[current]
        if target not in distances or ways[target] != 1:
            continue  # Do not invent a connection or choose an ambiguous path.
        current = target
        while current != source:
            if current not in result:
                result.append(current)
            current = parent[current]
    if len(result) > settings.top_tables:
        raise ValueError('Verified join paths require more tables than TOP_TABLES allows. Increase TOP_TABLES or narrow the request.')
    return result


def retrieve_context(state):
    catalog = live_or_static_catalog()
    plan = state.get('plan', {})
    intent = state.get('intent', {})
    query = plan.get('retrieval_query') or state['question']
    required = list(dict.fromkeys(t for t in plan.get('tables', []) if t in catalog['tables']))
    identified = required or list(dict.fromkeys(
        t for t in intent.get('required_tables', []) if t in catalog['tables']))
    if len(identified) > settings.top_tables:
        raise ValueError('The query requires more tables than TOP_TABLES allows. Narrow the request or increase TOP_TABLES.')
    # Confidence is the existing intent model score, not a vector distance.
    # Do not pad a confident selection with unrelated nearest neighbours.
    if intent.get('confidence', 0) > 0.75 and identified:
        selected = identified
        candidates = examples()
    else:
        result = get_store().retrieve(query, catalog)
        selected = list(dict.fromkeys(identified + [
            t for t in result['tables'] if t in catalog['tables']
        ]))[:settings.top_tables]
        candidates = result['examples']
    selected = include_join_tables(selected, catalog)
    selected_set = set(selected)
    selected_examples = [ex for ex in candidates
                         if ex.get('tables') and set(ex['tables']).issubset(selected_set)][:settings.top_examples]

    # Rebuild exact context for selected tables so planner-required tables cannot be lost by vector ranking.
    context = {'tables': {}}
    for table in selected:
        info = catalog['tables'][table]
        context['tables'][table] = {
            'description': info.get('description',''),
            'columns': info.get('columns',{}),
            'foreign_keys': info.get('foreign_keys',[]),
            'live_columns': info.get('live_columns', []),
        }
    glossary = dict(business_glossary())
    glossary['query_rules'] = {t: rules for t, rules in glossary.get('query_rules', {}).items()
                              if t in selected_set}
    glossary['synonyms'] = [entry for entry in glossary.get('synonyms', [])
                            if entry.get('maps_to', '').split('.')[0] in selected_set]
    context['business_glossary'] = glossary
    context['verified_relationships'] = [rel for rel in catalog.get('relationships', [])
                                         if rel['from_table'] in selected and rel['to_table'] in selected]

    sampled = {}
    if settings.enable_data_sampling:
        policy = security_policy()
        for table in selected:
            for column in policy.get('sample_value_columns', {}).get(table, []):
                if column in catalog['tables'].get(table, {}).get('columns', {}):
                    try: sampled[f'{table}.{column}'] = sample_distinct(table, column)
                    except Exception: pass
    return {'schema_context': context, 'retrieved_tables': selected, 'examples': selected_examples, 'sampled_values': sampled}
