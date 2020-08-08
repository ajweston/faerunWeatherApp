from weather import weather
import random
import pygame
import math


class weatherGrid:
    def dist(self, x1, x2, y1, y2):
        d = math.sqrt(((x2 - x1) * (x2 - x1)) + ((y2 - y1) * (y2 - y1)))
        return d
        
    def angle(self, x1,x2,y1,y2):
        deltaX = x2 - x1
        deltaY = y2 - y1
        angle = math.atan2(deltaY,deltaX)
        if angle < 0:
            angle = angle + 360
        if angle > 360: 
            angle = angle - 360
        return angle

    
    def __init__(self, m_data):
        self.yMax = int(m_data.mapHeight / m_data.gridSpread) + 1
        self.xMax = int(m_data.mapWidth / m_data.gridSpread) + 1
        #determin max/min base temp
        day = (30*(m_data.month-1))+m_data.day
        
        maxPwr = -((pow((day-m_data.maxMean),2))/(2*pow(m_data.maxStdDev,2)))
        maxMul = (m_data.maxCurve * 500)*(1/(m_data.maxStdDev*math.sqrt(2*math.pi)))
        self.maxTemp = maxMul*pow(math.e,maxPwr)+m_data.maxOffset
        
        minPwr = -((pow((day-m_data.minMean),2))/(2*pow(m_data.minStdDev,2)))
        minMul = (m_data.minCurve * 500)*(1/(m_data.minStdDev*math.sqrt(2*math.pi)))
        self.minTemp = minMul*pow(math.e,minPwr)+m_data.minOffset
        
        self.weather = []
        fileError = False
        try:
            weatherFile = open('./weatherData.csv', 'r')  
            if weatherFile.closed:
                fileError = True
        except:
            fileError = True
        for x in range(0, self.xMax):
            column = []
            for y in range(0, self.yMax):
                column.insert(y, weather())
            self.weather.insert(x, column)
            
        if fileError:    
            print('Error while opening saved weather data, reinitializing weather system.')
            # reinitialize 2D weather grid
            for x in range(0, self.xMax):
                for y in range(0, self.yMax):
                    self.weather[x][y].windDirection = random.randint(0, 7)
                    self.weather[x][y].windSpeed = random.randint(0, 100)
                    self.weather[x][y].precipitation = random.randint(0, 100)
                    self.weather[x][y].pressure = random.randint(0,100)
                    self.weather[x][y].temperature = random.randint(0, 100)
                    self.weather[x][y].terrainType = random.randint(0, 5)

        else:
            line = weatherFile.readline()
            if line == "":
                for x in range(0, self.xMax):
                    for y in range(0, self.yMax):
                        self.weather[x][y].windDirection = random.randint(0, 7)
                        self.weather[x][y].windSpeed = random.randint(0, 100)
                        self.weather[x][y].precipitation = random.randint(0, 100)
                        self.weather[x][y].pressure = random.randint(0,100)
                        self.weather[x][y].temperature = random.randint(0, 100)
                        self.weather[x][y].terrainType = random.randint(0, 5)
            else:
                fields = line.split(':')
                xCheck = fields[1]
                line = weatherFile.readline()
                fields = line.split(':')
                yCheck = fields[1]
                
                if int(xCheck) != self.xMax or int(yCheck) != self.yMax:
                    print(f'Saved weather data does not match the current grid size. Found {int(xCheck)}x{int(yCheck)}, expected {self.xMax}x{self.yMax}')
                    # reinitialize 2D weather grid
                    
                    for x in range(0, self.xMax):
                        column = []
                        for y in range(0, self.yMax):
                            column.insert(y, weather())
                        self.weather.insert(x, column)
                    for x in range(0, self.xMax):
                        for y in range(0, self.yMax):
                            self.weather[x][y].precipitation = random.randint(0, 100)
                            self.weather[x][y].pressure = random.randint(0,100)
                            self.weather[x][y].temperature = random.randint(0, 100)
                else:
                    line = weatherFile.readline()
                    while(1):
                        line = weatherFile.readline()
                        fields = line.split(',')
                        if len(fields) < 7:
                            break
                        self.weather[int(fields[0])][int(fields[1])].windDirection = int(fields[2])
                        self.weather[int(fields[0])][int(fields[1])].windSpeed = int(fields[3])
                        self.weather[int(fields[0])][int(fields[1])].temperature = int(fields[4])
                        self.weather[int(fields[0])][int(fields[1])].precipitation = int(fields[5])
                        self.weather[int(fields[0])][int(fields[1])].pressure = int(fields[6])
                        self.weather[int(fields[0])][int(fields[1])].terrainType = int(fields[7])
            
        self.gridActive = False
        self.pressureActive = False
    
    def tempUpdate(self,x,y,data,terrainType):
        
        temp = pow((y/331),data.interpolationPower)*self.maxTemp + (1-pow((y/331),data.interpolationPower))*self.minTemp
        
        return int(temp + random.randint(-data.noiseMax, data.noiseMax))

    def advance(self, m_data):
        #update most values
        
        #determin max/min base temp
        day = (30*(m_data.month-1))+m_data.day
        
        maxPwr = -((pow((day-m_data.maxMean),2))/(2*pow(m_data.maxStdDev,2)))
        maxMul = (m_data.maxCurve * 500)*(1/(m_data.maxStdDev*math.sqrt(2*math.pi)))
        self.maxTemp = maxMul*pow(math.e,maxPwr)+m_data.maxOffset
        
        minPwr = -((pow((day-m_data.minMean),2))/(2*pow(m_data.minStdDev,2)))
        minMul = (m_data.minCurve * 500)*(1/(m_data.minStdDev*math.sqrt(2*math.pi)))
        self.minTemp = minMul*pow(math.e,minPwr)+m_data.minOffset
        
        for x in range(0, self.xMax):
            for y in range(0, self.yMax):
                self.weather[x][y].temperature = self.tempUpdate(x,y,m_data,self.weather[x][y].terrainType)+random.randint(-m_data.noiseMax, m_data.noiseMax)
                self.weather[x][y].pressure = random.randint(0, 100)
                if self.weather[x][y].pressure > 100:
                    self.weather[x][y].pressure = 0
                self.weather[x][y].windSpeed = int(m_data.curveWidth * pow(float(self.weather[x][y].pressure - m_data.xOffset),2.0) + m_data.yOffset + random.randint(-m_data.windNoise, m_data.windNoise))
        
        #update windDirection, point away from warmest surrounding tile
        for x in range(1, self.xMax-1):
            for y in range(1,self.yMax-1):
                highest = -1  
                direction = -1
                if self.weather[x-1][y-1].pressure > highest:
                    highest = self.weather[x-1][y-1].pressure
                    direction = 3
                if self.weather[x][y-1].pressure > highest:
                    highest = self.weather[x][y-1].pressure
                    direction = 4
                if self.weather[x+1][y-1].pressure > highest:
                    highest = self.weather[x+1][y-1].pressure
                    direction = 5
                if self.weather[x+1][y].pressure > highest:
                    highest = self.weather[x+1][y].pressure
                    direction = 6
                if self.weather[x+1][y+1].pressure > highest:
                    highest = self.weather[x+1][y+1].pressure
                    direction = 7
                if self.weather[x][y+1].pressure > highest:
                    highest = self.weather[x][y+1].pressure
                    direction = 0
                if self.weather[x-1][y+1].pressure > highest:
                    highest = self.weather[x-1][y+1].pressure
                    direction = 1
                if self.weather[x-1][y].pressure > highest:
                    highest = self.weather[x-1][y].pressure
                    direction = 2
                self.weather[x][y].windDirection = direction
        for x in range(0,self.yMax):
            self.weather[x][0].windDirection = self.weather[x][1].windDirection
            self.weather[x][self.yMax-1].windDirection = self.weather[x][self.yMax-2].windDirection
        for y in range(1,self.yMax-1):
            self.weather[0][y].windDirection = self.weather[1][y].windDirection
            self.weather[self.xMax-1][y].windDirection = self.weather[self.xMax-2][y].windDirection


    def draw(self, screen, m_data, m_camera):
        # draw pressure
        if self.pressureActive:
            # get boundaries
            minX = m_camera.posX / (m_data.gridSpread * m_camera.zoom) - 1
            if minX < 0:
                minX = 0
            maxX = (m_camera.posX + m_data.screenWidth) / (m_data.gridSpread* m_camera.zoom) + 1
            if maxX > self.xMax:
                maxX = self.xMax
            minY = m_camera.posY / (m_data.gridSpread* m_camera.zoom) - 1
            if minY < 0:
                minY = 0
            maxY = (m_camera.posY + m_data.screenHeight) / (m_data.gridSpread* m_camera.zoom) + 1
            if maxY > self.yMax:
                maxY = self.yMax
            minX = int(minX)
            maxX = int(maxX)
            minY = int(minY)
            maxY = int(maxY)

            # configure surface
            s = pygame.Surface((m_data.gridSpread *m_camera.zoom, m_data.gridSpread *m_camera.zoom))  # the size of your rect
            s.set_alpha(200)  # alpha level
            s.fill((0, 255, 0))  # this fills the entire surface

            # draw the pressure markers
            for x in range(minX, maxX):
                for y in range(minY, maxY):
                    red = self.weather[x][y].pressure*2.55
                    s.fill((int(red),0,int(255-red)))
                    screen.blit(s, (int((x * m_data.gridSpread * m_camera.zoom) - m_camera.posX),
                                    int((y * m_data.gridSpread* m_camera.zoom) - m_camera.posY)))  # (0,0) are the top-left coordinates
        # draw grid
        if self.gridActive:
            for x in range(0, m_data.mapWidth, int(m_data.gridSpread)):
                pygame.draw.line(screen, (0, 0, 0), (int(x*m_camera.zoom - m_camera.posX), int(0 - m_camera.posY)),
                                 (int(x*m_camera.zoom - m_camera.posX), int(m_data.mapHeight*m_camera.zoom - m_camera.posY)), 1)
            for y in range(0, m_data.mapHeight, int(m_data.gridSpread)):
                pygame.draw.line(screen, (0, 0, 0), (int(0 - m_camera.posX), int(y*m_camera.zoom - m_camera.posY)),
                                 (int(m_data.mapWidth*m_camera.zoom - m_camera.posX), int(y*m_camera.zoom - m_camera.posY)), 1)

            baseX = m_data.selectX * m_data.gridSpread * m_camera.zoom - m_camera.posX
            baseY = m_data.selectY * m_data.gridSpread * m_camera.zoom - m_camera.posY
            thickness = 2
            pygame.draw.line(screen, (255, 255, 255), (baseX, baseY),
                             (baseX + m_data.gridSpread* m_camera.zoom, baseY), thickness)
            pygame.draw.line(screen, (255, 255, 255), (baseX, baseY + m_data.gridSpread* m_camera.zoom),
                             (baseX + m_data.gridSpread* m_camera.zoom, baseY + m_data.gridSpread* m_camera.zoom), thickness)
            pygame.draw.line(screen, (255, 255, 255), (baseX, baseY),
                             (baseX, baseY + m_data.gridSpread* m_camera.zoom), thickness)
            pygame.draw.line(screen, (255, 255, 255), (baseX + m_data.gridSpread* m_camera.zoom, baseY),
                             (baseX + m_data.gridSpread* m_camera.zoom, baseY + m_data.gridSpread* m_camera.zoom), thickness)
                             
         
    def shutdown(self):
        weatherFile = open('./weatherData.csv', 'w')
 
        if weatherFile.closed:
            print('Error while saving weather data.')
            return
        weatherFile.write(f'Xmax:{self.xMax}\n')
        weatherFile.write(f'Ymax:{self.yMax}\n')
        weatherFile.write('CellX,CellY,windDirection,windSpeed,temperature,precipitation,pressure,terrainType\n')
        for x in range(0, self.xMax):
            for y in range(0, self.yMax):
                weatherFile.write(f'{x},{y},{self.weather[x][y].windDirection},{self.weather[x][y].windSpeed},{self.weather[x][y].temperature},{self.weather[x][y].precipitation},{self.weather[x][y].pressure},{self.weather[x][y].terrainType}\n')
        weatherFile.close()
        
