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

    @target_country.setter
    def target_country(self, target_country):
        self._target_country = target_country

    @searched_country.setter
    def searched_country(self, searched_country):
        self._searched_country = searched_country

    @start_page.setter
    def start_page(self, start_page):
        self._start_page = start_page

    @end_page.setter
    def end_page(self, end_page):
        self._end_page = end_page

    @url.setter
    def url(self, url):
        self._url = url

