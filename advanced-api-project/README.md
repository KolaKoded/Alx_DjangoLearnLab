# Django Book API

## Overview

This Django application provides an API for managing books, including functionalities to list, retrieve, create, update, and delete book records. The API is built using Django REST Framework and includes custom permissions and validation to ensure proper access control and data integrity.

## Views

### `ListView`

**Purpose:** Retrieve a list of all books.

- **Endpoint:** `/api/books/`
- **Method:** `GET`
- **Permissions:** 
  - No special permissions are required; accessible to all authenticated users.
- **Description:** This view returns a paginated list of all book records in the database. It uses the `BookSerializer` to serialize the data.

### `DetailView`

**Purpose:** Retrieve details of a single book.

- **Endpoint:** `/api/books/<int:pk>/`
- **Method:** `GET`
- **Permissions:** 
  - No special permissions are required; accessible to all authenticated users.
- **Description:** This view returns detailed information about a specific book identified by its primary key (`pk`). It uses the `BookSerializer` to serialize the data.

### `CreateView`

**Purpose:** Create a new book record.

- **Endpoint:** `/api/books/create/`
- **Method:** `POST`
- **Permissions:**
  - `IsAuthenticated`: The user must be logged in.
  - `IsAdminOrEditor`: The user must have 'admin' or 'editor' role.
- **Custom Settings/Validation:**
  - **Publication Year Validation:** Ensures that the publication year cannot be set to a future date. If the publication year is in the future, it returns a 400 Bad Request response with an appropriate error message.
- **Description:** This view allows authenticated users with 'admin' or 'editor' roles to create a new book record. The request data is validated to ensure the publication year is not in the future before saving.

### `UpdateView`

**Purpose:** Update an existing book record.

- **Endpoint:** `/api/books/update/<int:pk>/`
- **Method:** `PUT` or `PATCH`
- **Permissions:**
  - `IsAuthenticated`: The user must be logged in.
  - `IsAdminOrEditor`: The user must have 'admin' or 'editor' role.
- **Custom Settings/Validation:**
  - **Publication Year Validation:** Ensures that the publication year cannot be set to a future date. If the publication year is in the future, it returns a 400 Bad Request response with an appropriate error message.
- **Description:** This view allows authenticated users with 'admin' or 'editor' roles to update an existing book record. The request data is validated to ensure the publication year is not in the future before saving.

### `DeleteView`

**Purpose:** Delete an existing book record.

- **Endpoint:** `/api/books/delete/<int:pk>/`
- **Method:** `DELETE`
- **Permissions:**
  - `IsAuthenticated`: The user must be logged in.
  - `IsAdmin`: The user must have 'admin' role.
- **Description:** This view allows authenticated users with 'admin' role to delete an existing book record. The book is identified by its primary key (`pk`).

## Custom Settings/Hooks

- **Custom Validation in `CreateView` and `UpdateView`:**
  - Both views include custom validation to ensure that the publication year of the book is not set to a future date. If validation fails, a 400 Bad Request response is returned with an error message.

- **Permissions:**
  - `IsAdminOrEditor`: Custom permission class to allow access to 'admin' and 'editor' users.
  - `IsAdmin`: Custom permission class to restrict access to 'admin' users only.

## Filtering, Searching, and Ordering

The `ListView` provides powerful functionalities for filtering, searching, and ordering the list of books. These features allow users to easily retrieve books based on specific criteria, search for books by keywords, and order the results according to different fields.

### Filtering

Filtering is implemented using Django REST Framework’s `DjangoFilterBackend`. Users can filter books by the following attributes:

- `title`
- `author`
- `publication_year`

#### How to Use Filtering

To filter the book list, add query parameters to your request URL.

**Example Requests:**

- **Filter books by author:**
  
  ```http
  GET /api/books/?author=J.K. Rowling

- **Filter books by publication year:**
  
  ```http
  GET /api/books/?publication_year=2000

- **Combine filters:**
  
  ```http
  GET /api/books/?author=J.K. Rowling&publication_year=2000
  
### Searching

Searching is integrated using Django REST Framework’s `SearchFilter`. Users can perform text-based searches on the following fields:

- `title`
- `author`

The search is case-insensitive and supports partial matches.

#### How to Use Searching

To search for books, use the  `search` query parameter in your request URL

**Example Requests:**

- **Search for books with "Harry" in the title:**
  
  ```http
  GET /api/books/?search=Harry

