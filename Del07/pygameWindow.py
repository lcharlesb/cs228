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
    def Draw1(self):
        image = pygame.image.load(r'./images/1.png')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
        image1 = pygame.image.load(r'./images/num1.jpg')
        self.screen.blit(image1, (constants.pygameWindowWidth/2,constants.pygameWindowDepth/2))
    def Draw2(self):
        image = pygame.image.load(r'./images/2.png')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
        image1 = pygame.image.load(r'./images/num2.jpg')
        self.screen.blit(image1, (constants.pygameWindowWidth/2,constants.pygameWindowDepth/2))
    def Draw3(self):
        image = pygame.image.load(r'./images/3.png')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
        image1 = pygame.image.load(r'./images/num3.jpg')
        self.screen.blit(image1, (constants.pygameWindowWidth/2,constants.pygameWindowDepth/2))
    def Draw4(self):
        image = pygame.image.load(r'./images/4.png')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
        image1 = pygame.image.load(r'./images/num4.jpg')
        self.screen.blit(image1, (constants.pygameWindowWidth/2,constants.pygameWindowDepth/2))
    def Draw5(self):
        image = pygame.image.load(r'./images/5.png')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
        image1 = pygame.image.load(r'./images/num5.jpg')
        self.screen.blit(image1, (constants.pygameWindowWidth/2,constants.pygameWindowDepth/2))
    def Draw6(self):
        image = pygame.image.load(r'./images/6.png')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
        image1 = pygame.image.load(r'./images/num6.jpg')
        self.screen.blit(image1, (constants.pygameWindowWidth/2,constants.pygameWindowDepth/2))
    def Draw7(self):
        image = pygame.image.load(r'./images/7.png')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
        image1 = pygame.image.load(r'./images/num7.jpg')
        self.screen.blit(image1, (constants.pygameWindowWidth/2,constants.pygameWindowDepth/2))
    def Draw8(self):
        image = pygame.image.load(r'./images/8.png')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
        image1 = pygame.image.load(r'./images/num8.jpg')
        self.screen.blit(image1, (constants.pygameWindowWidth/2,constants.pygameWindowDepth/2))
    def Draw9(self):
        image = pygame.image.load(r'./images/9.png')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
        image1 = pygame.image.load(r'./images/num9.jpg')
        self.screen.blit(image1, (constants.pygameWindowWidth/2,constants.pygameWindowDepth/2))
