"""help.py: Implement the Idle help menu.
Contents are subject to revision at any time, without notice.


Help => About IDLE: display About Idle dialog


Help => IDLE Help: Display help.html with proper formatting.

HelpParser - Parse help.html and render to tk Text.

HelpText - Display formatted help.html.

HelpFrame - Contain text, scrollbar, and table-of-contents.

HelpWindow - Display HelpFrame in a standalone window.

show_idlehelp - Create HelpWindow. Called in EditorWindow.help_dialog.
"""

from html.parser import HTMLParser
from idlelib.config import idleConf
from os.path import abspath, dirname, isfile, join
from platform import python_version
from tkinter import Menu, Text, Toplevel
from tkinter import font as tkfont
from tkinter.ttk import Frame, Menubutton, Scrollbar, Style

## About IDLE ##


## IDLE Help ##


class HelpParser(HTMLParser):
    """Render help.html into a text widget.

    Parses a modern HTML page with sections, headings, paragraphs,
    and lists. Renders content into a tkinter Text widget.
    """

    def __init__(self, text):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.text = text
        self.tags = ""
        self.show = False
        self.level = 0
        self.toc = []
        self.header = ""
        self.in_section = False
        self.skip_content = False
        self.in_header = None
        self.in_p = False
        self.in_li = False
        self.list_type = None
        self.list_counter = 0

    def handle_starttag(self, tag, attrs):
        "Handle start tags in help.html."
        attrs_dict = dict(attrs)
        class_ = attrs_dict.get("class", "")

        if tag == "section":
            self.in_section = True
            self.show = True
        elif tag == "nav":
            self.skip_content = True
        elif tag in ("h1", "h2", "h3"):
            self.in_header = tag
            self.tags = tag
            self.header = ""
            if self.show:
                self.text.insert("end", "\n\n")
        elif tag == "p" and self.show and not self.skip_content:
            self.in_p = True
            self.tags = "p"
        elif tag == "ul" and self.show:
            self.list_type = "ul"
            self.list_counter = 0
            self.level += 1
            self.tags = f"l{self.level}"
        elif tag == "ol" and self.show:
            self.list_type = "ol"
            self.list_counter = 0
            self.level += 1
            self.tags = f"l{self.level}"
        elif tag == "li" and self.show:
            self.in_li = True
            if self.list_type == "ol":
                self.list_counter += 1
                prefix = f"\n{self.list_counter}. "
            else:
                prefix = "\n• "
            self.text.insert("end", prefix, (self.tags,))
        elif tag == "pre" and self.show:
            self.tags = "preblock"
            self.text.insert("end", "\n\n")
        elif tag == "code" and self.show:
            self.tags = "pre"
        elif tag == "strong" or tag == "b":
            self.tags = self.tags + " strong" if self.tags else "strong"
        elif tag == "em" or tag == "i":
            self.tags = self.tags + " em" if self.tags else "em"
        elif tag == "a":
            pass
        elif tag == "span":
            if class_ == "material-icons":
                self.skip_content = True

    def handle_endtag(self, tag):
        "Handle end tags in help.html."
        if tag == "section":
            self.in_section = False
            self.show = False
        elif tag == "nav":
            self.skip_content = False
        elif tag in ("h1", "h2", "h3"):
            if self.show and self.header:
                indent = "    " if tag == "h3" else "" if tag == "h1" else "  "
                self.toc.append((indent + self.header, self.text.index("insert")))
            self.in_header = None
            self.tags = ""
        elif tag == "p":
            self.in_p = False
            self.tags = ""
        elif tag == "li":
            self.in_li = False
        elif tag in ("ul", "ol"):
            self.level = max(0, self.level - 1)
            self.tags = f"l{self.level}" if self.level > 0 else ""
            self.list_type = None
        elif tag == "pre":
            self.tags = ""
        elif tag == "code":
            self.tags = ""
        elif tag in ("strong", "b", "em", "i"):
            self.tags = ""
        elif tag == "span":
            self.skip_content = False

    def handle_data(self, data):
        "Handle text data in help.html."
        if not self.show or self.skip_content:
            return

        if self.in_header:
            self.header += data.strip()
            d = data.strip()
            if d:
                self.text.insert("end", d, (self.tags,))
        elif self.in_li:
            d = data.strip()
            if d:
                self.text.insert("end", d, (self.tags,))
        elif self.in_p:
            d = data.replace("\n", " ").strip()
            if d:
                self.text.insert("end", d + " ", (self.tags,))
        else:
            d = data.replace("\n", " ").strip()
            if d:
                self.text.insert("end", d, (self.tags,))


