#!/usr/bin/python3
import netComb
from tkinter import *
from PIL import Image
import sys
import os
import random

size_pictures = (150, 137)
gap = 5

class ShowDialog:
    def __init__(self, frm):
        self.form = frm
        self.choice = IntVar()


    def create_dialog(self, correct_answer):
        self.choice.set(1)
        self.info = Label(self.form, text="Správně "+str(0),
                          justify = LEFT, padx=20, font=("Serif", "20"))\
            .grid(row=0, columnspan=2, sticky=W+E+N, pady=40)
        Label(self.form, text="Znáš správnou odpověď?", justify = LEFT,
              padx=20, font=("Serif","20")).grid(row=1, columnspan=2, sticky=W+E+N, pady=40)
        Radiobutton(self.form, text="Je to síť krychle a všechny protilehlé strany dávají součet 7",
                    padx = 20, variable=self.choice, value=1, font=("Serif","10")).grid(row=2, columnspan=2,  sticky=W)
        Radiobutton(self.form, text="Je to síť krychle ale některé protilehlé strany dávají jiný součet",
                    padx = 20, variable=self.choice, value=2, font=("Serif","10")).grid(row=3, columnspan=2, sticky=W)
        Radiobutton(self.form, text="Tohle není žádná krychle ale jen náhodný shluk čtverečků!",
                    padx = 20, variable=self.choice, value=3, font=("Serif","10")).grid(row=4, columnspan=2, sticky=W)


class ShowNet:
    pics = []

    def __init__(self, canvas, net_good, net_bad):
        """
        :param canvas: where to draw nets
        :param net_good: list of numbered cube-nets
        :param net_bad: list of coords, which only resemble cube-nets
        """
        self.canvas = canvas
        self.net_good = (net_good, len(net_good))
        self.net_bad = (net_bad, len(net_bad))
        for i in range(6):
            one_path = os.path.join(os.getcwd(), "img", "f{n}.gif".format(n=i+1))
            img = PhotoImage(file=one_path)
            ShowNet.pics.append(img) 

    def show(self, coord):
        """
        :param coord: {(1, 2): 1, (2, 0): 6, (3, 0): 5, (0, 2): 4, (2, 1): 3, (1, 1): 2}
        :return:
        for x in range(1,16):
            canvas.delete(ShowNet.pics[x])

        """
        self.canvas.delete(ALL)
        for x in coord:
            self.canvas.create_image(x[0]*(size_pictures[0]+gap), x[1]*(size_pictures[1]+gap), anchor=NW, image=ShowNet.pics[coord[x]-1])

    def _create_perm(self, right):
        """
        :param right: True -> keep right numbering, False -> break right numbering
        :return: dictionary for translate numbers
        """
        res = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
        nums = [1, 2, 3]
        while len(nums)>0:
            i = random.randint(1,6)
            while res[i] != 0:
                i = i % 6 + 1
            res[i] = nums.pop()
            res[7-i] = 7-res[i]
        if not right:
            while True:
                x,y = random.randint(1, 6),  random.randint(1, 6)
                if (x+y)!=7:
                    res[x], res[y] = res[y], res[x]
                    break
        return res

    def create_problem(self, correct_answer):
        """
        :param correct_answer:  1 -> right net-cube, right-numbered;
                                2 -> only right net-cube, numbered incorrect;
                                3 -> all is wrong
        :return:
        """
        if correct_answer == 3:
            q = random.randrange(1, self.net_bad[1])
            perm = self._create_perm(True)
            problem = {self.net_bad[0][q][i]:perm[i+1] for i in range(6)}
        else:
            q = random.randrange(1, self.net_good[1])
            perm = self._create_perm(correct_answer == 1)
            problem = {x: perm[self.net_good[0][q][x]] for x in self.net_good[0][q]}
        self.show(problem)



class GeometrieTest:
    def __init__(self, master):
        self.frameL = Frame(master)
        self.frameL.pack(padx=20, pady=20, side=LEFT)
        self.frameR = Frame(master)
        self.frameR.pack(padx=5, pady=10, side=LEFT)
        self.dialog = ShowDialog(self.frameR)
        self.next_button = Button(self.frameR, text="Další", font=("Serif","10"), command=self.click_next)
        self.next_button.grid(row=5, column=0, pady=20)
        self.button = Button(self.frameR, text="QUIT", fg="red", font=("Serif","10"), command=self.frameR.quit)
        self.button.grid(row=5, column=1, pady=20)
        self.sh = self.create_net_place()
        self.count = 0
        self.click_next()

    def create_net_place(self):
        canvas_width = 700
        canvas_height = 700
        canvas = Canvas(self.frameL, width=canvas_width, height=canvas_height)
        canvas.pack()
        sh = ShowNet(canvas, netComb.res_cubes, netComb.res_nocubes)
        return sh


    def click_next(self):
        category = random.randint(1, 3)
        self.sh.create_problem(category)
        self.dialog.create_dialog(category)
        if self.dialog.choice == category:
            self.dialog.info.config(text="Spr odpovědí: {s}".format(s=self.count), width=100)
            self.dialog.info.update_idletasks()







def main(): #run mianloop
    root = Tk()
    app = GeometrieTest(root)
    root.mainloop()

if __name__ == '__main__':
    main()


