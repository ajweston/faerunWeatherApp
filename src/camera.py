class camera:
    def __init__(self):
        self.posX = 0
        self.posY = 0
        self.deltaX = 0
        self.deltaY = 0

    def boundaryCheck(self, mapWidth, mapHeight, screenWidth, screenHeight):
        if self.posX < 0:
            self.posX = 0
        if self.posX > mapWidth - screenWidth:
            self.posX = mapWidth - screenWidth
        if self.posY < 0:
            self.posY = 0
        if self.posY > mapHeight - screenHeight:
            self.posY = mapHeight - screenHeight