- **Search for books by an author:**
  
  ```http
  GET /api/books/?search=Tolkien

### Ordering

Ordering is enabled through Django REST Framework’s `OrderingFilter`. Users can order books by any field in the `Book` model. The most commonly used fields are:

- `title`
- `publication_year`

By default, results are ordered in ascending order. To order in descending order, prefix the field with a minus sign (`-`).

#### How to Use Ordering

To order the books, use the `ordering` query parameter in your request URL.

**Example Requests:**

- **Order books by title (ascending):**
  
  ```http
  GET /api/books/?ordering=title

- **Order books by publication year (descending):**
  
  ```http
  GET /api/books/?ordering=-publication_year

- **Combine ordering fields:**
  
  ```http
  GET /api/books/?ordering=title,-publication_year

This will order the results by title in ascending order, and for books with the same title, it will order by publication year in descending order.

## Testing Strategy

The testing strategy for this application follows Django REST Framework’s `APITestCase` class to perform unit and integration tests for the `Book` API endpoints. The tests cover creating, updating, deleting, filtering, and searching books, as well as ensuring that the correct HTTP status codes are returned. Additionally, there are tests for ensuring proper authentication and ordering of books by title and publication year.

### Test Cases

1. **Test Book Creation (`test_create_book`):**
   - **Objective:** Test if a book can be created with valid data.
   - **Test:** Sends a `POST` request to create a book. Verifies that the response status code is 201 (Created) and checks that the newly created book's title is correct.

2. **Test Book Update (`test_update_book`):**
   - **Objective:** Ensure that a book can be updated.
   - **Test:** Sends a `PUT` request to update an existing book's details and verifies that the changes are correctly applied.

3. **Test Book Deletion (`test_delete_book`):**
   - **Objective:** Test if a book can be deleted.
   - **Test:** Sends a `DELETE` request to remove a book. Verifies that the response status code is 204 (No Content) and ensures the book is deleted from the database.

4. **Test Filtering Books by Author (`test_filter_books_by_author`):**
   - **Objective:** Test if books can be filtered by author name.
   - **Test:** Sends a `GET` request with the author name filter. Verifies that the response contains only books by the specified author.

5. **Test Searching Books (`test_search_books`):**
   - **Objective:** Ensure that books can be searched by title.
   - **Test:** Sends a `GET` request to search for books by a title keyword. Verifies that the correct book is returned.

6. **Test Ordering Books by Title (`test_order_books_by_title`):**
   - **Objective:** Ensure that books can be ordered by title.
   - **Test:** Sends a `GET` request with an ordering query for the title. Verifies that books are returned in the correct order.

7. **Test Ordering Books by Publication Year (`test_order_books_by_publication_year`):**
   - **Objective:** Ensure that books can be ordered by their publication year.
   - **Test:** Sends a `GET` request with an ordering query for publication year. Verifies that books are ordered correctly.

8. **Test Authentication Requirement (`test_authentication_required`):**
   - **Objective:** Ensure that authentication is required for book creation.
   - **Test:** Logs out the test user and attempts to create a book. Verifies that the response status code is 403 (Forbidden).

### Running the Tests

1. **Set up the Test Environment:**
   - Ensure that Django and the required test framework are properly set up.
   - Make sure the test database is initialized.

2. **Run the Tests:**
   - Execute the following command to run all tests:
     ```bash
     python manage.py test api
     ```

3. **View Results:**
   - After running the tests, Django will display a summary of all tests, showing how many passed, failed, or were skipped.

### Interpreting Test Results

- **Pass (OK):** Indicates that the test passed successfully, meaning the feature works as expected.
- **Fail (FAIL):** Indicates a test failure, meaning the expected behavior was not met. Check the failure message and traceback for details.
- **Skip (SKIP):** Means the test was skipped, which might happen due to certain conditions not being met.

Make sure to review any failed test cases and address issues based on the feedback provided by the test output.


## Setup

1. **Install Dependencies:**
   - Ensure you have Django and Django REST Framework installed in your environment.

2. **Apply Migrations:**
   - Run `python manage.py makemigrations` and `python manage.py migrate` to apply database changes.

3. **Run the Server:**
   - Start the development server with `python manage.py runserver`.

4. **Access the API:**
   - Use Postman or any HTTP client to interact with the API endpoints.

## Usage

- **Listing Books:** Send a `GET` request to `/api/books/`.
- **Retrieving a Book:** Send a `GET` request to `/api/books/<int:pk>/`.
- **Creating a Book:** Send a `POST` request to `/api/books/create/` with the book data.
- **Updating a Book:** Send a `PUT` or `PATCH` request to `/api/books/uodate/<int:pk>/` with the updated book data.
- **Deleting a Book:** Send a `DELETE` request to `/api/books/delete/<int:pk>/`.

