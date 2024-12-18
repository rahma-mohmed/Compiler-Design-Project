import re

start_symbol = ""
productions = {}
first_table = {}
follow_table = {}

def creatProduction(file_path):
    global start_symbol, productions
    with open(file_path, "r") as file:
        for production in file:
            lhs, rhs = re.split(r"->", production)
            rhs = re.split(r"\||\n", rhs)
            productions[lhs.strip()] = set(rhs) - {''}
            if not start_symbol:
                start_symbol = lhs.strip()

def isNonterminal(symbol):
    return symbol.isupper()

def eliminateLeftRecursion():
    global productions
    new_productions = {}
    for nt, rules in productions.items():
        alpha_rules = set()  
        beta_rules = set()  
        for rule in rules:
            if rule.startswith(nt): 
                alpha_rules.add(rule[len(nt):])
            else:
                beta_rules.add(rule)
        
        if alpha_rules:
            nt_new = nt + "'" 
            while nt_new in productions:  
                nt_new += "'"
            new_productions[nt] = {beta + nt_new for beta in beta_rules}
            new_productions[nt_new] = {alpha + nt_new for alpha in alpha_rules} | {"#"}
        else:
            new_productions[nt] = rules
    
    productions = new_productions

def performLeftFactoring():
    global productions
    new_productions = {}
    for nt, rules in productions.items():
        prefix_map = {}
        for rule in rules:
            prefix = rule[0]
            if prefix not in prefix_map:
                prefix_map[prefix] = []
            prefix_map[prefix].append(rule)
        
        new_rules = set()
        for prefix, grouped_rules in prefix_map.items():
            if len(grouped_rules) > 1:
                nt_new = nt + "'"  
                while nt_new in productions:  
                    nt_new += "'"
                new_rules.add(prefix + nt_new)
                new_productions[nt_new] = {rule[1:] or "#" for rule in grouped_rules}
            else:
                new_rules.add(grouped_rules[0])
        new_productions[nt] = new_rules
    
    productions.update(new_productions)

def firstFunc(symbol):
    if symbol in first_table:
        return first_table[symbol]
    
    if isNonterminal(symbol):
        first = set()
        for production in productions[symbol]:
            if production:
                first_element = production[0]
                fst = firstFunc(first_element)
                first = first.union(fst)
        return first
    else:
        return set(symbol)

def followFunc(symbol):
    if symbol not in follow_table:
        follow_table[symbol] = set()
    for nt in productions.keys():
        for rule in productions[nt]:
            pos = rule.find(symbol)
            if pos != -1:
                if pos == (len(rule) - 1):
                    if nt != symbol:
                        follow_table[symbol] = follow_table[symbol].union(followFunc(nt))
                else:
                    first_next = set()
                    for next in rule[pos + 1:]:
                        fst_next = firstFunc(next)
                        first_next = first_next.union(fst_next - {'#'})
                        if '#' not in fst_next:
                            break
                    if '#' in fst_next:
                        if nt != symbol:
                            follow_table[symbol] = follow_table[symbol].union(followFunc(nt))
                            follow_table[symbol] = follow_table[symbol].union(first_next) - {'#'}
                    else:
                        follow_table[symbol] = follow_table[symbol].union(first_next)
    return follow_table[symbol]

def compute_first_follow(file_path):
    global first_table, follow_table
    creatProduction(file_path)
    eliminateLeftRecursion()
    performLeftFactoring()
    
    for nt in productions:
        first_table[nt] = firstFunc(nt)
    follow_table[start_symbol] = set('$')
    for nt in productions:
        follow_table[nt] = followFunc(nt)
    

    result = {}
    for nt in productions:
        result[nt] = (list(first_table[nt]), list(follow_table[nt]))
    return result  
