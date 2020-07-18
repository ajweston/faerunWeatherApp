import pygame
import tkinter as tk
from tkinter import messagebox

SHOW_GRID = 0x01
SHOW_INFO = 0x02
SHOW_PRECIP = 0x04

def settingsPopup(m_data):
    settingsWindow = tk.Tk()
    label = tk.Label(
        text="Settings",
        fg="black",
        bg="white",
        width=30,
        height=1
    )
    label1 = tk.Label(
        text="Screen Width",
        fg="black",
        bg="white",
        width=30,
        height=1
    )
    entry1 = tk.Entry(fg="black", bg="white", width=50)

    label2 = tk.Label(
        text="Screen Height",
        fg="black",
        bg="white",
        width=30,
        height=1
    )
    entry2 = tk.Entry(fg="black", bg="white", width=50)

    def settingsButton():
        try:
            screenWidth = int(entry1.get())
            screenHeight = int(entry2.get())
            m_data.config['Screen']['width'] = str(screenWidth)
            m_data.config['Screen']['height'] = str(screenHeight)
            pygame.display.set_mode((screenWidth, screenHeight))
            with open('config.ini', 'w') as configfile:
                m_data.config.write(configfile)
            settingsWindow.destroy()
        except:
            messagebox.showwarning(title='Error', message='Invalid Screen Dimensions')

    button = tk.Button(
        text="Update",
        width=25,
        height=5,
        bg="white",
        fg="black",
        command=settingsButton
    )
    # pack
    label.pack()
    label1.pack()
    entry1.pack()
    label2.pack()
    entry2.pack()
    button.pack()

    settingsWindow.mainloop()
    m_data.config.read('config.ini')

    m_data.screenWidth = int(m_data.config['Screen']['width'])
    m_data.screenHeight = int(m_data.config['Screen']['height'])

def drawInfoBlock(screen, m_data, m_weatherGrid, font12):
    if m_data.state & SHOW_INFO:
        # background
        s = pygame.Surface((int(m_data.screenWidth / 4), m_data.screenHeight))  # the size of your rect
        s.set_alpha(200)  # alpha level
        s.fill((255, 255, 255))  # this fills the entire surface
        screen.blit(s, (m_data.screenWidth - int(m_data.screenWidth / 4), 0))  # (0,0) are the top-left coordinates
        # text
        text = font12.render(f'{m_data.months[m_data.month - 1]}, {m_data.day}', False, (0, 0, 0))
        screen.blit(text, (m_data.screenWidth - int(m_data.screenWidth / 4) + 10, 10))

        text = font12.render(f'Precipitation: {m_weatherGrid.weather[m_data.selectX][m_data.selectY].precipitation}', False, (0, 0, 0))
        screen.blit(text, (m_data.screenWidth - int(m_data.screenWidth / 4) + 10, 40))

        text = font12.render(f'Temperature: {m_weatherGrid.weather[m_data.selectX][m_data.selectY].temperature}',
                             False, (0, 0, 0))
        screen.blit(text, (m_data.screenWidth - int(m_data.screenWidth / 4) + 10, 70))

        text = font12.render(f'Coordinates: {m_data.selectX}, {m_data.selectY}', False, (0, 0, 0))
        screen.blit(text, (m_data.screenWidth - int(m_data.screenWidth / 4) + 10, m_data.screenHeight-160))


def popupButtons(screen, m_data, mouseX, mouseY, font12):
    if mouseX < 80 and mouseY < 80:
        pygame.draw.rect(screen, (100, 100, 200), (0, 0, 80, 80))
        settingsText = font12.render('Show Info', False, (0, 0, 0))
        screen.blit(settingsText, (10, 30))
    if mouseX < 80 and 80 < mouseY < 160:
        pygame.draw.rect(screen, (200, 100, 100), (0, 80, 80, 80))
        settingsText = font12.render('Show Grid', False, (0, 0, 0))
        screen.blit(settingsText, (10, 110))
    if mouseX < 80 and 160 < mouseY < 240:
        pygame.draw.rect(screen, (100, 255, 100), (0, 160, 80, 80))
        settingsText = font12.render('Show', False, (0, 0, 0))
        screen.blit(settingsText, (25, 190))
        settingsText = font12.render('Precipitation', False, (0, 0, 0))
        screen.blit(settingsText, (8, 200))

    if m_data.state & SHOW_INFO:
        if mouseX > m_data.screenWidth - 80 and mouseY > m_data.screenHeight - 80:
            pygame.draw.rect(screen, (200, 200, 200), (m_data.screenWidth - 80, m_data.screenHeight - 80, 80, 80))
            settingsText = font12.render('Next Day', False, (0, 0, 0))
            screen.blit(settingsText, (m_data.screenWidth - 70, m_data.screenHeight - 50))


def processInput(data, mouseX, mouseY, m_camera, m_ruler, m_weatherGrid):
    for event in pygame.event.get():
        # control events
        if event.type == pygame.QUIT:
            data.running = False

        # key input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if data.state & SHOW_INFO:
                    data.day += 1
                    if data.day > 30:
                        data.day = 1
                        data.month += 1
                    if data.month > 12:
                        data.month = 1
                    m_weatherGrid.advance()


            if event.key == pygame.K_LEFT:
                m_camera.deltaX = -data.movementBase
            elif event.key == pygame.K_RIGHT:
                m_camera.deltaX = data.movementBase
            if event.key == pygame.K_UP:
                m_camera.deltaY = -data.movementBase
            elif event.key == pygame.K_DOWN:
                m_camera.deltaY = data.movementBase
            if event.key == pygame.K_BACKSPACE:
                m_ruler.clear()
            if event.key == pygame.K_ESCAPE:
                settingsPopup(data)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                m_camera.deltaX = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                m_camera.deltaY = 0
        # mouse input
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not (data.leftClick):
                    data.leftClick = True
                    if mouseX < 80 and mouseY < 80:
                        if data.state & SHOW_INFO:
                            data.state = data.state & ~SHOW_INFO
                        else:
                            data.state = data.state | SHOW_INFO

                    if mouseX < 80 and 80 < mouseY < 160:
                        m_weatherGrid.gridActive = not (m_weatherGrid.gridActive)
                        m_weatherGrid.precipitationActive = False
                    if mouseX < 80 and 160 < mouseY < 240:
                        if not(m_weatherGrid.precipitationActive):
                            m_weatherGrid.precipitationActive = True
                            m_weatherGrid.gridActive = True
                        else:
                            m_weatherGrid.precipitationActive = False
                            m_weatherGrid.gridActive = False
                    if data.state & SHOW_INFO:
                        if mouseX > data.screenWidth - 80 and mouseY > data.screenHeight - 80:
                            data.day += 1
                            if data.day > 30:
                                data.day = 1
                                data.month += 1
                            if data.month > 12:
                                data.month = 1
                            m_weatherGrid.advance()

                    data.selectX = int((mouseX + m_camera.posX)/data.gridSpread)
                    data.selectY = int((mouseY + m_camera.posY) / data.gridSpread)
            if event.button == 3:
                if not (data.rightClick):
                    data.rightClick = True
                    m_ruler.addPoint(mouseX + m_camera.posX, mouseY + m_camera.posY)


        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                data.leftClick = False
            if event.button == 3:
                data.rightClick = False
