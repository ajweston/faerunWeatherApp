class weather:
    windDirections = ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest']
    precipitations = ['Sunny', 'Cloudy', 'Light Rain', 'Heavy Rain', 'Sleet', 'Light Snow', 'Heavy Snow',
                      'Thunder Storm', 'Severe']

    def __init__(self):
        self.windDirection = 0
        self.windSpeed = 0
        self.temperature = 0
        self.precipitation = 0
        self.terrainType = 0
