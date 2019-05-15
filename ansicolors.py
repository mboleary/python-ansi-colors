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
    italic = False #3 (Not Widely Supported)
    underline = False #4
    slowBlink = False #5
    rapidBlink = False #6 (not widely supported)
    reverseVideo = False #7
    conceal = False #8 (Not Widely Supported)
    crossedOut = False #9
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

    def __init__(self, reset=False, bold=False, faint=False, italic=False, underline=False, slowBlink=False, rapidBlink=False, reverseVideo=False, conceal=False, crossedOut=False):
        if reset:
            reset = True
        if bold:
            self.bold = True
        if faint:
            self.faint = True
        if italic:
            self.italic = True
        if underline:
            self.underline = True
        if slowBlink:
            self.slowBlink = True
        if rapidBlink:
            self.rapidBlink = True
        if reverseVideo:
            self.reverseVideo = True
        if conceal:
            self.conceal = True
        if crossedOut:
            self.crossedOut = True
    
    # Resets all Paramters in Object
    def resetAll(self):
        self.reset = False #0
        self.bold = False #1
        self.faint = False #2
        self.italic = False #3 (Not Widely Supported)
        self.underline = False #4
        self.slowBlink = False #5
        self.rapidBlink = False #6 (not widely supported)
        self.reverseVideo = False #7
        self.conceal = False #8 (Not Widely Supported)
        self.crossedOut = False #9
        self.color_bg = 0
        self.color_fg = 0
        self.color_bg_rgb = False
        self.color_fg_rgb = False

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
    # @param val (boolean) - If True, then add Reset Effect
    def setReset(self, val):
        if val:
            self.reset = True
        elif not val:
            self.reset = False

    # Italicize all text
    # @param val (boolean) - If True, then text is italicized
    def setItalic(self, val):
        if val:
            self.italic = True
        elif not val:
            self.italic = False

    # Make text Blink Slowly
    # @param val (boolean) - If True, then text will blink
    def setSlowBlink(self, val):
        if val:
            self.slowBlink = True
        elif not val:
            self.slowBlink = False

    # Make Text Blink Rapidly
    # @param val (boolean) - If True, then text will blink rapidly
    def setRapidBlink(self, val):
        if val:
            self.rapidBlink = True
        elif not val:
            self.rapidBlink = False

    # Reverses Background and Foreground Colors
    # @param val (boolean) - If True, then text Colors are Reversed
    def setReverseVideo(self, val):
        if val:
            self.reverseVideo = True
        elif not val:
            self.reverseVideo = False

    # Conceal the Text
    # @param val (boolean) - If True, then text is Concealed
    def setConceal(self, val):
        if val:
            self.conceal = True
        elif not val:
            self.conceal = False

    # Cross Out Text
    # @param val (boolean) - If True, then text Effects are Reset
    def setCrossedOut(self, val):
        if val:
            self.crossedOut = True
        elif not val:
            self.crossedOut = False

    # Set the Foreground Color of the Text
    # @param color (int or (int, int) from pre-defined color values) - Color to change the text to
    def setFGColor(self, color):
        # Check for Color Definition
        val = -1
        if color == -1:
            self.color_fg_rgb = False
            self.color_fg = 0
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
            self.color_bg = 0
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
        if self.italic:
            if len(s) > 0:
                s += ";"
            s += "3"
        if self.underline:
            if len(s) > 0:
                s += ";"
            s += "4"
        if self.slowBlink:
            if len(s) > 0:
                s += ";"
            s += "5"
        if self.rapidBlink:
            if len(s) > 0:
                s += ";"
            s += "6"
        if self.reverseVideo:
            if len(s) > 0:
                s += ";"
            s += "7"
        if self.conceal:
            if len(s) > 0:
                s += ";"
            s += "8"
        if self.crossedOut:
            if len(s) > 0:
                s += ";"
            s += "9"
        if self.color_fg > 0:
            if len(s) > 0:
                s += ";"
            if self.color_fg == 38 and self.color_fg_rgb != False and type(self.color_fg_rgb) is list:
                s += "38;2;" + str(self.color_fg_rgb[0]) + ";" + str(self.color_fg_rgb[1]) + ";" + str(self.color_fg_rgb[2])
            elif self.color_fg == 38 and self.color_fg_rgb != False and type(self.color_fg_rgb) is int:
                s += "38;5;" + str(self.color_fg_rgb)
            else:
                s += str(self.color_fg)
        if self.color_bg > 0:
            if len(s) > 0:
                s += ";"
            if self.color_bg == 48 and self.color_bg_rgb != False and type(self.color_bg_rgb) is list:
                s += "48;2;" + str(self.color_bg_rgb[0]) + ";" + str(self.color_bg_rgb[1]) + ";" + str(self.color_bg_rgb[2])
            elif self.color_bg == 48 and self.color_bg_rgb != False and type(self.color_bg_rgb) is int:
                s += "48;5;" + str(self.color_bg_rgb)
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

    ansi = Text()
    print(ansi.getColoredText("Normal Text"))
    ansi.setBold(True)
    print(ansi.getColoredText("Bold"))
    ansi.setBold(False)
    ansi.setFaint(True)
    print(ansi.getColoredText("Faint"))
    ansi.setFaint(False)
    ansi.setItalic(True)
    print(ansi.getColoredText("Italic"))
    ansi.setItalic(False)
    ansi.setUnderline(True)
    print(ansi.getColoredText("Underline"))
    ansi.setUnderline(False)
    ansi.setSlowBlink(True)
    print(ansi.getColoredText("Slow Blink"))
    ansi.setSlowBlink(False)
    ansi.setRapidBlink(True)
    print(ansi.getColoredText("Rapid Blink"))
    ansi.setRapidBlink(False)
    ansi.setReverseVideo(True)
    print(ansi.getColoredText("Reverse Video"))
    ansi.setReverseVideo(False)
    ansi.setConceal(True)
    print(ansi.getColoredText("Concealed"))
    ansi.setConceal(False)
    ansi.setCrossedOut(True)
    print(ansi.getColoredText("Crossed-Out"))
    ansi.setCrossedOut(False)

    ansi.setBold(True)
    ansi.setFGColor(ansi.BRIGHT_MAGENTA)
    ansi.resetAll()
    print(ansi.getColoredText("This should be normal Text"))
    
    print("Testing N Colors...")
    s = ""
    for i in range(0,255):
        ansi.setFGColorN(i)
        ansi.setBGColorN(255 - i)
        s += ansi.getColoredText(str(i)) + " "
    print(s)
    ansi.resetAll()

    print("Testing All Possible RGB Colors (This takes awhile)...")
    s = ""
    for i in range(0,255):
        for j in range(0,255):
            for k in range(0,255):
                ansi.setFGColorRGB(r=i, g=j, b=k)
                ansi.setFGColorRGB(r=255-i, g=255-j, b=255-k)
                s += ansi.getColoredText("[" + str(i) + "," + str(j) + "," + str(k) + "]") + " "
    print(s)

    print("Testing Finished.")

if __name__ == "__main__":
    test()