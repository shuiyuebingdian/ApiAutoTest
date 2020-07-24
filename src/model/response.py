
class Response:

    def __init__(self):
        self.status = 0
        self.errorMsg = ""
        self.data = None
        self.error = False


class Chart:

    def __init__(self):
        self.xaxis = []
        self.series = []


class Area:

    def __init__(self):
        self.cities = []
        self.provinces = []
        self.regions = []
        self.tiers = []
