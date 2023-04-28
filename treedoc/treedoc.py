from treedoc_node import TreedocNode, TreedocNodeContent


class Treedoc:
    """
    CRDT treedoc implementation
    """

    def __init__(self):
        self.left = None
        self.root = None

    def add(self, index, sign, client):
        if self.root is None:
            self.root = TreedocNode(TreedocNodeContent(sign, client.identificator, client.local_counter), None, index)
        else:
            current = self.root
            while current.left is not None or current.right is not None:
                if current.index == index:
                    # в одну ноду несколько символов
                    pass
                elif current.index > index:
                    pass

    def delete(self, index, sign, client):
        pass
