from flask import Flask, request, jsonify, logging, render_template_string
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)
CORS(app)

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

def get_db_connection():
    conn = psycopg2.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        dbname=db_name,
    )
    return conn

@app.route('/add-data', methods=['POST'])
def add_data():
    try:
        app.logger.info("backend --------------------")
        app.logger.info(request)
        print("----------------request")
        data = request.json
        print(data)
        app.logger.info("----data----")
        app.logger.info(data)
        name = data.get('name')
        quantity = data.get('quantity')
        price = data.get('price')

        if not all([name, quantity, price]):
            return jsonify({'error': 'Missing data fields'}), 400

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        create_table_query = '''
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            quantity INTEGER NOT NULL,
            price DECIMAL(10, 2) NOT NULL
        );
        '''
        cursor.execute(create_table_query)
        cursor.execute(
            "INSERT INTO products (name, quantity, price) VALUES (%s, %s, %s) RETURNING id",
            (name, quantity, price)
        )
        product_id = cursor.fetchone()['id']

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'id': product_id, 'name': name, 'quantity': quantity, 'price': price}), 201
    except Exception as e:
        print(e)
        app.logger.error(str(e))

        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)