When do we actually need to use Vector Search?

there is a good amount of overhead that comes from vector search, including the need to encode the user query, which take time even with the simplest and fastest model

the overall process includes taking all of the documents, encoding said documents (in batches to speed it up), put the vectors inside the database and use it

The question becomes - is it worth it?

When you start out the projects, you should first look into the simplest use case, whcih is the text search as opposed to vector search since vector search pair with RAG is often advocated by vector search vendors. You can add vector search when it is really needed.

How do I know if vector search is worth it? Use the comparative evaluation of text vs vector search from the future materials to gain an insight. If the improvement is not significantly larger for vector search, it would make sense to save yourself a headache and simply use text search

You can also use hybrid search (text and vector)