import os,fuckit as fr
from tkinter import *
import temp
# check put_moves_2 function
def valid(x,y):
    return (0<=x and x<=7 and y<=7 and y>=0) 

def update_all(board):
    for i in board.get_bl()+board.get_wl():
        i.put_moves_2(board)
        
def game_over(board ):
    if board.is_mate()[0]:
        return board.is_mate()
    elif  board.is_stalemate()[0]:
        return board.is_stalemate()
    else:
        return False

class bored:

    def __init__(self) -> None:
        self.b = [['.' for i in range(8)] for k in range(8)]
        self.move_count = 0
        self.whitelist,self.blacklist = {},{}#dict of pieces:piece.moves for white and black
        self.whitemoves, self.blackmoves = [],[] # list of all possible moves for white and black
        self.captured_w, self.captured_b = [],[]# list of captured white and black pieces
        self.wk,self.bk = (7,4),(0,4) #locations of white and black kings
        self.forced = 0 #en passant check
        self.forced_piece = '' #piece which is going to be en passanted
        self.forced_moves=[] # moves which the en passanter can make?
        self.matew,self.mateb=[],[]#list of king moves

    """DO NOT TOUCH ZONE"""
#----------------------------------------------------------------------------------------------------------------------------------
    
    def print(self): #prints the board in a readable format
        print()
        for i in self.b:
            for j in i:
                print(j,end=' | ')
            print()
        
    def is_piece(self,x,y): # returns True if piece at x,y 
        return  self.b[x][y] != '.' 
    
    def get_piece(self,x,y): # returns the piece at x,y
        return(self.b[x][y])
    
    def set_piece(self,piece,x,y):# puts piece at x,y
        self.b[x][y] = piece

    def get_wl(self): # returns the list of white pieces
        return list(self.whitelist.keys())
    
    def get_bl(self): # returns the list of black pieces
        return list(self.blacklist.keys())
    
    def is_check(self,piece): #returns true if check 
        return  (self.wk if piece.c else self.bk) in (self.blackmoves if piece.c else self.whitemoves) 
    
    def is_mate(self): # returns (True,color) if color has been mated
        if self.is_check(K1):   
            #print(self.whitemoves)
            return (not (len(self.whitemoves)), "BLACK WINS")
        elif self.is_check(K1_):
            #print(self.blackmoves)
            return (not (len(self.blackmoves)), "WHITE WINS")
        else:
            return (False, "NOT MATE")
        
    def move(self,piece,x,y,promote_to=0): # moves the piece to x,y

        self.forced = 0

        if piece.c != (self.move_count-1)%2: # checks which colors turn it is
            print("Not Your Turn")
            return
        
        if (x,y) not in piece.moves: # checks if the chosen square is in the piece's moves list
            print("Not in moves list")
            return 
        
        if self.is_piece(x,y): # if there is a piece at x,y then capture it
            self.capture(self.get_piece(x,y))
            

        if piece.piece == "P" and x in (0,7): # if the piece is a pawn and has reached to the end of the board, promote it to the chosen piece
            if not promote_to:
                piece.promote(input("Enter Piece To Promote To\t"))
            else:
                piece.promote(promote_to)
        
        if piece.piece =="P" and abs(piece.x-x) == 2: # if en passant has been enabled
            self.forced = 1

        if (x,y) in self.forced_moves:   #checks if x,y is in the en passant moves list
            self.capture(self.forced_piece)
            self.forced_piece=''
            self.forced_moves=[]

        self.set_piece('.',piece.x,piece.y) 
        self.set_piece(piece,x,y) 

        if piece.piece == "K": # if piece is a king, update king position variable
            if piece.c:
                self.wk = (x,y)
            else: self.bk = (x,y)
        
        self.move_count+=1
        piece.x = x
        piece.y = y
        self.forced_piece = piece
        
        update_all(self)

        #if __name__ == '__main__':
        #self.print()
    
    def capture(self,piece):    #adds captured piece to board's list of captured pieces and replaces original 
        self.captured_w.append(piece) if piece.c else self.captured_b.append(piece)
        if piece.c:
            del self.whitelist[piece] 
        else: 
            del self.blacklist[piece]

    def total_move_updater(self,piece): # updates the whitemoves and blackmoves list to reflect the current board 
        if piece.c:
            self.whitemoves = []
            for i in self.whitelist.values():
                for j in i: self.whitemoves.append(j)
        else:
            self.blackmoves = []
            for i in self.blacklist.values():
                for j in i: self.blackmoves.append(j)

    def would_be_check(self,piece,x,y,not_ = 1): # returns True if the move would cause a check, False if not. 
        king = self.wk if piece.c else self.bk #If not_1 = False, then the function changes to a would_block_check function, returning True if the move would stop check
            
        if (x,y) not in piece.moves:
            return 
        
        whit,blac = [],[]
        tb = [['.' for i in range(8)] for k in range(8)]
        
        for i in range(8):
            for j in range(8):
                tb[i][j] = (self.get_piece(i,j)).copy() if self.is_piece(i,j) else '.'
                tb[i][j] = (self.get_piece(i,j)).copy() if self.is_piece(i,j) else '.'
        tb[piece.x][piece.y] = '.'
        tb[x][y] = piece.copy()
        tb[x][y][0] =x
        tb[x][y][1] = y

        for i in tb:
            for j in i:
                if j!='.':
                    whit.append(temp.classify(j,tb)) if j[2] else None
                    blac.append(temp.classify(j,tb)) if not j[2] else None
        whiter,blacker = [],[] #list of squares in sight of white, list of squares in sight of black
        for i in whit:
            for j in i:
                whiter.append(j)
        for i in blac:
            for j in i:
                blacker.append(j)
        if piece.piece == "K":
            king = (x,y)
        return  (king in (blacker if piece.c else whiter)) if not_ else not (king in (blacker if piece.c else whiter))
    
    def is_stalemate(self): #returns (True,Color) if stalemate
        if not self.is_check(K1) and not len(self.whitemoves):
            return (True,"STALEMATE, GAME DRAWN (WHITE STALEMATE)")
        elif not self.is_check(K1_) and not len(self.blackmoves):
            return(True,"STALEMATE, GAME DRAWN (BLACK STALEMATE)")
        else:
            return (False,"NOT STALEMATE")
