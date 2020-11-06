import os
import sys
scriptdir = os.path.join('/Users/leo/PycharmProjects/notepadpp', 'pyflakes')
sys.path.insert(0, scriptdir)
import ast
from pyflakes import checker


class GDChecker(checker.Checker):
    """An AST visitor that finds the definition of a target object."""

    def __init__(self, tree, lineno, name, filename='(none)'):
        """Initialize the checker and search for the target.

        Args:
          tree: an ast.Node representing the root of a tree.
          lineno: int, the line number of the object to be searched for.
          name: string, the identifier of the object.
          filename: optional string representing the module's file name.
        """
        self.name = name
        self.lineno = lineno
        self.target = None
        self.targetScope = None
        super(GDChecker, self).__init__(tree, filename)

    def getScope(self, target):
        """
        Find the target's scope.

        Given an ast.Node representing the target object, travel up the stack of
        scopes to find the node that originally defined the object.
        """
        if target in self.scope:
            return self.scope[target]
        for scope in self.scopeStack[-2::-1]:
            if target in scope:
                return scope[target]
        # Was not found: this is probably an attribute declared in another
        # method, or perhaps an undefined reference.
        print('Sorry, no definition found.')

    def handleChildren(self, tree, omit=None):
        """
        Check if the `attr` of the current node matches target before iterating
        through child nodes.
        """
        if (hasattr(tree, 'lineno') and tree.lineno == self.lineno
              and hasattr(tree, 'attr') and tree.attr == self.name):
            self.target = tree
            scope = self.getScope(tree.attr)
            self.targetScope = scope

        for node in checker.iter_child_nodes(tree):
            self.handleNode(node, tree)

    def NAME(self, node):
        """
        Visitor function for `Name` nodes: check if it matches target before
        handling node.
        """
        super(GDChecker, self).NAME(node)
        if node.lineno == self.lineno and node.id == self.name:
            self.target = node
            self.targetScope = self.getScope(node.id)


# pyflakes Checker sets a lot of names explicitly to point at its handleChildren
# method. We need to re-point them to our overridden version.
for x in dir(checker.Checker):
    obj = getattr(checker.Checker, x)
    if obj == checker.Checker.handleChildren:
        setattr(GDChecker, x, GDChecker.handleChildren)


def goto_definition(word, row, col, contents=None):
    """
    Main function called by vim.

    Parses the buffer into an AST, then uses the Checker to find the definition
    of the identifier under the cursor, and moves the cursor to the position of
    that definition.
    """

    # filename = 'preference.py'
    # with open(filename, 'r') as f:
    #     contents = f.read()
    # contents = 'Vbox = QVBoxLayout()\nVbox.addWidget(self.buttonsWidget)'

    tree = ast.parse(contents)

    # row, col begins from 0

    parser = GDChecker(tree, row, word)
    scope = parser.targetScope

    try:
        if scope:
            source = parser.targetScope.source
            # If it's a function arg set, find the relevant one.
            if isinstance(scope, checker.Argument):
                for arg in scope.source.args.args:
                    if arg.id == word:
                        source = arg
            return (source.lineno, source.col_offset)
        else:
            return (None, None)
    except:
        return (None, None)


if __name__ == '__main__':
    goto_definition()