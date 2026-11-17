from database import get_db


def _book_to_dict(row) -> dict:
    return {
        "id": row[0],
        "title": row[1],
        "author": row[2],
        "isbn": row[3],
        "available": bool(row[4]),
    }


def list_books(available_only: bool = False) -> list[dict]:
    conn = get_db()
    if available_only:
        rows = conn.execute("SELECT * FROM books WHERE available = 1").fetchall()
    else:
        rows = conn.execute("SELECT * FROM books").fetchall()
    conn.close()
    return [_book_to_dict(r) for r in rows]


def get_book(book_id: int) -> dict | None:
    conn = get_db()
    row = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    conn.close()
    return _book_to_dict(row) if row else None


def create_book(title: str, author: str, isbn: str) -> dict:
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO books (title, author, isbn, available) VALUES (?, ?, ?, 1)",
        (title, author, isbn),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM books WHERE id = ?", (cur.lastrowid,)).fetchone()
    conn.close()
    return _book_to_dict(row)


def delete_book(book_id: int) -> None:
    conn = get_db()
    conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()


def set_book_availability(book_id: int, available: bool) -> None:
    conn = get_db()
    conn.execute(
        "UPDATE books SET available = ? WHERE id = ?",
        (1 if available else 0, book_id),
    )
    conn.commit()
    conn.close()
