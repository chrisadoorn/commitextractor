# java_parser

#### Introduction
The java_parser module analyses only java code.
The parser uses antlr4 (https://www.antlr.org/).
The grammar (g4 files) has been downloaded from https://github.com/antlr/grammars-v4
To use the parser it is necessary to install a java runtime and follow the instructions on https://www.antlr.org/download.html.
After installing the parser, it is necessary to generate the python interface to the java runtime for this grammar.
The generated files are included in this project( The JavaParser* and JavaLexer* files).

The module reads data from a view made for this purpose, java_parser_selection_view.
Result of the process are stored in java_parse_result.
The results are overwritten when the analysis is repeated. 

#### configuration
The module reuses the commitextractor.ini file.
It sets the processtap to _java_parsing_
It's specific configuration items are in its module section.
 **Module**
* **java_parser**
 **Options**  
* **loglevel** The loglevel for this module. This has to be a valid string representation of a loglevel (see https://docs.python.org/3/library/logging.html#levels)
* **run_parallel** The number of processes to run parrallel. As this module uses a lot of computing power it is advisible to run multiple processes at once. Different project will then be processed at once. However, a single project will always be processed sequential.
* **vorige_stap** The previous completed step. Standard is to perform this module after completing _zoekterm_controleren_ 

