import logging


def __is_import_usage(path: list[str]) -> bool:
    length = len(path)
    return path[length - 1] == 'complilationUnit' and path[length - 2] == 'importDeclaration' and path[
        length - 3] == 'import'


def __is_extends_usage(path: list[str]) -> bool:
    """
    Both internal classes as normal classes can extend another class.
    In both cases the structure and depth of the tree is the same.
    :param path:
    :return:
    """
    try:
        startindex = path.index('extends')
        if startindex >= 4:
            return path[startindex + 1] == 'class' and path[startindex + 2] == 'classDeclaration'
    except ValueError:
        return False
    # default
    return False


def __is_implements_usage(path: list[str]) -> bool:
    """
    Both internal classes as normal classes can implement an interface
    In both cases the structure and depth of the tree is the same.
    [['Runnable', 'typeIdentifier', 'classOrInterfaceType', 'typeType', 'typeList', 'implements', 'class', 'classDeclaration', 'typeDeclaration', 'complilationUnit']]
    :param path:
    :return:
    """
    try:
        startindex = path.index('implements')
        return startindex > 0
    except ValueError:
        return False


def __is_instance_variable_usage(path: list[str]) -> bool:
    """
    Instance variables are declared within the classBodyDeclaration
    :param path:
    :return:
    """
    busy = 0
    for element in path:
        if element == 'fieldDeclaration':
            if busy == 0:
                busy = 1
                continue
            else:
                busy = 0
                continue
        if element == 'memberDeclaration':
            if busy == 1:
                busy = 2
                continue
            else:
                busy = 0
                continue
        if element == 'classBodyDeclaration':
            if busy == 2:
                busy = 3
                break
            else:
                busy = 0
                continue

    # default
    return busy == 3


def __is_local_variable_usage(path: list[str]) -> bool:
    """
    Local variables are declared as localVariableDeclaration
    :param path:
    :return:
    """
    busy = 0
    for element in path:
        if element == 'localVariableDeclaration':
            if busy == 0:
                busy = 1
                break
            else:
                busy = 0
                continue

    # default
    return busy == 1


def __is_method_argument_usage(path: list[str]) -> bool:
    """
    The argument of a function is a formalParameter of a methodDeclaration
    of a memberDeclaration within a classBodyDeclaration
    'formalParameter', ..., 'methodDeclaration', 'memberDeclaration', 'classBodyDeclaration'
    :param path:
    :return:
    """
    busy = 0
    for element in path:
        if element in ['formalParameter', 'formalParameters']:
            busy = 1
            continue
        if element in ['constructorDeclaration', 'methodDeclaration']:
            if busy == 1:
                busy = 2
                continue
            else:
                busy = 0
                continue
        if element in ['classDeclaration', 'enumDeclaration', 'memberDeclaration']:
            if busy == 2:
                busy = 3
                continue
            else:
                busy = 0
                continue
        if element == 'classBodyDeclaration':
            if busy == 3:
                busy = 4
                break
            else:
                busy = 0
                continue
    # default
    return busy == 4


def __is_method_argumenttype_usage(path: list[str]) -> bool:
    """
    are defined as typeArgument ( last item before path got trimmed)
    :param path:
    :return:
    """
    try:
        return path.index('typeArgument') == len(path) - 1
    except ValueError:
        return False


def __is_method_result_usage(path: list[str]) -> bool:
    """
    The result of a function is the typeTypeOrVoid of a methodDeclaration
    of a memberDeclaration within a classBodyDeclaration
    'typeTypeOrVoid', 'methodDeclaration', 'memberDeclaration', 'classBodyDeclaration'
    :param path:
    :return:
    """
    busy = 0
    for element in path:
        if element == 'typeTypeOrVoid':
            if busy == 0:
                busy = 1
                continue
            else:
                busy = 0
                continue
        if element == 'methodDeclaration':
            if busy == 1:
                busy = 2
                continue
            else:
                busy = 0
                continue
        if element == 'memberDeclaration':
            if busy == 2:
                busy = 3
                continue
            else:
                busy = 0
                continue
        if element == 'classBodyDeclaration':
            if busy == 3:
                busy = 4
                break
            else:
                busy = 0
                continue

    # default
    return busy == 4


def __is_instantation_usage(path: list[str]) -> bool:
    """
    Instantation happens when a new object is created by an expression
    'creator', 'new', 'expression'
    :param path:
    :return:
    """
    busy = 0
    for element in path:
        if element == 'creator':
            if busy == 0:
                busy = 1
                continue
            else:
                busy = 0
                continue
        if element == 'new':
            if busy == 1:
                busy = 2
                continue
            else:
                busy = 0
                continue
        if element == 'expression':
            if busy == 2:
                busy = 3
                break
            else:
                busy = 0
                continue
    # default
    return busy == 3


def __is_generics_extends_usage(path: list[str]) -> bool:
    """
    When is class is typed as T extends <classname>
    'typeBound', 'extends', 'typeParameter'

    :param path:
    :return:
    """
    busy = 0
    for element in path:
        if element == 'typeBound':
            if busy == 0:
                busy = 1
                continue
            else:
                busy = 0
                continue
        if element == 'extends':
            if busy == 1:
                busy = 2
                continue
            else:
                busy = 0
                continue
        if element == 'typeParameter':
            if busy == 2:
                busy = 3
                break
            else:
                busy = 0
                continue
    # default
    return busy == 3


def __is_static_call(path: list[str]) -> bool:
    """
    Static starts  always with searchword, then followed by  'identifier', 'primary'
    :param path:
    """
    if len(path) < 3:
        return False

    return path[1] == 'identifier' and path[2] == 'primary'


