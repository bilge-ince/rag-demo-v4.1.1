import argparse
# import streamlit as st
from enum import Enum
from dotenv import load_dotenv
import os

from db import get_connection

from commands.chat import chat
from commands.create_db import create_db
from commands.import_data import import_data_s3

load_dotenv()


class Command(Enum):
    CREATE_DB = "create-db"
    IMPORT_DATA_S3 = "import-data-s3"
    CHAT = "chat"


def main():
    parser = argparse.ArgumentParser(description="Application Description")

    subparsers = parser.add_subparsers(
        title="Subcommands",
        dest="command",
        help="Display available subcommands",
    )

    # create-db command
    subparsers.add_parser(
        Command.CREATE_DB.value, help="Create a database"
    ).set_defaults(func=create_db)

    # import-data-s3 command
    import_data_s3_parser = subparsers.add_parser(
        Command.IMPORT_DATA_S3.value, help="Import data from S3 bucket"
    )
    import_data_s3_parser.add_argument(
        "preparer_retriever_name", type=str, help="Specify a name that will be used as both preparer and retriever name"
    )
    import_data_s3_parser.set_defaults(func=import_data_s3)

    # chat command
    chat_parser = subparsers.add_parser(Command.CHAT.value, help="Use chat feature")
    chat_parser.set_defaults(func=chat)

    args = parser.parse_args()

    if args.command == Command.CHAT.value:
        if hasattr(args, "func"):
                aidb_model_name = "llama"
                operation_type = "completions"
                model_full_name = "llama3.2-vision"
                url="http://host.docker.internal:11434/v1/chat/completions"
                conn = get_connection()
                with conn.cursor() as cur:
                    # ollama is running in my local and the aidb is installed in the docker env.
                    # therefore pass the url param to the docker : http://host.docker.internal:11434/v1/chat/completions
                    cur.execute(f"""select aidb.create_model('{aidb_model_name}', '{operation_type}', '{{"model":"{model_full_name}", "url":"{url}"}}'::JSONB);""")
                conn.commit()
                conn.close()
                args.func(args, aidb_model_name)
    elif (
        (args.command == Command.IMPORT_DATA_S3.value)
        or (args.command == Command.CREATE_DB.value)
    ):
        args.func(args)
    else:
        print("Invalid command. Use '--help' for assistance.")


if __name__ == "__main__":
    main()
