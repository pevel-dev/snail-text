class Treedoc:
    def __init__(self):
        self.root = None

    def insert(self, value, pos_id_left, pos_id_right, local_tick, client_id):
        if pos_id_left is None and pos_id_right is None:
            self.root = Node(value, )
        elif pos_id_left is None and pos_id_right is not None:
            pass
        elif pos_id_right is None and pos_id_left is not None:
            pass
        else:
            pass

    def delete(self, pos_id):
        pass

    def insert_at(self, value, index, local_tick, client_id):
        pass

    def delete_at(self, index):
        pass

    def get_sequence(self):
        pass


class Node:
    def __init__(self, value, mini=False, left=None, right=None, tick, client_id):
        self.value = value
        self.left = left
        self.right = right
        self.mini = mini
        self.tick = tick
        self.client_id = client_id
