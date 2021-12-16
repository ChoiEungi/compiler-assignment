from sly import Lexer, Parser


class JSONLexer(Lexer):
    tokens = {'{', '}', '[', ']', ',', ':',"number", "string","true","false","null"}
    literals = {'{', '}', '[', ']', ',', ':'}
    ignore = " \t\n\r"

    @_(r'"((\n)|.)*?"')
    def string(self, t):
        t.value = t.value.strip("\"")
        return t

    @_(r'-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?')
    def number(self, t):
        return t
    
    @_(r'true')
    def true(self, t):
        return t
    
    @_(r'false')
    def false(self, t):
        return t
    
    @_(r'null')
    def null(self, t):
        return t

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1
        raise Exception("Token Error")


class JSONParser(Parser):
    tokens = JSONLexer.tokens
    start = "json"

    @_('object',
       'array')
    def json(self, p):
        return p[0]

    @_('"{" members "}"')
    def object(self, p):
        return {key: value for key, value in p.members}

    @_('pair')
    def members(self, p):
        return [p.pair]

    @_('pair "," members')
    def members(self, p):
        return [p.pair] + p.members

    @_('string ":" value')
    def pair(self, p):
        return p.string, p.value

    @_('"[" elements "]"')
    def array(self, p):
        return p.elements

    @_('value')
    def elements(self, p):
        return [p.value]

    @_('value "," elements')
    def elements(self, p):
        return [p.value] + p.elements

    @_('string','number', 'object', 'array', 'true', 'false', 'null')
    def value(self, p):
        return p[0]

    def error(self, p):
        if p is None:
            raise ValueError("error at end of token!")
        if p.value == "}":
            raise ValueError("empty object")
        if p.value == "]":
            raise ValueError("empty array")

        raise ValueError("Parsing error at token %s" % str(p))



if __name__ == "__main__":
    lexer = JSONLexer()
    parser = JSONParser()



    json_text = \
    """{"menu": {
          "id": "file",
          "value": [1], 
          "popup": {
            "menuitem": [
              {"value": "New", "onclick": "CreateNewDoc()"},
              {"value": "Open", "onclick": "OpenDoc()"},
              {"value": "Close", "onclick": "CloseDoc()"}
            ],
            "delay" : 1.5
          }
        }
    }\
        """

    tokenized_json = lexer.tokenize(json_text)
    for i in tokenized_json:
        print(i)

    result = parser.parse(lexer.tokenize(json_text))

    print(result)
