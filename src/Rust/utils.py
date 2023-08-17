from pyparsing import QuotedString, cppStyleComment, rest_of_line
import re

##########################PARSER#############################################################
#takes a text and removes single and multiline comments and literals
def parseText(source_code : str) -> str:
    # Define parsers for strings and comments
    commentparser = cppStyleComment
    multilineparser = QuotedString("'", multiline=True) | QuotedString('"', multiline=True)
    text = (multilineparser.suppress().transform_string(CleanUpFullText(source_code)))
    return commentparser.suppress().transform_string(text)

#clean up empty lines, remove multiple spaces with a single space
def CleanUpFullText(script: str) -> str:
    output_lines = []
    lines = script.split('\n')
    for line in lines:
        line = re.sub(r'\s+', ' ', line).lstrip().rstrip()
        output_lines.append(line)
    return '\n'.join(output_lines)


##########################DIFFTEXT#############################################################
#clean up lines not preceded by +, empty lines, remove multiple spaces with a single space and remove single line comments and literals
def CleanUpDiffText(script: str) -> str:
    output_lines = []
    lines = script.split('\n')
    for line in lines:
        line = splits(re.sub(r"(['\"].*?['\"])", " ", re.sub(r'\s+', ' ', line)).lstrip().rstrip())
        if check_first_character(line) and any(char != '+' for char in line):
            output_lines.append(line)
    return '\n'.join(output_lines)

def check_first_character(line):
    if stripped_line := line.lstrip():
        first_char = stripped_line[0]
        if first_char == '+':
            return True
    return False

#clean up lines with single line comments
def splits(script: str) -> str:
    return script.split('//')[0] if '//' in script else script