class HelpText(Text):
    "Display help.html."

    def __init__(self, parent, filename):
        "Configure tags and feed file to parser."
        uwide = idleConf.GetOption("main", "EditorWindow", "width", type="int")
        uhigh = idleConf.GetOption("main", "EditorWindow", "height", type="int")
        uhigh = 3 * uhigh // 4  # Lines average 4/3 of editor line height.
        Text.__init__(
            self,
            parent,
            wrap="word",
            highlightthickness=0,
            padx=5,
            borderwidth=0,
            width=uwide,
            height=uhigh,
        )

        normalfont = self.findfont(["TkDefaultFont", "arial", "helvetica"])
        fixedfont = self.findfont(["TkFixedFont", "monaco", "courier"])
        self["font"] = (normalfont, 12)
        self.tag_configure("em", font=(normalfont, 12, "italic"))
        self.tag_configure("strong", font=(normalfont, 12, "bold"))
        self.tag_configure("h1", font=(normalfont, 20, "bold"))
        self.tag_configure("h2", font=(normalfont, 18, "bold"))
        self.tag_configure("h3", font=(normalfont, 15, "bold"))
        self.tag_configure("p", lmargin1=10, lmargin2=10)
        self.tag_configure("pre", font=(fixedfont, 12), background="#f6f6ff")
        self.tag_configure(
            "preblock",
            font=(fixedfont, 10),
            lmargin1=25,
            borderwidth=1,
            relief="solid",
            background="#eeffcc",
        )
        self.tag_configure("l1", lmargin1=25, lmargin2=25)
        self.tag_configure("l2", lmargin1=50, lmargin2=50)
        self.tag_configure("l3", lmargin1=75, lmargin2=75)
        self.tag_configure("l4", lmargin1=100, lmargin2=100)

        self.parser = HelpParser(self)
        with open(filename, encoding="utf-8") as f:
            contents = f.read()
        self.parser.feed(contents)
        self["state"] = "disabled"

    def findfont(self, names):
        "Return name of first font family derived from names."
        for name in names:
            if name.lower() in (x.lower() for x in tkfont.names(root=self)):
                font = tkfont.Font(name=name, exists=True, root=self)
                return font.actual()["family"]
            elif name.lower() in (x.lower() for x in tkfont.families(root=self)):
                return name


class HelpFrame(Frame):
    "Display html text, scrollbar, and toc."

    def __init__(self, parent, filename):
        Frame.__init__(self, parent)
        self.text = text = HelpText(self, filename)
        self.style = Style(parent)
        self["style"] = "helpframe.TFrame"
        self.style.configure("helpframe.TFrame", background=text["background"])
        self.toc = toc = self.toc_menu(text)
        self.scroll = scroll = Scrollbar(self, command=text.yview)
        text["yscrollcommand"] = scroll.set

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)  # Only expand the text widget.
        toc.grid(row=0, column=0, sticky="nw")
        text.grid(row=0, column=1, sticky="nsew")
        scroll.grid(row=0, column=2, sticky="ns")

    def toc_menu(self, text):
        "Create table of contents as drop-down menu."
        toc = Menubutton(self, text="TOC")
        drop = Menu(toc, tearoff=False)
        for lbl, dex in text.parser.toc:
            drop.add_command(label=lbl, command=lambda dex=dex: text.yview(dex))
        toc["menu"] = drop
        return toc


class HelpWindow(Toplevel):
    "Display frame with rendered html."

    def __init__(self, parent, filename, title):
        Toplevel.__init__(self, parent)
        self.wm_title(title)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        HelpFrame(self, filename).grid(column=0, row=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)


def show_idlehelp(parent):
    "Create HelpWindow; called from Idle Help event handler."
    filename = join(abspath(dirname(__file__)), "help.html")
    if not isfile(filename):
        return
    HelpWindow(parent, filename, "JereIDE Help (%s)" % python_version())


if __name__ == "__main__":
    from unittest import main

    main("idlelib.idle_test.test_help", verbosity=2, exit=False)

    from idlelib.idle_test.htest import run

    run(show_idlehelp)