def __is_blockstatement_modifier(path: list[str]) -> bool:
    """
    Reserved keywords only ( synchronized, volatile) starts  always with searchword, then followed by  'statement', 'blockStatement'
    synchronized', 'modifier', 'classBodyDeclaration
    :param path:
    """
    if path[0] not in ('volatile', 'synchronized'):
        return False

    busy = 0
    for element in path:
        if element == 'statement':
            if busy == 0:
                busy = 1
                continue
            else:
                busy = 0
                continue
        if element == 'blockStatement':
            if busy == 1:
                busy = 2
                break
            else:
                busy = 0
                continue
        else:
            busy = 0
            continue
    # default
    return busy == 2


def __is_classbody_modifier(path: list[str]) -> bool:
    """
    Static starts  always with searchword, then followed by  'modifier', 'classBodyDeclaration'
    :param path:
    """
    if len(path) < 3:
        return False

    return path[1] == 'modifier' and path[2] == 'classBodyDeclaration'


def __is_class_declaration(path: list[str]) -> bool:
    """
       starts  always with searchword, then followed by  'identifier', 'class', 'classDeclaration'
      :param path:
      """
    if len(path) < 4:
        return False

    return path[1] == 'identifier' and path[2] == 'class' and path[3] == 'classDeclaration'


def __is_enum_declaration(path: list[str]) -> bool:
    """
       starts  always with searchword, then followed by  'identifier', 'enum', 'enumDeclaration'
      :param path:
      """
    if len(path) < 4:
        return False

    return path[1] == 'identifier' and path[2] == 'enum' and path[3] == 'enumDeclaration'


def __is_type_declaration_usage(path: list[str]) -> bool:
    """
       starts  always with searchword, then followed by  'typeIdentifier', 'classOrInterfaceType', 'typeType'
      :param path:
      """
    if len(path) < 4:
        return False
    is_identifier = path[1] == 'typeIdentifier' or path[1] == 'identifier'
    return is_identifier and path[2] == 'classOrInterfaceType' and path[3] == 'typeType'


def __is_constructor_declaration(path: list[str]) -> bool:
    """
      starts  always with searchword, then followed by  'identifier', 'constructorDeclaration'
      :param path:
      """
    if len(path) < 3:
        return False

    return path[1] == 'identifier' and path[2] == 'constructorDeclaration'


def __is_interface_definition(path: list[str]) -> bool:
    """
      starts  always with searchword, then followed by   'identifier', 'interface', 'interfaceDeclaration'
      :param path:
      """
    if len(path) < 4:
        return False

    return path[1] == 'identifier' and path[2] == 'interface' and path[3] == 'interfaceDeclaration'


def __is_literal(path: list[str]) -> bool:
    """

      :param path:
      """
    literal_identifier = 'literal' in path
    return literal_identifier


def __is_annotation(path: list[str]) -> bool:
    """

      :param path:
      """
    return '@' in path


def __is_lone_identifier(path: list[str]) -> bool:
    """
      Only as last resort
      :param path:
      """
    if len(path) < 2:
        return False
    next_is_identifier = path[1] == 'identifier' or path[1] == 'typeIdentifier'
    return next_is_identifier


def __trim_path(path: list[str]) -> list[str]:
    """
    In nested declarations ( blocks, methods, ...) we don't want to seek in the containing code.
    Therefore, we trim part the path
    When we reach equals sign  ( = ), we have found use within an expression
    When we reach accolade sign ( { ),we reached a block definition
    When we reach angle bracket sign ( < ),we reached a type definition
    :param path:
    :return:
    """
    rv = []
    for element in path:
        if element in ['=', '{', '<']:
            break
        else:
            rv.append(element)
    return rv


def determine_searchword_usage(paths: list[[str]], zoekterm: str) -> list[(str, int)]:
    """
    The searchword will be the first element of each searchlist.
    The lists will be in ordered in usage within the sourcefile.
    :param paths:
    :param zoekterm:
    :return:
    """
    results = []
    for path in paths:
        complete_path = path.copy()
        if __is_literal(path):
            # literals (stringwaardes) worden niet verder verwerkt.
            continue
        path = __trim_path(path)
        if __is_import_usage(path):
            results.append('import')
            continue
        if __is_extends_usage(path):
            results.append('extends')
            continue
        if __is_instance_variable_usage(path):
            results.append('instance_variable')
            continue
        if __is_local_variable_usage(path):
            results.append('local_variable')
            continue
        if __is_method_result_usage(path):
            results.append('method_result')
            continue
        if __is_method_argument_usage(path):
            results.append('method_argument')
            continue
        if __is_method_argumenttype_usage(path):
            results.append('method_typeargument')
            continue
        if __is_instantation_usage(path):
            results.append('instantation')
            continue
        if __is_generics_extends_usage(path):
            results.append('generics_extend')
            continue
        if __is_implements_usage(path):
            results.append('implements')
            continue
        if __is_static_call(path):
            results.append('static_use')
            continue
        if __is_blockstatement_modifier(path):
            results.append('blockstatement')
            continue
        if __is_classbody_modifier(path):
            results.append('classbody_modifier')
            continue
        if __is_class_declaration(path):
            results.append('class_declaration')
            continue
        if __is_enum_declaration(path):
            results.append('enum_declaration')
            continue
        if __is_constructor_declaration(path):
            results.append('constructor_declaration')
            continue
        if __is_type_declaration_usage(path):
            results.append('type_declaration')
            continue
        if __is_interface_definition(path):
            results.append('interface_definition')
            continue
        if __is_annotation(path):
            results.append('annotation')
            continue
        if __is_lone_identifier(path):
            results.append('identifier')
            continue

        else:
            results.append('unknown')
            logging.warning('unknown usage')
            logging.warning(str(complete_path))

    return results
