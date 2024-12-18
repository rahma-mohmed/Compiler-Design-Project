TOKENS = [
    ("ASSIGN", "="),
    ("PLUS", "+"),
    ("MINUS", "-"),
    ("MULT", "*"),
    ("DIV", "/"),
    ("LARGERTHAN", ">"),
    ("LESSTHAN", "<"),
    ("EQUALS", "=="),
    ("NOTEQUALS", "!="),
    ("LPAREN", "("),
    ("RPAREN", ")"),
    ("LBRACE", "{"),
    ("RBRACE", "}"),
    ("LBRACKET", "["),
    ("RBRACKET", "]"),
    ("COLON", ":"),
    ("COMMA", ","),
    ("NUMBER", "0123456789"),
    ("WHITESPACE", " \t\n"),
]

KEYWORDS = {"if", "else", "for", "print", "in", "range"}

def is_identifier_start(char):
    return char.isalpha() or char == "_"

def is_identifier_part(char):
    return char.isalnum() or char == "_"

def tokenize(code):
    tokens = []
    i = 0
    line = 1
    col = 1

    while i < len(code):
        char = code[i]

        if char in " \t\n":
            if char == "\n":
                line += 1
                col = 1
            else:
                col += 1
            i += 1
            continue

        if is_identifier_start(char):
            identifier = char
            i += 1
            col += 1
            while i < len(code) and is_identifier_part(code[i]):
                identifier += code[i]
                i += 1
                col += 1
            if identifier in KEYWORDS:
                tokens.append(("KEYWORD", identifier))
            else:
                tokens.append(("ID", identifier))
            continue

        # quote_type = ' \ "
        if char in "'\"":
            quote_type = char
            string_literal = ""
            i += 1
            col += 1
            while i < len(code) and code[i] != quote_type:
                # مافيش قافله استرينج
                if code[i] == "\n":
                    raise ValueError(f"Unterminated string literal at line {line}, col {col}")
                string_literal += code[i]
                i += 1
                col += 1
            if i >= len(code) or code[i] != quote_type:
                raise ValueError(f"Unterminated string literal at line {line}, col {col}")
            i += 1  
            col += 1
            tokens.append(("STRING", string_literal))
            continue

        #multi-character operators: == , !=
        if i + 1 < len(code) and code[i:i + 2] in {"==", "!="}:
            tokens.append(("OPERATOR", code[i:i + 2]))
            i += 2
            col += 2
            continue

        # single-character tokens
        for type, character in TOKENS:
            if char in character:
                if type == "NUMBER":
                    number = char
                    i += 1
                    col += 1
                    while i < len(code) and code[i] in "0123456789":
                        number += code[i]
                        i += 1
                        col += 1
                    tokens.append((type, number))
                else:
                    tokens.append((type, char))
                    i += 1
                    col += 1
                break
        else:
            raise ValueError(f"Unexpected character '{char}' at line {line}, col {col}")

    return tokens
