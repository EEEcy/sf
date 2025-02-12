# Week 4: Data Management with FastAPI, SQLAlchemy, ChromaDB, OpenAI, and LangChain

## Introduction

This lab guides you through developing a RESTful API using Python's FastAPI framework and integrating it with SQLAlchemy ORM for database interactions. You will also learn how to use ChromaDB, a vector database, to perform semantic searches based on text embeddings. Additionally, you will implement CRUD operations, integrate the OpenAI API and LangChain for text generation and RAG, and document your API using Swagger UI.

---

## Before Class – Setup (Individual)

Read up on SQLAlchemy and Alembic basics: understand Base, Session, and ORM concepts. Understand how to manage database migrations.

### Install Prerequisites:
   - Install the following extensions in VS Code (Ctrl+Shift+X):
     - SQLite Viewer by Florian Klampfer.

### Download and extract the Lab Repository:
   Extract the lab file and navigate to its directory using the command line:
   ```bash
   cd week4-python-lab
   ```

### Set Up a Virtual Environment:
   Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows Command Prompt (not Power Shell), use venv\Scripts\activate
   ```

### Install Dependencies:
   Install project dependencies using the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

### Initialize the Database:
   Follow these steps to set up and manage the SQLite database for your project using Alembic and SQLAlchemy.

---

#### Initialize Alembic
1. Run the following command to initialize Alembic in your project (if there is no `migrations` folder or it's empty):
   ```bash
   alembic init migrations
   ```
   - This creates a `migrations` directory with the following structure:
     ```
     migrations/
       env.py
       README
       script.py.mako
       versions/
     ```
   - The `env.py` file is the main configuration file for Alembic.

---

#### Update the Database URL
1. Open the `alembic.ini` file in the root of your project.
2. Update the `sqlalchemy.url` setting with the path to your SQLite database:
   ```ini
   sqlalchemy.url = sqlite:///./app.db
   ```
   - This points to an SQLite database file named `app.db` in your project root.

---

#### Configure `env.py` for Model Detection
1. Open the file `migrations/env.py`.
2. Update the file to include your `Book` and `Review` models.
3. Modify `env.py` as follows:

   ```python
   from logging.config import fileConfig
   from sqlalchemy import engine_from_config, pool
   from alembic import context

   # Import your SQLAlchemy models
   from app.db.db import Base
   from app.models.book import Book  # Import Book model
   from app.models.review import Review  # Import Review model

   # Set up Alembic Config
   config = context.config
   fileConfig(config.config_file_name)

   # Set the target metadata to Base.metadata
   target_metadata = Base.metadata

   def run_migrations_offline():
       """Run migrations in 'offline' mode."""
       context.configure(
           url=config.get_main_option("sqlalchemy.url"),
           target_metadata=target_metadata,
           literal_binds=True,
       )
       with context.begin_transaction():
           context.run_migrations()

   def run_migrations_online():
       """Run migrations in 'online' mode."""
       connectable = engine_from_config(
           config.get_section(config.config_ini_section),
           prefix="sqlalchemy.",
           poolclass=pool.NullPool,
       )

       with connectable.connect() as connection:
           context.configure(connection=connection, target_metadata=target_metadata)

           with context.begin_transaction():
               context.run_migrations()

   if context.is_offline_mode():
       run_migrations_offline()
   else:
       run_migrations_online()
   ```

   - This ensures that Alembic knows about your `Book` and `Review` models by referencing `Base.metadata`.

---

#### Create a Migration File
1. Run the following command to generate a migration file based on your `Book` and `Review` models:
   ```bash
   alembic revision --autogenerate -m "Create books and reviews tables"
   ```
   - Alembic compares your `Base.metadata` (which includes `Book` and `Review` models) with the current database schema and generates the SQL commands required to create the tables.
   - The migration file will be created in the `migrations/versions` directory.

---

#### Apply the Migration
1. Apply the migration to create the `books` and `reviews` tables in the database:
   ```bash
   alembic upgrade head
   ```
   - This runs the migration script and creates the database schema in `app.db`.

---

#### Verify the Setup
1. Open the SQLite database file (`app.db`) using **SQLite Viewer** in VS Code or another SQLite client.
2. Verify that the `books` and `reviews` tables are created and match the schema defined in your models.

---

#### Summary of database setup steps
Execute the below sequentially:
- Initialize Alembic:
   ```bash
   alembic init migrations
   ```
- Update the database URL in `alembic.ini`:
   ```ini
   sqlalchemy.url = sqlite:///./app.db
   ```
- Create the migrations:
   ```bash
   alembic revision --autogenerate -m "Create books and reviews tables"
   ```
- Apply the migration:
   ```bash
   alembic upgrade head
   ```

- Verify the Database: Open app.db using `SQLite Viewer` in VS Code, confirm the books table is created.

---

### Run the Application:
   ```bash
   uvicorn app.main:app --reload
   ```

### Access the API:
   - API Endpoints: `http://localhost:8000/books`
   - Swagger Documentation: `http://localhost:8000/docs`

