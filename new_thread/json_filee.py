import json


class json_file:
    __instance__ = None

    def __init__(self):
        self.json = {'source': [], 'target': []}
        super().__init__()
        if json_file.__instance__ is None:
            json_file.__instance__ = self
        else:
            raise Exception("Instance Active.Method Get Instance")

    @staticmethod
    def getInstance():
        if not json_file.__instance__:
            json_file()
        return json_file.__instance__

    def set_new_json(self):
        self.json.clear()
        self.json.update({
            'source': [],
            'target': []
        })

    def add_source(self, key, value):
        self.json['source'].append({
            f'{key}': f'{value}'
        })

    def add_target(self, key, value):
        self.json['target'].append({
            f'{key}': f'{value}'
        })

    def show_json_file(self):
        print(json.dumps(self.json))

    def delete_one_data(self, asin):
        for data in range(len(self.json.get('source'))):
            if self.json.get('source')[data].get(asin):
                del self.json.get('source')[data]
                break
