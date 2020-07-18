from weather import weather
import random
import pygame


class weatherGrid:
    def __init__(self, m_data):
        self.yMax = int(m_data.mapHeight / m_data.gridSpread) + 1
        self.xMax = int(m_data.mapWidth / m_data.gridSpread) + 1

        # initialize 2D weather grid
        self.weather = []
        for x in range(0, self.xMax):
            column = []
            for y in range(0, self.yMax):
                column.insert(y, weather())
            self.weather.insert(x, column)
        for x in range(0, self.xMax):
            for y in range(0, self.yMax):
                self.weather[x][y].precipitation = random.randint(0, 100)
                self.weather[x][y].temperature = random.randint(0, 100)

        self.gridActive = False
        self.precipitationActive = False

    def advance(self):
        for x in range(0, self.xMax):
            for y in range(0, self.yMax):
                self.weather[x][y].precipitation += 5
                if self.weather[x][y].precipitation > 100:
                    self.weather[x][y].precipitation = 0

    def draw(self, screen, m_data, m_camera):
        # draw precipitation
        if self.precipitationActive:
            # get boundaries
            minX = m_camera.posX / m_data.gridSpread - 1
            if minX < 0:
                minX = 0
            maxX = (m_camera.posX + m_data.screenWidth) / m_data.gridSpread + 1
            if maxX > self.xMax:
                maxX = self.xMax
            minY = m_camera.posY / m_data.gridSpread - 1
            if minY < 0:
                minY = 0
            maxY = (m_camera.posY + m_data.screenHeight) / m_data.gridSpread + 1
            if maxY > self.yMax:
                maxY = self.yMax
            minX = int(minX)
            maxX = int(maxX)
            minY = int(minY)
            maxY = int(maxY)

            # configure surface
            s = pygame.Surface((m_data.gridSpread, m_data.gridSpread))  # the size of your rect
            s.set_alpha(200)  # alpha level
            s.fill((0, 255, 0))  # this fills the entire surface

            # draw the precipitation markers
            for x in range(minX, maxX):
                for y in range(minY, maxY):
                    # check precipitation type
                    if self.weather[x][y].precipitation < m_data.sunnyMax:
                        continue
                    elif self.weather[x][y].precipitation < m_data.cloudyMax:
                        s.fill((100, 100, 100))
                    elif self.weather[x][y].precipitation < m_data.lightMax and self.weather[x][y].temperature > 34:
                        s.fill((0, 200, 0))
                    elif self.weather[x][y].precipitation < m_data.lightMax and self.weather[x][
                        y].temperature <= 34:
                        s.fill((238, 177, 218))
                    elif self.weather[x][y].precipitation < m_data.heavyMax and self.weather[x][y].temperature > 34:
                        s.fill((0, 100, 0))
                    elif self.weather[x][y].precipitation < m_data.heavyMax and self.weather[x][
                        y].temperature <= 34:
                        s.fill((196, 107, 167))
                    else:
                        s.fill((255,0,0))
                    screen.blit(s, (int((x * m_data.gridSpread) - m_camera.posX),
                                    int((y * m_data.gridSpread) - m_camera.posY)))  # (0,0) are the top-left coordinates
        # draw grid
        if self.gridActive:
            for x in range(0, m_data.mapWidth, m_data.gridSpread):
                pygame.draw.line(screen, (0, 0, 0), (int(x - m_camera.posX), int(0 - m_camera.posY)),
                                 (int(x - m_camera.posX), int(m_data.mapHeight - m_camera.posY)), 1)
            for y in range(0, m_data.mapHeight, m_data.gridSpread):
                pygame.draw.line(screen, (0, 0, 0), (int(0 - m_camera.posX), int(y - m_camera.posY)),
                                 (int(m_data.mapWidth - m_camera.posX), int(y - m_camera.posY)), 1)

            baseX = m_data.selectX * m_data.gridSpread - m_camera.posX
            baseY = m_data.selectY * m_data.gridSpread - m_camera.posY
            thickness = 2
            pygame.draw.line(screen, (255, 255, 255), (baseX, baseY),
                             (baseX + m_data.gridSpread, baseY), thickness)
            pygame.draw.line(screen, (255, 255, 255), (baseX, baseY + m_data.gridSpread),
                             (baseX + m_data.gridSpread, baseY + m_data.gridSpread), thickness)
            pygame.draw.line(screen, (255, 255, 255), (baseX, baseY),
                             (baseX, baseY + m_data.gridSpread), thickness)
            pygame.draw.line(screen, (255, 255, 255), (baseX + m_data.gridSpread, baseY),
                             (baseX + m_data.gridSpread, baseY + m_data.gridSpread), thickness)
