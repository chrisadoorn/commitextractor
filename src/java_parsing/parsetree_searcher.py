from nltk import Tree


def find_class_use(node: Tree, classname: str, found: bool):
    try:
        node.label()
    except AttributeError:
        return False
    else:
        label = node.label()
        if node.label() == 'typeType':
            leaves_list = node.leaves()
            found = leaves_list.__contains__(classname)

        # if False :
        #
        #     if node.label() == 'typeType' and node.label() == classname:
        #         return True
        if not found:
            for child in node:
                found = found or find_class_use(child, classname, found)
        return found


def to_nltk_tree(tree_as_string: str) -> Tree:
    return Tree.fromstring(tree_as_string, '()')

