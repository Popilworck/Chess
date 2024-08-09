""" 
eventually try to make undo and change would_be_check
"""

class Board:
    def __init__(self) -> None:
        self.board :list[list[Piece]] = [['.' for i in range(8)] for j in range(8)]
        self.castling_rights = {0:["OO","OOO"],1:["OO","OOO"]}
        self.en_passant:bool = False
        self.piece_being_bricked: Piece = None
        self.move_count = 0

    def get_piece(self,x,y): 
        return self.board[y][x] if isinstance(self.board[y][x],Piece) else False
    
    def func(self,todo:str):
        self.__dict__["pl"] = []
        for row in self.board:
            for p in row:
                if isinstance(p,Piece):
                    self.__dict__["pl"].append(p)
                    if p.type == "K":
                            exec(f'self.__dict__["white"] = p{todo}') if p.color else exec(f'self.__dict__["black"] = p{todo}')

    def is_check(self, piece = None): 
        self.func('.get_pos()')
        white_king = self.__dict__['white']
        black_king = self.__dict__['black']
        piece_list:list[Piece] = self.__dict__['pl']
        white_move_list, black_move_list = [j for i in piece_list for j in i.moves if i.color],[j for i in piece_list for j in i.moves if not i.color]
        if piece is not None:
            return white_king in black_move_list if piece.color else black_king in white_move_list
        return (white_king in black_move_list, black_king in white_move_list)
    
    def is_mate(self):
        checks = self.is_check()
        self.func('.moves')
        black_king_moves = self.__dict__['black']
        white_king_moves = self.__dict__['white']
        return (not white_king_moves and checks[0], not black_king_moves and checks[1])
    
    def is_stalemate(self):
        checks = self.is_check()
        piece_list = [j for i in self.board for j in i if isinstance(j,Piece)]
        white_move_list, black_move_list = [j for i in piece_list for j in i.moves if i.color],[j for i in piece_list for j in i.moves if not i.color]
        return ((not white_move_list and not checks[0]),  (not black_move_list and not checks[1]))

    def move(self,piece,x:int,y:int,promote:str = None, ):
        
        if piece.color == self.move_count %2:
            return False

        if (x,y) not in piece.moves:
            return False
        
        tx,ty = piece.x,piece.y

        if "R" in piece.type:
            try:
                if tx ==0 : self.castling_rights[piece.color].remove("OOO")
                elif tx ==7:  self.castling_rights[piece.color].remove("OO")
            except:pass

        if "P" in piece.type:
            if y in (0,7):
                piece.type = promote

            if abs(ty-y) ==2:
                self.en_passant = True
                self.piece_being_bricked = piece

            if self.piece_being_bricked:
                if x == self.piece_being_bricked.x:
                    captured_list.append(self.piece_being_bricked)
                    piece_list.remove(self.piece_being_bricked)
                    self.board[self.piece_being_bricked.x][self.piece_being_bricked.y] = '.'
                
        if piece.type == "K":
            if abs(tx - x) == 2:
                if tx>x: #O-O-O
                    self.castle(piece,x,y,tx,ty,0)
                else: #O-O
                    self.castle(piece,x,y,tx,ty,7)
            self.castling_rights[piece.color].clear()
            return True

        result = self.get_piece(x,y)
        if result:
            captured_list.append(result)
            piece_list.remove(result)
        
        self.board[y][x] = piece
        piece.x,piece.y = x,y
        self.board[ty][tx] = '.'
        
        if __name__ == '__main__':
            self.print()

        if self.en_passant and "P" not in piece.type:
            self.en_passant = False

        self.move_count +=1

        update_all()

        return True
        
    def castle(self,piece,x:int,y:int,tx:int,ty:int,type:int): #type is 0 for long and 7 for short
        rook = self.board[type][y]
        k  = -1 if type else 1
        self.board[y][x] = piece
        self.board[y][tx+k]= rook
        self.board[ty][tx] = '.'
        self.board[y][type] = '.'
        piece.x = x
        rook.x = tx+k

    def print(self) -> None:
        print()
        for i in self.board:
            for j in i:
                print(j,end = '|')
            print()

