import logging

from nltk import Tree


def find_class_use(node: Tree, classname: str, found: bool) -> bool:
    """

    :param node: A tree or subtree
    :param classname: The name you are looking for
    :param found:
    :return: boolean, True if the searched name is found as a Type definition.
    """
    if found:
        return found

    if isinstance(node, Tree):
        if node.label() == 'typeType':
            leaves_list = node.leaves()
            found = classname in leaves_list

        if not found:
            for child in node:
                found = found or find_class_use(child, classname, found)
        return found
    else:
        return False


def find_import(node: Tree, packagenaam: str, classname: str, found: bool) -> bool:
    """

    :param packagenaam:
    :param node: A tree or subtree
    :param classname: The name you are looking for
    :param found:
    :return: boolean, True if the searched name is found.
    """
    if found:
        return found

    if isinstance(node, Tree):
        if node.label() == 'importDeclaration':
            leaves_list = node.leaves()
            import_statement = ''.join(leaves_list)
            expected_name = 'import' + packagenaam + '.' + classname + ';'
            expected_wildcard = 'import' + packagenaam + '.*;'
            found = import_statement == expected_name or import_statement == expected_wildcard
            if not found:
                # als classname een punt bevat dan kan de import zowel compleet, als via het gedeelte voor de punt
                # import java.util.Collections; werkt voor Collections.synchronizedList
                # import java.util.Collections.synchronizedList;  werkt ook voor Collections.synchronizedList;
                if classname.find('.') > -1:
                    first_part = classname.split('.')[0]
                    expected_shortname = 'import' + packagenaam + '.' + first_part + ';'
                    found = import_statement == expected_shortname

        if node.label() == 'packageDeclaration':
            leaves_list = node.leaves()
            package_statement = ''.join(leaves_list)
            expected = 'package' + packagenaam + ';'
            found = expected == package_statement

        if not found:
            for child in node:
                found = found or find_import(child, packagenaam, classname, found)
        return found
    else:
        return False


def find_alternative_import(node: Tree, packagenaam: str, classname: str, found: bool) -> bool:
    """
    Function used to exclude an alternative namespace
    Necessary to check for use of alternatives of keywords in java.lang package.
    :param packagenaam:
    :param node: A tree or subtree
    :param classname: The name you are looking for
    :param found:
    :return: boolean, True if the searched name is found.
    """
    if found:
        return found

    if isinstance(node, Tree):
        if node.label() == 'importDeclaration':
            leaves_list = node.leaves()
            import_statement = ''.join(leaves_list)
            correct_import = 'import' + packagenaam + '.' + classname + ';'
            alternative_import = '.' + classname + ';'
            found = import_statement.endswith(alternative_import) and not import_statement == correct_import

        if found:
            for child in node:
                found = found or find_import(child, packagenaam, classname, found)
        return found
    else:
        return False


def find_import_library(node: Tree, packagenaam: str, found: bool) -> bool:
    """
    For category 'libraries'. Check that something from this library is imported.
    Classname is irrelevant.
    :param node:
    :param packagenaam:
    :param found:
    :return:
    """
    if found:
        return found

    if isinstance(node, Tree):
        if node.label() == 'importDeclaration':
            leaves_list = node.leaves()
            import_statement = ''.join(leaves_list)
            expected_name = 'import' + packagenaam + '.'
            expected_static_name =  'import' + 'static' +  packagenaam + '.'
            found = import_statement.startswith(expected_name) or import_statement.startswith(expected_static_name)

        if node.label() == 'packageDeclaration':
            leaves_list = node.leaves()
            package_statement = ''.join(leaves_list)
            expected = 'package' + packagenaam + ';'
            found = expected == package_statement

        if not found:
            for child in node:
                found = found or find_import_library(child, packagenaam, found)
        return found
    else:
        return False


def to_nltk_tree(tree_as_string: str) -> Tree:
    """
    Convert an antlr4 tree as string to a nltk tree.
    For some reason the parser does not always ends with a matching pair of
    :param tree_as_string:
    :return: nltk Tree object
    """
    aantal_openen = tree_as_string.count('(')
    aantal_sluiten = tree_as_string.count(')')
    verschil = aantal_openen - aantal_sluiten
    if aantal_openen > aantal_sluiten:
        padding = ')' * verschil
        tree_as_string = tree_as_string + padding
        logging.info('to_nltk_tree : padding with ' + padding)
    if aantal_openen < aantal_sluiten:
        tree_as_string = tree_as_string[:verschil]
        logging.info('to_nltk_tree : removing with ' + str(verschil))
    return Tree.fromstring(tree_as_string, '()')


def leaves_with_path(tree: Tree, path: list) -> list:
    """
    Return the leaves of the tree.

        >>> t = Tree.fromstring("(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))")
        >>> t.leaves()
        ['the', 'dog', 'chased', 'the', 'cat']

    :return: a list containing this tree's leaves.
        The order reflects the order of the
        leaves in the tree's hierarchical structure.
    :rtype: list
    """
    leaves = []

    for child in tree:
        if isinstance(child, Tree):
            copied_path = path.copy()
            copied_path.append(child.label())
            leaves.extend(leaves_with_path(child, copied_path))
        else:
            path.append(child)
            leaves.append(path)
    return leaves
