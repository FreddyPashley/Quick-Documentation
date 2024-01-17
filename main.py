import flask

"""
    # Subtitle
    text
    # Subtitle 2
    1. op1
    2. op2
    3. op3
"""

class Documentation:
    def __init__(self, title:str="My Documentation", authors:dict={}, openOnStart:bool=False, downloadHTML:bool=False, thread:bool=True, order:str="alphabetical") -> None:
        self.thread = thread
        self.title = title
        self.functions = []
        self.authors = authors
        self.openonstart = openOnStart
        self.downloadAutomatically = downloadHTML
        self.order = "c" if order == "chronological" else "a"

    def addFunction(self, function, credit:str=None):
        function.author_credit = credit
        self.functions.append(function)
    
    def start(self, host:str="127.0.0.1", port:int=5000):
        if self.order == "a": self.functions.sort(key=lambda x: x.__name__)
        def generateHTML():
            head = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>[TITLE]</title></head><body>'
            html = head.replace("[TITLE]", self.title)
            css = """
            <style>
            body {font-family:sans-serif;background-color:#2b2b2b;padding:5px;color:#fff;}
            a {color:#fff;}
            </style>
            """
            html += "\n".join([i.strip() for i in css.split("\n")])

            html += f"<h1><center>{self.title}</center></h1>"

            if self.authors != {}:
                authorStr = "<br>".join([f'<a href="{"#" if self.authors[k] is None else self.authors[k]}">{k}</a>' for k in self.authors.keys()])
                html += "<p><b>Authors:</b></p><p>"+authorStr+"</p>"

            if self.functions != []:
                html += "<h1>Contents</h1>\n<ul>"
                for function in self.functions:
                    html += f'<li><a href="#{function.__name__}">{function.__name__}</a>'
                html += "</ul><br>"

            for function in self.functions:
                authorCredit = f"<p>By <a href=\"{self.authors[function.author_credit]}\">{function.author_credit}</a></p>" if function.author_credit is not None and function.author_credit in self.authors else ''
                string = f'<hr><h2 id="{function.__name__}">{function.__name__}</h2>{authorCredit}'
                if "return" in function.__annotations__:
                    string += f"<h3>Return type: {function.__annotations__['return'].__name__}</h3>"
                if function.__code__.co_argcount > 0:
                    string += f"<h3>Parameters ({function.__code__.co_argcount}):</h3><ul>"
                    for varName in function.__code__.co_varnames:
                        varType = f" ({function.__annotations__[varName].__name__})" if varName in function.__annotations__.keys() else ""
                        string += f"<li>{varName}{varType}</li>"
                    string += "</ul>"
                
                html += "\n".join([i.strip() for i in string.split("\n")])

            html += "\n</body></html>"

            html = html.replace("<hr>", "<hr>\n")
            return html


        HTML = generateHTML()

        if self.downloadAutomatically:
            with open(self.title+".html", "w") as f:
                f.write(HTML)

        app = flask.Flask("docs")
        @app.route("/")
        def index(): return HTML
        if self.openonstart:
            import webbrowser
            webbrowser.open(f"http://{host}:{port}")
        if self.thread:
            from threading import Thread
            self.thread = Thread(target=app.run, kwargs={"host":host, "port":port}, daemon=False)
            self.thread.start()
        else:
            app.run(host, port)



if __name__ == "__main__": pass