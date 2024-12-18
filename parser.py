class ParseNode:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []

    def __str__(self, level=0, is_last=True):
        edge = "└── " if is_last else "├── "
        ret = "  " * level + edge + repr(self.value) + "\n"

        for i, child in enumerate(self.children):
            ret += child.__str__(level + 1, is_last=(i == len(self.children) - 1))
        
        return ret


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def match(self, expected_type):
        token = self.current_token()
        if token and token[0] == expected_type:
            self.pos += 1
            return token
        else:
            raise SyntaxError(f"Expected {expected_type}, found {token}")

    def parse_program(self):
        return ParseNode("Program", self.parse_statements())

    def parse_statements(self):
        statements = []
        while self.current_token():
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        token = self.current_token()
        if token[0] == "ID":
            return self.parse_assignment()
        elif token[0] == "KEYWORD" and token[1] == "if":
            return self.parse_if_statement()
        elif token[0] == "KEYWORD" and token[1] == "else":
            return self.parse_else_statement()
        elif token[0] == "KEYWORD" and token[1] == "print":
            return self.parse_print_statement()
        else:
            raise SyntaxError(f"Unexpected statement: {token}")

    def parse_assignment(self):
        id_token = self.match("ID")
        self.match("ASSIGN")
        expr = self.parse_expression()
        return ParseNode("Assignment", [ParseNode(id_token), expr])

    def parse_else_statement(self):
        self.match("KEYWORD") 
        self.match("COLON")
        else_body = self.parse_statements()
        return ParseNode("Else", else_body)

    def parse_if_statement(self):
        self.match("KEYWORD")  
        condition = self.parse_expression()  
        self.match("COLON")
        body = self.parse_statements()

        else_node = None
        if self.current_token() and self.current_token()[0] == "KEYWORD" and self.current_token()[1] == "else":
            else_node = self.parse_else_statement() 

        children = [
            condition,
            ParseNode("Body", body)
        ]
    
        if else_node:
            children.append(ParseNode("Else", [else_node]))  # Only add the Else node if it exists

        return ParseNode("IfStatement", children)

    def parse_print_statement(self):
        self.match("KEYWORD") 
        self.match("LPAREN")  
        arguments = []

        while self.current_token() and self.current_token()[0] != "RPAREN":
            if self.current_token()[0] == "COMMA":
                self.match("COMMA")  
            else:
                if self.current_token()[0] == "STRING":
                    arguments.append(ParseNode(self.match("STRING")))
                elif self.current_token()[0] == "ID":
                    arguments.append(ParseNode(self.match("ID")))
                else:
                    raise SyntaxError(f"Unexpected token in print statement: {self.current_token()}")

        self.match("RPAREN")  
        return ParseNode("Print", arguments)
    
    def parse_expression(self):
        left = self.parse_term()
        while self.current_token() and self.current_token()[0] in {"PLUS", "MINUS"}:
            op = self.match(self.current_token()[0])
            right = self.parse_term()
            left = ParseNode("Expression", [left, ParseNode(op), right])

        while self.current_token() and self.current_token()[0] in {"LARGERTHAN", "LESSTHAN", "EQUALS", "NOTEQUALS"}:
            op = self.match(self.current_token()[0])  
            right = self.parse_term()
            left = ParseNode("RelationalExpression", [left, ParseNode(op), right])

        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.current_token() and self.current_token()[0] in {"MULT", "DIV"}:
            op = self.match(self.current_token()[0])
            right = self.parse_factor()
            left = ParseNode("Term", [left, ParseNode(op), right])
        return left

    def parse_factor(self):
        token = self.current_token()
        if token[0] == "NUMBER":
            return ParseNode(self.match("NUMBER"))
        elif token[0] == "ID":
            return ParseNode(self.match("ID"))
        elif token[0] == "STRING":
            return ParseNode(self.match("STRING"))
        elif token[0] == "LPAREN":
            self.match("LPAREN")
            expr = self.parse_expression()
            self.match("RPAREN")
            return expr
        elif token[0] == "LBRACKET":  
            self.match("LBRACKET")
            elements = []
            while self.current_token() and self.current_token()[0] != "RBRACKET":
                if self.current_token()[0] == "COMMA":
                    self.match("COMMA")  
                else:
                    elements.append(self.parse_expression())
            self.match("RBRACKET")
            return ParseNode("Array", elements)
        else:
            raise SyntaxError(f"Unexpected factor: {token}")


