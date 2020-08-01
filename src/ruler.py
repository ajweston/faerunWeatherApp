import pygame
import math

def truncate(number, decimals=0):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor

class ruler:


    def __init__(self):
        self.points = []
        self.zoomPoints = []
        self.distances = []
        self.active = False
        self.numPoints = 0
        self.MILES_PER_PIXEL = 0.762

    def dist(self, x1, x2, y1, y2, m_camera):
        d = math.sqrt(((x2 - x1) * (x2 - x1)) + ((y2 - y1) * (y2 - y1)))
        return (m_camera.zoom * d / self.MILES_PER_PIXEL)

    def addPoint(self,x,y, m_camera):
        self.points.append((x,y))
        self.numPoints += 1
        if self.numPoints >= 2:
            self.active = True
            lastPoint = self.points[-2]
            self.distances.append(self.dist(x, lastPoint[0], y, lastPoint[1], m_camera))
        self.zoomPoints = self.points.copy()
        
    def zoomChange(self, m_camera):
        for i in range(0,len(self.points)):
            self.zoomPoints[i] = self.points[i][0] * m_camera.zoom, self.points[i][1] * m_camera.zoom
            
    def clear(self):
        self.points = []
        self.distances = []
        self.numPoints = 0
        self.active = False

    def draw(self, screen, cameraX, cameraY, font):
        if self.active:
            # draw lines and circles
            for i in range(0,len(self.zoomPoints)-1):
                pos1 = (int(self.zoomPoints[i][0]-cameraX), int(self.zoomPoints[i][1]-cameraY))
                pos2 = (int(self.zoomPoints[i+1][0] - cameraX), int(self.zoomPoints[i+1][1] - cameraY))
                pygame.draw.line(screen,(0,0,0),pos1,pos2, 5)
                color = (0,0,0)
                if i == 0:
                    color = (0,255,0)
                elif i == len(self.zoomPoints)-1:
                    color = (255,0,0)
                pygame.draw.circle(screen,color,pos1,int(15))
            color = (255,0,0)
            pos1 = (int(self.zoomPoints[-1][0] - cameraX), int(self.zoomPoints[-1][1] - cameraY))
            pygame.draw.circle(screen,color,pos1,int(15))
            # draw leg distances
            for j in range(0, len(self.zoomPoints)-1):
                pos2 = (self.zoomPoints[j + 1][0] - cameraX, self.zoomPoints[j + 1][1] - cameraY)

                distText = font.render(f'{truncate(self.distances[j],2)} miles', False, (100, 0, 0))
                screen.blit(distText, (pos2[0]+20, pos2[1]+30))
            # draw total distance
            sum = 0
            for k in range(0, len(self.distances)):
                sum += self.distances[k]
            pos2 = (self.zoomPoints[-1][0] - cameraX, self.zoomPoints[-1][1] - cameraY)
            distText = font.render(f'{truncate(sum, 2)} miles', False, (0, 100, 0))
            screen.blit(distText, (pos2[0] + 20, pos2[1] + 60))
