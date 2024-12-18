import re

TYPE_SIZES = {
    'int': 2,
    'float': 4,
    'char': 1,
}

def generate_symbol_table(code):
    pattern = r"(\w+)\s*=\s*(.*)"
    lines = code.strip().split('\n')
    symbol_table = []
    current_address = 0

    def get_var_type_and_size(var_value):
        if re.match(r'^[\d\+\-\*/\(\) ]+$', var_value): 
            return 'int', TYPE_SIZES['int']
        elif var_value.startswith('[') and var_value.endswith(']'):  
            num_elements = len(re.findall(r'\d+', var_value))
            return 'arr', TYPE_SIZES['int'] * num_elements
        elif '"' in var_value:
            return 'char', TYPE_SIZES['char'] * len(var_value.replace('"', '')) 
        else:
            return 'int', TYPE_SIZES['int']

    for line_num, line in enumerate(lines, 1):
        match = re.match(pattern, line.strip())
        if match:
            var_name, var_value = match.groups()
            var_type, var_size = get_var_type_and_size(var_value)
            symbol_table.append({
                'counter': len(symbol_table) + 1,
                'Variable Name': var_name,
                'Object Address': current_address,
                'Type': var_type,
                'Dim': 0 if var_type in ['int', 'float', 'char'] else 1,
                'Line Declared': line_num,
                'Line Reference': []
            })
            current_address += var_size

    for line_num, line in enumerate(lines, 1):
        for var in symbol_table:
            if var['Variable Name'] in line and var['Line Declared'] != line_num:
                if "print" in line.strip():
                    if var['Variable Name'] in re.findall(r'\w+', line):
                        var['Line Reference'].append(line_num)
                elif "[" not in line.strip():
                    var['Line Reference'].append(line_num)

    return symbol_table
