from flask import Flask, jsonify, request
from rule_engine import parse_rule, combine_rules, evaluate_rule
import mysql.connector
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def api_root():
    return jsonify({"message": "API is working!"})

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'khushbu123',
    'database': 'rule_engine_db'
}

def init_db():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS rules (
            id INT AUTO_INCREMENT PRIMARY KEY,
            rule_string TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS rule_metadata (
            rule_id INT,
            attribute VARCHAR(255),
            `condition` VARCHAR(255),
            value VARCHAR(255),
            FOREIGN KEY (rule_id) REFERENCES rules(id) ON DELETE CASCADE
        )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        logging.info("Database initialized successfully.")
    except mysql.connector.Error as e:
        logging.error(f"Database initialization error: {e}")

def store_rule(rule_string):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO rules (rule_string) VALUES (%s)", (rule_string,))
        rule_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        logging.info("Rule saved successfully: %s", rule_string)
        return rule_id
    except mysql.connector.Error as e:
        logging.error(f"Error saving rule: {e}")
        return None

@app.route('/api/rules', methods=['POST'])
def create_rule():
    data = request.json
    rule_string = data.get('rule_string')

    if not rule_string:
        return jsonify({"error": "Rule string is required"}), 400

    try:
        rule_ast = parse_rule(rule_string)
    except SyntaxError as e:
        return jsonify({"error": f"Invalid rule syntax: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    rule_id = store_rule(rule_string)

    if rule_id is None:
        return jsonify({"error": "Failed to save the rule in the database."}), 500

    return jsonify({"rule_id": rule_id, "rule_ast": str(rule_ast)}), 201

@app.route('/api/rules', methods=['GET'])
def get_rules():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT id, rule_string, created_at FROM rules")
        rules = cursor.fetchall()
        cursor.close()
        conn.close()
        
        rules_list = [{"id": rule[0], "rule_string": rule[1], "created_at": rule[2]} for rule in rules]
        return jsonify({"rules": rules_list}), 200

    except mysql.connector.Error as e:
        logging.error(f"Error fetching rules: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/evaluate_rule', methods=['POST'])
def evaluate_user():
    data = request.json
    rule_string = data.get('rule_string')
    user_data = data.get('user_data')

    if not rule_string:
        return jsonify({"error": "Rule string is required"}), 400
    if not user_data or not isinstance(user_data, dict):
        return jsonify({"error": "User data is required and should be a dictionary"}), 400

    try:
        rule = parse_rule(rule_string)
        result = evaluate_rule(rule, user_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"result": result})

@app.route('/api/combine_rules', methods=['POST'])
def combine_and_store_rules():
    data = request.json
    rule_strings = data.get('rules')

    if not rule_strings or not isinstance(rule_strings, list):
        return jsonify({"error": "A list of rule strings is required"}), 400

    try:
        ast_rules = [parse_rule(r) for r in rule_strings]
        combined_ast = combine_rules(ast_rules)
        combined_rule_string = " AND ".join(rule_strings)
        
        rule_id = store_rule(combined_rule_string)
        
        return jsonify({"rule_id": rule_id, "combined_ast": str(combined_ast)}), 201
    except Exception as e:
        logging.error(f"Error in combine_and_store_rules: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
