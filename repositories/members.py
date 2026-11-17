from database import get_db


def _member_to_dict(row) -> dict:
    return {
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "type": row[3],
    }


def list_members() -> list[dict]:
    conn = get_db()
    rows = conn.execute("SELECT * FROM members").fetchall()
    conn.close()
    return [_member_to_dict(r) for r in rows]


def get_member(member_id: int) -> dict | None:
    conn = get_db()
    row = conn.execute("SELECT * FROM members WHERE id = ?", (member_id,)).fetchone()
    conn.close()
    return _member_to_dict(row) if row else None


def get_member_by_email(email: str) -> dict | None:
    conn = get_db()
    row = conn.execute("SELECT * FROM members WHERE email = ?", (email,)).fetchone()
    conn.close()
    return _member_to_dict(row) if row else None


def create_member(name: str, email: str, member_type: str) -> dict:
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO members (name, email, type) VALUES (?, ?, ?)",
        (name, email, member_type),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM members WHERE id = ?", (cur.lastrowid,)).fetchone()
    conn.close()
    return _member_to_dict(row)
