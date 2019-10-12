import pygame
import constants

class PYGAME_WINDOW:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((constants.pygameWindowWidth,constants.pygameWindowDepth))
    def Prepare(self):
        pygame.event.get()
        self.screen.fill((255,255,255))
    def Reveal(self):
        pygame.display.update()
    def Draw_Black_Circle(self,x,y):
        pygame.draw.circle(self.screen, (0,0,0), (x,y), 10)
    def Draw_Black_Line(self, xBase, yBase, xTip, yTip, width):
        # print(xBase)
        # print(yBase)
        # print(xTip)
        # print(yTip)
        pygame.draw.line(self.screen, (0,0,0), (xBase, yBase), (xTip, yTip), width)
    def Draw_Instruction_Picture(self):
        image = pygame.image.load(r'./images/pic.png')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
    def Draw_Instruction_Right(self):
        image = pygame.image.load(r'./images/right.jpg')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
    def Draw_Instruction_Left(self):
        image = pygame.image.load(r'./images/left.jpg')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
    def Draw_Instruction_Up(self):
        image = pygame.image.load(r'./images/up.jpg')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
    def Draw_Instruction_Down(self):
        image = pygame.image.load(r'./images/down.jpg')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
    def Draw_Instruction_In(self):
        image = pygame.image.load(r'./images/in.jpg')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
    def Draw_Instruction_Out(self):
        image = pygame.image.load(r'./images/out.jpg')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
    def Draw_Instruction_Success(self):
        image = pygame.image.load(r'./images/success.jpg')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
