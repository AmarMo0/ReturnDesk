import sqlite3

DB_PATH = "support.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cases (
                case_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT NOT NULL,
                request_type TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'open'
            )
            """
        )
        conn.commit()


def get_existing_case(order_id: str, request_type: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        return conn.execute(
            """
            SELECT *
            FROM cases
            WHERE order_id = ?
            AND request_type = ?
            AND status = 'open'
            LIMIT 1
            """,
            (order_id, request_type),
        ).fetchone()


def create_case(order_id: str, request_type: str):

    existing_case = get_existing_case(order_id, request_type)

    if existing_case is not None:
        return existing_case

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        cursor = conn.execute(
            """
            INSERT INTO cases (order_id, request_type, status)
            VALUES (?, ?, ?)
            """,
            (order_id, request_type, "open"),
        )

        case_id = cursor.lastrowid

        conn.commit()

        return conn.execute(
            "SELECT * FROM cases WHERE case_id = ?",
            (case_id,),
        ).fetchone()