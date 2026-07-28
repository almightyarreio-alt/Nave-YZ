from tree_sitter import Language, Parser
from tree_sitter_javascript import language
import json

JS = Language(language())

parser = Parser()
parser.language = JS


class Extractor:

    def __init__(self, code):

        self.code = code
        self.lines = code.splitlines()

        self.tree = parser.parse(
            bytes(code, "utf8")
        )

        self.data = {
            "functions": [],
            "variables": [],
            "classes": []
        }

    def text(self, node):
        return self.code[
            node.start_byte:node.end_byte
        ]

    def visit(self, node):

        # -----------------------
        # Function Declaration
        # -----------------------

        if node.type == "function_declaration":

            name = node.child_by_field_name("name")

            self.data["functions"].append({

                "name": self.text(name),

                "line": node.start_point[0] + 1

            })

        # -----------------------
        # Class
        # -----------------------

        elif node.type == "class_declaration":

            name = node.child_by_field_name("name")

            self.data["classes"].append({

                "name": self.text(name),

                "line": node.start_point[0] + 1

            })

        # -----------------------
        # Variáveis
        # -----------------------

        elif node.type == "variable_declarator":

            name = node.child_by_field_name("name")

            self.data["variables"].append({

                "name": self.text(name),

                "line": node.start_point[0] + 1

            })

        for child in node.children:
            self.visit(child)


codigo = open(
    "script.js",
    encoding="utf8"
).read()

ex = Extractor(codigo)

ex.visit(ex.tree.root_node)

with open(
    "estrutura.json",
    "w",
    encoding="utf8"
) as f:

    json.dump(
        ex.data,
        f,
        indent=4,
        ensure_ascii=False
    )

print("OK")