#----------------------------------------------------------------------------------------------------------------------------------

class piece:
    
    def __init__(self, piece,x,y,color,board):
        self.piece = piece
        self.x = x
        self.y = y
        board.set_piece(self,x,y)
        self.moves = []
        self.c = color
        self.put_moves_2(board)
        #self.k = (7,4) if self.c else (0,4)

    """ DO NOT TOUCH ZONE"""
#----------------------------------------------------------------------------------------------------------------------------------

    def promote(self,a): 
        self.piece = a

    def put_moves(self,board): #adds moves, without checking for legality
        self.moves = []

        def rook(): #fixed
            tx = self.x
            ty = self.y
            
            for z in [1,-1]:
                while (valid(tx,ty)): # downwards then upwards

                    if not board.is_piece(tx,ty): 
                        self.moves.append((tx,ty))
                    else:
                        if board.get_piece(tx,ty) != self:                            
                            if board.get_piece(tx,ty).c == self.c:
                                break
                            else:
                                self.moves.append((tx,ty))
                                break
                    tx+=z
                tx = self.x

                while (valid(tx,ty)): # left then right
                    if not board.is_piece(tx,ty): 
                        self.moves.append((tx,ty))
                    else:
                        if board.get_piece(tx,ty) != self:                            
                            if board.get_piece(tx,ty).c == self.c:
                                break
                            else:
                                self.moves.append((tx,ty))
                                break
                    ty+=z
                ty = self.y
                
        def bishop(): #fixed
            tx = self.x
            ty = self.y
            for z in [1,-1]:
                for v in [1,-1]:
                    while(valid(tx,ty)):
                        if not board.is_piece(tx,ty):
                            self.moves.append((tx,ty))
                        else:
                            if board.get_piece(tx,ty) != self:                            
                                if board.get_piece(tx,ty).c == self.c:
                                    break
                                else:
                                    self.moves.append((tx,ty))
                                    break
                        tx+=z
                        ty+=v
                    tx = self.x
                    ty = self.y
        
        def knight():#fixed
            for z in [1,2,-1,-2]:
                    for v in [1,-1] if abs(z) ==2 else [2,-2]:
                        if valid(self.x+z,self.y+v):
                            self.moves.append((self.x+z,self.y+v)) if not board.is_piece(self.x+z,self.y+v) or self.c != board.get_piece(self.x+z,self.y+v).c else None

        def pawn():# fixed
            z = -1 if self.c else 1
            if valid(self.x+z,self.y):
                self.moves.append((self.x+z,self.y)) if not board.is_piece(self.x+z,self.y) else None
                for v in [1,-1]:
                    if valid(self.x+z,self.y+v) and board.is_piece(self.x+z,self.y+v):
                        self.moves.append((self.x+z,self.y+v)) if board.get_piece(self.x+z,self.y+v).c != self.c else None
            k=z*2
            if (valid(self.x+k,self.y)) and self.x == 6 if self.c else self.x == 1:
                if not board.is_piece(self.x+k,self.y) and not board.is_piece(self.x+z,self.y):
                    self.moves.append((self.x+k,self.y))
            
        if 'R' in self.piece:
            rook()

        if  "B" in self.piece:
            bishop()
            
        if "Q" in self.piece:
            rook()
            bishop()
        
        if 'N' in self.piece:
            knight()

        if "P" in self.piece:
            pawn()

        if "K" == self.piece:
            if self.c:board.wk = self.get_loc() 
            else: board.bk = self.get_loc()
            for i in [1,-1]:
                x = self.x
                y = self.y

                def chong(x,y):
                    if valid(x,y): 
                        if board.is_piece(x,y):
                            if board.get_piece(x,y).c != self.c:
                                self.moves.append((x,y))
                        else:
                            self.moves.append((x,y))

                chong(x,y+i)
                chong(x+i,y)
                chong(x+i,y+i)
                chong(x+i,y-i)

        self.moves.sort()

    def get_moves(self,board):
        self.put_moves_2(board)
        return self.moves
    
    def get_color(self):
        return self.c
    
    def get_loc(self):
        return((self.x,self.y))
    
    def __str__(self) -> str:
        return(self.piece if self.c else self.piece.lower())

    def copy(self):
        return [self.x,self.y,self.c,self.piece]

    def get_image(self):
        return self.piece if self.c else self.piece+'_'
    
