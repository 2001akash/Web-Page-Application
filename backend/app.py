from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Akash@123'
app.config['MYSQL_DB'] = 'testdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/api/testcases', methods=['GET'])
def get_test_cases():
    try:
        logging.debug("Trying to get cursor")
        cur = mysql.connection.cursor()
        logging.debug("Cursor acquired")
        cur.execute("SELECT * FROM testcases")
        testcases = cur.fetchall()
        cur.close()
        return jsonify(testcases)
    except Exception as e:
        logging.error(f"Error fetching test cases: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/testcases/<int:id>', methods=['PUT'])
def update_test_case(id):
    try:
        status = request.json['status']
        logging.debug(f"Trying to update test case with id: {id} and status: {status}")
        cur = mysql.connection.cursor()
        cur.execute("UPDATE testcases SET status = %s WHERE id = %s", (status, id))
        mysql.connection.commit()
        cur.close()
        socketio.emit('status_update', {'id': id, 'status': status})
        return '', 204
    except Exception as e:
        logging.error(f"Error updating test case: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/test_db_connection', methods=['GET'])
def test_db_connection():
    try:
        logging.debug("Testing MySQL connection...")
        logging.debug(f"MySQL Host: {app.config['MYSQL_HOST']}")
        logging.debug(f"MySQL User: {app.config['MYSQL_USER']}")
        logging.debug(f"MySQL Password: {app.config['MYSQL_PASSWORD']}")
        logging.debug(f"MySQL DB: {app.config['MYSQL_DB']}")
        logging.debug(f"mysql object: {mysql}")

        if mysql is None:
            raise Exception("MySQL object is None")
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT VERSION()")
        db_version = cur.fetchone()
        cur.close()
        return jsonify({"db_version": db_version}), 200
    except Exception as e:
        logging.error(f"Error connecting to database: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    socketio.run(app, debug=True)