---

## Activity 1: Working with SQLAlchemy for CRUD Operations
### Objective: 
Use SQLAlchemy ORM to interact with a SQLite database and implement basic CRUD (Create, Read, Update, Delete) operations for a `Book` entity.

### Tasks:
  1. Understand the code in `models/book.py`, `services/book_service.py`, and `routes/books.py`.
  2. Test all endpoints using Swagger UI or the REST Client:
     - GET `/books`
     - POST `/books`
     - PUT `/books/{id}`
     - DELETE `/books/{id}`

### Notes:
  - Use SQLite as the database. The schema is managed via **Alembic migrations**.
  - You can view the database using **SQLite Viewer** in VS Code.

---

## Activity 2: Modeling Relationships with SQLAlchemy
### Objective: 
Use SQLAlchemy to manage database persistence for `Book` and `Review` entities, focusing on modeling relationships.

### Tasks:
  1. Understand the relationship between `Book` and `Review`:
     - `Book` is an entity with a one-to-many relationship to `Review`.
     - Use SQLAlchemy's `relationship()` and `ForeignKey` to define the relationship.
  2. Implement and test:
     - Fix issues in the `update_review` method in `routes/reviews.py`.
     - Update `review_service.py` to support CRUD operations for reviews.
  4. Test CRUD operations for both `Book` and `Review` entities using Swagger UI or the REST Client, e.g.:
     - POST `/books/{id}/reviews`
     - GET `/books/{id}/reviews`


### Notes:
  - Use Alembic to manage migrations for new tables (e.g., `reviews` table).
  - Verify the relationship schema and data using SQLite Viewer.

---

## Activity 3: Exploring ChromaDB and AI Integration

### Objective:
1. Learn how to add and query data in ChromaDB.
2. Understand the difference between raw list-style search results and AI-enhanced natural language summaries.

### Tasks:
Follow the following steps:

#### Add Books to ChromaDB

1. **Endpoint**: `/chroma`
2. **Description**: Add a book's title and description to ChromaDB, where embeddings will be generated for semantic search.

3. **Instructions**:
   - Use the following sample data to add books:

     **Example 1**:
     ```http
     POST /chroma
     Content-Type: application/json

     {
         "book_id": "1",
         "title": "Deep Learning for Natural Language Processing",
         "description": "This comprehensive book provides an in-depth overview of deep learning techniques tailored for natural language processing (NLP). Starting with foundational concepts in deep learning and their applications to NLP, the book delves into the implementation of neural networks, recurrent networks, and attention mechanisms like transformers. It covers practical examples, such as building machine translation systems, text summarizers, and sentiment analysis tools. Advanced topics like GPT-based models and fine-tuning BERT for specific tasks are also explored. Each chapter includes hands-on exercises to reinforce theoretical concepts, making it ideal for both beginners and seasoned professionals in the field of NLP."
     }
     ```

     **Example 2**:
     ```http
     POST /chroma
     Content-Type: application/json

     {
         "book_id": "2",
         "title": "Python Programming for Data Science and Machine Learning",
         "description": "This book serves as a comprehensive guide to using Python for data science and machine learning. Readers will learn how to process and visualize data using libraries like NumPy, Pandas, and Matplotlib. It covers essential machine learning algorithms such as linear regression, decision trees, clustering, and support vector machines, along with detailed explanations of their implementation in Python. Advanced topics include neural networks with TensorFlow and PyTorch, natural language processing, and deep learning techniques. Each chapter provides real-world datasets for hands-on projects, ranging from building recommendation systems to predictive analytics. Designed for data enthusiasts, the book bridges the gap between theory and practical implementation."
     }
     ```

