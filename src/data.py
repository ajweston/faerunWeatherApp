import configparser

class data:

    months = ['January', 'February', 'March', 'April', 'May', 'June','July','August','September','October','November','December']

    def __init__(self):
        # initialize data
        self.running = True
        self.state = 0
        self.ruler = 0
        self.leftClick = False
        self.rightClick = False
        self.lCtrl = False
        self.mapWidth = 0
        self.mapHeight = 0

        # import configuration
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.screenWidth = int(self.config['Screen']['width'])
        self.screenHeight = int(self.config['Screen']['height'])

        self.movementBase = int(self.config['Movement']['baseSpeed'])
        self.movementMultiplier = int(self.config['Movement']['multiplier'])
        self.movementSlow = float(self.config['Movement']['slow'])
        self.gridSpread = int(self.config['Grid']['spread'])

        self.month = int(self.config['Last Date']['month'])
        self.day = int(self.config['Last Date']['day'])

        self.cloudyMax = int(self.config['Precipitation']['cloudyMax'])
        self.sunnyMax = int(self.config['Precipitation']['sunnyMax'])
        self.lightMax = int(self.config['Precipitation']['lightMax'])
        self.heavyMax = int(self.config['Precipitation']['heavyMax'])

        self.selectX = 0
        self.selectY = 0

    def updateScreenDimensions(self, width, height):
        self.screenWidth = width
        self.screenHeight = height

        self.config['Screen']['width'] = str(width)
        self.config['Screen']['height'] = str(height)
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def shutdown(self):
        self.config['Last Date']['month'] = str(self.month)
        self.config['Last Date']['day'] = str(self.day)
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

