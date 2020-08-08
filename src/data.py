import configparser
import pygame

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
        self.zoomKey = False

        # import configuration
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        
        #temperature parameters
        self.noiseMax = int(self.config['Temperature']['noiseMax'])
        self.minMean = float(self.config['Temperature']['minMean'])
        self.minStdDev = float(self.config['Temperature']['minStdDev'])
        self.minCurve = float(self.config['Temperature']['minCurve'])
        self.minOffset = float(self.config['Temperature']['minOffset'])
        self.maxMean = float(self.config['Temperature']['maxMean'])
        self.maxStdDev = float(self.config['Temperature']['maxStdDev'])
        self.maxCurve = float(self.config['Temperature']['maxCurve'])
        self.maxOffset = float(self.config['Temperature']['maxOffset'])
        self.interpolationPower = float(self.config['Temperature']['interpolationPower'])

        #other parameters
        self.screenWidth = int(self.config['Screen']['width'])
        self.screenHeight = int(self.config['Screen']['height'])
        
        self.leftbutton = int(self.config['Mouse']['leftbutton'])
        self.rightbutton = int(self.config['Mouse']['rightbutton'])

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
        
        self.curveWidth = float(self.config['Wind Speed']['curveWidth'])
        self.xOffset = int(self.config['Wind Speed']['xOffset'])
        self.yOffset = int(self.config['Wind Speed']['yOffset'])
        self.windNoise = int(self.config['Wind Speed']['windNoiseMax'])

        self.selectX = 0
        self.selectY = 0
        # load map image
        gameMap = pygame.image.load('res/faerunMap.jpg')
        self.mapWidth, self.mapHeight = gameMap.get_size()
        self.mapSurface = pygame.Surface((self.mapWidth, self.mapHeight))  # the size of your rect
        self.mapSurface.blit(gameMap,(0,0))
        self.mapSurfaceDraw = self.mapSurface

    def scaleMap(self,zoom):
        self.mapSurfaceDraw = pygame.transform.scale(self.mapSurface, (int(self.mapWidth*zoom),int(self.mapHeight*zoom)))

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

