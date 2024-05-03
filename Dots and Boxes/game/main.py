<<<<<<< HEAD
from tkinter import *
from typing import Optional
import numpy as np
from State import State
from AIBot import AIBot


class Game:
    def __init__(self, player1: Optional[AIBot] = None, player2: Optional[AIBot] = None):
        self.window = Tk()
        self.window.title("Dots and Boxes")
        self.canvas = Canvas(self.window, width=Board, height=Board, bg='#F4EAEA')
        self.canvas.pack()
        self.startPlayer1 = True
        self.refresh()
        self.player1 = player1
        self.player2 = player2
        self.p1 = ''
        self.p2 = ''
        self.nameOfPlayers()
        self.play_again()

    def play_again(self):
        self.refresh()
        self.boardStatus = np.zeros(shape=(Dots - 1, Dots - 1))
        self.rowStatus = np.zeros(shape=(Dots, Dots - 1))
        self.colStatus = np.zeros(shape=(Dots - 1, Dots))
        self.pointsScored = False
       
        self.startPlayer1 = not self.startPlayer1
        self.player1Turn = not self.startPlayer1
        self.reset_board = False
        self.turntext_handle = []

        self.marked_boxes = []
        self.turnText()

        self.turn()

    def mainloop(self):
        self.window.mainloop()

    def nameOfPlayers(self):
        if self.player1 == None and self.player2 == None:
            self.p1='Player 1'
            self.p2 ='Player 2'
        elif self.player1 != None and self.player2 != None:
            self.p1 = 'Computer 1'
            self.p2 = 'Computer 2'
        else:
            self.p1 = 'Computer'
            self.p2 = 'You'
    def occupied(self, logicalPos, type):
        x = logicalPos[0]
        y = logicalPos[1]
        occupied = True

        if type == "row" and self.rowStatus[y][x] == 0:
            occupied = False
        if type == "col" and self.colStatus[y][x] == 0:
            occupied = False

        return occupied

    def culc_logicalPos(self, gridPos):
        gridPos = np.array(gridPos)
        position = (gridPos - distance / 4) // (distance / 2)
        type = False
        logicalPos = []
        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            x = int((position[0] - 1) // 2)
            y = int(position[1] // 2)
            logicalPos = [x, y]
            type = "row"

        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            y = int((position[1] - 1) // 2)
            x = int(position[0] // 2)
            logicalPos = [x, y]
            type = "col"

        return logicalPos, type

    def Scored(self):
        self.pointsScored = True

    def complate_box(self):
        boxes = np.argwhere(self.boardStatus == -4)
        for box in boxes:
            if list(box) not in self.marked_boxes and list(box) != []:
                self.marked_boxes.append(list(box))
                color = clPlayer1
                self.shade_box(box, color)

        boxes = np.argwhere(self.boardStatus == 4)
        for box in boxes:
            if list(box) not in self.marked_boxes and list(box) != []:
                self.marked_boxes.append(list(box))
                color = clPlayer2
                self.shade_box(box, color)

    def updateBoard(self, type, logicalPos):
        x = logicalPos[0]
        y = logicalPos[1]
        point = 1
        playerModifier = 1
        if self.player1Turn:
            playerModifier = -1

        if y < (Dots - 1) and x < (Dots - 1):
            self.boardStatus[y][x] = (abs(self.boardStatus[y][x]) + point) * playerModifier
            if abs(self.boardStatus[y][x]) == 4:
                self.Scored()

        if type == "row":
            self.rowStatus[y][x] = 1
            if y >= 1:
                self.boardStatus[y - 1][x] = (abs(self.boardStatus[y - 1][x]) + point) * playerModifier
                if abs(self.boardStatus[y - 1][x]) == 4:
                    self.Scored()

        elif type == "col":
            self.colStatus[y][x] = 1
            if x >= 1:
                self.boardStatus[y][x - 1] = (abs(self.boardStatus[y][x - 1]) + point) * playerModifier
                if abs(self.boardStatus[y][x - 1]) == 4:
                    self.Scored()

    def isGameOver(self):
        return (self.rowStatus == 1).all() and (self.colStatus == 1).all()

    # Drawing Functions:
    # Functions to draw the state of the game!

    def drawEdge(self, type, logicalPos):
        if type == "row":
            x1 = (distance / 2 +logicalPos[0] * distance)
            x2 = x1 + distance
            y1 = (distance / 2 +logicalPos[1] * distance)
            y2 = y1
        elif type == "col":
            y1 = (distance / 2 +logicalPos[1] * distance)
            y2 = y1 + distance
            x1 = (distance / 2 + logicalPos[0] * distance)
            x2 = x1

        if self.player1Turn:
            color = cPlayer1
        else:
            color = cPlayer2
        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=wEdge)

    def showGameOver(self):
        player1_score = len(np.argwhere(self.boardStatus == -4))
        player2_score = len(np.argwhere(self.boardStatus == 4))

        if player1_score > player2_score:
            text = "Winner: "+self.p1
            color = cPlayer1
        elif player2_score > player1_score:
            text = "Winner: "+self.p2
            color = cPlayer2
        else:
            text = "Its a tie"
            color = "gray"

        self.canvas.delete("all")
        self.canvas.create_text(Board / 2,Board / 3,font="cmr 40 bold",fill=color,text=text)

        score_text = "Scores \n"
        self.canvas.create_text(Board / 2,5 * Board / 8,font="cmr 30 bold",fill=cDot,text=score_text)

        score_text = self.p1+" : " + str(player1_score) + "\n"
        score_text += self.p2+" : " + str(player2_score) + "\n"

        self.canvas.create_text(Board / 2,3 * Board / 4,font="cmr 20 bold",fill=cDot,text=score_text)
        self.reset_board = True

        score_text = "Click to play again \n"
        self.canvas.create_text(Board / 2, 15 * Board / 16,font="cmr 15 bold",fill="gray",text=score_text)

    def refresh(self):
        for i in range(Dots):
            x = i * distance + distance / 2
            self.canvas.create_line(x,distance / 2,x,Board - distance / 2,fill="#E4CBCB",dash=(2, 2))
            self.canvas.create_line(distance / 2,x,Board - distance / 2,x,fill="#E4CBCB",dash=(2, 2))

        for i in range(Dots):
            for j in range(Dots):
                x1 = i * distance + distance / 2
                x2 = j * distance + distance / 2
                self.canvas.create_oval(x1 - wDot / 2,x2 - wDot / 2,x1 + wDot / 2,x2 + wDot / 2,fill=cDot,outline=cDot)

    def turnText(self):
        text = "Next turn: "
        if self.player1Turn:
            text += self.p1
            color = cPlayer1
        else:
            text += self.p2
            color = cPlayer2

        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(Board - 5 * len(text),Board - distance / 8,font="cmr 15 bold",text=text,fill=color)

    def shade_box(self, box, color):
        x1 = (distance / 2 + box[1] * distance + wEdge / 2)
        y1 = (distance / 2 + box[0] * distance + wEdge / 2)
        x2 = x1 + distance - wEdge
        y2 = y1 + distance - wEdge
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def click(self, event):
        if not self.reset_board:
            gridPos = [event.x, event.y]
            logicalPos, valid_input = self.culc_logicalPos(gridPos)
            self.update(valid_input, logicalPos)
        else:
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False

    def update(self, valid_input, logicalPos):
        if valid_input and not self.occupied(logicalPos, valid_input):
            self.window.unbind(CLICK)
            self.updateBoard(valid_input, logicalPos)
            self.drawEdge(valid_input, logicalPos)
            self.complate_box()
            self.refresh()
            self.player1Turn = (not self.player1Turn if not self.pointsScored else self.player1Turn)
            self.pointsScored = False

            if self.isGameOver():
                self.showGameOver()
                self.window.bind(CLICK, self.click)
            else:
                self.turnText()
                self.turn()

    def turn(self):
        current_bot = self.player1 if self.player1Turn else self.player2
        if current_bot is None:
            self.window.bind(CLICK, self.click)
        else:
            self.window.after(INTERVAL, self.botTurn, current_bot)

    def botTurn(self, bot: AIBot):
        action = bot.transitionModel(State(self.boardStatus.copy(),self.rowStatus.copy(),self.colStatus.copy(),self.player1Turn))
        self.update(action.Type, action.Position)

Board = 500
Dots = int(input("Enter the Size of the Game Grid (Ex: 4,5...): "))
sSize = (Board / 3 - Board / 8) / 2
sThickness = 50
cDot = "#800000"
cPlayer1 = "#009B9B"
clPlayer1 = "#00CCCC"
cPlayer2 = "#C80000"
clPlayer2 = "#FF6464"

wDot = 0.2 * Board / Dots
wEdge = 0.1 * Board / Dots
distance = Board / (Dots)

INTERVAL = 100
CLICK = "<Button-1>"

if __name__ == "__main__":
    print("Select game mode:")
    print("1. Player 1 vs Player 2")
    print("2. Computer vs You")
    print("3. Computer 1 vs Computer 2")

    while True:
        mode = input("Enter game mode (1-3): ")
        if mode in ["1", "2", "3"]:
            break
        print("Invalid input, please enter number 1-3")

    if mode == "1":
        game_instance = Game(None, None)
    elif mode == "2":
        game_instance = Game(AIBot(Dots), None)
    else:
        game_instance = Game(AIBot(Dots), AIBot(Dots))

    game_instance.mainloop()


=======
from tkinter import *
from typing import Optional
import numpy as np
from State import State
from AIBot import AIBot


class Game:
    def __init__(self, player1: Optional[AIBot] = None, player2: Optional[AIBot] = None):
        self.window = Tk()
        self.window.title("Dots and Boxes")
        self.canvas = Canvas(self.window, width=Board, height=Board, bg='#F4EAEA')
        self.canvas.pack()
        self.startPlayer1 = True
        self.refresh()
        self.player1 = player1
        self.player2 = player2
        self.p1 = ''
        self.p2 = ''
        self.nameOfPlayers()
        self.play_again()

    def play_again(self):
        self.refresh()
        self.boardStatus = np.zeros(shape=(Dots - 1, Dots - 1))
        self.rowStatus = np.zeros(shape=(Dots, Dots - 1))
        self.colStatus = np.zeros(shape=(Dots - 1, Dots))
        self.pointsScored = False
       
        self.startPlayer1 = not self.startPlayer1
        self.player1Turn = not self.startPlayer1
        self.reset_board = False
        self.turntext_handle = []

        self.marked_boxes = []
        self.turnText()

        self.turn()

    def mainloop(self):
        self.window.mainloop()

    def nameOfPlayers(self):
        if self.player1 == None and self.player2 == None:
            self.p1='Player 1'
            self.p2 ='Player 2'
        elif self.player1 != None and self.player2 != None:
            self.p1 = 'Computer 1'
            self.p2 = 'Computer 2'
        else:
            self.p1 = 'Computer'
            self.p2 = 'You'
    def occupied(self, logicalPos, type):
        x = logicalPos[0]
        y = logicalPos[1]
        occupied = True

        if type == "row" and self.rowStatus[y][x] == 0:
            occupied = False
        if type == "col" and self.colStatus[y][x] == 0:
            occupied = False

        return occupied

    def culc_logicalPos(self, gridPos):
        gridPos = np.array(gridPos)
        position = (gridPos - distance / 4) // (distance / 2)
        type = False
        logicalPos = []
        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            x = int((position[0] - 1) // 2)
            y = int(position[1] // 2)
            logicalPos = [x, y]
            type = "row"

        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            y = int((position[1] - 1) // 2)
            x = int(position[0] // 2)
            logicalPos = [x, y]
            type = "col"

        return logicalPos, type

    def Scored(self):
        self.pointsScored = True

    def complate_box(self):
        boxes = np.argwhere(self.boardStatus == -4)
        for box in boxes:
            if list(box) not in self.marked_boxes and list(box) != []:
                self.marked_boxes.append(list(box))
                color = clPlayer1
                self.shade_box(box, color)

        boxes = np.argwhere(self.boardStatus == 4)
        for box in boxes:
            if list(box) not in self.marked_boxes and list(box) != []:
                self.marked_boxes.append(list(box))
                color = clPlayer2
                self.shade_box(box, color)

    def updateBoard(self, type, logicalPos):
        x = logicalPos[0]
        y = logicalPos[1]
        point = 1
        playerModifier = 1
        if self.player1Turn:
            playerModifier = -1

        if y < (Dots - 1) and x < (Dots - 1):
            self.boardStatus[y][x] = (abs(self.boardStatus[y][x]) + point) * playerModifier
            if abs(self.boardStatus[y][x]) == 4:
                self.Scored()

        if type == "row":
            self.rowStatus[y][x] = 1
            if y >= 1:
                self.boardStatus[y - 1][x] = (abs(self.boardStatus[y - 1][x]) + point) * playerModifier
                if abs(self.boardStatus[y - 1][x]) == 4:
                    self.Scored()

        elif type == "col":
            self.colStatus[y][x] = 1
            if x >= 1:
                self.boardStatus[y][x - 1] = (abs(self.boardStatus[y][x - 1]) + point) * playerModifier
                if abs(self.boardStatus[y][x - 1]) == 4:
                    self.Scored()

    def isGameOver(self):
        return (self.rowStatus == 1).all() and (self.colStatus == 1).all()

    # Drawing Functions:
    # Functions to draw the state of the game!

    def drawEdge(self, type, logicalPos):
        if type == "row":
            x1 = (distance / 2 +logicalPos[0] * distance)
            x2 = x1 + distance
            y1 = (distance / 2 +logicalPos[1] * distance)
            y2 = y1
        elif type == "col":
            y1 = (distance / 2 +logicalPos[1] * distance)
            y2 = y1 + distance
            x1 = (distance / 2 + logicalPos[0] * distance)
            x2 = x1

        if self.player1Turn:
            color = cPlayer1
        else:
            color = cPlayer2
        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=wEdge)

    def showGameOver(self):
        player1_score = len(np.argwhere(self.boardStatus == -4))
        player2_score = len(np.argwhere(self.boardStatus == 4))

        if player1_score > player2_score:
            text = "Winner: "+self.p1
            color = cPlayer1
        elif player2_score > player1_score:
            text = "Winner: "+self.p2
            color = cPlayer2
        else:
            text = "Its a tie"
            color = "gray"

        self.canvas.delete("all")
        self.canvas.create_text(Board / 2,Board / 3,font="cmr 40 bold",fill=color,text=text)

        score_text = "Scores \n"
        self.canvas.create_text(Board / 2,5 * Board / 8,font="cmr 30 bold",fill=cDot,text=score_text)

        score_text = self.p1+" : " + str(player1_score) + "\n"
        score_text += self.p2+" : " + str(player2_score) + "\n"

        self.canvas.create_text(Board / 2,3 * Board / 4,font="cmr 20 bold",fill=cDot,text=score_text)
        self.reset_board = True

        score_text = "Click to play again \n"
        self.canvas.create_text(Board / 2, 15 * Board / 16,font="cmr 15 bold",fill="gray",text=score_text)

    def refresh(self):
        for i in range(Dots):
            x = i * distance + distance / 2
            self.canvas.create_line(x,distance / 2,x,Board - distance / 2,fill="#E4CBCB",dash=(2, 2))
            self.canvas.create_line(distance / 2,x,Board - distance / 2,x,fill="#E4CBCB",dash=(2, 2))

        for i in range(Dots):
            for j in range(Dots):
                x1 = i * distance + distance / 2
                x2 = j * distance + distance / 2
                self.canvas.create_oval(x1 - wDot / 2,x2 - wDot / 2,x1 + wDot / 2,x2 + wDot / 2,fill=cDot,outline=cDot)

    def turnText(self):
        text = "Next turn: "
        if self.player1Turn:
            text += self.p1
            color = cPlayer1
        else:
            text += self.p2
            color = cPlayer2

        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(Board - 5 * len(text),Board - distance / 8,font="cmr 15 bold",text=text,fill=color)

    def shade_box(self, box, color):
        x1 = (distance / 2 + box[1] * distance + wEdge / 2)
        y1 = (distance / 2 + box[0] * distance + wEdge / 2)
        x2 = x1 + distance - wEdge
        y2 = y1 + distance - wEdge
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def click(self, event):
        if not self.reset_board:
            gridPos = [event.x, event.y]
            logicalPos, valid_input = self.culc_logicalPos(gridPos)
            self.update(valid_input, logicalPos)
        else:
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False

    def update(self, valid_input, logicalPos):
        if valid_input and not self.occupied(logicalPos, valid_input):
            self.window.unbind(CLICK)
            self.updateBoard(valid_input, logicalPos)
            self.drawEdge(valid_input, logicalPos)
            self.complate_box()
            self.refresh()
            self.player1Turn = (not self.player1Turn if not self.pointsScored else self.player1Turn)
            self.pointsScored = False

            if self.isGameOver():
                self.showGameOver()
                self.window.bind(CLICK, self.click)
            else:
                self.turnText()
                self.turn()

    def turn(self):
        current_bot = self.player1 if self.player1Turn else self.player2
        if current_bot is None:
            self.window.bind(CLICK, self.click)
        else:
            self.window.after(INTERVAL, self.botTurn, current_bot)

    def botTurn(self, bot: AIBot):
        action = bot.transitionModel(State(self.boardStatus.copy(),self.rowStatus.copy(),self.colStatus.copy(),self.player1Turn))
        self.update(action.Type, action.Position)

Board = 500
Dots = int(input("Enter the Size of the Game Grid (Ex: 4,5...): "))
sSize = (Board / 3 - Board / 8) / 2
sThickness = 50
cDot = "#800000"
cPlayer1 = "#009B9B"
clPlayer1 = "#00CCCC"
cPlayer2 = "#C80000"
clPlayer2 = "#FF6464"

wDot = 0.2 * Board / Dots
wEdge = 0.1 * Board / Dots
distance = Board / (Dots)

INTERVAL = 100
CLICK = "<Button-1>"

if __name__ == "__main__":
    print("Select game mode:")
    print("1. Player 1 vs Player 2")
    print("2. Computer vs You")
    print("3. Computer 1 vs Computer 2")

    while True:
        mode = input("Enter game mode (1-3): ")
        if mode in ["1", "2", "3"]:
            break
        print("Invalid input, please enter number 1-3")

    if mode == "1":
        game_instance = Game(None, None)
    elif mode == "2":
        game_instance = Game(AIBot(Dots), None)
    else:
        game_instance = Game(AIBot(Dots), AIBot(Dots))

    game_instance.mainloop()


>>>>>>> f0a8fb5dfb2784b38af1cda5cd8726640744375b
