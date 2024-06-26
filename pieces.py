import os,fuckit as fr
from tkinter import *
import copy

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

def new_start(board,piece,x,y):
    if piece.piece == "K":
        king = (x,y)
    else:
        king  = board.wk if piece.c else board.bk
    ox,oy = piece.x,piece.y
    board.b[ox][oy] = '.'
    board.b[x][y] = piece
    c = piece.c
    piecelist =[]
    for i in board.b:
        for j in i:
            if j!='.':
                if j.c!= c: piecelist.append(j)
    movelist = []
    for i in piecelist:
        for j in i.put_moves(board):
            movelist.append(j)
    return king in movelist

class bored:

    def __init__(self, ini = [['.' for i in range(8)] for k in range(8)], mc =0,wm=[],bm=[],cw=[],cb=[],wk=(7,4),bk=(0,4),f=0,fp='',fm=[],mb=[],mw=[],ccb=False,ccw=False) -> None:
        self.b = ini
        self.move_count = mc
        self.whitelist,self.blacklist = {},{}#dict of pieces:piece.moves for white and black
        self.whitemoves, self.blackmoves = wm,bm # list of all possible moves for white and black
        self.captured_w, self.captured_b = cw,cb# list of captured white and black pieces
        self.wk,self.bk = wk,bk #locations of white and black kings
        self.forced = f #en passant check
        self.forced_piece = fp #piece which is going to be en passanted
        self.forced_moves= fm # moves which the en passanter can make?
        self.matew,self.mateb= mw,mb#list of king moves
        self.ccb,self.ccw = ccb,ccw

    def copy(self): #returns a deepcopy of itself
        return copy.deepcopy(self)
    
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
    
    def can_castle(self,piece):

        lcp,scp = True,True
        k,r1,r2 = ((7,4),(7,0),(7,7)) if piece.c else ((0,4),(0,0),(0,7))

        if self.wk != (7,4) if piece.c else self.bk != (0,4): #king hasnt moved
            return False
        
        row = [(7,i) for i in range(8) if i not in (0,4,7)] if piece.c else [(0,i) for i in range(8) if i not in (0,4,7)] 

        for i,j in row: 
            if self.is_piece(i,j):# both pieces see eachother 
                if row.index((i,j))>2: scp = False
                else: lcp = False
            if i in (self.blacklist if piece.c else self.whitelist): #no black piece stops castling
                if row.index((i,j))>2: scp = False
                else: lcp = False

        if self.is_piece(r2[0],r2[1]):
            scp = False if self.get_piece(r2[0],r2[1]).copy()[-1] not in ("R") else scp #rooks havent moved
        if self.is_piece(r1[0],r1[1]):
            lcp = False if self.get_piece(r1[0],r1[1]).copy()[-1] not in ("R") else lcp

        return [scp,lcp]
    
    def is_mate(self): # returns (True,color) if color has been mated
        if self.is_check(K1):   
            #print(self.whitemoves)
            return (not (len(self.whitemoves)), "BLACK WINS")
        elif self.is_check(K1_):
            #print(self.blackmoves)
            return (not (len(self.blackmoves)), "WHITE WINS")
        else:
            return (False, "NOT MATE")
    
    def castle(self,piece,x,y):
        self.b[x][y] = piece # moves the king
        
        if y == 6: #moves the rook
            roook = self.get_piece(x,7)
            roook.x = x
            roook.y = y-1
            print(roook.copy())
            self.b[x][y-1] = self.b[x][7]
            self.b[x][7] = '.'
        else:
            roook = self.get_piece(x,0)
            roook.x = x
            roook.y = y+1
            self.b[x][y+1] = self.b[x][0]
            self.b[x][0] = '.'

        self.b[piece.x][piece.y] = "."
        if piece.c:
            self.wk = (x,y)
        else: self.bk = (x,y)

        self.move_count+=1
        piece.x = x
        piece.y = y
        self.forced_piece = piece
        
        update_all(self)
        
    def move(self,piece,x,y,promote_to=0): # moves the piece to x,y

        self.forced = 0

        if piece.c != (self.move_count-1)%2: # checks which colors turn it is
            return ("Not Your Turn")
        
        if (x,y) not in piece.moves: # checks if the chosen square is in the piece's moves list
            return ("Not in moves list")
        
        if piece.piece == "K" and abs(piece.y - y) == 2:
                self.castle(piece,x,y)
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

    def would_be_check(self,piece,x,y): # returns True if the move would cause a check, False if not. 
        return new_start(self.copy(),piece,x,y)
    
    def is_stalemate(self): #returns (True,Color) if stalemate
        if not self.is_check(K1) and not len(self.whitemoves):
            return (True,"STALEMATE, GAME DRAWN (WHITE STALEMATE)")
        elif not self.is_check(K1_) and not len(self.blackmoves):
            return(True,"STALEMATE, GAME DRAWN (BLACK STALEMATE)")
        else:
            return (False,"NOT STALEMATE")

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

    def promote(self,a): 
        self.piece = a

    def put_moves(self,board): #adds moves, without checking for legality
        self.moves = []

        def rook(): #fixed
            tx = self.x
            ty = self.y
            
            def func(a,b,tx,ty):
                while (valid(tx,ty)): 

                    if not board.is_piece(tx,ty): 
                        self.moves.append((tx,ty))
                    else:
                        if board.get_piece(tx,ty) != self:                            
                            if board.get_piece(tx,ty).c == self.c:
                                break
                            else:
                                self.moves.append((tx,ty))
                                break
                    tx+=a
                    ty+=b 

            for z in [1,-1]:
                func(z,0,tx,ty) #down and up 
                func(0,z,tx,ty) #right and left

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

        return self.moves

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
        
        if self.piece == "K": #updates the list of king moves possible and castling rights
            if self.c:
                board.matew = self.moves
            else:
                board.mateb = self.moves

            a = board.can_castle(self)
            sc = a[0] if a else False
            lc = a[1] if a else False

            if self.c:
                if sc: self.moves.append((7,6))
                if lc: self.moves.append((7,2))
            else:
                if sc: self.moves.append((0,6))
                if lc: self.moves.append((0,2))

        self.moves.sort() # final list of moves after everything needed has been adjusted

        if self.c: # adds or updates the list of white and black pieces in the board class and correctly sets their moves
            board.whitelist[self] = self.moves
        else:
            board.blacklist[self] = self.moves
        
        board.total_move_updater(self) #updates all possible moves for white and black after the piece's moves have been set

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
