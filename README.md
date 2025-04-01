# Building a Library Management System using REST API

Building a robust Library Management System API using Flask, SQLAlchemy, and JWT authentication. This guide explains each step in detail—from cloning the repository and installing dependencies to running the application and testing the endpoints. Whether you’re a beginner or an experienced developer, this step-by-step process will help you understand and implement a secure, scalable RESTful API for managing library operations.


📺 [Watch the demo video](https://youtu.be/VDEtDVWlocY)

---

## Introduction

The Library Management System API is a RESTful service designed to handle common library tasks such as user registration and management, secure user authentication with JSON Web Tokens (JWT), book management (creation, retrieval, updates, and deletion), and tracking of book borrowing and returning transactions. With role-based access control, administrative endpoints are protected, ensuring that only authorized users can perform critical operations.

---

## Cloning the Repository

To get started, you’ll need to clone the repository from GitHub. Follow these steps:

1. Open your terminal (Command Prompt, PowerShell, or any terminal of your choice).
2. Run the following command to clone the repository (replace `<repository_url>` with the actual URL of your repository):

   ```
   git clone <repository_url>
   ```

3. Once the cloning process is complete, navigate to the project directory:

   ```
   cd library_management
   ```

---

## Setting Up the Environment

### Creating and Activating a Virtual Environment

It is recommended to use a virtual environment to manage project dependencies. Execute the following commands:

- **Create a virtual environment:**

  ```
  python -m venv venv
  ```

- **Activate the virtual environment:**

  - On **Windows** (using PowerShell):

    ```
    .\venv\Scripts\Activate.ps1
    ```

  - On **macOS/Linux**:

    ```
    source venv/bin/activate
    ```

### Installing Dependencies

With your virtual environment activated, install the necessary packages by running:

```
pip install -r requirements.txt
```

The `requirements.txt` file includes all the pinned versions required for the project, ensuring compatibility. The key dependencies are:
- Flask 2.1.2
- Flask-SQLAlchemy 2.5.1
- Flask-JWT-Extended 4.4.0
- Passlib 1.7.4 (with bcrypt 3.2.0)
- Werkzeug 2.0.3
- SQLAlchemy (version below 2.0)

---

## Running the Application

To start the Library Management System API, execute the following command in your terminal:

```
python run.py
```

The server will start in debug mode and the API will be accessible at [http://127.0.0.1:5000](http://127.0.0.1:5000). The root endpoint provides a simple confirmation that the API is running.

---

## Detailed REST API Endpoints

Below is an overview of the main endpoints available in the API.

### Authentication

- **POST /auth/login**  
  *Purpose:* Authenticates a user and returns a JWT token.  
  *Request Body Example:*
  ```json
  {
    "username": "admin",
    "password": "admin123"
  }
  ```  
  *Success Response (200 OK):*
  ```json
  { "access_token": "<JWT_TOKEN>" }
  ```
  *Error Responses:*  
  - 400 if required fields are missing.  
  - 401 if credentials are invalid.

### User Management

- **POST /users**  
  *Purpose:* Creates a new user (can be an admin or a regular user).  
  *Request Body Example:*
  ```json
  {
    "username": "admin",
    "password": "admin123",
    "role": "admin"
  }
  ```  
  *Success Response (201 Created):*
  ```json
  { "msg": "User 'admin' created successfully" }
  ```
  *Error Response:*  
  - 400 for missing data or duplicate username.

- **GET /users** *(Admin Only)*  
  *Purpose:* Retrieves a list of all users.  
  *Required Header:*  
  ```
  Authorization: Bearer <JWT_TOKEN>
  ```  
  *Success Response (200 OK):*
  ```json
  [
    { "id": 1, "username": "admin", "role": "admin" },
    { "id": 2, "username": "user1", "role": "user" }
  ]
  ```
  *Error Response:*  
  - 403 if the requester lacks admin privileges.

- **PUT /users/<user_id>**  
  *Purpose:* Updates user details. Admins can update any user; regular users can update only their own information.  
  *Request Body Example:*
  ```json
  {
    "username": "newadmin",
    "password": "newpassword",
    "role": "admin"
  }
  ```  
  *Success Response (200 OK):*
  ```json
  { "msg": "User '<user_id>' updated" }
  ```
  *Error Responses:*  
  - 403 for unauthorized access.  
  - 404 if the user is not found.

### Book Management

- **POST /books** *(Admin Only)*  
  *Purpose:* Creates a new book record.  
  *Required Header:*  
  ```
  Authorization: Bearer <JWT_TOKEN>
  ```  
  *Request Body Example:*
  ```json
  {
    "title": "Flask for Beginners",
    "author": "John Doe",
    "isbn": "1234567890",
    "published_year": 2021,
    "category": "Programming",
    "quantity": 5
  }
  ```  
  *Success Response (201 Created):*
  ```json
  { "msg": "Book 'Flask for Beginners' created" }
  ```
  *Error Responses:*  
  - 400 for missing fields.  
  - 403 if the user is not an admin.

- **GET /books**  
  *Purpose:* Retrieves a list of books with optional filtering parameters (title, author, isbn).  
  *Required Header:*  
  ```
  Authorization: Bearer <JWT_TOKEN>
  ```  
  *Success Response (200 OK):*  
  Returns an array of book objects.

- **PUT /books/<book_id>** *(Admin Only)*  
  *Purpose:* Updates an existing book record.  
  *Request Body Example:*
  ```json
  {
    "title": "Updated Title",
    "quantity": 10
  }
  ```  
  *Success Response (200 OK):*
  ```json
  { "msg": "Book '<book_id>' updated" }
  ```
  *Error Responses:*  
  - 403 if not an admin.  
  - 404 if the book is not found.

- **DELETE /books/<book_id>** *(Admin Only)*  
  *Purpose:* Deletes a book record.  
  *Success Response (200 OK):*
  ```json
  { "msg": "Book '<book_id>' deleted" }
  ```
  *Error Responses:*  
  - 403 for unauthorized access.  
  - 404 if the book is not found.

### Transaction Management

- **POST /transactions/borrow**  
  *Purpose:* Allows a user to borrow a book, reducing the available quantity by one.  
  *Required Header:*  
  ```
  Authorization: Bearer <JWT_TOKEN>
  ```  
  *Request Body Example:*
  ```json
  { "book_id": 1 }
  ```  
  *Success Response (200 OK):*
  ```json
  { "msg": "Book 'Flask for Beginners' borrowed" }
  ```
  *Error Responses:*  
  - 400 if `book_id` is missing or if the book is unavailable.  
  - 404 if the book is not found.

- **POST /transactions/return**  
  *Purpose:* Allows a user to return a previously borrowed book, increasing its available quantity by one.  
  *Required Header:*  
  ```
  Authorization: Bearer <JWT_TOKEN>
  ```  
  *Request Body Example:*
  ```json
  { "book_id": 1 }
  ```  
  *Success Response (200 OK):*
  ```json
  { "msg": "Book 'Flask for Beginners' returned" }
  ```
  *Error Responses:*  
  - 400 if `book_id` is missing or if no active borrow transaction exists.  
  - 404 if the book is not found.

---

## Cloning and Installing the Repository

To get started with the project:

1. **Clone the Repository:**
   - Open your terminal and run:
     ```
     git clone <repository_url>
     cd library_management
     ```
2. **Set Up Your Environment:**
   - Create a virtual environment:
     ```
     python -m venv venv
     ```
   - Activate the environment:
     - Windows:
       ```
       .\venv\Scripts\Activate.ps1
       ```
     - macOS/Linux:
       ```
       source venv/bin/activate
       ```
3. **Install Dependencies:**
   - Run:
     ```
     pip install -r requirements.txt
     ```

---

## Running the Application

To launch the API, simply run:

```
python run.py
```

The application will start in debug mode and will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000). Use your favorite API testing tool (like the VS Code REST Client or Postman) to interact with the endpoints.

---


```

---

This article provides a detailed, step-by-step explanation of the Library Management System API. It covers all aspects of the project, including setup, installation, API endpoint details, and running the application—ideal for a blog post or GitHub documentation.
