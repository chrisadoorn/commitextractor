from pyparsing import QuotedString, cppStyleComment, rest_of_line

#takes a text and removes single and multiline comments and literals
def parseText(source_code : str) -> str:
    # Define a parser for multiline strings with QuotedString
    multilineparser = QuotedString("'", multiline=True) | QuotedString('"', multiline=True)
    # Define a parser for C++ style comments
    commentparser = rest_of_line + cppStyleComment + rest_of_line
    comment3 = (multilineparser.suppress().transform_string(script))
    comment4 = (commentparser.suppress().transform_string(comment3))
    return comment4

#het te vergelijken woord moet evenlang zijn als het item in de sequence
def check(word, sequence) -> (str,bool):
    found = False
    for index, item in enumerate(sequence):
        testword = word[:len(sequence[int(f"{index}")])]
        if item == testword:
            found = True
            break
    return (testword,found)
#                if c in self.identifier_alphabet:
    #                    w = self.concat(line_list, c)
    #               value1, value2 = check(w, text_to_find);
    #               if value2:
#                   instances_found.append(value1)

#puts the use statements all in one line in fulltext
def UseStatementsOneLine(file_path: str) -> str:
    content = ""
    inside_braces = False
    with open(file_path, 'r') as file:
        for line in file:
            if not inside_braces:
                if 'use ' in line and ';' in line:
                    if line.index('use') < 2:
                        content += line.lstrip()
                elif 'use ' in line and line.index('use') < 2 and ';' not in line:
                    if line.index('use') < 2:
                        inside_braces = True
                        end_index = line.index('{') + 1
                        content += line[0:end_index]
                        modules_inside_braces = line[end_index:].split(',')
                        for module in modules_inside_braces:
                            if len(module) > 1:
                                if is_last_element(modules_inside_braces, module):
                                    content += f"{module.lstrip().rstrip()}"
                                else:
                                    content += f"{module.lstrip().rstrip()},"
                else:
                    content += line
            else:
                modules_inside_braces = line[0:].split(',')
                for module in modules_inside_braces:
                    if len(module) > 1:
                        if is_last_element(modules_inside_braces, module):
                            content += f"{module.lstrip().rstrip()}"
                        else:
                            content += f"{module.lstrip().rstrip()},"
                if ';' in line:
                    content += f"\n"
                    inside_braces = False
    return content

#puts the use statements all in one line in difftext
def UseStatementsOneLineDiffText(file_path: str) -> str:
    content = ""
    inside_braces = False
    with open(file_path, 'r') as file:
        for line in file:
            if not inside_braces:
                if 'use ' in line and ';' in line:
                    if line.index('use') < 2:
                        content += line.lstrip()
                elif 'use ' in line and line.index('use') < 2 and ';' not in line:
                    if line.index('use') < 2:
                        inside_braces = True
                        end_index = line.index('{') + 1
                        content += line[0:end_index]
                        modules_inside_braces = line[end_index:].split(',')
                        for module in modules_inside_braces:
                            if len(module) > 1:
                                if is_last_element(modules_inside_braces, module):
                                    content += f"{module.lstrip().rstrip()}"
                                else:
                                    content += f"{module.lstrip().rstrip()},"
                else:
                    content += line
            else:
                modules_inside_braces = line[0:].split(',')
                for module in modules_inside_braces:
                    if len(module) > 1:
                        if is_last_element(modules_inside_braces, module):
                            content += f"{remove_char(module).lstrip().rstrip()}"
                        else:
                            content += f"{remove_char(module).lstrip().rstrip()},"
                if ';' in line:
                    content += f"\n"
                    inside_braces = False
    return content

def is_last_element(lst, element):
    return element in lst and lst.index(element) == len(lst) - 1

def remove_char(input_str: str):
    input1 = input_str.replace('+', '')
    return input1.replace('-', '')

#makes the simultaneously binding of a list of paths with a common prefix, using the glob-like brace syntax use a::b::{c, d, e::f, g::h::i}
#into individual paths
def transform_paths(file_path: str):
    output_lines = []

    with open(file_path, 'r') as file:
        for line in file:
            if 'use std::{' in line:
                modules = line.split('use std::{')[1].split('};')[0].split(',')
                prefix, _ = line.split('use std::{')
                for module in modules:
                    if '{' not in module and '}' not in module:
                        output_lines.append(f"{prefix}use std::{module.lstrip().rstrip()};")
                    elif '}' in module:
                        prefix3, _ = module.split('}')
                        output_lines.append(f"{prefix}use std::{prefix2.lstrip().rstrip()}{prefix3.lstrip().rstrip()};")
                    elif '{' in module:
                        prefix2, postfix = module.split('{')
                        output_lines.append(f"{prefix}use std::{prefix2.lstrip().rstrip()}{postfix.lstrip().rstrip()};")
            else:
                output_lines.append(line)
    return '\n'.join(output_lines)


if __name__ == "__main__":
    file_path = "../../tests/data/read_diff_rust.txt"
    result = UseStatementsOneLine(file_path)
    print(result)
    """file_path = "./data/read_diff_rust.txt"
    output_text = transform_paths(file_path)
    print(output_text)"""