from nltk import Tree


def find_class_use(node: Tree, classname: str, found: bool) -> bool:
    """

    :param node: A tree or subtree
    :param classname: The name you are looking for
    :param found:
    :return: boolean, True if the searched name is found.
    """
    if found:
        return found

    if isinstance(node, Tree):
        if node.label() == 'typeType':
            leaves_list = node.leaves()
            found = leaves_list.__contains__(classname)

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


def to_nltk_tree(tree_as_string: str) -> Tree:
    """
    Convert an antlr4 tree as string to a nltk tree.
    :param tree_as_string:
    :return: nltk Tree object
    """
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
