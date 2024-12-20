class Square:

    def __init__(self,row,col,piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        pass

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def hasPiece(self):
        return self.piece != None

    def isEmpty(self):
        return not self.hasPiece()

    def hasTeamPiece(self,color):
        return self.hasPiece() and self.piece.color == color       

    def hasEnemyPiece(self,color):
        return self.hasPiece() and self.piece.color != color

    def isEmptyOrEnemy(self,color):
        return self.isEmpty() or self.hasEnemyPiece(color)

    @staticmethod
    def inRange(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True