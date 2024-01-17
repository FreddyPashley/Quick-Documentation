import flask

# (DEFAULT VARIABLES?)
# INDENT TEXT FOR FUNCTION CONTENT

class Documentation:
    def __init__(
            self,
            title:str="My Documentation",
            authors:dict={},
            openOnStart:bool=True,
            downloadHTML:bool=False,
            thread:bool=True,
            order:str="alphabetical",
            keepAlive:bool=False,
            introduction:str=None,
            bg:str="cfcfcf",
            fg:str="000",
            icon:str=None
            ) -> None:
        self.thread = thread
        self.title = title
        self.functions = []
        self.classes = []
        self.authors = authors
        self.openonstart = openOnStart
        self.downloadAutomatically = downloadHTML
        self.order = "c" if order == "chronological" else "a"
        self.keepAlive = keepAlive
        self.introduction = introduction
        self.bg = bg
        self.fg = fg
        self.icon = icon

    def addFunction(
            self,
            function,
            credit:str=None
            ) -> None:
        function.author_credit = credit
        self.functions.append(function)
    
    def addClass(
            self,
            object,
            credit:str=None
            ) -> None:
        object.author_credit = credit
        self.classes.append(object)
    
    def start(
            self,
            host:str="127.0.0.1",
            port:int=5000,
            delay:int=0
            ) -> str:
        if self.order == "a":
            self.functions.sort(key=lambda x: x.__name__)
            self.classes.sort(key=lambda x: x.__name__)

        def generateHTML():
            head = '<!DOCTYPE html><html lang="en">\n<head>\n[ICONPATH]<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>[TITLE]</title>\n</head>\n<body>\n'
            html = head.replace("[TITLE]", self.title)
            if self.icon:
                html = html.replace("[ICONPATH]", f'<link rel="icon" href="{self.icon}">\n')
            else:
                html = html.replace("[ICONPATH]", "")
            css = """
            <style>
            body {font-family:sans-serif;background-color:#"""+self.bg+""";padding:5px;color:#"""+self.fg+""";}
            a {color:#"""+self.fg+""";}
            </style>\n
            """
            html += "\n".join([i.strip() for i in css.split("\n")])
            html += f"<h1><center>{self.title}</center></h1>"

            if self.authors != {}:
                aStrs = []
                for k in self.authors.keys():
                    aStrs.append(f'<a href="{"#" if self.authors[k] is None else self.authors[k]}">{k}</a>')
                authorStr = "<br>\n".join(aStrs)
                html += "<p><b>Authors:</b></p>\n<p>"+authorStr+"</p>"

            html += "\n<h1>Contents</h1>\n<ul>\n"
            if self.introduction:
                html += f'<li><a href="#docs-intro">Introduction</a></li>\n'
            if self.classes != []:
                html += f"</ul>\n<p>Classes</p>\n<ul>\n"
                for class_ in self.classes:
                    html += f'<li><a href="#{class_.__name__}">{class_.__name__}</a></li>\n'
            if self.functions != []:
                html += f"</ul>\n<p>Functions</p>\n<ul>\n"
                for function in self.functions:
                    html += f'<li><a href="#{function.__name__}">{function.__name__}</a></li>\n'
            if self.functions != [] or self.classes != []:
                html += "</ul><br>\n"

            if self.introduction:
                html += f'<hr><h2 id="docs-intro">Introduction</h2>\n'
                for line in self.introduction.split("\n"):
                    if line != "":
                        html += f"<p>{line}</p>\n"

            for class_ in self.classes:
                if class_.author_credit is not None and class_.author_credit in self.authors:
                    authorCredit = f'<p>By <a href="{self.authors[class_.author_credit]}">{class_.author_credit}</a></p>'
                else:
                    authorCredit = ""
                html += f'<hr><h2 id="{class_.__name__}"><i>class</i> {class_.__name__}</h2>\n{authorCredit}'
                classFunctions = [i for i in class_.__dict__ if "__" not in i and i != "author_credit"]
                if "__init__" in class_.__dict__:
                    classFunctions.insert(0, "__init__")
                for fname in classFunctions:
                    string = ""
                    function = class_.__dict__[fname]
                    string += f'<h3 style="margin-left: 20px;" id="{function.__name__}"><i>function</i> {function.__name__}</h3>\n'
                    if "return" in function.__annotations__ and function.__annotations__["return"] is not None:
                        string += f'<h4 style="margin-left: 20px;">Return type: {function.__annotations__["return"].__name__}</h4>\n'
                    if function.__code__.co_argcount > 0:
                        string += f'<h4 style="margin-left: 20px;">Parameters ({function.__code__.co_argcount}):</h4>\n<ul>\n'
                        for varName in function.__code__.co_varnames:
                            varType = f" ({function.__annotations__[varName].__name__})" if varName in function.__annotations__.keys() else ""
                            string += f"<li>{varName}{varType}</li>\n"
                        string += "</ul>\n"
                    if function.__doc__:
                        docStr = [i.strip() for i in str(function.__doc__).split("\n")]
                        while "" in docStr: docStr.remove("")
                        for i, line in enumerate(docStr):
                            if line.startswith("# "):
                                docStr[i] = ["title", line.strip("##").strip()]
                            elif line.startswith("## "):
                                docStr[i] = ["subtitle", line.strip("#").strip()]
                            elif line.startswith(".. "):
                                line = line.strip(".. ")
                                docStr[i] = ["num", line]
                            elif line.startswith(". "):
                                line = line.strip(". ")
                                docStr[i] = ["bullet", line]
                            else:
                                docStr[i] = ["text", line]
                        ul, ol = False, False
                        for line in docStr:
                            lineType, line = line
                            if ol == True and not lineType == "num":
                                string += "</ol>\n"
                                ol = False
                            if ul == True and not lineType == "bullet":
                                string += "</ul>\n"
                                ul = False
                            if lineType == "title":
                                string += f'<h4 style="margin-left: 20px;">{line}</h4>\n'
                            elif lineType == "subtitle":
                                string += f'<h5 style="margin-left: 20px;">{line}</h5>\n'
                            elif lineType == "text":
                                string += f'<p style="margin-left: 20px;">{line}</p>\n'
                            elif lineType == "num":
                                if ol == False:
                                    string += '<ol style="margin-left: 20px;">\n'
                                ol = True
                                string += f"<li>{line.strip()}</li>\n"
                            elif lineType == "bullet":
                                if ul == False:
                                    string += '<ul style="margin-left: 20px;">\n'
                                ul = True
                                string += f"<li>{line.strip()}</li>\n"
                        if ol == True:
                            string += "</ol>\n"
                            ol = False
                        if ul == True:
                            string += "</ul>\n"
                            ul = False
                    
                    html += "\n".join([i.strip() for i in string.split("\n")])

            for function in self.functions:
                if function.author_credit is not None and function.author_credit in self.authors:
                    authorCredit = f'<p>By <a href="{self.authors[function.author_credit]}">{function.author_credit}</a></p>'
                else:
                    authorCredit = ""
                string = f'<hr><h2 id="{function.__name__}"><i>function</i> {function.__name__}</h2>\n{authorCredit}'
                if "return" in function.__annotations__:
                    string += f"<h3>Return type: {function.__annotations__['return'].__name__}</h3>\n"
                if function.__code__.co_argcount > 0:
                    string += f"<h3>Parameters ({function.__code__.co_argcount}):</h3>\n<ul>\n"
                    for varName in function.__code__.co_varnames:
                        varType = f" ({function.__annotations__[varName].__name__})" if varName in function.__annotations__.keys() else ""
                        string += f"<li>{varName}{varType}</li>\n"
                    string += "</ul>\n"
                if function.__doc__:
                    docStr = [i.strip() for i in str(function.__doc__).split("\n")]
                    while "" in docStr: docStr.remove("")
                    for i, line in enumerate(docStr):
                        if line.startswith("# "):
                            docStr[i] = ["title", line.strip("##").strip()]
                        elif line.startswith("## "):
                            docStr[i] = ["subtitle", line.strip("#").strip()]
                        elif line.startswith(".. "):
                            line = line.strip(".. ")
                            docStr[i] = ["num", line]
                        elif line.startswith(". "):
                            line = line.strip(". ")
                            docStr[i] = ["bullet", line]
                        else:
                            docStr[i] = ["text", line]
                    ul, ol = False, False
                    for line in docStr:
                        lineType, line = line
                        if ol == True and not lineType == "num":
                            string += "</ol>\n"
                            ol = False
                        if ul == True and not lineType == "bullet":
                            string += "</ul>\n"
                            ul = False
                        if lineType == "title":
                            string += f"<h3>{line}</h3>\n"
                        elif lineType == "subtitle":
                            string += f"<h4>{line}</h4>\n"
                        elif lineType == "text":
                            string += f"<p>{line}</p>\n"
                        elif lineType == "num":
                            if ol == False:
                                string += "<ol>\n"
                            ol = True
                            string += f"<li>{line.strip()}</li>\n"
                        elif lineType == "bullet":
                            if ul == False:
                                string += "<ul>\n"
                            ul = True
                            string += f"<li>{line.strip()}</li>\n"
                    if ol == True:
                        string += "</ol>\n"
                        ol = False
                    if ul == True:
                        string += "</ul>\n"
                        ul = False
                
                html += "\n".join([i.strip() for i in string.split("\n")])

            html += "\n</body></html>"

            html = html.replace("<hr>", "<hr>\n")
            return html


        HTML = generateHTML()

        if self.downloadAutomatically or not self.keepAlive:
            with open(self.title+".html", "w") as f:
                f.write(HTML)
        
        if self.keepAlive:
            app = flask.Flask("docs")
            @app.route("/")
            def index():
                return HTML
            
            if delay:
                from time import sleep
                sleep(delay)

            if self.openonstart:
                import webbrowser
                webbrowser.open(f"http://{host}:{port}")
                del webbrowser

            if self.thread:
                from threading import Thread
                self.thread = Thread(target=app.run, kwargs={"host":host, "port":port}, daemon=False)
                self.thread.start()
            else:
                app.run(host, port)

        elif self.openonstart:
            import os
            import webbrowser
            pathToFile = os.getcwd()+f"/{self.title}.html"
            webbrowser.open(f"file:///{pathToFile}")
            del os
            del webbrowser



if __name__ == "__main__": pass