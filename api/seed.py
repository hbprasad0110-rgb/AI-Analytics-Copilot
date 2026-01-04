import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from db import get_conn
load_dotenv()
STATUSES = ["processing", "shipped", "delivered", "cancelled"]

def seed():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS orders (
              order_id INT PRIMARY KEY,
              user_id INT,
              status TEXT,
              created_at TIMESTAMP,
              amount NUMERIC
            );
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
              item_id INT PRIMARY KEY,
              order_id INT REFERENCES orders(order_id),
              product TEXT,
              quantity INT,
              price NUMERIC
            );
            """)

            # clear old demo data
            cur.execute("DELETE FROM order_items;")
            cur.execute("DELETE FROM orders;")

            now = datetime.now()
            for oid in range(1, 501):
                user_id = random.randint(1, 80)
                status = random.choice(STATUSES)
                created_at = now - timedelta(days=random.randint(0, 120))
                amount = round(random.uniform(10, 400), 2)

                cur.execute(
                    "INSERT INTO orders(order_id, user_id, status, created_at, amount) VALUES (%s,%s,%s,%s,%s)",
                    (oid, user_id, status, created_at, amount)
                )

                # items
                for k in range(random.randint(1, 4)):
                    item_id = oid * 10 + k
                    product = random.choice(["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones"])
                    qty = random.randint(1, 3)
                    price = round(random.uniform(5, 150), 2)
                    cur.execute(
                        "INSERT INTO order_items(item_id, order_id, product, quantity, price) VALUES (%s,%s,%s,%s,%s)",
                        (item_id, oid, product, qty, price)
                    )

        conn.commit()
    print("✅ Seeded demo data successfully!")

if __name__ == "__main__":
    seed()
