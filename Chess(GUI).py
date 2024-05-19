from tkinter import *
from tkinter import messagebox
from pieces import bored,piece,update_all,choose_piece
import os
cwd = os.getcwd()
window = Tk()
window.configure(bg='black')
window.wm_attributes('-transparentcolor', 'forest green')

o = lambda a:a/1536
p = lambda a:a/888
fr = lambda a: (f'{a}')
fonts = lambda a:("Inter ExtraBold", a * -1,'bold')

chosen_piece = ''
piece_chosen = False
clicknum = 0

images = {"B": PhotoImage(file=rf"{cwd}\sprites\B.png"),
"B_" : PhotoImage(file=rf"{cwd}\sprites\b_.png"),
'K' : PhotoImage(file=rf"{cwd}\sprites\K.png"),
'K_': PhotoImage(file=rf"{cwd}\sprites\k_.png"),
'N' : PhotoImage(file=rf"{cwd}\sprites\N.png"),
'N_': PhotoImage(file=rf"{cwd}\sprites\N_.png"),
'P': PhotoImage(file=rf"{cwd}\sprites\P.png"),
'P_': PhotoImage(file=rf"{cwd}\sprites\p_.png"),
'Q': PhotoImage(file=rf"{cwd}\sprites\Q.png"),
'Q_': PhotoImage(file=rf"{cwd}\sprites\q_.png"),
'R' : PhotoImage(file=rf"{cwd}\sprites\R.png"),
'R_': PhotoImage(file=rf"{cwd}\sprites\r_.png"),
'KNOOK':PhotoImage(file=rf"{cwd}\sprites\knook.png")}
def construct():
    for i in range(8):
        for j in range(8):
            btn= Button(window,font=("Inter ExtraBold", 20 * -1,"bold"),command= lambda x=i,y=j:move_piece(x,y))
            btn.configure(bg="saddle brown") if (i+j)%2 else btn.configure(bg="bisque")
            if b.is_piece(i,j):
                knook =  images[(b.get_piece(i,j).get_image())]
                btn.configure(image =knook,)
                btn.image = knook
            btn.place(relx=o(j*107+350),rely=p(i*107),width=110,height=110)
            grid[i][j] = btn
    Button(window,image=choose_piece("KNOOK"),command= lambda: window.destroy()).place(relx=o(1470),rely=p(0))

def reset_color():
    for i in range(8):
        for j in range(8):
            grid[i][j].configure(bg="saddle brown") if (i+j)%2 else grid[i][j].configure(bg="bisque")

def move_piece(x,y):
    global clicknum,chosen_piece,piece_chosen
    if not clicknum:
        if b.is_piece(x,y):
            clicknum=1
            chosen_piece = b.get_piece(x,y)
            piece_chosen = TRUE
            for (i,j) in chosen_piece.get_moves(b):
                grid[i][j].configure(bg = 'light gray')
            return
        else:
            reset_color()
            clicknum = 0
            return
    else:
        if (x,y) in chosen_piece.get_moves(b):
            b.move(chosen_piece,x,y)
            construct()
            if b.is_mate()[0] and b.move_count>2:
                messagebox.showinfo("CHECKMATE", f"CHECKMATE. {b.is_mate()[1]} WINS")
                window.destroy()
                return
            clicknum=0
            chosen_piece=''
            piece_chosen = False
            return
        else:
            messagebox.showerror("ERROR", "NOT IN MOVES LIST") 
            reset_color()
            clicknum = 0
            chosen_piece = ''
            piece_chosen = False
            return
    


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
