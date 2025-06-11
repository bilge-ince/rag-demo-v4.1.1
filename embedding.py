from db import get_connection

def create_retriever():
    conn = get_connection()
    cursor = conn.cursor()
    # Replace the nim_embeddings with embeddings for an embedding model with OpenAI compatible enpoint
    cursor.execute("""SELECT aidb.create_model('text-nim-embeddings'
                         ,'nim_embeddings'
                         ,'{"url":  "http://nv-embedqa-e5-v5-1xgpu-predictor.default.svc.cluster.local/v1/embeddings"
                         ,"model": "nvidia/nv-embedqa-e5-v5"}');""")
    # use the unique_id column as the key for chunks
    # id is the default key column and using non-chunked data
    cursor.execute(f"""
            SELECT aidb.create_table_knowledge_base(
               name => 'chunk_retriever'
               ,source_table => 'chunked_data_html'
               ,source_data_column => 'chunks'
               ,source_data_format => 'Text'
               ,source_key_column => 'unique_id'
               ,model_name => 'text-nim-embeddings' 
               ,auto_processing => 'Live');""")
    
    conn.commit()
    # comment out this line if there is no data in documents table
    cursor.execute(f"""SELECT aidb.bulk_embedding('chunk_retriever');""")
    conn.commit()
    print("bulk embedding is completed")
    conn.commit()
    return None
