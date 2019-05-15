#!/usr/bin/python3
# Implementation of generating Pretty ANSI Text for Console
# Brady O'Leary (2019). https://github.com/mboleary

# https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
# https://stackoverflow.com/questions/2616906/how-do-i-output-coloured-text-to-a-linux-terminal

ESCAPE = "\033["
SEP = ";"
END = "m"
RESET = ESCAPE + "0" + END

class Text:
    # Color RGB Arrays [R, G, B]

    reset = False #0
    bold = False #1
    faint = False #2
    underline = False #3
    color_fg = 0 #30-37, 38, 39, 90-97
    color_fg_rgb = False # For option 38 (array) and 39 (integer), or False if unused
    color_bg = 0 #40-47, 48, 49, 100-107
    color_bg_rgb = False # for option 48 (array) and 49 (integer), or False if unused

    # Pre-defined Color Values (Foreground, Background)
    NONE = -1
    BLACK = (30, 40)
    RED = (31, 41)
    GREEN = (32, 42)
    YELLOW = (33, 43)
    BLUE = (34, 44)
    MAGENTA = (35, 45)
    CYAN = (36, 46)
    WHITE = (37, 47)
    BRIGHT_BLACK = (90, 100)
    BRIGHT_RED = (91, 101)
    BRIGHT_GREEN = (92, 102)
    BRIGHT_YELLOW = (93, 103)
    BRIGHT_BLUE = (94, 104)
    BRIGHT_MAGENTA = (95, 105)
    BRIGHT_CYAN = (96, 106)
    BRIGHT_WHITE = (97, 107)

    def __init__(self, reset=False, bold=False, faint=False, underline=False):
        if reset:
            reset = True
        if bold:
            self.bold = True
        if faint:
            self.faint = True
        if underline:
            self.underline = True
    
    # Set Value of Bold
    # @param val (boolean) - If True, then text is bold
    def setBold(self, val):
        if val:
            self.bold = True
        elif not val:
            self.bold = False

    # Set Value of Faint
    # @param val (boolean) - If True, then text is faint
    def setFaint(self, val):
        if val:
            self.faint = True
        elif not val:
            self.faint = False

    # Set Value of Underline
    # @param val (boolean) - If True, then text is underlined
    def setUnderline(self, val):
        if val:
            self.underline = True
        elif not val:
            self.underline = False

    # Reset all Effects
    # @param val (boolean) - If True, then text Effects are Reset
    def setReset(self, val):
        if val:
            self.reset = True
        elif not val:
            self.reset = False

    # Set the Foreground Color of the Text
    # @param color (int or (int, int) from pre-defined color values) - Color to change the text to
    def setFGColor(self, color):
        # Check for Color Definition
        val = -1
        if color == -1:
            self.color_fg_rgb = False
            self.color_fg = -1
            return
        if isinstance(color, tuple):
            val = color[0]
        else:
            val = color
        if (val > 30 and val < 37) or (val > 90 and val < 97):
            self.color_fg_rgb = False
            self.color_fg = val
        else:
            raise ValueError("Color must be between 30 and 37")

    # Set RGB Value for Foregound Color
    # @param r (int) - Red Value
    # @param g (int) - Green Value
    # @param b (int) - Blue Value
    def setFGColorRGB(self, r=0, g=0, b=0):
        if r >= 0 and g >= 0 and b >= 0:
            self.color_fg = 38 # Use Custom Color
            self.color_fg_rgb = [r, g, b]
        else:
            raise ValueError("RGB Values must be Greater or Equal to 0")

    # Set Foreground Color to 256-color mode Color
    # @param n (int) - Color to set text
    def setFGColorN(self, n=0):
        if n >= 0 and n <= 255:
            self.color_fg = 38 # USe Custom Color
            self.color_fg_rgb = n
        else:
            raise ValueError("Color Value must be between 0 and 255")

    # Set the Foreground Color of the Text
    # @param color (int or (int, int) from pre-defined color values) - Color to change the text to
    def setBGColor(self, color):
        # Check for Color Definition
        if color == -1:
            self.color_bg_rgb = False
            self.color_bg = -1
            return
        val = -1
        if isinstance(color, tuple):
            val = color[1]
        else:
            val = color
        if (val > 40 and val < 47) or (val > 100 and val < 107):
            self.color_bg_rgb = False
            self.color_bg = val
        else:
            raise ValueError("Color must be between 40 and 47")

    # Set RGB Value for Background Color
    # @param r (int) - Red Value
    # @param g (int) - Green Value
    # @param b (int) - Blue Value

    def setBGColorRGB(self, r=0, g=0, b=0):
        if r >= 0 and g >= 0 and b >= 0:
            self.color_fg = 48 # Use Custom Color
            self.color_fg_rgb = [r, g, b]
        else:
            raise ValueError("RGB Values must be Greater or Equal to 0")

    # Set Background Color to 256-color mode Color
    # @param n (int) - Color to set text
    def setBGColorN(self, n=0):
        if n >= 0 and n <= 255:
            self.color_bg = 48 # USe Custom Color
            self.color_bg_rgb = n
        else:
            raise ValueError("Color Value must be between 0 and 255")

    # Get ANSI Text with Effects
    def getANSIText(self):
        s = ""
        if self.reset:
            s += "0"
        if self.bold:
            if len(s) > 0:
                s += ";"
            s += "1"
        if self.faint:
            if len(s) > 0:
                s += ";"
            s += "2"
        if self.underline:
            if len(s) > 0:
                s += ";"
            s += "3"
        if self.color_fg > 0:
            if len(s) > 0:
                s += ";"
            if self.color_fg == 38 and self.color_fg_rgb != False and type(self.color_fg_rgb) is list:
                s += "38;2;" + str(self.color_fg_rgb[0]) + ";" + str(self.color_fg_rgb[1]) + ";" + str(self.color_fg_rgb[2])
            elif self.color_fg == 38 and self.color_fg_rgb != False and type(self.color_fg_rgb) is int:
                s += "33;5" + str(self.color_fg_rgb)
            else:
                s += str(self.color_fg)
        if self.color_bg > 0:
            if len(s) > 0:
                s += ";"
            if self.color_bg == 38 and self.color_bg_rgb != False and type(self.color_bg_rgb) is list:
                s += "38;2;" + str(self.color_bg_rgb[0]) + ";" + str(self.color_bg_rgb[1]) + ";" + str(self.color_bg_rgb[2])
            elif self.color_bg == 38 and self.color_bg_rgb != False and type(self.color_bg_rgb) is int:
                s += "33;5" + str(self.color_bg_rgb)
            else:
                s += str(self.color_bg)
        s = ESCAPE + s + END
        return s

    # Get Colored Text
    def getColoredText(self, text):
        start = self.getANSIText()
        return start + text + RESET

# Tests the Module if module is run as a program
def test():
    ansi = Text(bold=True)
    ansi.setFGColor(ansi.RED)
    print(ansi.getColoredText("Hello World"))
    ansi.setBGColor(ansi.MAGENTA)
    print(ansi.getColoredText("Hello World"))
    ansi.setBGColor(ansi.NONE)
    ansi.setFGColorN(130)
    print(ansi.getColoredText("Hello World"))
    ansi.setFGColorRGB(r=20, g=50, b=130)
    print(ansi.getColoredText("Hello World"))
    print("I should be normal ;)")

if __name__ == "__main__":
    test()