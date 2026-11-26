
import sqlite3
import requests

# Fetches book details from Open Library and saves them in a local SQLite database

SEARCH_ENDPOINT = "https://openlibrary.org/search.json"
DB_FILE = "books.db"


def get_books_from_api(search_term="python", max_results=20):
    """
    Searches Open Library for books based on the given search term.
    Returns the list of matching books along with their title,
    author name and first publication year.
    """
    payload = {
        "q": search_term,
        "limit": max_results,
        "fields": "title,author_name,first_publish_year"
    }

  
    resp = requests.get(SEARCH_ENDPOINT, params=payload, timeout=10)
    resp.raise_for_status()

    # Converting the API response into JSON and get the matching book records
    data = resp.json()
    return data.get("docs", [])


def store_in_db(book_list, db_path=DB_FILE):
    """
    Takes the book records received from the API and stores them
    in SQLite. Existing books are ignored to avoid duplicate entries.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Create the books table if it doesn't already exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            year INTEGER,
            UNIQUE(title, author)
        )
    """)

    # Go through each book and pick the details we need
    for item in book_list:
        title = item.get("title")

        # Skip records where the title is missing
        if not title:
            continue

        # Some books may have multiple authors, so combine their names into one string
        authors_raw = item.get("author_name", [])
        author_str = ", ".join(authors_raw) if authors_raw else None

        pub_year = item.get("first_publish_year")

        # Insert the book into the database.
        # If the same title and author combination already exists, ignore it.
        cur.execute(
            "INSERT OR IGNORE INTO books (title, author, year) VALUES (?, ?, ?)",
            (title, author_str, pub_year)
        )

    # Save the changes and return the connection for retrieving the records
    conn.commit()
    return conn


def main():
    """
    Runs the complete process: fetches books from Open Library,
    stores them in SQLite, retrieves the saved records and displays them.
    """
    books = get_books_from_api()
    db_conn = store_in_db(books)

    # Read the saved books back from the database, ordered by publication year
    cur = db_conn.cursor()
    cur.execute("SELECT title, author, year FROM books ORDER BY year")
    results = cur.fetchall()

    # Display the book details in a simple, readable format
    for title, author, year in results:
        yr_display = year if year else "n/a"
        auth_display = author if author else "unknown"
        print(f"{yr_display} | {title} | {auth_display}")

    db_conn.close()


if __name__ == "__main__":
    main()
