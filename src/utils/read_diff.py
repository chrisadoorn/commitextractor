def clean_line_java(line):
    # first clean diff characteristics
    # then language specific
    return clean_java_comment(clean_diff_line(line))


def clean_diff_line(line):
    # strip (+ / - sign)
    line = line[2:]
    # strip trailing spaces, including line ending
    return line.strip()


def clean_java_comment(line):
    # strip line comment
    pos_comment = line.find('//')
    if pos_comment > -1:
        line = line[:pos_comment]
    return line


def read_diff_file(filepath):
    print("lees bestand: " + filepath)
    file = open(filepath, 'rt')
    lines = file.readlines()
    file.close()

    newlines = 0
    removedlines = 0
    for line in lines:
        # count lines beginnend met +
        if line.startswith('+', 1):
            newlines = newlines + 1
            clean_line_java(line)
        if line.startswith('-', 1):
            removedlines = removedlines + 1
            clean_line_java(line)

    print("aantal regels in bestand: " + str(len(lines)))
    print("aantal nieuwe regels: " + str(newlines))
    print("aantal oude regels:  " + str(removedlines))
