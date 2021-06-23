class request_data:
    __instance__ = None

    def __init__(self):
        if request_data.__instance__ is None:
            request_data.__instance__ = self
        else:
            raise Exception("Instance Active.Method Get Instance")

    @staticmethod
    def getInstance():
        if not request_data.__instance__:
            request_data()
        return request_data.__instance__

    def set_request_data(self, url, target_country, searched_country, start_page, end_page):
        self._url = url
        self._target_country = target_country
        self._searched_country = searched_country
        self._start_page = start_page
        self._end_page = end_page

    @property
    def url(self):
        return self._url

    @property
    def target_country(self):
        return self._target_country

    @property
    def searched_country(self):
        return self._searched_country

    @property
    def start_page(self):
        return self._start_page

    @property
    def end_page(self):
        return self._end_page
