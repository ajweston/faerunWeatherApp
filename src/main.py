import pygame

from data import data
from camera import camera
from ruler import ruler
from weatherGrid import weatherGrid
import utilities

SHOW_GRID = 0x01
SHOW_INFO = 0x02
SHOW_PRECIP = 0x04


def main():
    # initialize data
    m_data = data()

    # pygame initialization
    pygame.init()
    # font
    pygame.font.init()  # you have to call this at the start,
    # if you want to use this module.
    font12 = pygame.font.SysFont('Comic Sans MS', 12)
    font30 = pygame.font.SysFont('Comic Sans MS', 30)

    # configure window setings
    screen = pygame.display.set_mode((m_data.screenWidth, m_data.screenHeight))
    pygame.display.set_caption("Weather App")
    icon = pygame.image.load('icon.png')
    pygame.display.set_icon(icon)

    # initialize camera
    m_camera = camera()

    # initialize ruler
    m_ruler = ruler()

    # load map image
    gameMap = pygame.image.load('faerunMap.jpg')
    m_data.mapWidth, m_data.mapHeight = gameMap.get_size()

    # initialize weather data
    m_weatherGrid = weatherGrid(m_data)

    m_weatherGrid.weather[50][0].precipitation = 50

    while m_data.running:
        # process events (input, etc.)
        mouseX, mouseY = pygame.mouse.get_pos()

        utilities.processInput(m_data, mouseX, mouseY, m_camera, m_ruler, m_weatherGrid)

        # update camera position
        m_camera.posX = m_camera.posX + m_camera.deltaX
        m_camera.posY = m_camera.posY + m_camera.deltaY
        m_camera.boundaryCheck(m_data.mapWidth, m_data.mapHeight, m_data.screenWidth, m_data.screenHeight)

        # fill screen
        screen.fill((0, 0, 0))

        # draw map
        screen.blit(gameMap, (int(-m_camera.posX), int(-m_camera.posY)))

        # weather grid draw
        m_weatherGrid.draw(screen, m_data, m_camera)

        # draw ruler
        m_ruler.draw(screen, m_camera.posX, m_camera.posY, font30)

        # draw info block
        utilities.drawInfoBlock(screen, m_data, m_weatherGrid, font12)

        # show popup buttons
        utilities.popupButtons(screen, m_data, mouseX, mouseY, font12)

        # update screen
        pygame.display.update()

    m_data.shutdown


main()
