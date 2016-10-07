from tkinter import *
#import time

canvas_width = 500
canvas_height = 500
left_dist = 50
top_dist = 150
cube_size = 200

pE = (left_dist, top_dist, 0)
pA = (left_dist, top_dist+cube_size, 0)
pB = (left_dist+cube_size, top_dist+cube_size, 0)
pF = (left_dist+cube_size, top_dist, 0)
pH = (left_dist, top_dist, cube_size)
pD = (left_dist, top_dist+cube_size, cube_size)
pC = (left_dist+cube_size, top_dist+cube_size, cube_size)
pG = (left_dist+cube_size, top_dist, cube_size)

points = {'A': [pA, 'black', 0], 'B': [pB, 'black', 0], 'C': [pC, 'black', 0], 'D': [pD, 'black', 0],
          'E': [pE, 'black', 0], 'F': [pF, 'black', 0], 'G': [pG, 'black', 0], 'H': [pH, 'black', 0],
          }

vector = (pow(0.5, 0.5)*0.5, pow(0.5, 0.5)*0.5)
sup_line = (4, None, '#ff0000')
full_line = (3, None, '#000')
dash_line = (2, (4, 4), '#000')
text_font = ("Purisa", 12)
text_vector = (-8, -10)
question = 0
frame = 0


def line(cnv, p1, p2, style=full_line):
    cnv.create_line(p1[0]+vector[0]*p1[2], p1[1]-vector[1]*p1[2],
                     p2[0]+vector[0]*p2[2], p2[1]-vector[1]*p2[2], dash=style[1], width=style[0], fill=style[2])
    print("Cara z bodu {p1x},{p1y} do bodu {p2x},{p2y}, dash= {d}, width={w}, fill={f}"
          .format(p1x=p1[0]+vector[0]*p1[2], p1y=p1[1]-vector[1]*p1[2], p2x=p2[0]+vector[0]*p2[2], p2y=p2[1]-vector[1]*p2[2],
                  d=style[1], w=style[0], f=style[2]))


def text_point(root, p,txt, color='#f00'):
    return root.create_text(p[0]+vector[0]*p[2]+text_vector[0], p[1]-vector[1]*p[2]+text_vector[1],
                         font=text_font, text=txt, fill=color)


def create_text_points(cnv):
    for p in points:
            points[p][2]=text_point(cnv, points[p][0], p, points[p][1])


def visible_points(cnv, show=True):
    for p in points:
        if show:
            cnv.itemconfigure(points[p][2], text=p)
        else:
            cnv.itemconfigure(points[p][2], text='')


def draw_cube(cnv):
    line(cnv, pA, pB)
    line(cnv, pB, pF)
    line(cnv, pF, pE)
    line(cnv, pE, pA)
    line(cnv, pD, pC, dash_line)
    line(cnv, pC, pG, )
    line(cnv, pG, pH)
    line(cnv, pH, pD, dash_line)
    line(cnv, pA, pD, dash_line)
    line(cnv, pB, pC)
    line(cnv, pE, pH)
    line(cnv, pF, pG)

def next_question():
    pass

master = Tk()
w = Canvas(master,
           width=canvas_width,
           height=canvas_height)
w.grid(row=0, column=0, columnspan=2, rowspan=2,
               sticky=W+E+N+S, padx=5, pady=5)

frame = Frame(master)
frame.grid(row=0,column=2, sticky="nw", padx=5, pady=5)
question = Label(frame, text="Přímky AE a EG jsou...", font=text_font).grid(row=0, column=0, sticky="nw")
var = IntVar()
Radiobutton(frame, text="Různoběžné", variable=var, value=1, font=text_font).grid(row=1, column=0, sticky="nw")
Radiobutton(frame, text="Rovnoběžné", variable=var, value=2, font=text_font).grid(row=2, column=0, sticky="nw")
Radiobutton(frame, text="Mimoběžné", variable=var, value=3, font=text_font).grid(row=3, column=0, sticky="nw")
button = Button(frame, text="Další otázka", fg="red", command=next_question).grid(row=4, column=0, sticky="se")

#w.pack()

#y = int(canvas_height / 2)
# w.create_line(0, y, canvas_width, y, fill="#476042")
draw_cube(w)
create_text_points(w)
w.itemconfigure(points['A'][2], fill='red')
visible_points(w, True)
line(w, pB, pC)

mainloop()
