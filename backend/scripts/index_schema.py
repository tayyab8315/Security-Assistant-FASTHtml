from backend.app.catalog import live_or_static_catalog, examples
from backend.app.vector_store import SchemaVectorStore

if __name__ == "__main__":
    catalog = live_or_static_catalog()
    store = SchemaVectorStore()
    store.reset()
    store.index_catalog(catalog, examples())
    print("Indexed tables:", ", ".join(catalog["tables"].keys()))
    print("Table vectors:", store.tables.count())
    print("Column vectors:", store.columns.count())
    print("Example vectors:", store.examples.count())
