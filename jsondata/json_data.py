class Logger(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(Logger, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance

    @staticmethod
    def psa():
        print("data")

print(Logger)

log = Logger()
log2 = Logger()

print(log is log2)

print(log)

print(log2)