import pygame
import constants

class PYGAME_WINDOW:

    pygameWindowWidth = 0
    pygameWindowDepth = 0

    def __init__(self):
        global pygameWindowWidth, pygameWindowDepth

        pygame.init()
        self.screen = pygame.display.set_mode((1000, 700))

        screenInfoObject = pygame.display.Info()
        pygameWindowWidth = screenInfoObject.current_w
        pygameWindowDepth = screenInfoObject.current_h

    def Prepare(self):
        pygame.event.get()
        self.screen.fill((255,255,255))

    def Reveal(self):
        pygame.display.update()

    def Draw_Black_Line(self, xBase, yBase, xTip, yTip, width):
        pygame.draw.line(self.screen, (0,0,0), (xBase, yBase), (xTip, yTip), width)

    def Draw_Line(self, xBase, yBase, xTip, yTip, width, green):
        color = (0,0,0)
        if(green == 1):
            color = (0, 255, 0)
        pygame.draw.line(self.screen, color, (xBase, yBase), (xTip, yTip), width)

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
    def Draw_Instruction_Failure(self):
        image = pygame.image.load(r'./images/failure.png')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))

    def Draw0(self):
        image = pygame.image.load(r'./images/0.png')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
    def Draw0Num(self):
        image1 = pygame.image.load(r'./images/num0.png')
        self.screen.blit(image1, (constants.pygameWindowWidth/2,constants.pygameWindowDepth/2))
    def Draw1(self):
        image = pygame.image.load(r'./images/1.png')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
    def Draw1Num(self):
        image1 = pygame.image.load(r'./images/num1.jpg')
        self.screen.blit(image1, (constants.pygameWindowWidth/2,constants.pygameWindowDepth/2))
    def Draw2(self):
        image = pygame.image.load(r'./images/2.png')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
    def Draw2Num(self):
        image1 = pygame.image.load(r'./images/num2.jpg')
        self.screen.blit(image1, (constants.pygameWindowWidth/2,constants.pygameWindowDepth/2))
    def Draw3(self):
        image = pygame.image.load(r'./images/3.png')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
    def Draw3Num(self):
        image1 = pygame.image.load(r'./images/num3.jpg')
        self.screen.blit(image1, (constants.pygameWindowWidth/2,constants.pygameWindowDepth/2))
    def Draw4(self):
        image = pygame.image.load(r'./images/4.png')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
    def Draw4Num(self):
        image1 = pygame.image.load(r'./images/num4.jpg')
        self.screen.blit(image1, (constants.pygameWindowWidth/2,constants.pygameWindowDepth/2))
    def Draw5(self):
        image = pygame.image.load(r'./images/5.png')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
    def Draw5Num(self):
        image1 = pygame.image.load(r'./images/num5.jpg')
        self.screen.blit(image1, (constants.pygameWindowWidth/2,constants.pygameWindowDepth/2))
    def Draw6(self):
        image = pygame.image.load(r'./images/6.png')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
    def Draw6Num(self):
        image1 = pygame.image.load(r'./images/num6.jpg')
        self.screen.blit(image1, (constants.pygameWindowWidth/2,constants.pygameWindowDepth/2))
    def Draw7(self):
        image = pygame.image.load(r'./images/7.png')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
    def Draw7Num(self):
        image1 = pygame.image.load(r'./images/num7.jpg')
        self.screen.blit(image1, (constants.pygameWindowWidth/2,constants.pygameWindowDepth/2))
    def Draw8(self):
        image = pygame.image.load(r'./images/8.png')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
    def Draw8Num(self):
        image1 = pygame.image.load(r'./images/num8.jpg')
        self.screen.blit(image1, (constants.pygameWindowWidth/2,constants.pygameWindowDepth/2))
    def Draw9(self):
        image = pygame.image.load(r'./images/9.png')
        self.screen.blit(image, (constants.pygameWindowWidth/2,0))
    def Draw9Num(self):
        image1 = pygame.image.load(r'./images/num9.jpg')
        self.screen.blit(image1, (constants.pygameWindowWidth/2,constants.pygameWindowDepth/2))

    def Display_CountDown(self, numberToDisplay, xMinus):
        font = pygame.font.Font('freesansbold.ttf', 64)
        fontColor = (0,0,0)
        countDownFont = font.render(str(numberToDisplay), True, fontColor)
        self.screen.blit(countDownFont, (constants.pygameWindowWidth/2 - xMinus, constants.pygameWindowDepth/2))
    def Display_Game_CountDown(self, numberToDisplay):
        font = pygame.font.Font('freesansbold.ttf', 64)
        fontColor = (0,0,0)
        countDownFont = font.render(str(numberToDisplay), True, fontColor)
        self.screen.blit(countDownFont, (constants.pygameWindowWidth/2 - 34, constants.pygameWindowDepth/12))

    def Display_Score_During_Game(self, numberToDisplay):
        if(numberToDisplay == 0):
            numberToDisplay = "000"

        font = pygame.font.Font('freesansbold.ttf', 38)
        fontColor = (0,0,0)
        countDownFont = font.render("Score: " + str(numberToDisplay), True, fontColor)
        self.screen.blit(countDownFont, (constants.pygameWindowWidth/2 - 96, (constants.pygameWindowDepth/12) * 8))

    def DrawArithmatic(self, additionOrSubtraction, numOne, numTwo):
        font = pygame.font.Font('freesansbold.ttf', 80)
        operator = ""

        if (additionOrSubtraction == 0):
            operator = " + "
        elif (additionOrSubtraction == 1):
            operator = " - "

        text = str(numOne) + operator + str(numTwo)
        fontColor = (255, 0, 0)
        arithmaticFont = font.render(text, True, fontColor)
        self.screen.blit(arithmaticFont, (((constants.pygameWindowWidth/2) - 80), (constants.pygameWindowDepth/2) - 12))
