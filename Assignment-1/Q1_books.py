import sqlite3
import requests

# grabs book search results from openlibrary and dumps them into a local sqlite file

SEARCH_ENDPOINT = "https://openlibrary.org/search.json"
DB_FILE = "books.db"


def get_books_from_api(search_term="python", max_results=20):
    payload = {
        "q": search_term,
        "limit": max_results,
        "fields": "title,author_name,first_publish_year"
    }
    resp = requests.get(SEARCH_ENDPOINT, params=payload, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data.get("docs", [])


def store_in_db(book_list, db_path=DB_FILE):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            year INTEGER,
            UNIQUE(title, author)
        )
    """)

    for item in book_list:
        title = item.get("title")
        if not title:
            continue

        authors_raw = item.get("author_name", [])
        author_str = ", ".join(authors_raw) if authors_raw else None
        pub_year = item.get("first_publish_year")

        cur.execute(
            "INSERT OR IGNORE INTO books (title, author, year) VALUES (?, ?, ?)",
            (title, author_str, pub_year)
        )

    conn.commit()
    return conn


def main():
    books = get_books_from_api()
    db_conn = store_in_db(books)

    cur = db_conn.cursor()
    cur.execute("SELECT title, author, year FROM books ORDER BY year")
    results = cur.fetchall()

    for title, author, year in results:
        yr_display = year if year else "n/a"
        auth_display = author if author else "unknown"
        print(f"{yr_display} | {title} | {auth_display}")

    db_conn.close()


if __name__ == "__main__":
    main()