def clean_line_rust(line):
    # first clean diff characteristics
    # then language specific
    return clean_rust_comment(clean_diff_line(line))


def clean_diff_line(line):
    # strip (+ / - sign)
    line = line[2:]
    # strip trailing spaces, including line ending
    return line.strip()


def clean_rust_comment(line):
    # strip line comment
    pos_comment = line.find('//')
    if pos_comment > -1:
        line = line[:pos_comment]
    return line

def clean_rust_toml(text):
    # strip line comment
    pos_comment = text.find('dependencies')
    if pos_comment > -1:
        text = text[pos_comment:]
    return text

def read_diff_file(datarow):
    print("lees bestand: " + datarow)
    file = open(filepath, 'rt')
    lines = file.readlines()

    newlines = 0
    removedlines = 0
    for line in lines:
        # count lines beginnend met +
        if line.startswith('+', 1):
            newlines = newlines + 1
            clean_line_rust(line)
        if line.startswith('-', 1):
            removedlines = removedlines + 1
            clean_line_rust(line)

    print("aantal regels in bestand: " + str(len(lines)))
    print("aantal nieuwe regels: " + str(newlines))
    print("aantal oude regels:  " + str(removedlines))