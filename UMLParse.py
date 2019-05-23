import itertools
import re


class Parse:

    def __init__(self, name: str):
        """
        This is the constructor for the tree structure of the parsed UML diagram.
        :param name: The name of the node
        """
        self.name = name
        self.left = list()  # type: [Parse]
        self.right = list()  # type: [Parse]

    def addparent(self, node: 'Parse'):
        self.parent = node

    def addleft(self, node : 'Parse'):
        """
        for the purposes of this parser, anything on the left side is falsey
        :param node: The node to be added to the left side.
        :return: None.
        """
        self.left.append(node)

    def getnamelist(self):
        """
        Gets a list of all the named elements of the tree.
        this returns a nested list, but it works good enough for now.
        :return: A list of all the elements names. Will become an iterator at one point once it progresses to that
        point
        """
        namelist = []
        namelist.append(self.name)
        for item in self.right:
            namelist.append(item.name)
            if item.right != []:
                namelist.extend(self.recursivename(item, list()))
        return namelist

    def recursivename(self, node, nlist: ['Parse']):
        """
        Recursive driver for the namelist function
        :param node: The current node to recursively drive
        :param nlist: the list to append the names too
        :return: the list
        """
        if node is not None:
            for item in node.right:
                nlist.append(item.name)
                nlist.append(self.recursivename(item, nlist))
                return nlist

    def printtree(self):
        """
        Debugging function to print the tree.
        :return:
        """
        print(f"Node {self.name} left: {str(self.left)} right: {str(self.right)}")
        for node in self.left:
            print(node.printtree())
        for node in self.right:
            print(node.printtree())

    def __repr__(self):
        return str(self.name)

    def startheight(self):
        """
        Gets the depth of the tree structure
        :return:
        """
        lDepth = 0
        rDepth = 0
        for item in self.left:
            lDepth = self.getheight(item)

        for item in self.right:
            rDepth = self.getheight(item)

        if lDepth > rDepth:
            return lDepth + 1
        else:
            return rDepth + 1

    def getheight(self, node=None):
        """Recursive function that is driven by startheight"""
        lDepth = 0
        rDepth = 0
        if node is None:
            return 0
        else:
            for item in node.left:
                lDepth = self.getheight(item)

            for item in node.right:
                rDepth = self.getheight(item)

            if lDepth > rDepth:
                return lDepth+1
            else:
                return rDepth+1

    def addright(self, node: 'Parse'):
        """
        for the purposes of this parser, anything on the right side is truthy
        the right side is also the default position for nodes that do not correspond to an if condition
        :param node: the node to be added to the right side
        :return: None.
        """
        self.right.append(node)
        self.right[-1].parent = self

    @staticmethod
    def test(teststr : str):
        """
        Debug function, currently used for ensuring it builds the tree correctly.
        :param teststr:
        :return:
        """
        top = None  # type: Parse
        current = None  # type: Parse
        for test in teststr.strip().splitlines():
            test = test.strip()
            print(test)
            group = re.match("([a-zA-Z0-9_]*)? --> ([a-zA-Z0-9_]*)?", test).groups()
            print(group)
            if top is None:
                top = Parse(group[0])
                top.addright(Parse(group[1]))
                current = top
            elif current.name != group[0]:
                # if the current node's name isn't the left side of the equation, we need to find it in the tree
                found = None
                # iterate through the tree, find a node with a corresponding name, set it to the current node.
                for node in current.right:
                    if node.name == group[0]:
                        current = node
                        found = True
                if found is None:
                    current.addright(Parse(group[0]))
                    current = current.right[-1]
                current.addright(Parse(group[1]))
            else:
                current.addright(Parse(group[1]))
        top.printtree()
        return top

    @staticmethod
    def readfile(filename : str):
        """
        :param filename: the filename to read
        :return: an object containing the parsed UML.
        """

        valid, umlStart, umlEnd = Parse.validate(filename)
        if valid:
            with open(filename, "r") as file:
                # this is doable with a comprehension but they're ugly.
                for line in itertools.islice(file, umlStart, umlEnd):
                    """
                    in each line there are 3 potential possibilities we can encounter for the bare bones parsing 
                    that needs to be done. it can look 
                    1)
                    X --> Y for node X connects to node Y, directly
                    2)
                    if "X" then starts a branch, branches follow the following pattern:
                    -->[true]"Top level"
                    -->"Level under top level"
                    else
                    -->[false]"Top level"
                    -->"Under False Top Level"
                    @endif
                    3) if a (*) is present it represents a start of end of a node, documentation is found here:
                    http://plantuml.com/activity-diagram-legacy
                    """

                    # the below string matches the combination of X --> Y
                    re.match(".*? --> .*?", line)

    @staticmethod
    def validate(filename : str) -> (bool, int, int):
        """
        :param filename: The file to be validated
        :return: a tuple containing a boolean of the files validity, the start, and end of the UML block.
        """
        bStart = 0
        bEnd = 0
        with open(filename, "r") as file:
            for nbr, line in enumerate(file):
                if "@startuml" in line:
                    bStart = nbr
                if "@enduml" in line:
                    bEnd = nbr
        return bStart == bEnd, bStart, bEnd

