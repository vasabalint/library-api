from database import get_db


def get_unreturned_loans_with_details() -> list[dict]:
    conn = get_db()
    rows = conn.execute(
        """
        SELECT loans.id, books.title, members.name, loans.due_date
        FROM loans
        JOIN books ON books.id = loans.book_id
        JOIN members ON members.id = loans.member_id
        WHERE loans.returned = 0
        """
    ).fetchall()
    conn.close()
    return [
        {
            "loan_id": r[0],
            "title": r[1],
            "member": r[2],
            "due_date": r[3],
        }
        for r in rows
    ]


def get_total_books_count() -> int:
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    conn.close()
    return total
