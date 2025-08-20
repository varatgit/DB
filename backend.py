import psycopg2
from psycopg2 import sql

def get_connection():
    """Establishes and returns a connection to the PostgreSQL database."""
    return psycopg2.connect(
        host="localhost",
        database="DB fin",
        user="postgres",
        password="vardhini"
    )

# --- CRUD Operations ---

def create_transaction(transaction_id, transaction_date, description, amount, type):
    """Inserts a new transaction into the database."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO transactions (transaction_id, transaction_date, description, amount, type)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (transaction_id, transaction_date, description, amount, type)
        )
        conn.commit()
        return "Transaction created successfully!"
    except Exception as e:
        conn.rollback()
        return f"Error: {e}"
    finally:
        conn.close()

def read_transactions(transaction_type=None, sort_by=None):
    """Reads transactions from the database, with optional filtering and sorting."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = "SELECT * FROM transactions"
        params = []
        
        if transaction_type and transaction_type != 'All':
            query += " WHERE type = %s"
            params.append(transaction_type)
        
        if sort_by:
            if sort_by == 'Amount':
                query += " ORDER BY amount DESC"
            elif sort_by == 'Date':
                query += " ORDER BY transaction_date DESC"
                
        cur.execute(query, params)
        transactions = cur.fetchall()
        return transactions
    finally:
        conn.close()

def update_transaction(transaction_id, new_description, new_amount):
    """Updates an existing transaction's description and amount."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE transactions
            SET description = %s, amount = %s
            WHERE transaction_id = %s
            """,
            (new_description, new_amount, transaction_id)
        )
        conn.commit()
        return "Transaction updated successfully!"
    except Exception as e:
        conn.rollback()
        return f"Error: {e}"
    finally:
        conn.close()

def delete_transaction(transaction_id):
    """Deletes a transaction from the database."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM transactions WHERE transaction_id = %s",
            (transaction_id,)
        )
        conn.commit()
        return "Transaction deleted successfully!"
    except Exception as e:
        conn.rollback()
        return f"Error: {e}"
    finally:
        conn.close()

# --- Aggregation Functions ---

def get_transaction_counts():
    """Returns the total number of transactions."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM transactions")
        return cur.fetchone()[0]
    finally:
        conn.close()

def get_total_revenue():
    """Returns the sum of all revenue transactions."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = 'Revenue'")
        return cur.fetchone()[0]
    finally:
        conn.close()

def get_total_expense():
    """Returns the sum of all expense transactions."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = 'Expense'")
        return cur.fetchone()[0]
    finally:
        conn.close()