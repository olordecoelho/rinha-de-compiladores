from typing import TypedDict, Literal
import copy

class RinhaError(Exception):
    def __init__(self, message):
        self.message = message

class Term(TypedDict):
    kind: Literal[
        'Int',
        'Str',
        'Call',
        'Binary',
        'Function',
        'Let',
        'If',
        'Print',
        'First',
        'Second',
        'Bool',
        'Tuple',
        'Var'
    ]

class Loc(TypedDict):
    start: int
    end: int
    filename: str

class Parameter(TypedDict):
    text: str
    location: Loc

class File(TypedDict):      
    name: str
    expression: Term
    location: Loc

class If(Term):
    condition: Term
    then: Term
    otherwise: Term
    location: Loc

class Let(Term):
    name: Parameter
    value: Term
    next: Term
    location: Loc

class Str(Term):
    value: str
    location: Loc

class Bool(Term):
    value: bool
    location: Loc

class Int(Term):
    value: int
    location: Loc

BinaryOp = Literal[
    'Add', 'Sub', 'Mul', 'Div', 'Rem', 'Eq', 'Neq', 'Lt', 'Gt', 'Lte', 'Gte', 'And', 'Or'
]

class Binary(Term):
    lhs: Term
    op: BinaryOp
    rhs: Term
    location: Loc

class Call(Term):
    callee: Term
    arguments: list[Term]
    location: Loc

class Function(Term):
    parameters: list[Parameter]
    value: Term
    location: Loc

class Print(Term):
    value: Term
    location: Loc

class First(Term):
    value: Term
    location: Loc

class Second(First):
    pass

class Tuple(Term):
    first: Term
    second: Term
    location: Loc

class Var(Term):
    text: str
    location: Loc

Env = dict[str]

class Closure(TypedDict):
    body: Term
    parameters: list[str]
    env: Env

class BaseValue(TypedDict):
    kind: str

class StringValue(BaseValue):
    value: str

class BooleanValue(BaseValue):
    value: bool

class IntValue(BaseValue):
    value: int

class ClosureValue(BaseValue):
    value: Closure

class TupleValue(BaseValue):
    first: BaseValue
    second: BaseValue

Value = TupleValue | ClosureValue | BooleanValue | IntValue | StringValue

# Utility function to convert a value into an appropriate string representation
def value_to_str(value: Value) -> str:
    if isinstance(value, dict):
        kind = value.get('kind')
        if kind == 'boolean':
            return 'true' if value.get('value') else 'false'
        elif kind == 'string':
            return value.get('value')
        elif kind == 'int':
            return str(value.get('value'))
        elif kind == 'closure':
            return "<#closure>"
        elif kind == 'tuple':
            first_value = value_to_str(value.get('first'))
            second_value = value_to_str(value.get('second'))
            return f"({first_value}, {second_value})"
    return str(value)

# Utility function to check if a value is a tuple
def is_tuple(value: Value) -> bool:
    return value['kind'] == 'tuple'

# Utility function to check if a value is an integer
def is_int(value: Value) -> bool:
    return value['kind'] == 'int'

# Utility function to convert a value into an appropriate string representation
def value_to_str(value: Value) -> str:
    kind = value['kind']
    if kind == 'boolean':
        return 'true' if value['value'] else 'false'
    elif kind == 'string':
        return value['value']
    elif kind == 'int':
        return str(value['value'])
    elif kind == 'closure':
        return "<#closure>"
    elif kind == 'tuple':
        first_value = value_to_str(value['first'])
        second_value = value_to_str(value['second'])
        return f"({first_value}, {second_value})"

# Utility function to raise an error with a message in Portuguese
def launch_error(message: str):
    raise RinhaError(message)

# Interpretation function for integers
def interpret_integer(term: Int, _) -> IntValue:
    return {'kind': 'int', 'value': term['value']}

# Interpretation function for strings
def interpret_string(term: Str, _) -> StringValue:
    return {'kind': 'string', 'value': term['value']}

# Interpretation function for boolean values
def interpret_boolean(term: Bool, _) -> BooleanValue:
    return {'kind': 'boolean', 'value': term['value']}

# Interpretation function for the "if" structure
def interpret_if(term: If, env: Env) -> Value:
    condition = interpret(term['condition'], env)
    if condition['value']:
        return interpret(term['then'], env)
    else:
        return interpret(term['otherwise'], env)

# Interpretation function for the "let" structure
def interpret_let(term: Let, env: Env) -> Value:
    new_env = copy.deepcopy(env)
    value = interpret(term['value'], new_env)
    new_env[term['name']['text']] = value
    return interpret(term['next'], new_env)

# Interpretation function for printing
def interpret_print(term: Print, env: Env) -> Value:
    result = interpret(term['value'], env)
    value_to_str(result) 
    return result['value']  

# Interpretation function for variables
def interpret_variable(term: Var, env: Env) -> Value:
    value = env.get(term['text'])
    if value is None:
        launch_error('não foi possível encontrar a variável {}'.format(term['text']))
    return value

# Interpretation function for function calls
def interpret_call(term: Call, env: Env) -> Value:
    function = interpret(term['callee'], env)
    if function['kind'] != 'closure':
        launch_error('não é possível chamar um valor que não é uma função')
    closure = function['value']
    parameters = closure['parameters']
    if len(parameters) != len(term['arguments']):
        launch_error('número diferente de argumentos')
    new_env = copy.deepcopy(env)
    for i in range(len(parameters)):
        new_env[parameters[i]] = interpret(term['arguments'][i], env)
    return interpret(closure['body'], new_env)

