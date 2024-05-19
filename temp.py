def valid(x,y):
    return (0<=x and x<=7 and y<=7 and y>=0) 
def classify(p,b):
    moves = []
    if 'R' in p:
        moves.extend(rook(p,b))
    if  "B" in p:
        moves.extend(bishop(p,b))
        
    if "Q" in p:
        moves.extend(rook(p,b))
        moves.extend(bishop(p,b))
    
    if 'N' in p:
        moves.extend(knight(p,b))

    if "P" in p:
        moves.extend(pawn(p,b))

    return moves

def rook(piece,board): #fixed
    moves = []
    tx = piece[0]
    ty = piece[1]
    for z in [1,-1]:
        while (valid(tx,ty)): # downwards then upwards
            if board[tx][ty] == '.': 
                moves.append((tx,ty))
            else:
                if board[tx][ty] != piece:                            
                    if board[tx][ty][2] == piece[2]:
                        break
                    else:
                        moves.append((tx,ty))
                        break
            tx+=z
        tx = piece[0]

        while (valid(tx,ty)): # left then right
            if  board[tx][ty] == '.': 
                moves.append((tx,ty))
            else:
                if board[tx][ty] != piece:          
                    if board[tx][ty][2]== piece[2]:
                        break
                    else:
                        moves.append((tx,ty))
                        break
            ty+=z
        ty = piece[1]
        #print(moves)
    return (sorted(moves))
def bishop(piece,board): #fixed
    moves =[]
    tx = piece[0]
    ty = piece[1]
    for z in [1,-1]:
        for v in [1,-1]:
            while(valid(tx,ty)):
                if  board[tx][ty] == '.':
                    moves.append((tx,ty))
                else:
                    if board[tx][ty] != piece:                            
                        if board[tx][ty][3] == piece[3]:
                            break
                        else:
                            moves.append((tx,ty))
                            break
                tx+=z
                ty+=v
            tx = piece[0]
            ty = piece[1]
    return moves

def knight(piece,board):#fixed
    moves = []
    for z in [1,2,-1,-2]:
            for v in [1,-1] if abs(z) ==2 else [2,-2]:
                if valid(piece[0]+z,piece[1]+v):
                    moves.append((piece[0]+z,piece[1]+v)) if  board[piece[0]+z][piece[1]+v] == '.' or piece[2] != board[piece[0]+z][piece[1]+v][2] else None

    return moves

def pawn(piece,board):# fixed
    moves = []
    z = -1 if piece[3] else 1
    if valid(piece[0]+z,piece[1]):
        moves.append((piece[0]+z,piece[1])) if  board[piece[0]+z][piece[1]] =='.' else None
        for v in [1,-1]:
            if valid(piece[0]+z,piece[1]+v) and not board[piece[0]+z][piece[1]+v]=='.':
                moves.append((piece[0]+z,piece[1]+v)) if board[piece[0]+z][piece[1]+v][2] != piece[2] else None
    k=z*2
    if (valid(piece[0]+k,piece[1])) and piece[0] == 6 if piece[2] else piece[0] == 1:
        if  board[piece[0]+k][piece[1]] == '.' and  board[piece[0]+z][piece[1]] =='.':
            moves.append((piece[0]+k,piece[1]))

    return moves