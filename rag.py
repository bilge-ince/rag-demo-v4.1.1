from db import get_connection
import openai
import backoff

template = """<s>[INST]
You are a friendly documentation search bot.
Use following piece of context to answer the question.
If the context is empty, try your best to answer without it.
Never mention the context.
Try to keep your answers concise unless asked to provide details.

Context: {context}
Question: {question}
[/INST]</s>
Answer:
"""

def retrieve_augmentation(query, topk, retriever_name):
    # query is the question to ask
    # topk is the number of documents to retrieve
    # retriever_name is the name of the retriever created in the database
    # clean punctuations and extra spaces
    query_str = ''.join(e for e in query if e.isalnum() or e.isspace())
    rag_query = ""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            try:
                # ParseHtml operation is storing the text into PG table, 
                # retrieve_text function will return the text from the associated table
                cursor.execute(
                        f"SELECT value FROM aidb.retrieve_text(%s, %s, %s);", (retriever_name, query_str, topk)
                    )
                rag_query = ' '.join(row[0] for row in cursor.fetchall())
            except Exception as e:
                print("Exception: retriever name is wrong")
                raise SystemExit(e)
            conn.commit()
    return rag_query

def rag_query(aidb_model_name, query, topk, retriever_name):
    # retriever_name is the name of the retriever created in the database
    # topk is the number of documents to retrieve
    # query is the question to ask

    rag_query = retrieve_augmentation(query, topk, retriever_name)
    query_template = template.format(context=rag_query, question=query)
    
    conn = get_connection()
    with conn.cursor() as cur:
        # an ollama model has been pulled and running on localhost
        # it has been also created in aidb with the name of local_llama
        # clean punctuations and extra spaces 
        query_decode = "SELECT decode_text FROM aidb.decode_text(%s, %s);"

        cur.execute(query_decode, (aidb_model_name, query_template,))
        result = cur.fetchone()
        return result[0]
    