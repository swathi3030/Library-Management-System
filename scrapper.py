import threading
from db import get_db_conn
from logger import get_logger

logger = get_logger(__name__)

def calculate_stock_value_batch(batch):
    total = sum(row[2] * row[3] for row in batch)
    logger.info(f"Batch: {[(row[1], row[2], row[3]) for row in batch]}")
    return total

def get_all_books():
    with get_db_conn() as conn:
        return conn.execute("SELECT * FROM Book").fetchall()

def calculate_total_stock_value():
    books = get_all_books()
    batches = [books[i:i+10] for i in range(0, len(books), 10)]
    results = []
    threads = []
    for batch in batches:
        thread = threading.Thread(target=lambda b: results.append(calculate_stock_value_batch(b)), args=(batch,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    total_value = sum(results)
    logger.info(f"Total stock value: {total_value}")
    return total_value