A = Board()

class Piece:
    def __init__(self, t:str, x:int, y: int , color: int) -> None:
        self.type = t
        self.x,self.y = x,y
        self.color = color
        self.moves: list[tuple] = []    
        set_piece(x,y,self)
        piece_list.append(self)
        update(self)

    def __str__(self) -> str:
        return self.type if self.color else self.type.lower()

    def copy(self):
        return Piece(self.type,self.x,self.y,self.color)
    
    def get_pos(self):
        return (self.x,self.y)

    def print(self) -> None:
        print(self,self.get_pos())

GLOBAL_BOARD_VAR = A if __name__ == '__main__'  else None

valid = lambda x,y : x in range(8) and y in range(8)

def put_moves(piece:Piece, board :Board) -> list:

    moves = []

    def func(a,b,tx,ty):
            while (valid(tx,ty)):
                result = board.get_piece(tx,ty)
                if result:
                    if result.color != piece.color: 
                        moves.append((tx,ty))
                    if result != piece: break
                else:
                    moves.append((tx,ty))
                tx+=a
                ty+=b 

    def rook(): #done
        tx = piece.x
        ty = piece.y
        for z in [1,-1]:
            func(0,z,tx,ty) #down and up 
            func(z,0,tx,ty) #right and left        

    def bishop(): #done
        tx = piece.x
        ty = piece.y
        for z in [1,-1]:
            for v in [1,-1]:
                func(z,v,tx,ty) # bottom right, bottom left, top right, top left
                tx = piece.x
                ty = piece.y
    
    def knight():#done
        for z in [1,2,-1,-2]:
                for v in [1,-1] if abs(z) ==2 else [2,-2]:
                    tx,ty = piece.x+z,piece.y+v
                    if valid(tx,ty):
                        result = board.get_piece(tx,ty)
                        if not result or result.color != piece.color:  moves.append((tx,ty))
                        
    def pawn():#done
        z = -1 if piece.color else 1

        for i in [1,2]:
            tx,ty = piece.x+i*z,piece.y
            if valid(tx,ty):
                result = board.get_piece(tx,ty)
                if result:
                    break
                if i==1 or piece.x in (6,1): moves.append((tx,ty))

        for i in [-1,1]:
            tx,ty = piece.x+z,piece.y+i
            try:
                result = board.get_piece(tx,ty)
                if result.color != piece.color: moves.append((tx,ty))
            except: pass

    if 'R' in piece.type: rook()

    if "B" in piece.type: bishop()
         
    if "Q" in piece.type:
        rook()
        bishop()
    
    if 'N' in piece.type: knight()

    if "P" in piece.type: pawn()

    if "K" in piece.type:

        def func(tx,ty):
            if not valid(tx,ty):    return
            result = board.get_piece(tx,ty) 
            if not result: 
                moves.append((tx,ty))
                return
            if result.color != piece.color: moves.append((tx,ty)) 

        for i in [1,-1]:
            x,y = piece.x,piece.y
            func(x,y+i)
            func(x+i,y)
            func(x+i,y+i)
            func(x+i,y-i)

    moves = list(set(sorted(moves)))
    return moves 

def put_moves_special(piece:Piece,board:Board):
    #adds castling
    castle = board.castling_rights[piece.color]
    piece_list = [p for row in board.board for p in row if isinstance(p,Piece)]

    if piece.type == "K" and any(castle):

        def func(a:int,b:int,c:int = 0):
            for x in range(c,a):
                if ((x,y) in other_color_moves_list):  
                    break
                result = board.get_piece(x,y)
                if result:
                    if result.color == piece.color and result.type in "KR":
                        continue
                    break
            else:
                piece.moves.append((b,y))
                piece.moves.sort()

        y = 7 if piece.color else 0
        other_color_piece_list = [i for i in piece_list if i.color != piece.color]
        other_color_moves_list = [i.moves for i in other_color_piece_list]
        if 'OOO' in castle:
            func(a = 5,b = 2)
        if "OO" in castle:
            func(a = 8,b = 6, c = 4)
    
    if "P" in piece.type and board.en_passant:
        peace = board.piece_being_bricked
        z = 1 if peace.color else -1
        x,y = peace.x,peace.y+z
        if abs(piece.x-x) == 1 and piece.y == y: piece.moves.append((x,y))
    
