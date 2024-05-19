import os
from tkinter import *
import temp

def valid(x,y):
    return (0<=x and x<=7 and y<=7 and y>=0) 

def update_all(board):
    for i in board.get_bl()+board.get_wl():
        i.put_moves_2(board)
        board.add_moves(i,i.c)

class bored:

    def __init__(self) -> None:
        self.b = [['.' for i in range(8)] for k in range(8)]
        self.move_count = 0
        self.whitelist,self.blacklist = [],[]
        self.whitemoves, self.blackmoves = [],[]
        self.captured_w, self.captured_b = [],[]
        self.wk,self.bk = (7,4),(0,4)
        self.forced = 0
        self.forced_piece = ''
        self.forced_moves=[]
        self.matew,self.mateb=[],[]

    def is_mate(self):
        return (not (len(self.matew) and len(self.mateb)), ("WHITE" if len(self.matew) else "BLACK"))

    def set_piece(self,piece,x,y):
        self.b[x][y] = piece

    def clear_square(self,x,y):
        self.b[x][y] = '.'

    def print(self):
        print()
        for i in self.b:
            for j in i:
                print(j,end=' | ')
            print()

    def get_piece(self,x,y):
        return(self.b[x][y])
    
    def is_piece(self,x,y):
        return False if self.b[x][y] == '.' else True

    def wlbl(self, a, c,d=1):
        if d:   self.whitelist.extend(a) if c else self.blacklist.extend(a)
        else:
            if c:
                self.whitelist = a
            else:
                self.blacklist = a
    
    def get_wl(self):
        return self.whitelist
    
    def get_bl(self):
        return self.blacklist
    
    def capture(self,piece):
        print(piece)
        self.captured_w.append(piece) if piece.c else self.captured_b.append(piece)
        whitelist.remove(piece) if piece.c else blacklist.remove(piece)
        self.whitelist.remove(piece) if piece.c else self.blacklist.remove(piece)
        self.clear_square(piece.x,piece.y)

    def get_move_count(self):
        return self.move_count
    
    def __str__(self):
        return(self.b)
    
    def add_moves(self,i,c):
        self.whitemoves.extend(i.moves) if c else self.blackmoves.extend(i.moves)
        self.whitemoves.sort() if c else self.blackmoves.sort()

    def get_moves(self,c):
        return self.whitemoves if c else self.blackmoves
    
    def is_check(self,piece):
        return  (self.wk if piece.c else self.bk) in (self.blackmoves if piece.c else self.whitemoves) 
    
    def would_be_check(self,piece,x,y):
        king = self.wk if piece.c else self.bk
            
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
        return (king in (blacker if piece.c else whiter))

    def move(self,piece,x,y):

        self.forced = 0

        if piece.c != (self.move_count-1)%2:
            print("Not Your Turn")
            return
        
        if (x,y) not in piece.moves:
            print("Not in moves list")
            return 
        
        if self.is_piece(x,y):
            self.capture(self.get_piece(x,y))
            

        if piece.piece == "P" and x in (0,7):
            piece.promote(input("Enter Piece To Promote To\t"))
        
        if piece.piece =="P" and abs(piece.x-x) == 2:
            self.forced = 1

        if (x,y) in self.forced_moves:
            self.capture(self.forced_piece)
            self.forced_piece=''
            self.forced_moves=[]

        self.clear_square(piece.x,piece.y)
        self.set_piece(piece,x,y)

        if piece.piece == "K":
            if piece.c:
                self.wk = (x,y)
            else: self.bk = (x,y)
        
        self.move_count+=1
        piece.x = x
        piece.y = y
        self.forced_piece = piece
        
        update_all(self)

        if __name__ == '__main__':
            self.print()

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

    def put_moves(self,board):
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
                self.moves.append((self.x,self.y+i)) if valid(self.x,self.y+i) and not board.is_piece(self.x,self.y+i) else None #right and left
                self.moves.append((self.x+i,self.y)) if valid(self.x+i,self.y) and not board.is_piece(self.x+i,self.y) else None #top and bottom
                self.moves.append((self.x+i,self.y+i)) if valid(self.x+i,self.y+i) and not board.is_piece(self.x+i,self.y+i) else None # top-right and bottom left
                self.moves.append((self.x+i,self.y-i)) if valid(self.x+i,self.y-i) and not board.is_piece(self.x+i,self.y-i) else None # top-left and bottom right

        self.moves.sort()
        
    def put_moves_2(self,board):
        self.put_moves(board)
        f = self.moves.copy()

        for i in f:
            if board.would_be_check(self,i[0],i[1]):
                self.moves.remove(i)

        if board.is_check(self) and self.piece != "K":
            #print("Check",self.c)
            self.moves=[]
            #print(self.moves)

        if self.piece == "P" and board.forced:
            x = board.forced_piece.copy()[0]
            y = board.forced_piece.copy()[1]
            
            if self.c != board.forced_piece.copy()[2] and abs(self.y-y) ==1 and self.x == x:
                k = self.y - y

                if (valid(self.x-1,self.y-k) if self.c else valid(self.x+1,self.y-k)):
                    self.moves.append((self.x-1,self.y-k)) if self.c else self.moves.append((self.x+1,self.y-k))
                    board.forced_moves.append((self.x-1,self.y-k)) if self.c else board.forced_moves.append((self.x+1,self.y-k)) 
        
        if self.piece == "K":
            if self.c:
                board.matew = self.moves
            else:
                board.mateb = self.moves

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
        return self.piece if self.c else self.piece.lower()+'_'
        
