import sqlite3

# Connect to the database
conn = sqlite3.connect('products.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        buying_price REAL
    )
''')
conn.commit()

# Example: Insert sample data (remove/comment after first run)
# cursor.executemany('INSERT INTO products (name, buying_price) VALUES (?, ?)', [
#     ('Product A', 150.0),
#     ('Product B', 220.0),
#     ('Product C', 99.0)
# ])
# conn.commit()

# Fetch and sort products by buying price (max to min)
cursor.execute('SELECT name, buying_price FROM products ORDER BY buying_price DESC')
results = cursor.fetchall()

print("Product Buying Prices (High to Low):")
for name, price in results:
    print(f"{name}: {price}")

conn.close()