class Data:
    """Singleton class with all global raw and derived market data"""

    instance = None
    class __Data:
        def __init__(self):
            self.ticks = dict()


    def __init__(self):
        if Data.instance is None:
            Data.instance = Data.__Data()
    def __getattr__(self, item):
        return getattr(Data.instance, item)
