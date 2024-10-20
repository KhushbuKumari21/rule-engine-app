
# Rule Engine with AST

## Objective
This application is a 3-tier rule engine designed to determine user eligibility based on attributes like age, department, income, etc. It uses Abstract Syntax Trees (AST) to represent conditional rules, allowing for dynamic creation, combination, and modification.

## Features
- AST-based rule creation and evaluation
- API to create, combine, and evaluate rules
- Integration with SQL databases like PostgreSQL or MySQL
- Error handling for invalid rule formats

## Technologies Used
- Python
- Flask (API framework)
- SQL/MySQL (Database)
- Requests (for API testing)

## Requirements

- Python 3.8+
- Flask 2.0.1
- MySQL or SQL Database

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/rule-engine-app.git
   cd rule-engine-app

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/weather-monitoring-system.git
   cd weather-monitoring-system
2. Set up your environment:
   pip install -r requirements.txt


3. Set up your MySQL database:
   
   CREATE DATABASE rule_engine_db;
   Update the database connection details in the database.py file.

4. Run the database setup script:
   python database.py

5. Run the application:
   python app.py



6. Access the API at http://127.0.0.1:5000.

## API Endpoints
### 1. Create Rule
**POST /create_rule**
- **Request Body**: 
    ```json
    {
        "rule": "age > 30 AND department = 'Sales'"
    }
    ```
- **Response**: 
    - **Success**: `201 Created`
    - **Error**: `400 Bad Request` (if the rule format is invalid)

### 2. Combine Rules
**POST /combine_rules**
- **Request Body**: 
    ```json
    {
        "rule_ids": [1, 2]
    }
    ```
- **Response**: 
    - **Success**: `200 OK`
    - **Error**: `400 Bad Request` (if no rules found)


 
## Running with Docker
1. Build the Docker image:
   docker build -t rule-engine-app

2. Run the application:
   docker run -p 5000:5000 rule-engine-app


## Testing
   python -m unittest tests/test_app.py

    


# Generatcoverage htmle a text report
coverage report
# Generate an HTML report
coverage html
## What work on which file
# app.py
1.API Root:
   Endpoint: /api
   Method: GET
   Description: Returns a simple message confirming the API is working.

2.Database intialization   
   Automatically initializes the MySQL database and creates necessary tables (rules and rule_metadata) upon startup.
3.Create Rule:
   Endpoint: /api/rules
   Method: POST
   Request Body: { "rule_string": "your_rule_here" }
   Description: Parses and stores a new rule in the database. Returns the rule ID and its AST representation.
4.Retrieve Rules:
  Endpoint: /api/rules
  Method: GET
  Description: Fetches and returns a list of all stored rules along with their IDs and creation timestamps.
  Evaluate Rule:
5.Endpoint: /api/evaluate_rule
  Method: POST
  Request Body: { "rule_string": "your_rule_here", "user_data": { "key": "value" } }
  Description: Evaluates the provided rule against the user data and returns the evaluation result (True/False).
6.Combine Rules:
  Endpoint: /api/combine_rules
  Method: POST
  Request Body: { "rules": ["rule1", "rule2"] }
  Description: Combines multiple rule strings into a single rule and stores it in the database. Returns the combined rule ID and AST.
7.Database Configuration
  Host: localhost
  User: root
  Password: khushbu123
  Database: rule_engine_db
8.Logging
  The application logs various events and errors for troubleshooting.
# database.py
 1. Rule Engine Database Module
  This module provides functionality to manage a MySQL database for storing rules and their metadata.

 2. Features

- **Database Connection**: Establishes a connection to the MySQL database with logging for error handling.
- **Database Initialization**: Creates necessary tables (`Rules` and `RuleMetadata`) if they don't exist.
- **Saving Rules**: Allows saving new rules to the `Rules` table.
- **Saving Rule Metadata**: Facilitates saving metadata related to rules in the `RuleMetadata` table.
- **Fetching Rules**: Retrieves rules by their IDs.
- **Updating Rules**: Updates existing rules in the `Rules` table.

## Usage

### Configuration

Ensure that the database configuration is correct in the `DB_CONFIG` dictionary:

```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'rule_engine_db',
    'user': 'root',
    'password': 'khushbu123'  
}
## rule_engine.py
1.Node Class:
  Represents a node in the AST. Each node can be either an operand (representing a condition) or an operator (AND/OR).
   (a)Attributes:
      type: Type of the node (either operand or operator).
      value: Holds the operator type or the operand's value.
      left and right: Pointers to the left and right children in the tree.
   (b)Methods:
      __repr__: String representation of the node for easy visualization.
2.Parsing Rules:
  (a)Function: parse_rule(rule_string: str) -> Node
     Takes a rule string (e.g., "age > 30 AND income < 100000") and parses it into an AST.
     Uses Python’s ast module to parse the expression and builds the AST recursively.
3.Combining Rules:
  (a)Function: combine_rules(rules: list[Node]) -> Node
     Combines multiple AST nodes into a single AST node using the AND operator.
     Checks that all inputs are of type Node and builds a combined tree structure.
4. Evaluating Rules:
   (a)Function: evaluate_rule(rule: Node, data: dict) -> bool
      Evaluates the AST against a given set of user data (in dictionary format).
      Handles both operands and operators:
         (i)For operands, it checks the condition (e.g., greater than, less than, equality).
         (ii)For operators, it recursively evaluates the left and right children, combining the results based on the operator (AND/OR).
