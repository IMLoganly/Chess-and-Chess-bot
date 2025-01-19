from const import *


class consoleBoard:

    def __init__(self,ROWS,COLS):

        '''
        0 = Black
        1 = White
        '''
        self.board = [["♖","♘","♗","♕","♔","♗","♘","♖"],
                      ["♙","♙","♙","♙","♙","♙","♙","♙"],
                      ["0","1","0","1","0","1","0","1"],
                      ["1","0","1","0","1","0","1","0"],
                      ["0","1","0","1","0","1","0","1"],
                      ["1","0","1","0","1","0","1","0"],
                      ["♟","♟","♟","♟","♟","♟","♟","♟"],
                      ["♜","♞","♝","♛","♚","♝","♞","♜"]]


        self.blankBoard = [["0","1","0","1","0","1","0","1"],
                           ["1","0","1","0","1","0","1","0"],
                           ["0","1","0","1","0","1","0","1"],
                           ["1","0","1","0","1","0","1","0"],
                           ["0","1","0","1","0","1","0","1"],
                           ["1","0","1","0","1","0","1","0"],
                           ["0","1","0","1","0","1","0","1"],
                           ["1","0","1","0","1","0","1","0"],]
        
    def showBoard(self):
        legend = {"0":"□","1":"■"}
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == "0" or self.board[i][j] == "1":
                    print(legend[self.board[i][j]],end=" ")
                else:
                    print(self.board[i][j],end=" ")
            print()


    def makeMove(self,intRow,intCol,finalRow,finalCol):
        temp = self.board[intRow][intCol]

        self.board[finalRow][finalCol] = temp
        self.board[intRow][intCol] = self.blankBoard[intRow][intCol]
        pass



test = consoleBoard(ROWS,COLS)
test.showBoard()

test.makeMove(1,0,3,0)
print()
test.showBoard()

test.makeMove(0,1,3,0)
print()
test.showBoard()
