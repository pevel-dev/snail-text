class TreedocNode:
    def __init__(self, content, parent, index):
        self.right = None
        self.left = None
        self.content = [content]
        self.parent = parent
        self.index = index
        self.deleted = False


class TreedocNodeContent:
    def __init__(self, char, client_identificator, client_local_counter):
        self.client_identificator = client_identificator
        self.char = char
        self.client_local_counter = client_local_counter
