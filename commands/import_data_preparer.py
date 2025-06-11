from db import get_connection


def import_data_s3_preparer(args):
    conn = get_connection()
    with conn:
        with conn.cursor() as curs:
            try:
                ## Please update the S3 bucket name to your own bucket
                curs.execute("""SELECT pgfs.create_storage_location('html_bucket_srv', 's3://...', options => '{"region":"eu-central-1", "skip_signature": "true"}');""")
                curs.execute("""SELECT aidb.create_volume('html_bucket_vol', 'html_bucket_srv', '/', 'application/html');""")
                
            except Exception as e:
                print("Server and volume already exist, continuing...")
                
            curs.execute("""
            SELECT aidb.create_volume_preparer(
                name => 'html_preparer_volume'
                ,operation => 'ParseHtml'
                ,source_volume_name => 'html_bucket_vol'
                ,destination_table => 'parsed_html_table'
                ,destination_data_column => 'parsed_html'
                ,destination_key_column => 'id'
                ,options => '{"method": "StructuredPlaintext"}'::JSONB);
        """)
            curs.execute("""SELECT aidb.bulk_data_preparation('html_preparer_volume');""")
            curs.execute("""SELECT aidb.create_table_preparer(
                name => 'preparer_chunk'
                ,operation => 'ChunkText'
                ,source_table => 'parsed_html_table'
                ,source_data_column => 'parsed_html'
                ,destination_table => 'chunked_data_html'
                ,destination_data_column => 'chunks'
                ,source_key_column => 'id'
                ,destination_key_column => 'id'
                ,options => '{"desired_length": 100, "max_length": 500}'::JSONB  -- Configuration for the ChunkText operation
            );""")
            curs.execute("""SELECT aidb.bulk_data_preparation('preparer_chunk');""")
            conn.commit()
    conn.close()
    print("import-data-s3 command executed. S3 bucket name: aidb-rag-app")