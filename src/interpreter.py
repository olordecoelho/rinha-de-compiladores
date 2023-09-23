import numpy as np
import sys

sys.setrecursionlimit(2000000)

class RinhaError(Exception):
    pass

class Closure:
    def __init__(self, func_node, environment):
        self.func_node = func_node
        self.environment = environment

def interpret(node, environment):
    
    execution_stack = [(node, environment)]

    while execution_stack:
        node, environment = execution_stack.pop()

    if isinstance(node, dict):
        kind = node.get("kind")
        if kind == "Int":
            return np.int32(node.get("value", 0))
        elif kind == "Str":
            return node.get("value")
        elif kind == "Bool":
            return node.get("value")
        elif kind == "Binary":
            lhs = interpret(node.get("lhs", node), environment)
            rhs = interpret(node.get("rhs", node), environment)
            op = node["op"]
            operators = {
                "Add": lambda x, y: str(x) + str(y) if isinstance(x, str) or isinstance(y, str) else x + y,
                "Sub": lambda x, y: x - y,
                "Mul": lambda x, y: x * y,
                "Div": lambda x, y: x // y if y != 0 else None,
                "Rem": lambda x, y: x % y if y != 0 else None,
                "Eq": lambda x, y: x == y,
                "Neq": lambda x, y: x != y,
                "Lt": lambda x, y: x < y,
                "Gt": lambda x, y: x > y,
                "Lte": lambda x, y: x <= y,
                "Gte": lambda x, y: x >= y,
                "And": lambda x, y: x and y,
                "Or": lambda x, y: x or y
            }
            if op == "Div" and rhs == 0:
                raise RinhaError("Divisão por zero")
            if op in operators:
                return operators[op](lhs, rhs)
            else:
                raise RinhaError(f"Operador não suportado: {op}")
        elif kind == "Let":
            name = node["name"]["text"]
            new_environment = {**environment}
            new_environment[name] = interpret(node["value"], new_environment)
            return interpret(node.get("next", node), new_environment)
        elif kind == "If":
            condition = interpret(node["condition"], environment)
            return interpret(node["then"] if condition else node["otherwise"], environment)
        elif kind == "Print":
            value = interpret(node["value"], environment)
            output = ", ".join(map(str, value)) if isinstance(value, tuple) else str(value)
            return value
        elif kind == "Function":
            return Closure(node, environment)
        elif kind == "Call":
            callee = interpret(node["callee"], environment)
            args = [interpret(arg, environment) for arg in node["arguments"]]
            if isinstance(callee, Closure):
                func_node = callee.func_node
                func_environment = {**callee.environment}
                func_environment.update({param["text"]: arg for param, arg in zip(func_node["parameters"], args)})
                return interpret(func_node["value"], func_environment)
            else:
                raise RinhaError(f"Chamada da função somente para função: {callee}")
        elif kind == "First":
            tuple_value = interpret(node["value"], environment)
            if isinstance(tuple_value, tuple):
                return tuple_value[0]
            else:
                raise RinhaError(f"Tupla era o que espera-se, mas recebemos {type(tuple_value).__name__}")
        elif kind == "Second":
            tuple_value = interpret(node["value"], environment)
            if isinstance(tuple_value, tuple):
                return tuple_value[1]
            else:
                raise RinhaError(f"Tupla era o que merecemos, mas foi {type(tuple_value).__name__} o que recebemos")
        elif kind == "Tuple":
            first = interpret(node["first"], environment)
            second = interpret(node["second"], environment)
            return (first, second)
        elif kind == "Var":
            var_name = node["text"]
            if var_name in environment:
                return environment[var_name]
            else:
                raise RinhaError(f"Variável '{var_name}' indefinida")
        elif kind == "Parameter":
            return node
    else:
        return node