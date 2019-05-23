from PIL import Image, ImageColor, ImageDraw, ImageFont
import UMLParse

class Process:
    def __init__(self, action: str):
        self.action = action

    def drawdiagram(self, tree: UMLParse.Parse):
        """
        draws the diagram for the nassi diagram. Branching is currently NOT supported. It's not too difficult to add,
        I just want to reduce complexity before I go about spreading out rectangles across the screen
        :param tree: The diagram to be passed in
        :return: Nothing.
        """
        ImageSize = (800, 800)
        ImageHandler = Image.new('RGB', ImageSize, color="white")
        Drawing = ImageDraw.Draw(ImageHandler)

        # First, we want a rectangle around the edge of our image.
        Drawing.rectangle([(0, 0), ImageSize], fill=None, outline="black", width=5)

        # Now, we need to see how many blocks we're going to draw. Essentially, the height of our tree.
        # then split the rectangle into that many components
        rows = tree.startheight()
        recHeight = ImageSize[0] / rows

        textList = tree.getnamelist()
        print(textList)
        for rect in range(rows):
            # draw each rectangle for the block
            Drawing.rectangle([(0, recHeight*rect), (ImageSize[0], (recHeight*rect)+recHeight)],
                              fill="white", outline="black", width=3)

            # now we need to write text. fix branching to come this week.
            cTextY = recHeight*rect + (recHeight / 2)
            cTextX = ImageSize[0] / 2

            print("Drawing Text")
            Drawing.text((cTextX, cTextY), textList[rect], fill=(0,0,0))



        ImageHandler.show()

class BranchingBlock:
    ...


class TestingLoop:
    ...


class Concurrent:
    ...