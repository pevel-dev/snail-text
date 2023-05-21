from crdt.heap import HeapCRDT


class File:
    def __init__(self, file_id):
        self.file_id = file_id
        # with open(f"files/{file_id}", "w+") as file:
        #     self.file = file.readlines()
        self.crdt = HeapCRDT(-1, "")

    def load_to_disk(self):
        pass