def create_pieces():# this function is obsolete
    global B, BN, BN_, BP, BP_, BQ, BQ_, BR, BR_, B_, EMPTY,K, K_, N, NB, NB_, NP, NP_, NQ, NQ_, NR, NR_, N_, P, PB, PB_, PN, PN_, PQ, PQ_, PR, PR_, P_, Q, QB, QB_, QN, QN_, QP, QP_, QR, QR_, Q_, R, RB, RB_, RN, RN_, RP, RP_, RQ, RQ_, R_,KNOOK
    cwd = os.getcwd()
    EMPTY = PhotoImage(file=rf"{cwd}\sprites\empty.png")
    B = PhotoImage(file=rf"{cwd}\sprites\B.png")
    BN = PhotoImage(file=rf"{cwd}\sprites\BN.png")
    BP = PhotoImage(file=rf"{cwd}\sprites\BP.png")
    BQ = PhotoImage(file=rf"{cwd}\sprites\BQ.png")
    BR = PhotoImage(file=rf"{cwd}\sprites\BR.png")
    B_ = PhotoImage(file=rf"{cwd}\sprites\b_.png")
    BN_ = PhotoImage(file=rf"{cwd}\sprites\BN_.png")
    BP_ = PhotoImage(file=rf"{cwd}\sprites\bp_.png")
    BQ_ = PhotoImage(file=rf"{cwd}\sprites\bq_.png")
    BR_ = PhotoImage(file=rf"{cwd}\sprites\br_.png")    
    K = PhotoImage(file=rf"{cwd}\sprites\K.png")
    K_ = PhotoImage(file=rf"{cwd}\sprites\k_.png")
    N = PhotoImage(file=rf"{cwd}\sprites\N.png")
    NB = PhotoImage(file=rf"{cwd}\sprites\NB.png")
    NB_ = PhotoImage(file=rf"{cwd}\sprites\Nb_.png")
    NP = PhotoImage(file=rf"{cwd}\sprites\NP.png")
    NP_ = PhotoImage(file=rf"{cwd}\sprites\Np_.png")
    NQ = PhotoImage(file=rf"{cwd}\sprites\NQ.png")
    NQ_ = PhotoImage(file=rf"{cwd}\sprites\Nq_.png")
    NR = PhotoImage(file=rf"{cwd}\sprites\NR.png")
    NR_ = PhotoImage(file=rf"{cwd}\sprites\Nr_.png")
    N_ = PhotoImage(file=rf"{cwd}\sprites\N_.png")
    P = PhotoImage(file=rf"{cwd}\sprites\P.png")
    PB = PhotoImage(file=rf"{cwd}\sprites\PB.png")
    PB_ = PhotoImage(file=rf"{cwd}\sprites\pb_.png")
    PN = PhotoImage(file=rf"{cwd}\sprites\PN.png")
    PN_ = PhotoImage(file=rf"{cwd}\sprites\pN_.png")
    PQ = PhotoImage(file=rf"{cwd}\sprites\PQ.png")
    PQ_ = PhotoImage(file=rf"{cwd}\sprites\pq_.png")
    PR = PhotoImage(file=rf"{cwd}\sprites\PR.png")
    PR_ = PhotoImage(file=rf"{cwd}\sprites\pr_.png")
    P_ = PhotoImage(file=rf"{cwd}\sprites\p_.png")
    Q = PhotoImage(file=rf"{cwd}\sprites\Q.png")
    QB = PhotoImage(file=rf"{cwd}\sprites\QB.png")
    QB_ = PhotoImage(file=rf"{cwd}\sprites\qb_.png")
    QN = PhotoImage(file=rf"{cwd}\sprites\QN.png")
    QN_ = PhotoImage(file=rf"{cwd}\sprites\qN_.png")
    QP = PhotoImage(file=rf"{cwd}\sprites\QP.png")
    QP_ = PhotoImage(file=rf"{cwd}\sprites\qp_.png")
    QR = PhotoImage(file=rf"{cwd}\sprites\QR.png")
    QR_ = PhotoImage(file=rf"{cwd}\sprites\qr_.png")
    Q_ = PhotoImage(file=rf"{cwd}\sprites\q_.png")
    R = PhotoImage(file=rf"{cwd}\sprites\R.png")
    RB = PhotoImage(file=rf"{cwd}\sprites\RB.png")
    RB_ = PhotoImage(file=rf"{cwd}\sprites\rb_.png")
    RN = PhotoImage(file=rf"{cwd}\sprites\RN.png")
    RN_ = PhotoImage(file=rf"{cwd}\sprites\rN_.png")
    RP = PhotoImage(file=rf"{cwd}\sprites\RP.png")
    RP_ = PhotoImage(file=rf"{cwd}\sprites\rp_.png")
    RQ = PhotoImage(file=rf"{cwd}\sprites\RQ.png")
    RQ_ = PhotoImage(file=rf"{cwd}\sprites\rq_.png")
    R_ = PhotoImage(file=rf"{cwd}\sprites\r_.png")
    KNOOK = PhotoImage(file=rf"{cwd}\sprites\knook.png")