4. **Expected Response**:
   ```json
   {
       "message": "Book 'Deep Learning for Natural Language Processing' added to ChromaDB successfully."
   }
   ```


### Search for Books with Raw List-Style Response:

1. **Endpoint**: `/chroma/similarities`
2. **Description**: Search for books based on a query and see the raw list-style response with metadata.

3. **Concept: Distance Score**:
   - The **distance score** measures the difference between the query and stored embeddings in ChromaDB.
   - **Range**:
     - Cosine distance typically ranges between `0` (most similar) and `2` (least similar).
   - **Smaller values indicate higher similarity**.
   - Use the `distance_threshold` parameter to filter results. For example:
     - `distance_threshold = 0.2`: Only very similar results are returned.
     - `distance_threshold = 1.0`: Includes broader matches.

4. **Instructions**:
   - Make a search query:
     ```http
     GET /chroma/similarities?query=Deep Learning&distance_threshold=1.0
     ```
   - Examine the returned response, which includes:
     - Metadata (title and description).
     - Distance scores for each result.

5. **Expected Response**:
   ```json
   {
   "query": "Deep Learning",
   "response": [
      {
         "description": "This comprehensive book provides an in-depth overview of deep learning techniques tailored for natural language processing (NLP). Starting with foundational concepts in deep learning and their applications to NLP, the book delves into the implementation of neural networks, recurrent networks, and attention mechanisms like transformers. It covers practical examples, such as building machine translation systems, text summarizers, and sentiment analysis tools. Advanced topics like GPT-based models and fine-tuning BERT for specific tasks are also explored. Each chapter includes hands-on exercises to reinforce theoretical concepts, making it ideal for both beginners and seasoned professionals in the field of NLP.",
         "title": "Deep Learning for Natural Language Processing",
         "distance": 0.8939606134347404
      }
   ]
   }
   ```

### Search with AI-Enhanced Summary

1. **Endpoint**: `/chroma/summary`
2. **Description**: Search for books and retrieve a natural language summary using OpenAI.

3. **Concept: AI-Enhanced Summaries**:
   - The `/chroma/summary` endpoint uses OpenAI's GPT model to convert the raw response into a natural language summary.
   - It summarizes:
     - The number of matching books.
     - Each book's title and a brief description.

4. **Instructions**:
   - Make the same search query:
     ```http
     GET /chroma/summary?query=Deep Learning&distance_threshold=1.0
     ```
   - Compare the response to the raw list-style response from `/chroma/similarities`.

5. **Expected Response**:
   ```json
   {
   "query": "Deep Learning",
   "response": "**Number of Books Found:** 1\n\n1. **Deep Learning for Natural Language Processing**  \n   This book offers a comprehensive overview of deep learning techniques specifically for natural language processing (NLP). It covers foundational concepts, neural networks, recurrent networks, and attention mechanisms like transformers. Practical examples include machine translation, text summarization, and sentiment analysis. Advanced topics such as GPT models and fine-tuning BERT are also discussed, with hands-on exercises included to reinforce learning, making it suitable for both beginners and experienced professionals in NLP."
   }
   ```

### Key Differences Between `/similarities` and `/summary`

| **Feature**         | **/similarities**                               | **/summary**                                    |
|----------------------|---------------------------------------------------|--------------------------------------------------|
| Response Type        | Raw JSON with metadata and distance scores        | Natural language summary of search results       |
| Distance Scores      | Explicitly included in the response               | Not shown directly, used internally for ranking |
| User-Friendly Output | Minimal formatting                                | Designed for user readability                    |


1. **Raw List-Style Response**:
   - Provides structured data directly from the database.
   - Useful for further programmatic access or analysis.

2. **AI-Enhanced Summary**:
   - Converts raw data into human-readable text.
   - Useful for user-facing applications where clarity and conciseness are essential.

### Additional Tasks for Students:

1. Add more books to ChromaDB using and repeat the search queries with more complex keywords.
2. Modify the `distance_threshold` parameter to observe how it affects the results.
   - For example:
     - `distance_threshold=0.5`
     - `distance_threshold=0.9`
3. Experiment with the prompt in the `generate_natural_language_response` function to customize the AI's response style.
4. Test and improve the implementation of the `delete_book` in `routes/chroma.py` method.
---

## Activity 4: Retrieval Augmented Generation (RAG)

