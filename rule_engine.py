import ast

class Node:
    def __init__(self, type: str, value=None):
        self.type = type
        self.left = None
        self.right = None
        self.value = value

    def __repr__(self):
        if self.type == 'operand':
            return f"({self.value[0]} {self.value[1]} {self.value[2]})"
        else:
            return f"({self.left} {self.type} {self.right})"

def parse_rule(rule_string: str) -> Node:
    expr = ast.parse(rule_string, mode='eval').body

    def build_ast(expr):
        if isinstance(expr, ast.BoolOp):
            node = Node(type='operator', value='AND' if isinstance(expr.op, ast.And) else 'OR')
            node.left = build_ast(expr.values[0])
            node.right = build_ast(expr.values[1])
            return node
        elif isinstance(expr, ast.Compare):
            left = expr.left.id
            op = type(expr.ops[0]).__name__
            if isinstance(expr.comparators[0], ast.Constant):
                comparator = expr.comparators[0].value
            else:
                raise ValueError("Unsupported operand type")
            return Node(type='operand', value=(left, op, comparator))
        else:
            raise ValueError("Unsupported operation")

    return build_ast(expr)

def combine_rules(rules: list[Node]) -> Node:
    if not all(isinstance(rule, Node) for rule in rules):
        raise ValueError("All rules must be of type Node.")
    
    if len(rules) == 1:
        return rules[0]
    
    combined_root = Node(type='operator', value='AND')
    combined_root.left = rules[0]
    
    for rule in rules[1:]:
        new_node = Node(type='operator', value='AND')
        new_node.left = combined_root
        new_node.right = rule
        combined_root = new_node
    
    return combined_root


def evaluate_rule(rule: Node, data: dict) -> bool:
    if rule.type == 'operand':
        attr, op, value = rule.value
        if op == 'Gt':
            return data[attr] > value
        elif op == 'Lt':
            return data[attr] < value
        elif op == 'Eq':
            return data[attr] == value
        else:
            raise ValueError(f"Unsupported operator: {op}")
    elif rule.type == 'operator':
        if rule.value == 'AND':
            return evaluate_rule(rule.left, data) and evaluate_rule(rule.right, data)
        elif rule.value == 'OR':
            return evaluate_rule(rule.left, data) or evaluate_rule(rule.right, data)
    return False