def choose_piece(p):
    create_pieces()
    if p == "B": return B
    elif p == "BN": return BN
    elif p == "bn_": return BN_
    elif p == "BP": return BP
    elif p == "bp_": return BP_
    elif p == "BQ": return BQ
    elif p == "bq_": return BQ_
    elif p == "BR": return BR
    elif p == "br_": return BR_
    elif p == "b_": return B_
    elif p == "K": return K
    elif p == "k_": return K_
    elif p == "N": return N
    elif p == "NB": return NB
    elif p == "nb_": return NB_
    elif p == "NP": return NP
    elif p == "np_": return NP_
    elif p == "NQ": return NQ
    elif p == "nq_": return NQ_
    elif p == "NR": return NR
    elif p == "nr_": return NR_
    elif p == "n_": return N_
    elif p == "P": return P
    elif p == "PB": return PB
    elif p == "pb_": return PB_
    elif p == "PN": return PN
    elif p == "pn_": return PN_
    elif p == "PQ": return PQ
    elif p == "pq_": return PQ_
    elif p == "PR": return PR
    elif p == "pr_": return PR_
    elif p == "p_": return P_
    elif p == "Q": return Q
    elif p == "QB": return QB
    elif p == "qb_": return QB_
    elif p == "QN": return QN
    elif p == "qn_": return QN_
    elif p == "QP": return QP
    elif p == "qp_": return QP_
    elif p == "QR": return QR
    elif p == "qr_": return QR_
    elif p == "q_": return Q_
    elif p == "R": return R
    elif p == "RB": return RB
    elif p == "rb_": return RB_
    elif p == "RN": return RN
    elif p == "rn_": return RN_
    elif p == "RP": return RP
    elif p == "rp_": return RP_
    elif p == "RQ": return RQ
    elif p == "rq_": return RQ_
    elif p == "r_": return R_
    elif p== "KNOOK": return KNOOK
    else: return EMPTY

b = bored()

K = piece("K",7,4,1,b)
K_ = piece("K",0,4,0,b)

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

Q = piece("Q",7,3,1,b)
Q_ = piece("Q",0,3,0,b)

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

whitelist = [R1,R2,B1,B2,Q,K,N1,N2,K,P1,P2,P3,P4,P5,P6,P7,P8]
blacklist = [R1_,R2_,B1_,B2_,N1_,N2_,Q_,K_,P1_,P2_,P3_,P4_,P5_,P6_,P7_,P8_]
b.wlbl(whitelist,1)
b.wlbl(blacklist,0)
update_all(b)

if __name__ =='__main__':
    b.print()
    while True:
        if b.is_mate() and b.move_count>2:
            print("CHECKMATE")
            break
        else:
            exec(input("Enter Command\t").strip())
            #print(K.moves)