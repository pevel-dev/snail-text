class Treedoc:
    def __init__(self, client_id, tick):
        self.root = None
        self.client_id = client_id
        self.tick = tick

    def insert(self, value, pos_id_left, pos_id_right):
        if not (pos_id_left < pos_id_right):
            raise Exception("pos_id_left must be less than pos_id_right")
        # TODO: проверить что между pos_id_left и pos_id_right нет элементов

        if pos_id_left is None and pos_id_right is None:
            self.root = Node(value, self.tick, self.client_id, False)
        elif pos_id_left is None and pos_id_right is not None:
            pass
        elif pos_id_right is None and pos_id_left is not None:
            pass
        else:
            node = self.get_node(pos_id_left)
            if node.right is not None:
                save = node.right
                node.right = BigNode(save.left, save.right)
                save.left, save.right = None, None
                node.right.add_node(save)
                node.right.add_node(Node(value, self.tick, self.client_id))
            else:
                node.right = Node(value, self.tick, self.client_id)

        self.tick += 1

    def delete(self, pos_id):
        pass

    def insert_at(self, value, index):
        pass

    def delete_at(self, index):
        pass

    def get_sequence(self):
        current = self.root
        while current is not None:
            current = current.left

        # сделаать обход + понимать posid

    def get_node(self, pos_id):
        current = self.root
        for i in pos_id:
            if i == "0":
                current = current.left
            elif i == "1":
                current = current.right
        return current

    @staticmethod
    def parent_or_grandparent(pos_id_u, pos_id_v):
        return pos_id_v[: len(pos_id_u)] == pos_id_u


class Node:
    def __init__(
            self,
            value,
            tick,
            client_id,
            deleted=False,
            left=None,
            right=None,
    ):
        self.value = value
        self.left = left
        self.right = right
        self.tick = tick
        self.client_id = client_id
        self.deleted = deleted


class BigNode:
    def __init__(self, left=None, right=None):
        self.nodes = []
        self.left = left
        self.right = right

    def add_node(self, node):
        self.nodes.append(node)
        self.nodes = sorted(self.nodes, key=lambda x: (x.client_id, x.tick))
