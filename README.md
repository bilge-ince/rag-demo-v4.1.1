# aidb-rag

An application to demonstrate how to create a Retrieval-Augmented Generation (RAG) system using `EDB's aidb extension v4.1.1` and `PostgreSQL v16+`. The chat console below showcases the features of a RAG system designed to answer questions specifically about EDB Bloggers. The biographies have been collected from EDB’s website. The system can seamlessly work with HTML files stored in a volume, such as object storage, with aidb managing the content from these sources using a preparer. Once a new file is added to the volume, aidb automates the process by integrating the new information into the pipeline, enabling the RAG to provide up-to-date answers. If no relevant data is available, the system will respond with: "I'm sorry, I couldn't find any information about this person."

![Sample Chat Console Output](/imgs/gui.png)

## Requirements

- Python 3
- PostgreSQL v16+
- aidb v4.1.1
- pgfs v2.0.1+

## Installation

1. Clone the repository:

  ```sh
  git clone git@github.com:EnterpriseDB/rag-demo-v4.1.1.git
  cd rag-demo-v4.1.1
  ```

2. Set up a virtual environment and install dependencies:

  ```sh
  virtualenv env -p `which python`
  source env/bin/activate
  pip install -r requirements.txt
  ```

3. Configure environment variables by copying and editing the `.env` file:

  ```sh
  cp .env-example .env
  ```

## Running the Application

### Database Connection

Connect to your PostgreSQL environment using the `psql` terminal and verify the connection:

```sh
psql -U uname -h p-xxx -p port_number -d edb_db
Password for user uname:
```

### Application Workflow

The application workflow is divided into two phases: Initialization and Chat.

#### Initialization Phase

Prepare the database and create the preparer, retriever, and embeddings:

1. View available commands:

  ```sh
  python app.py --help
  ```

2. Usage:

  ```sh
  python app.py [-h] {create-db, import-data-s3, chat}
  ```

3. Example: Import data from an object storage source (e.g., S3 bucket):

  ```sh
  python app.py import-data-s3
  ```

#### Chat Phase

Use the chat functionality to interact with the RAG system:

1. View help for the chat application:

  ```sh
  streamlit run app_x.py --help
  ```

2. Usage with Hugging Face Generative Models (requires a CUDA environment) or Ollama Models (runs on CPU, ensure the model is pulled and running):

  ```sh
  streamlit run app.py chat
  ```

## Application Description

### Options

```sh
-h, --help            Show this help message and exit
```

### Subcommands

```sh
{create-db, import-data-s3, chat}
        Display available subcommands
  create-db           Create a database
  import-data-s3      Use an object storage (e.g., S3 bucket) as a source for aidb retriever
  chat                Use the chat feature
```

By following these steps, you can set up and use the RAG system effectively.

### Updating from Object Storage

If an update is required from the object storage, simply call the `bulk_data_preparation` function as shown below:

```sql
SELECT aidb.bulk_data_preparation('preparer_retriever_name');
```