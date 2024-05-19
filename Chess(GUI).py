from tkinter import *
from tkinter import messagebox
from pieces import bored,piece,update_all,choose_piece


window = Tk()
window.configure(bg='black')
window.wm_attributes('-transparentcolor', 'forest green')

o = lambda a:a/1536
p = lambda a:a/888
fr = lambda a: (f'{a}')
fonts = lambda a:("Inter ExtraBold", a * -1,'bold')

chosen_piece = ''
piece_chosen = False

def construct():
    for i in range(8):
        for j in range(8):
            btn= Button(window,font=("Inter ExtraBold", 20 * -1,"bold"),)
            btn.configure(bg="saddle brown") if (i+j)%2 else btn.configure(bg="bisque")
            if b.is_piece(i,j):
                knook =  choose_piece(b.get_piece(i,j).get_image())
                btn.configure(image =knook,command= lambda x=i,y=j:move_color(x,y))
                btn.image = knook
            else:
                btn.configure(command= lambda x=i,y=j:empty_sqaure(x,y))
            btn.place(relx=o(j*107+350),rely=p(i*107),width=110,height=110)
            grid[i][j] = btn
    Button(window,image=choose_piece("KNOOK"),command= lambda: window.destroy()).place(relx=o(1470),rely=p(0))

def reset_color():
    for i in range(8):
        for j in range(8):
            grid[i][j].configure(bg="saddle brown") if (i+j)%2 else grid[i][j].configure(bg="bisque")

def empty_sqaure(x=0,y=0):
    global piece_chosen,chosen_piece
    if piece_chosen:
        if (x,y) in chosen_piece.moves:
            b.move(chosen_piece,x,y)
            piece_chosen=''
            chosen_piece = False
            construct()
            if b.is_mate()[0] and b.move_count>2:
                messagebox.showinfo("CHECKMATE", f"CHECKMATE. {b.is_mate()[1]} WINS")
                window.destroy()
                return
        else:
            messagebox.showerror("ERROR", "NOT IN MOVES LIST") 
            reset_color()
    else: reset_color()

def move_color(x,y):
    reset_color()
    p = b.get_piece(x,y)
    for i in p.get_moves(b):
        grid[i[0]][i[1]].configure(bg='light gray')
    global piece_chosen,chosen_piece
    chosen_piece = p
    piece_chosen = True


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

grid =[list('.')*8 for i in range(8)]

construct()

for i in range(8):
    Label(window,text=chr(i+65),font = fonts(18),bg = 'black',fg = 'white').place(relx = o(i*107+400),rely = p(865))
    Label(window,text = f'{8-i}',font = fonts(18),bg= 'black',fg = 'white').place(rely = o(i*196+30),relx = p(710))
Label(window,text = 'CLOSE',font = fonts(18),bg= 'black',fg = 'white').place(rely = o(120),relx = p(850))
print()
window.attributes('-fullscreen',True)
window.bind('<Escape>',lambda a: window.destroy())
window.mainloop()