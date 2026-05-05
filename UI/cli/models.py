class Property:
    def __init__(self, name:str):
        self.name = name
        self.input:str = ''
        self.value:float = 0.0

class PropertiesList:
    def __init__(self, name:str,options:list[Property]):
        self.name = name
        self.props = options