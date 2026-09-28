from __future__ import annotations
import hashlib
from typing import Any
import chromadb
from .config import settings
from .llm import embed_texts


class SchemaVectorStore:
    def __init__(self):
        self.schema_client = chromadb.PersistentClient(path=settings.admin_schemas_path)
        self.tables = self.schema_client.get_or_create_collection("schema_tables")
        self.columns = self.schema_client.get_or_create_collection("schema_columns")
        self.examples = self.schema_client.get_or_create_collection("sql_examples")
        self.relationships = self.schema_client.get_or_create_collection("schema_relationships")

    @staticmethod
    def _id(prefix: str, text: str) -> str:
        return prefix + hashlib.sha1(text.encode("utf-8")).hexdigest()[:20]

    def reset(self) -> None:
        for client, name in (
            (self.schema_client, "schema_tables"),
            (self.schema_client, "schema_columns"),
            (self.schema_client, "sql_examples"),
        ):
            try:
                client.delete_collection(name)
            except Exception:
                pass
        self.tables = self.schema_client.get_or_create_collection("schema_tables")
        self.columns = self.schema_client.get_or_create_collection("schema_columns")
        self.examples = self.schema_client.get_or_create_collection("sql_examples")
        self.relationships = self.schema_client.get_or_create_collection("schema_relationships")

    def index_catalog(self, catalog: dict[str, Any], examples: list[dict[str, Any]]) -> None:
        table_docs, table_ids, table_meta = [], [], []
        column_docs, column_ids, column_meta = [], [], []
        for table, info in catalog["tables"].items():
            table_doc = f"table {table}. {info.get('description','')} Columns: " + ", ".join(info.get("columns", {}).keys())
            relationships = [r for r in catalog.get('relationships', [])
                             if table in (r['from_table'], r['to_table'])]
            if relationships:
                table_doc += ' Verified business joins: ' + '; '.join(
                    f"{r['from_table']}.{r['from_column']} = {r['to_table']}.{r['to_column']} ({r['type']})"
                    for r in relationships)
            table_docs.append(table_doc)
            table_ids.append(self._id("t_", table))
            table_meta.append({"table": table})
            for col, desc in info.get("columns", {}).items():
                doc = f"table {table}, column {col}. {desc if isinstance(desc, str) else desc.get('description', '')} Table meaning: {info.get('description', '')}"
                if isinstance(desc, dict):
                    doc += " Synonyms: " + ", ".join(desc.get("synonyms", [])) + " Sample values: " + ", ".join(map(str, desc.get("sample_values", [])))
                column_docs.append(doc)
                column_ids.append(self._id("c_", table + "." + col))
                column_meta.append({"table": table, "column": col})

        if table_docs:
            self.tables.upsert(ids=table_ids, documents=table_docs, metadatas=table_meta, embeddings=embed_texts(table_docs))
        if column_docs:
            self.columns.upsert(ids=column_ids, documents=column_docs, metadatas=column_meta, embeddings=embed_texts(column_docs))

        ex_docs, ex_ids, ex_meta = [], [], []
        for ex in examples:
            doc = f"Question: {ex['question']}\nSQL: {ex['sql']}\nNotes: {ex.get('notes','')}"
            ex_docs.append(doc)
            ex_ids.append(self._id("e_", ex["question"] + ex["sql"]))
            ex_meta.append({"tables": ",".join(ex.get("tables", [])), "sql": ex["sql"], "question": ex["question"]})
        if ex_docs:
            self.examples.upsert(ids=ex_ids, documents=ex_docs, metadatas=ex_meta, embeddings=embed_texts(ex_docs))

    def retrieve(self, question: str, catalog: dict[str, Any]) -> dict[str, Any]:
        q_emb = embed_texts([question])[0]
        table_hits = self.tables.query(query_embeddings=[q_emb], n_results=min(settings.top_tables, max(1, self.tables.count())))
        selected_tables = list(dict.fromkeys(m["table"] for m in (table_hits.get("metadatas") or [[]])[0] if m["table"] in catalog["tables"]))

        col_hits = self.columns.query(query_embeddings=[q_emb], n_results=min(settings.top_columns, max(1, self.columns.count())))
        col_meta = (col_hits.get("metadatas") or [[]])[0]
        # Multi-stage: table retrieval first, then columns constrained to retrieved tables.
        selected_cols: dict[str, list[str]] = {t: [] for t in selected_tables}
        for m in col_meta:
            if m["table"] in selected_cols and m["column"] not in selected_cols[m["table"]]:
                selected_cols[m["table"]].append(m["column"])

        schema_context = {"tables": {}}
        for table in selected_tables:
            info = catalog["tables"][table]
            # Ranking must not hide valid columns needed by the question.
            cols = list(dict.fromkeys(selected_cols.get(table, []) + list(info.get("columns", {}))))
            schema_context["tables"][table] = {
                "description": info.get("description", ""),
                "columns": {c: info.get("columns", {}).get(c, "") for c in cols if c in info.get("columns", {})},
                "foreign_keys": info.get("foreign_keys", []),
            }

        ex_count = self.examples.count()
        retrieved_examples = []
        if ex_count:
            from .catalog import examples
            current_examples = {(ex['question'], ex['sql']) for ex in examples()}
            ex_hits = self.examples.query(query_embeddings=[q_emb], n_results=min(settings.top_examples, ex_count))
            for m in (ex_hits.get("metadatas") or [[]])[0]:
                # Persisted embeddings may predate schema changes. Never feed
                # removed or superseded SQL examples back into generation.
                if (m['question'], m['sql']) not in current_examples:
                    continue
                retrieved_examples.append({"question": m["question"], "sql": m["sql"], "tables": m.get("tables", "").split(",") if m.get("tables") else []})
        return {"tables": selected_tables, "schema_context": schema_context, "examples": retrieved_examples}
