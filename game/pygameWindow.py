import pygame
import constants

class PYGAME_WINDOW:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((constants.pygameWindowWidth, constants.pygameWindowDepth))

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
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, (constants.pygameWindowWidth/2 - xMinus,constants.pygameWindowDepth/2 - yMinus))
    def Draw_Instruction_Right(self):
        image = pygame.image.load(r'./images/right.jpg')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, (constants.pygameWindowWidth/2 - xMinus,constants.pygameWindowDepth/2 - yMinus))
    def Draw_Instruction_Left(self):
        image = pygame.image.load(r'./images/left.jpg')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3-xMinus,constants.pygameWindowDepth/2 - yMinus))
    def Draw_Instruction_Up(self):
        image = pygame.image.load(r'./images/up.jpg')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3-xMinus,constants.pygameWindowDepth/2 - yMinus))
    def Draw_Instruction_Down(self):
        image = pygame.image.load(r'./images/down.jpg')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3-xMinus,constants.pygameWindowDepth/2 - yMinus))
    def Draw_Instruction_In(self):
        image = pygame.image.load(r'./images/in.jpg')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3-xMinus,constants.pygameWindowDepth/2 - yMinus))
    def Draw_Instruction_Out(self):
        image = pygame.image.load(r'./images/out.jpg')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3-xMinus,constants.pygameWindowDepth/2 - yMinus))
    def Draw_Instruction_Success(self):
        image = pygame.image.load(r'./images/success.jpg')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3 - xMinus,(constants.pygameWindowDepth/2) - yMinus))
    def Draw_Instruction_Failure(self):
        image = pygame.image.load(r'./images/failure.jpg')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3 - xMinus,constants.pygameWindowDepth/2 - yMinus))

    def Draw_Menu(self):
        image = pygame.image.load(r'./images/learn_icon.png')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/8)*5 - xMinus, constants.pygameWindowDepth/3 - yMinus))
        image = pygame.image.load(r'./images/game_icon.png')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/8)*5 - xMinus, (constants.pygameWindowDepth/3)*2 - yMinus))
        image = pygame.image.load(r'./images/menu0.png')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/8)*7 - xMinus, constants.pygameWindowDepth/3 - yMinus))
        image = pygame.image.load(r'./images/menu1.png')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/8)*7- xMinus, (constants.pygameWindowDepth/3)*2 - yMinus))


    def Draw0(self):
        image = pygame.image.load(r'./images/0.png')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3 - xMinus, constants.pygameWindowDepth/4 - yMinus))
    def Draw0Num(self):
        image = pygame.image.load(r'./images/num0.png')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3 - xMinus, constants.pygameWindowDepth/2))
    def Draw1(self):
        image = pygame.image.load(r'./images/1.png')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3 - xMinus, constants.pygameWindowDepth/4 - yMinus))
    def Draw1Num(self):
        image = pygame.image.load(r'./images/num1.jpg')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3 - xMinus, constants.pygameWindowDepth/2))
    def Draw2(self):
        image = pygame.image.load(r'./images/2.png')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3 - xMinus, constants.pygameWindowDepth/4 - yMinus))
    def Draw2Num(self):
        image = pygame.image.load(r'./images/num2.jpg')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3 - xMinus, constants.pygameWindowDepth/2))
    def Draw3(self):
        image = pygame.image.load(r'./images/3.png')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3 - xMinus, constants.pygameWindowDepth/4 - yMinus))
    def Draw3Num(self):
        image = pygame.image.load(r'./images/num3.jpg')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3 - xMinus, constants.pygameWindowDepth/2))
    def Draw4(self):
        image = pygame.image.load(r'./images/4.png')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3 - xMinus, constants.pygameWindowDepth/4 - yMinus))
    def Draw4Num(self):
        image = pygame.image.load(r'./images/num4.jpg')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3 - xMinus, constants.pygameWindowDepth/2))
    def Draw5(self):
        image = pygame.image.load(r'./images/5.png')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3 - xMinus, constants.pygameWindowDepth/4 - yMinus))
    def Draw5Num(self):
        image = pygame.image.load(r'./images/num5.jpg')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3 - xMinus, constants.pygameWindowDepth/2))
    def Draw6(self):
        image = pygame.image.load(r'./images/6.png')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3 - xMinus, constants.pygameWindowDepth/4 - yMinus))
    def Draw6Num(self):
        image = pygame.image.load(r'./images/num6.jpg')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3 - xMinus, constants.pygameWindowDepth/2))
    def Draw7(self):
        image = pygame.image.load(r'./images/7.png')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3 - xMinus, constants.pygameWindowDepth/4 - yMinus))
    def Draw7Num(self):
        image = pygame.image.load(r'./images/num7.jpg')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3 - xMinus, constants.pygameWindowDepth/2))
    def Draw8(self):
        image = pygame.image.load(r'./images/8.png')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3 - xMinus, constants.pygameWindowDepth/4 - yMinus))
    def Draw8Num(self):
        image = pygame.image.load(r'./images/num8.jpg')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3 - xMinus, constants.pygameWindowDepth/2))
    def Draw9(self):
        image = pygame.image.load(r'./images/9.png')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3 - xMinus, constants.pygameWindowDepth/4 - yMinus))
    def Draw9Num(self):
        image = pygame.image.load(r'./images/num9.jpg')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/4)*3 - xMinus, constants.pygameWindowDepth/2))

    def Display_CountDown(self, numberToDisplay):
        font = pygame.font.Font('freesansbold.ttf', 64)
        fontColor = (0,0,0)
        countDownFont = font.render(str(numberToDisplay), True, fontColor)
        xMinus = countDownFont.get_rect().size[0]/2
        yMinus = countDownFont.get_rect().size[1]/2
        self.screen.blit(countDownFont, ((constants.pygameWindowWidth/4)*3 - xMinus, constants.pygameWindowDepth/2 - yMinus))
    def Display_Game_CountDown(self, numberToDisplay):
        font = pygame.font.Font('freesansbold.ttf', 58)
        fontColor = (0,0,0)
        countDownFont = font.render(str(numberToDisplay), True, fontColor)
        xMinus = countDownFont.get_rect().size[0]/2
        yMinus = countDownFont.get_rect().size[1]/2
        self.screen.blit(countDownFont, ((constants.pygameWindowWidth/4)*3 - xMinus, constants.pygameWindowDepth/12 - yMinus))

    def Display_Score_During_Game(self, numberToDisplay):
        if(numberToDisplay == 0):
            numberToDisplay = "000"

        font = pygame.font.Font('freesansbold.ttf', 38)
        fontColor = (0,0,0)
        countDownFont = font.render("Score: " + str(numberToDisplay), True, fontColor)
        xMinus = countDownFont.get_rect().size[0]/2
        yMinus = countDownFont.get_rect().size[1]/2
        self.screen.blit(countDownFont, ((constants.pygameWindowWidth/4)*3 - xMinus, (constants.pygameWindowDepth/12)*8))

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
        xMinus = arithmaticFont.get_rect().size[0]/2
        yMinus = arithmaticFont.get_rect().size[1]/2
        self.screen.blit(arithmaticFont, (((constants.pygameWindowWidth/4)*3 - xMinus), (constants.pygameWindowDepth/2) - yMinus/2))

    def Display_Game_End(self, gold, silver, bronze, score):
        if gold == -1:
            gold = 0
        if silver == -1:
            silver = 0
        if bronze == -1:
            bronze = 0

        font = pygame.font.Font('freesansbold.ttf', 38)
        fontColor = (0,0,0)

        image = pygame.image.load(r'./images/gold.jpg')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/8)*5 - xMinus, constants.pygameWindowDepth/4 - yMinus))

        if score == gold:
            fontColor = (0, 255, 0)
        goldFont = font.render(str(gold), True, fontColor)
        xMinus = goldFont.get_rect().size[0]/2
        yMinus = goldFont.get_rect().size[1]/2
        self.screen.blit(goldFont, ((constants.pygameWindowWidth/8)*7 - xMinus, constants.pygameWindowDepth/4 - yMinus))
        fontColor = (0,0,0)

        image = pygame.image.load(r'./images/silver.jpg')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/8)*5 - xMinus, (constants.pygameWindowDepth/4)*2 - yMinus))

        if score == silver:
            fontColor = (0, 255, 0)
        silverFont = font.render(str(silver), True, fontColor)
        xMinus = silverFont.get_rect().size[0]/2
        yMinus = silverFont.get_rect().size[1]/2
        self.screen.blit(silverFont, ((constants.pygameWindowWidth/8)*7 - xMinus, (constants.pygameWindowDepth/4)*2 - yMinus))
        fontColor = (0,0,0)

        image = pygame.image.load(r'./images/bronze.jpg')
        xMinus = image.get_rect().size[0]/2
        yMinus = image.get_rect().size[1]/2
        self.screen.blit(image, ((constants.pygameWindowWidth/8)*5 - xMinus, (constants.pygameWindowDepth/4)*3 - yMinus))

        if score == bronze:
            fontColor = (0, 255, 0)
        bronzeFont = font.render(str(bronze), True, fontColor)
        xMinus = bronzeFont.get_rect().size[0]/2
        yMinus = bronzeFont.get_rect().size[1]/2
        self.screen.blit(bronzeFont, ((constants.pygameWindowWidth/8)*7 - xMinus, (constants.pygameWindowDepth/4)*3 - yMinus))
        fontColor = (0,0,0)
