##
# The parser consists of three components, each of which handles a different stage of the
# parsing process. The three stages are:
import string



# Stage 1: Lexical analysis, break down the input into tokens
# Stage 2: Syntactic analysis: parse tree
# Stage 3: Semantic analysis


JAVA_IDENTIFIER_GRAMMAR = list(string.ascii_lowercase) + list(string.ascii_uppercase) + ['_', '$'] + \
                          [str(i) for i in list(range(0, 10))]


def find_all_identifiers(text: str):
    start_word = False
    word = ""
    identifiers = []
    string_literal_found = False
    start_comment_found = False
    end_comment_found = False
    for c in list(text):
        if c == '"':
            if string_literal_found:
                string_literal_found = False
            else:
                string_literal_found = True
        if string_literal_found:
            continue

        if c == '/':
            if start_comment_found:
                break
            elif end_comment_found:
                end_comment_found = False
                identifiers = []
                continue
            else:
                start_comment_found = True
                continue

        if c == '*':
            if start_comment_found:
                break
            else:
                end_comment_found = True
                continue

        start_comment_found = False
        if c in JAVA_IDENTIFIER_GRAMMAR:
            word += c
            start_word = True
        else:
            if start_word:
                start_word = False
                identifiers.append(word)
                word = ""
    if start_word:
        identifiers.append(word)
    return identifiers


if __name__ == '__main__':
    print(find_all_identifiers('fr9om//" //a"_pp "//{import :"app.'))
    print(find_all_identifiers('fr9om /* a_pp  app.'))
    print(find_all_identifiers('fr9om */ a_pp  app.'))