def remove_illegal_moves(piece:Piece, board:Board):
        for move in piece.moves.copy():
            if would_be_check(board,piece,move[0],move[1]):
                piece.moves.remove(move) if move in piece.moves else None

def update_all():
    
    if not GLOBAL_BOARD_VAR:
        return 
    
    for i in piece_list:
        i.moves = put_moves(i,GLOBAL_BOARD_VAR)
    for i in piece_list:
        remove_illegal_moves(i,GLOBAL_BOARD_VAR)
    for i in piece_list:
        put_moves_special(i,GLOBAL_BOARD_VAR)

def update(i:Piece):
    
    if not GLOBAL_BOARD_VAR:
        return 
    
    i.moves = put_moves(i,GLOBAL_BOARD_VAR)
    remove_illegal_moves(i,GLOBAL_BOARD_VAR)
    put_moves_special(i,GLOBAL_BOARD_VAR)

def would_be_check(b:Board, piece:Piece, x:int,y:int):

    tx,ty = piece.x,piece.y
    old_piece = b.get_piece(x,y)
    if old_piece:
        if old_piece.color == piece.color : return True

    b.board[y][x] = piece
    b.board[ty][tx] = '.'
    pieces = [p for row in b.board for p in row if isinstance(p,Piece)]
    for i in pieces: i.moves = put_moves(i,b)
    white_pieces = [i for i in pieces if i.color]
    black_pieces = [i for i in pieces if not i.color]
    white_moves = [j for i in white_pieces for j in put_moves(i,b)]
    black_moves = [j for i in black_pieces for j in put_moves(i,b)]

    for i in pieces:
        if i.color == piece.color and i.type == "K":
            king = (i.x,i.y)

    FINAL = (black_moves if piece.color else white_moves)
    b.board[y][x] = old_piece
    b.board[ty][tx] = piece

    return (king in FINAL)

def set_piece(x,y,piece:Piece,board:Board=GLOBAL_BOARD_VAR):
    if board:
        board.board[y][x] = piece

piece_list :list[Piece] = [] 
captured_list :list[Piece] = []

if __name__ == "__main__":
    K1 = Piece("K",4,7,1)
    K1_ = Piece("K",4,0,0)

    R1 = Piece("R",0,7,1)
    R2 = Piece("R",7,7,1)
    R1_ = Piece("R",0,0,0)
    R2_ = Piece("R",7,0,0) 

    N1 = Piece("N",1,7,1)
    N2 = Piece("N",6,7,1)
    N1_ = Piece("N",1,0,0)
    N2_ = Piece("N",6,0,0)

    B1 = Piece("B",2,7,1)
    B2 = Piece("B",5,7,1)
    B1_ = Piece("B",2,0,0)
    B2_ = Piece("B",5,0,0)

    Q1 = Piece("Q",3,7,1)
    Q1_ = Piece("Q",3,0,0)

    P1 = Piece("P",0,6,1)
    P2 = Piece("P",1,6,1)
    P3 = Piece("P",2,6,1)
    P4 = Piece("P",3,6,1)
    P5 = Piece("P",4,6,1)
    P6 = Piece("P",5,6,1)
    P7 = Piece("P",6,6,1)
    P8 = Piece("P",7,6,1)

    P1_ = Piece("P",0,1,0)
    P2_ = Piece("P",1,1,0)
    P3_ = Piece("P",2,1,0)
    P4_ = Piece("P",3,1,0)
    P5_ = Piece("P",4,1,0)
    P6_ = Piece("P",5,1,0)
    P7_ = Piece("P",6,1,0)
    P8_ = Piece("P",7,1,0)
    update_all()
    GLOBAL_BOARD_VAR.print()
    while True:
        try:
            exec(input("Enter Command\t"))
        except Exception as e:
            print(e)