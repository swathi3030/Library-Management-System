from db import get_db_conn
from logger import get_logger

logger = get_logger(__name__)

def calculate_total_stock_value():
    try:
        with get_db_conn() as conn:
            rows = conn.execute("SELECT price, copies FROM Book").fetchall()
            total_value = sum(price * copies for price, copies in rows)
            logger.info(f"Total stock value: {total_value}")
            return total_value
    except Exception as e:
        logger.error(f"Failed to calculate stock value: {e}")
        return 0