#----------------------------------------------------------------------------------------------------------------------------------

    def put_moves_2(self,board):
        self.put_moves(board) #all moves possible have been put, even illegal moves

        for i in self.moves.copy(): #removes all moves which would cause a check to occur
            if board.would_be_check(self,i[0],i[1]):
                self.moves.remove(i)

        if self.piece == "P" and board.forced: # adds en passant to pawn moves
            x = board.forced_piece.copy()[0]
            y = board.forced_piece.copy()[1]
            if self.c != board.forced_piece.copy()[2] and abs(self.y-y) ==1 and self.x == x:
                k = self.y - y
                if (valid(self.x-1,self.y-k) if self.c else valid(self.x+1,self.y-k)):
                    self.moves.append((self.x-1,self.y-k)) if self.c else self.moves.append((self.x+1,self.y-k))
                    board.forced_moves.append((self.x-1,self.y-k)) if self.c else board.forced_moves.append((self.x+1,self.y-k)) 
        
        if board.is_check(self): # removes all moves which dont block check if there is a check
            for i in self.moves.copy():
                if not board.would_be_check(self,i[0],i[1],0): # if not would block check
                    self.moves.remove(i)
  
        if self.piece == "K": #updates the list of king moves possible
            if self.c:
                board.matew = self.moves
            else:
                board.mateb = self.moves

        self.moves.sort() # final list of moves after everything needed has been adjusted

        if self.c: # adds or updates the list of white and black pieces in the board class and correctly sets their moves
            board.whitelist[self] = self.moves
        else:
            board.blacklist[self] = self.moves
        
        board.total_move_updater(self) #updates all possible moves for white and black after the piece's moves have been set


