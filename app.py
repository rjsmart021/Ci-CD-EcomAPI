from flask import Flask
from flask_marshmallow import Marshmallow
import mysql.connector
from mysql.connector import Error 
from Marshmallow import Schema, fields, ValidationError 
from password import my_password
#------------------------------------------------------------------------------------
app = Flask(__name__)
ma = Marshmallow(app)

#Order schema using Marshmallow
class OrderSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    customer_id = fields.Int(required=True)
    date = fields.Date(required=True)

#Initialize schema
order_schema = OrderSchema()
order_schema = OrderSchema(many=True)
#--------------------------------------------------------------------------------------
def get_db_connection():
    """Connect to the MySQL database and return the connection object"""
# Database connection parameters
db_name = "e_commerce_db"
user = "root"
password = my_password # <== Your own password here
host = "localhost"

try:
    # Attempting to establish a connection
    conn = mysql.connector.connect(
        database=db_name,
        user=user,
        password=password,
        host=host
    )
    # Check if the connection is successful
    print("Connected to MySQL database successfully")
    return conn

except Error as e:
    #Handling any connection errors
    print(f"Error: {e}")
    return None

#------------------------------------------------------------------------------
#POST route with Validation
@app.route('/orders', methods=['POST'])
def add_order():
    try:
        #Validate and desrialize input
        order_data = order_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = conn.cursor()
        query = "INSERT INTO Orders (date, customer_id) VALUES (%s, %s)"
        cursor.excecute(query, (order_data['date'], order_data['customer_id']))
        conn.commit()
        return jsonify({"message": "order added successfully"}, 201)
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()
#-----------------------------------------------------------------------------------------------
# Get route for all orders
@app.route('/orders', methods=['GET'])
def get_orders():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.excecute("SELECT * FROM Orders WHERE id = %s", (order_id,))
    order = cursor.fetchone()
    cursor.close()
    conn.close()

    if order:
        return order_schema.jsonify(order)
    else: 
        return jsonify({"error": "Order not found"}), 404
#-----------------------------------------------------------------------------------------------------------
#PUT route with Validation
@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    try:
        #validate and deserialize input
        order_data = order_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = conn.cursor()
        query = "UPDATE Orders SET data = %s, customer_id = %s WHERE id = %s"
        cursor.execute(query, (order_date['date'], order_data["customer_id"], order_id))
        conn.commit()
        return jsonify({"message": "Order updated successfully"}), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

#--------------------------------------------------------------------------------------------------------------
#DELETE route
@app.route('/orders/int:order_id>', methods=['DELETE'])
    def delete_order(order_id):
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Fatabase connection failed"}), 500
        
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Orders Where id = %s", (order_id,))
            conn.commit()
            return jsonify({"message": Order deleted successfully}), 200
        
        except Error as e:
            return jsonify({"error": str(e)}), 500
        
        finally:
            cursor.close()
            conn.close()

    if__name__== '__main__':
    app.run(debug=True):
