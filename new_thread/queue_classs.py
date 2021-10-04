import queue


class data_queue(queue.Queue):
    __instance__ = None

    def __init__(self):
        self.list = []
        super().__init__()
        if data_queue.__instance__ is None:
            data_queue.__instance__ = self
        else:
            raise Exception("Instance Active.Method Get Instance")

    @staticmethod
    def getInstance():
        if not data_queue.__instance__:
            data_queue()
        return data_queue.__instance__

    def get_data(self):
        return self.get()

    def check_queue(self, data):
        if data not in self.queue:
            self.put(data)
            self.list.append(data)
        print(len(self.queue))

    def add_data_to_list(self, data):
        if data not in self.list:
            self.put(data)
            self.list.append(data)

    def delete_from_list(self,asin):
        self.list.remove(asin)

    def clear_list(self):
        self.list.clear()
