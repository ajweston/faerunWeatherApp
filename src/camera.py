import pygame

class camera:
    minZoom = 0.5
    maxZoom = 1.5

    def __init__(self):
        self.posX = 0
        self.posY = 0
        self.deltaX = 0
        self.deltaY = 0
        self.zoom = 1.0
        self.deltaMultiplier = 1.0
    
    def changeZoom(self,upDown, data):
        if upDown:
            self.zoom = self.zoom + 0.1
            if self.zoom > camera.maxZoom:
                self.zoom = camera.maxZoom
        else:
            self.zoom = self.zoom - 0.1
            if self.zoom < camera.minZoom:
                self.zoom = camera.minZoom
        data.scaleMap(self.zoom)
        
            
    def boundaryCheck(self, mapWidth, mapHeight, screenWidth, screenHeight):
        if self.posX < -80:
            self.posX = -80
        if self.posX > (((mapWidth* self.zoom)) - screenWidth) + 80:
            self.posX = (((mapWidth * self.zoom) - screenWidth) ) + 80
        if self.posY < -80:
            self.posY = -80
        if self.posY > ((mapHeight  * self.zoom - screenHeight)) + 80:
            self.posY = ((mapHeight  * self.zoom - screenHeight)) + 80