# Interpretation function for binary operations
def interpret_binary_operation(term: Binary, env: Env) -> Value:
    left = interpret(term['lhs'], env)
    right = interpret(term['rhs'], env)
    operator = term['op']

    if operator == 'Add':
        if is_int(left) and is_int(right):
            return {'kind': 'int', 'value': left['value'] + right['value']}
        elif left['kind'] == 'string' or right['kind'] == 'string':
            return {'kind': 'string', 'value': value_to_str(left) + value_to_str(right)}
        else:
            launch_error('operação de adição inválida para tipos {} e {}'.format(left['kind'], right['kind']))

    elif operator in ['Sub', 'Mul', 'Div', 'Rem']:
        if is_int(left) and is_int(right):
            if operator == 'Sub':
                return {'kind': 'int', 'value': left['value'] - right['value']}
            elif operator == 'Mul':
                return {'kind': 'int', 'value': left['value'] * right['value']}
            elif operator == 'Div':
                if right['value'] == 0:
                    launch_error('divisão por zero')
                return {'kind': 'int', 'value': left['value'] // right['value']}
            elif operator == 'Rem':
                if right['value'] == 0:
                    launch_error('resto de divisão por zero')
                return {'kind': 'int', 'value': left['value'] % right['value']}
        else:
            launch_error('operação aritmética inválida para tipos {} e {}'.format(left['kind'], right['kind']))

    elif operator in ['Eq', 'Neq', 'Lt', 'Gt', 'Lte', 'Gte']:
        if left['kind'] == right['kind']:
            if operator == 'Eq':
                return {'kind': 'boolean', 'value': left['value'] == right['value']}
            elif operator == 'Neq':
                return {'kind': 'boolean', 'value': left['value'] != right['value']}
            elif operator == 'Lt':
                return {'kind': 'boolean', 'value': left['value'] < right['value']}
            elif operator == 'Gt':
                return {'kind': 'boolean', 'value': left['value'] > right['value']}
            elif operator == 'Lte':
                return {'kind': 'boolean', 'value': left['value'] <= right['value']}
            elif operator == 'Gte':
                return {'kind': 'boolean', 'value': left['value'] >= right['value']}
        else:
            launch_error('operação de comparação inválida para tipos {} e {}'.format(left['kind'], right['kind']))

    elif operator in ['And', 'Or']:
        if left['kind'] == 'boolean' and right['kind'] == 'boolean':
            if operator == 'And':
                return {'kind': 'boolean', 'value': left['value'] and right['value']}
            elif operator == 'Or':
                return {'kind': 'boolean', 'value': left['value'] or right['value']}
        else:
            launch_error('operação lógica inválida para tipos {} e {}'.format(left['kind'], right['kind']))

# Interpretation function for the "function" structure
def interpret_function(term: Function, env: Env) -> Value:
    parameters = term['parameters']
    body = term['value']

    # Capture the environment at the time of function creation
    env_at_creation = env

    def closure(args: list[Value]) -> Value:
        new_env = copy.deepcopy(env_at_creation)
        
        # Associate arguments with parameters in the function's environment
        for parameter, argument_value in zip(parameters, args):
            new_env[parameter['text']] = argument_value

        return interpret(body, new_env)

    # Return a dictionary with the appropriate structure
    return {'kind': 'closure', 'value': {'body': body, 'parameters': [parameter['text'] for parameter in parameters], 'env': env_at_creation}}

# Interpretation function for the "tuple" structure
def interpret_tuple(term: Tuple, env: Env) -> Value:
    first = interpret(term['first'], env)
    second = interpret(term['second'], env)
    return {'kind': 'tuple', 'first': first, 'second': second}

# Interpretation function for the "first" structure
def interpret_first(term: First, env: Env) -> Value:
    tuple_value = interpret(term['value'], env)
    if tuple_value['kind'] != 'tuple':
        launch_error('a expressão não é uma tupla')
    return tuple_value['first']

# Interpretation function for the "second" structure
def interpret_second(term: Second, env: Env) -> Value:
    tuple_value = interpret(term['value'], env)
    if tuple_value['kind'] != 'tuple':
        launch_error('a expressão não é uma tupla')
    return tuple_value['second']

# Main interpretation function
def interpret(term: Term, env: Env) -> Value:
    kind = term['kind']
    if kind == 'Int':
        return interpret_integer(term, env)
    elif kind == 'Str':
        return interpret_string(term, env)
    elif kind == 'Bool':
        return interpret_boolean(term, env)
    elif kind == 'If':
        return interpret_if(term, env)
    elif kind == 'Let':
        return interpret_let(term, env)
    elif kind == 'Print':
        return interpret_print(term, env)
    elif kind == 'Var':
        return interpret_variable(term, env)
    elif kind == 'Call':
        return interpret_call(term, env)
    elif kind == 'Binary':
        return interpret_binary_operation(term, env)
    elif kind == 'Function':
        return interpret_function(term, env)
    elif kind == 'Tuple':
        return interpret_tuple(term, env)
    elif kind == 'First':
        return interpret_first(term, env)
    elif kind == 'Second':
        return interpret_second(term, env)

class Interpreter:
    def __init__(self, json_data):
        self.file: File = json_data

    def run(self):
        return interpret(self.file, {})
