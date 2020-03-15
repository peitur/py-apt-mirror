class Quick(object):
    __data = {
        "defaults":{
            "header": '\033[95m',
            "info": '\033[94m',
            "ok": '\033[92m',
            "warning": '\033[93m',
            "fail": '\033[91m',
        },
        "format":{
            "bold": '\033[1m'
        },
        "end": {
            "end": '\033[0m',
            "nc": '\x1b[0m'
        }
    }

    def info():
        return Quick.__data['defaults']['info']

    def warning():
        return Quick.__data['defaults']['warning']

    def fail():
        return Quick.__data['defaults']['fail']

    def ok():
        return Quick.__data['defaults']['ok']

    def header():
        return Quick.__data['defaults']['header']

    def nc():
        return Quick.getNC()

    def getDefaults():
        return Quick.__data['defaults'].keys()

    def getQuickFormats():
        return Quick.__data['format'].keys()

    def getEnings():
        return Quick.__data['end'].keys()

    def getDefault( c ):
        c = c.lower()
        if c.lower() in Quick.__data['defaults']:
            return DefQuickault.__data['defaults'][c]
        raise AttributeError("No such text default %s"%(c))

    def getQuickFormat( c ):
        c = c.lower()
        if c.lower() in __data['format']:
            return Quick.__data['format'][c]
        raise AttributeError("No such text reset %s"%(c))

    def getEnd():
        return Quick.__data['end']["end"]

    def getNC():
        return Quick.__data['end']["nc"]


class Formatting (object):
    __data = {
        "format": {
            "bold": "\x1b[1m",
            "dim": "\x1b[2m",
            "italic": "\x1b[3m",
            "underlined": "\x1b[4m",
            "blink": "\x1b[5m",
            "reverse": "\x1b[7m",
            "hidden": "\x1b[8m",
        },
        "reset": {
            "reset": "\x1b[0m",
            "bold": "\x1b[21m",
            "dim": "\x1b[22m",
            "italic": "\x1b[23m",
            "underlined": "\x1b[24",
            "blink": "\x1b[25m",
            "reverse": "\x1b[27m",
            "hidden": "\x1b[28m",
        }
    }

    def getFormats():
        return Formatting.__data['format'].keys()

    def getResets():
        return Formatting.__data['reset'].keys()

    def getFormat( c ):
        c = c.lower()
        if c.lower() in Formatting.__data['format']:
            return Formatting.__data['format'][c]
        raise AttributeError("No such text format %s"%(c))

    def getReset( c ):
        c = c.lower()
        if c.lower() in Formatting.__data['reset']:
            return Formatting.__data['reset'][c]
        raise AttributeError("No such text reset %s"%(c))


class Colors (object):
    __data = {
        "text": {
            "default": "\x1b[39m",
            "black": "\x1b[30m",
            "red": "\x1b[31m",
            "green": "\x1b[32m",
            "yellow": "\x1b[33m",
            "blue": "\x1b[34m",
            "magenta": "\x1b[35m",
            "cyan": "\x1b[36m",
            "lightgray": "\x1b[37m",
            "darkgray": "\x1b[90m",
            "lightred": "\x1b[91m",
            "lightgreen": "\x1b[92m",
            "lightyellow": "\x1b[93m",
            "lightblue": "\x1b[94m",
            "lightmagenta": "\x1b[95m",
            "lightcyan": "\x1b[96m",
            "white": "\x1b[97m",
        },
        "background":{
            "default": "\x1b[49m",
            "black": "\x1b[40m",
            "red": "\x1b[41m",
            "green": "\x1b[42m",
            "yellow": "\x1b[43m",
            "blue": "\x1b[44m",
            "magenta": "\x1b[45m",
            "cyan": "\x1b[46m",
            "lightgray": "\x1b[47m",
            "darkgray": "\x1b[100m",
            "lightred": "\x1b[101m",
            "lightgreen": "\x1b[102m",
            "lightyellow": "\x1b[103m",
            "lightblue": "\x1b[104m",
            "lightmagenta": "\x1b[105m",
            "lightcyan": "\x1b[106m",
            "white": "\x1b[107m",
        }
    }

    def getTextColors():
        return Colors.__data['text'].keys()

    def getBackgroundColors():
        return Colors.__data['background'].keys()

    def getTextColor( c ):
        c = c.lower()
        if c.lower() in Colors.__data['text']:
            return Colors.__data['text'][c]
        raise AttributeError("No such text color %s"%(c))

    def getBackgroundColor( c ):
        c = c.lower()
        if c.lower() in Colors.__data['background']:
            return Colors.__data['background'][c]
        raise AttributeError("No such text color %s"%(c))


if __name__ == "__main__":
    text = "testingtesting123456789"

    nc = Quick.nc()
    sep = Quick.header()

    print( "%s%s%s" % ( sep,"="*30, nc ) )
    for c in Quick.getDefaults():
        cc = Quick.getDefault(c)
        print("%-16s - %s%s%s" % ( c, cc, text, nc ))


    print( "%s%s%s" % ( sep,"="*30, nc ) )
    for c in Colors.getTextColors():
        cc = Colors.getTextColor(c)
        print("%-16s - %s%s%s" % ( c, cc, text, nc ))

    print( "%s%s%s" % ( sep,"="*30, nc ) )
    for c in Colors.getBackgroundColors():
        cc = Colors.getBackgroundColor(c)
        print("%-16s - %s%s%s" % ( c, cc, text, nc ))

    print( "%s%s%s" % ( sep,"="*30, nc ) )
    for c in Formatting.getFormats():
        cc = Formatting.getFormat(c)
        print("%-16s - %s%s%s" % (c, cc, text, nc ))

    print( "%s%s%s" % ( sep,"="*30, nc ) )
    for c in Formatting.getResets():
        cc = Formatting.getReset(c)
        print("%-16s - %s%s%s" % (c, cc, text, nc ))
