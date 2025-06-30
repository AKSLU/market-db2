from flask import Flask, render_template, redirect
import psycopg2

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        dbname="base",
        user="postgres",
        password="20062007",
        host="localhost",
        port="5432"
    )

@app.route('/items')
def show_items():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT items2.id, название, цена, описание, image_url, count, postavshic
            FROM items2
            JOIN quantity ON items2.id = quantity.id
        """)
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('items.html', items=items)
    except:
        return "Ошибка при загрузке товаров"

@app.route('/buys')
def show_buys():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.id, i.название, b.quantity
            FROM buys b
            JOIN items2 i ON b.item_id = i.id
        """)
        buys = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('buys.html', buys=buys)
    except  Exception as e:
        return "Ошибка при загрузке покупок: {e}"

@app.route('/buy/<int:item_id>')
def buy(item_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT count FROM quantity WHERE id = %s", (item_id,))
        result = cursor.fetchone()

        if result and result[0] > 0:
            cursor.execute("UPDATE quantity SET count = count - 1 WHERE id = %s", (item_id,))
            cursor.execute("INSERT INTO buys (item_id, quantity) VALUES (%s, 1)", (item_id,))
            conn.commit()

        cursor.close()
        conn.close()
    except Exception as e:
        return f"Ошибка при покупке: {e}"

    return redirect('/items')

if __name__ == '__main__':
    app.run(debug=True)