**RAG** is a method where we use a LLM combined with an external knowledge source (like a PDF or database). Instead of the model guessing from its own (limited or outdated) training data, it “retrieves” relevant context from **fresh, external** documents and then generates an answer based on that context.

### Key Steps in RAG
1. **Indexing**  
   - Break your document(s) into smaller chunks.
   - Convert each chunk into a numeric vector (embedding) that captures its semantic meaning.
   - Store these vectors in a vector database.

2. **Retrieval**  
   - Take a user question, convert it to a vector, and find the most semantically similar chunks in the database.

3. **Generation**  
   - Combine the user question **and** the retrieved chunks into a prompt.
   - Send that prompt to a LLM, e.g., `gpt-4o-mini` to generate a final, context-aware answer.

---

### Mechanism Behind Our RAG Implementation

In this implementation, we use LangChain, which is a popular open-source framework that enables developers to build LLM-enabled applications. In the code, we have:

#### The Service Class (`PdfRagService`)
- **`create_vectorstore_from_pdf(file_path: str)`**  
  1. **Load** the PDF (on disk) with `PyPDFLoader`.  
  2. **Split** the PDF text into chunks with `RecursiveCharacterTextSplitter`.  
  3. **Embed** those chunks using `OpenAIEmbeddings`.  
  4. **Store** them in a **Chroma** vector database **in memory**.

- **`answer_query_with_vectorstore(question: str)`**  
  1. **Retrieve** the top-k similar chunks from the Chroma DB.  
  2. **Call** OpenAI API (using `gpt-4o-mini`) via a retrieval QA chain (LangChain) to generate the answer. 

#### FastAPI Routes
1. **`POST /pdf`**  
   - Receives a PDF file via HTTP upload.  
   - Writes it to a temporary file (so it has a valid file path).  
   - Calls `create_vectorstore_from_pdf()` to index the PDF’s content in memory.

2. **`POST /question`**  
   - Receives a JSON body with `{"question": "..."}`.  
   - Calls `answer_query_with_vectorstore(...)` to retrieve relevant chunks and get an answer from GPT.  
   - Returns the answer in JSON format.

By **uploading** the PDF once, you build an **in-memory** knowledge base. Then when you **ask** a question, the system:
1. Converts your question to an embedding.
2. Finds the best matching text chunks from your uploaded PDF.
3. Sends them along with your question to the LLM.
4. The LLM reads those chunks, forming an accurate answer based on the **actual text** of your PDF.

---

### Folder & Code Structure

```
app/
├── main.py                # FastAPI entry point
├── routes/
│   └── pdf_rag.py         # Your upload & question endpoints
└── services/
    └── pdf_rag_service.py # The PdfRagService class
```

### How to Use Swagger (FastAPI Docs) to Test

1. **Run** your FastAPI server (e.g., `uvicorn app.main:app --reload`).
2. Open your browser at:  
   **`http://127.0.0.1:8000/docs`**  
   - This is the **Swagger UI** (auto-generated by FastAPI).
3. You’ll see two endpoints:
   - `POST /pdf` (look under the `Default` or a relevant router tag).
   - `POST /question`.

### Uploading a PDF
1. **Find** the `POST /pdf` endpoint in the Swagger UI.
2. Click **“Try it out”**.
3. Next to `file`, click **“Choose File”** and select your PDF (e.g., `mitb-curriculum.pdf`).
4. Click **“Execute”**.  
   - If it’s successful, you’ll see `{"message":"PDF uploaded and indexed in-memory successfully."}` in the response.

### Asking a Question
1. **Find** the `POST /question` endpoint.
2. Click **“Try it out”**.
3. Enter a JSON body. For example:
   ```json
   {
     "question": "What is the course Applied Geospatial Analytics (0.5 CU) about?"
   }
   ```
4. Click **“Execute”**.
5. You’ll see a response with your `question` and an `answer` from `gpt-4o-mini`. The answer should be based on the relevant chunk(s) from your uploaded PDF.

---

### Summary of Concepts

- **RAG**: We augment a LLM by letting it retrieve relevant data from external sources.
- **Vector Store**: We store **embeddings** of PDF chunks in Chroma for quick semantic search.
- **LangChain**: Provides helpful tools and patterns for chunking, embedding, retrieving, and chaining LLMs.
- **FastAPI**: Exposes everything as RESTful endpoints, easy to integrate & test with Swagger UI.