def create_pieces():# this function is obsolete
    global B, B_, EMPTY,K, K_, N, N_, P, P_, Q, Q_, R, R_,KNOOK
    cwd = os.getcwd()
    EMPTY = PhotoImage(file=rf"{cwd}\sprites\empty.png")
    B = PhotoImage(file=rf"{cwd}\sprites\B.png")
    B_ = PhotoImage(file=rf"{cwd}\sprites\b_.png") 
    K = PhotoImage(file=rf"{cwd}\sprites\K.png")
    K_ = PhotoImage(file=rf"{cwd}\sprites\k_.png")
    N = PhotoImage(file=rf"{cwd}\sprites\N.png")
    N_ = PhotoImage(file=rf"{cwd}\sprites\N_.png")
    P = PhotoImage(file=rf"{cwd}\sprites\P.png")
    P_ = PhotoImage(file=rf"{cwd}\sprites\p_.png")
    Q = PhotoImage(file=rf"{cwd}\sprites\Q.png")
    Q_ = PhotoImage(file=rf"{cwd}\sprites\q_.png")
    R = PhotoImage(file=rf"{cwd}\sprites\R.png")
    R_ = PhotoImage(file=rf"{cwd}\sprites\r_.png")
    KNOOK = PhotoImage(file=rf"{cwd}\sprites\knook.png")

def choose_piece(p):
    create_pieces()
    #exec(f'return({p.upper()})')
    if p == "B": return B
    elif p == "b_": return B_
    elif p == "K": return K
    elif p == "k_": return K_
    elif p == "N": return N
    elif p == "n_": return N_
    elif p == "P": return P
    elif p == "p_": return P_
    elif p == "Q": return Q
    elif p == "q_": return Q_
    elif p == "R": return R
    elif p == "r_": return R_
    elif p== "KNOOK": return KNOOK
    else: return EMPTY

b = bored()

K1 = piece("K",7,4,1,b)
K1_ = piece("K",0,4,0,b)

R1 = piece("R",7,0,1,b)
R2 = piece("R",7,7,1,b)
R1_ = piece("R",0,0,0,b)
R2_ = piece("R",0,7,0,b) 


N1 = piece("N",7,1,1,b)
N2 = piece("N",7,6,1,b)
N1_ = piece("N",0,1,0,b)
N2_ = piece("N",0,6,0,b)

B1 = piece("B",7,2,1,b)
B2 = piece("B",7,5,1,b)
B1_ = piece("B",0,2,0,b)
B2_ = piece("B",0,5,0,b)

Q1 = piece("Q",7,3,1,b)
Q1_ = piece("Q",0,3,0,b)

P1 = piece("P",6,0,1,b)
P2 = piece("P",6,1,1,b)
P3 = piece("P",6,2,1,b)
P4 = piece("P",6,3,1,b)
P5 = piece("P",6,4,1,b)
P6 = piece("P",6,5,1,b)
P7 = piece("P",6,6,1,b)
P8 = piece("P",6,7,1,b)

P1_ = piece("P",1,0,0,b)
P2_ = piece("P",1,1,0,b)
P3_ = piece("P",1,2,0,b)
P4_ = piece("P",1,3,0,b)
P5_ = piece("P",1,4,0,b)
P6_ = piece("P",1,5,0,b)
P7_ = piece("P",1,6,0,b)
P8_ = piece("P",1,7,0,b)


update_all(b)

if __name__ =='__main__':
    b.print()
    while not game_over(b):
            with fr:
                exec(input("Enter Command\t"))
            #print(K.moves)
    else:
        print(game_over(b))
