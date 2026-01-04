SCHEMA_TEXT = """
Database: copilot_db (PostgreSQL)

Table: orders
- order_id (int)
- user_id (int)
- status (text)
- created_at (timestamp)
- amount (numeric)

Table: order_items
- item_id (int)
- order_id (int)
- product (text)
- quantity (int)
- price (numeric)

Relationships:
- order_items.order_id -> orders.order_id
"""
