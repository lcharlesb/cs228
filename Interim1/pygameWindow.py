from __future__ import division
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
    def DrawDatabaseData(self, database, userName, numSuccesses, countAttempts, previousPercentage, currUserRank):

        # Digit attempts:
        userEntry = database[userName]
        zero = userEntry['digit'+str(0)+'attempted']
        one = userEntry['digit'+str(1)+'attempted']
        two = userEntry['digit'+str(2)+'attempted']
        three = userEntry['digit'+str(3)+'attempted']
        four = userEntry['digit'+str(4)+'attempted']
        five = userEntry['digit'+str(5)+'attempted']
        six = userEntry['digit'+str(6)+'attempted']
        seven = userEntry['digit'+str(7)+'attempted']
        eight = userEntry['digit'+str(8)+'attempted']
        nine = userEntry['digit'+str(9)+'attempted']
        font = pygame.font.Font('freesansbold.ttf', 16)
        text = ["Number of attempts: ",
                "0: " + str(zero),
                "1: " + str(one),
                "2: " + str(two),
                "3: " + str(three),
                "4: " + str(four),
                "5: " + str(five),
                "6: " + str(six),
                "7: " + str(seven),
                "8: " + str(eight),
                "9: " + str(nine),
                ]
        summary = []
        for line in text:
            summary.append(font.render(line, True, (255, 0, 0)))
        posX = (constants.pygameWindowWidth // 12)
        posY = (constants.pygameWindowDepth // 2)
        position = posX, posY
        for line in range(len(summary)):
            self.screen.blit(summary[line], (position[0], position[1] + (line*16) + (4*line)))

        # Percentages:
        percentage = 0
        if countAttempts != 0:
            percentage = float((numSuccesses / countAttempts) * 100)
        percentageText = "Current session success rate: " + str(percentage) + "%"
        percentageFontColor = (255, 0, 0)
        if percentage >= 80:
            percentageFontColor = (0, 255, 0)
        elif percentage >= 60:
            percentageFontColor = (235, 235, 0)
        else:
            percentageFontColor = (255, 0, 0)
        percentageFont = font.render(percentageText, True, percentageFontColor)
        previousPercentage = previousPercentage * 100
        previousPercentageText = "Previous session success rate: " + str(previousPercentage) + "%"
        previousPercentageFontColor = (255, 0, 0)
        if previousPercentage >= 80:
            previousPercentageFontColor = (0, 255, 0)
        elif previousPercentage >= 60:
            previousPercentageFontColor = (235, 235, 0)
        else:
            previousPercentageFontColor = (255, 0, 0)
        previousPercentageFont = font.render(previousPercentageText, True, previousPercentageFontColor)
        percentagePosY = constants.pygameWindowDepth - 32
        percentagePosX = 32
        self.screen.blit(percentageFont, (percentagePosX, percentagePosY))
        self.screen.blit(previousPercentageFont, (percentagePosX, percentagePosY + 16))

        # Rank:
        rankText = "Rank: " + str(currUserRank)
        rankFontColor = (0, 0, 255)
        rankFont = font.render(rankText, True, rankFontColor)
        self.screen.blit(rankFont, (posX, posY - 32))
