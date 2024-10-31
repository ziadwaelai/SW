import re
from abc import ABC, abstractmethod

# Token types
INTEGER, PLUS, MINUS, MULTIPLY, DIVIDE, POWER, REGEX, VALUE, PATTERN, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'POWER', 'REGEX', 'VALUE', 'PATTERN', 'EOF'
)

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {repr(self.value)})"

    def __repr__(self):
        return self.__str__()

class TokenFactory:
    @staticmethod
    def create_token(text):
        if text.isdigit():
            return Token(INTEGER, int(text))
        elif text == '+':
            return Token(PLUS, text)
        elif text == '-':
            return Token(MINUS, text)
        elif text == '*':
            return Token(MULTIPLY, text)
        elif text == '/':
            return Token(DIVIDE, text)
        elif text == '^':
            return Token(POWER, text)
        elif text == "Regex":
            return Token(REGEX, text)
        elif text.startswith('"') and text.endswith('"'):
            return Token(PATTERN, text[1:-1])  # Remove quotes from the pattern
        else:
            return Token(VALUE, text.strip())

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def get_next_token(self):
        if self.pos >= len(self.text):
            return Token(EOF, None)

        current_char = self.text[self.pos]

        # Skip whitespace
        if current_char.isspace():
            self.pos += 1
            return self.get_next_token()

        # Handle Regex function
        if self.text[self.pos:].startswith("Regex"):
            self.pos += len("Regex")
            return TokenFactory.create_token("Regex")

        # Extract attribute value and pattern
        if current_char == '(' or current_char == ',' or current_char == ')':
            self.pos += 1
            return self.get_next_token()  # Ignore separators

        # Handle pattern inside quotes
        if current_char == '"':
            pattern_value = ''
            self.pos += 1  # Skip opening quote
            while self.pos < len(self.text) and self.text[self.pos] != '"':
                pattern_value += self.text[self.pos]
                self.pos += 1
            self.pos += 1  # Skip closing quote
            return TokenFactory.create_token(f'"{pattern_value}"')

        # Capture attribute value or other tokens
        value = ''
        while self.pos < len(self.text) and self.text[self.pos] not in ",) ":
            value += self.text[self.pos]
            self.pos += 1
        return TokenFactory.create_token(value)

# Base Operator using Command Pattern
class Operator(ABC):
    @abstractmethod
    def execute(self, *args):
        pass

class RegexOperator(Operator):
    def execute(self, value, pattern):
        return bool(re.match(pattern, value))

class ArithmeticOperator(Operator):
    def execute(self, expression):
        try:
            return eval(expression)  # For demo purposes only; replace eval in production
        except Exception as e:
            raise ValueError(f"Error evaluating arithmetic expression: {e}")

class OperatorFactory:
    """Factory that maps tokens to their respective operators."""
    OPERATORS = {
        "REGEX": RegexOperator,
        "ARITHMETIC": ArithmeticOperator,
    }

    @staticmethod
    def get_operator(token_type):
        operator_class = OperatorFactory.OPERATORS.get(token_type)
        if operator_class is None:
            raise ValueError(f"Unknown operator for token type: {token_type}")
        return operator_class()  # Instantiate the operator class

class Interpreter:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise ValueError(f"Unexpected token type. Expected {token_type} but got {self.current_token.type}")

    def parse_expression(self):
        # Check if the expression is a Regex operation
        if self.current_token.type == "REGEX":
            self.eat("REGEX")
            value = self.current_token.value
            self.eat(VALUE)
            pattern = self.current_token.value
            self.eat(PATTERN)
            operator = OperatorFactory.get_operator("REGEX")
            return operator.execute(value, pattern)
        
        # Default to arithmetic evaluation for non-Regex expressions
        operator = OperatorFactory.get_operator("ARITHMETIC")
        return operator.execute(self.lexer.text)

class Context:
    """Defines the context in which expressions are evaluated."""
    def __init__(self, expression):
        self.lexer = Lexer(expression)
        self.interpreter = Interpreter(self.lexer)

    def evaluate(self):
        return self.interpreter.parse_expression()

def main():
    while True:
        try:
            text = input("calc> ")
            if not text:
                continue

            context = Context(text)
            result = context.evaluate()
            print(result)
        except EOFError:
            break
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
