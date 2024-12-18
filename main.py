import tkinter as tk
from tkinter import ttk, scrolledtext
from lexer import tokenize
from parser import Parser
from symbol import generate_symbol_table
from FirstFollow import compute_first_follow  

def analyze_lexical():
    with open("Code.txt", "r") as file:
        code = file.read()

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Lexical Analysis (Scanner)\n\n", "header")
    tokens = tokenize(code)
    result_text.insert(tk.END, "Tokens:\n", "subheader")
    result_text.insert(tk.END, "\n\n")
    result_text.insert(tk.END, str(tokens) + "\n")

    result_text.tag_configure("header", foreground="#7F00FF", font=("Arial", 12, "bold"))
    result_text.tag_configure("subheader", foreground="darkgreen", font=("Arial", 11, "italic"))

def analyze_parser():
    with open("Code.txt", "r") as file:
        code = file.read()

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Syntax Analysis (Parser)\n\n", "header")
    tokens = tokenize(code)
    parser = Parser(tokens)
    parse_tree = parser.parse_program()
    result_text.insert(tk.END, "    Parse Tree:\n", "subheader")
    result_text.insert(tk.END, "\n\n")
    result_text.insert(tk.END, str(parse_tree) + "\n", "indented")

    result_text.tag_configure("header", foreground="#7F00FF", font=("Arial", 12, "bold"))
    result_text.tag_configure("subheader", foreground="darkgreen", font=("Arial", 11, "italic"))
    result_text.tag_configure("indented", lmargin1=20, font=("Consolas", 10))

def display_symbol_table():
    with open("Code.txt", "r") as file:
        code = file.read()

    symbol_table = generate_symbol_table(code)

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Symbol Table\n\n", "header")
    result_text.insert(tk.END, f"{'Counter':<10}{'Variable Name':<15}{'Object Address':<20}{'Type':<10}{'Dim':<5}{'Line Declared':<15}{'Line Reference'}\n", "table_header")

    for entry in symbol_table:
        line = f"{entry['counter']:<10}{entry['Variable Name']:<15}{entry['Object Address']:<20}{entry['Type']:<10}{entry['Dim']:<5}{entry['Line Declared']:<15}{','.join(map(str, entry['Line Reference']))}\n"
        result_text.insert(tk.END, line)

    result_text.tag_configure("header", foreground="#7F00FF", font=("Arial", 12, "bold"))
    result_text.tag_configure("table_header", foreground="darkblue", font=("Consolas", 10, "bold"))

def display_first_follow():
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "FIRST and FOLLOW Sets\n\n", "header")
    
    first_follow = compute_first_follow('Rule.txt')  
    
    result_text.insert(tk.END, f"{'Non-Terminal':<20}{'First Set':<30}{'Follow Set'}\n", "table_header")
    for nt, (first_set, follow_set) in first_follow.items():
        line = f"{nt:<20}{', '.join(first_set):<30}{', '.join(follow_set)}\n"
        result_text.insert(tk.END, line)
    
    result_text.tag_configure("header", foreground="#7F00FF", font=("Arial", 12, "bold"))
    result_text.tag_configure("table_header", foreground="darkblue", font=("Consolas", 10, "bold"))

root = tk.Tk()
root.title("Compiler Design")
root.geometry("900x700")

frame = ttk.Frame(root, padding=(90, 0, 0, 0))
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

header_label = ttk.Label(frame, text="Code Analysis Tool", font=("Arial", 16, "bold"), foreground="#7F00FF")
header_label.grid(row=0, column=1, pady=10)

style = ttk.Style()
style.configure(
    "Custom.TButton",
    background="#4CAF50",
    foreground="darkgreen",
    height=3,
    font=("Arial", 10, "bold")
)

button_frame = ttk.Frame(frame)
button_frame.grid(row=1, column=0, columnspan=3, pady=10, padx=10)

lexical_button = ttk.Button(button_frame, text="Lexical Analyzer", command=analyze_lexical, style="Custom.TButton")
lexical_button.grid(row=0, column=0, padx=10)

parser_button = ttk.Button(button_frame, text="Syntax Analyzer", command=analyze_parser, style="Custom.TButton")
parser_button.grid(row=0, column=1, padx=10)

symbol_table_button = ttk.Button(button_frame, text="Display Symbol Table", command=display_symbol_table, style="Custom.TButton")
symbol_table_button.grid(row=0, column=2, padx=10)

first_follow_button = ttk.Button(button_frame, text="FIRST and FOLLOW", command=display_first_follow, style="Custom.TButton")
first_follow_button.grid(row=0, column=3, padx=10)

result_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=100, height=35, font=("Consolas", 10))
result_text.grid(row=2, column=0, columnspan=3, pady=10)

root.mainloop()
