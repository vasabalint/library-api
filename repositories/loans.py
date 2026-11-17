from database import get_db
from rules import money


def _loan_to_dict(row) -> dict:
    return {
        "id": row[0],
        "book_id": row[1],
        "member_id": row[2],
        "due_date": row[3],
        "returned": bool(row[4]),
        "fine": money(row[5]),
        "fine_paid": bool(row[6]),
        "renewals": row[7],
        "checked_out": row[8],
    }


def list_loans() -> list[dict]:
    conn = get_db()
    rows = conn.execute("SELECT * FROM loans").fetchall()
    conn.close()
    return [_loan_to_dict(r) for r in rows]


def get_loan(loan_id: int) -> dict | None:
    conn = get_db()
    row = conn.execute("SELECT * FROM loans WHERE id = ?", (loan_id,)).fetchone()
    conn.close()
    return _loan_to_dict(row) if row else None


def get_loans_by_member(member_id: int) -> list[dict]:
    conn = get_db()
    rows = conn.execute("SELECT * FROM loans WHERE member_id = ?", (member_id,)).fetchall()
    conn.close()
    return [_loan_to_dict(r) for r in rows]


def create_loan(book_id: int, member_id: int, due_date: str, checked_out: str) -> dict:
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO loans (book_id, member_id, due_date, checked_out) VALUES (?, ?, ?, ?)",
        (book_id, member_id, due_date, checked_out),
    )
    conn.execute("UPDATE books SET available = 0 WHERE id = ?", (book_id,))
    conn.commit()
    row = conn.execute("SELECT * FROM loans WHERE id = ?", (cur.lastrowid,)).fetchone()
    conn.close()
    return _loan_to_dict(row)


def return_loan(loan_id: int, book_id: int, fine: float) -> dict:
    conn = get_db()
    conn.execute("UPDATE loans SET returned = 1, fine = ? WHERE id = ?", (fine, loan_id))
    conn.execute("UPDATE books SET available = 1 WHERE id = ?", (book_id,))
    conn.commit()
    row = conn.execute("SELECT * FROM loans WHERE id = ?", (loan_id,)).fetchone()
    conn.close()
    return _loan_to_dict(row)


def renew_loan(loan_id: int, new_due_date: str) -> dict:
    conn = get_db()
    conn.execute(
        "UPDATE loans SET due_date = ?, renewals = renewals + 1 WHERE id = ?",
        (new_due_date, loan_id),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM loans WHERE id = ?", (loan_id,)).fetchone()
    conn.close()
    return _loan_to_dict(row)


def pay_fine(loan_id: int) -> dict:
    conn = get_db()
    conn.execute("UPDATE loans SET fine_paid = 1 WHERE id = ?", (loan_id,))
    conn.commit()
    row = conn.execute("SELECT * FROM loans WHERE id = ?", (loan_id,)).fetchone()
    conn.close()
    return _loan_to_dict(row)
