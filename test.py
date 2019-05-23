import UMLParse
import nassi

# This is super buggy still. Trees with lists are kinda icky to work with. Works with trees of size 2, however.
if __name__ == "__main__":
    A = UMLParse.Parse.test("""
    A --> B
    B --> C
    C --> D
    """)

    B = nassi.Process("")
    B.drawdiagram(A)

