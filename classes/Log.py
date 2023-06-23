
class Log:
    def __init__(self, widget):
        self.widget = widget

    def addLineToLog(self, text, text_color='black', background_color='white'):
        self.widget.print(text, text_color=text_color, background_color=background_color, autoscroll=True)
