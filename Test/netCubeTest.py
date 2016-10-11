#!/usr/bin/python3
import netComb
from tkinter import *
#from PIL import Image
import os
import random
import sys

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'RedisManaging'))
from redisClient import RedisClient, Identity

size_pictures = (150, 137)
gap = 5


class ShowDialog:
    def __init__(self, parent):
        self.parent = parent
        self.form = parent.frameR
        self.create_dialog()


    def create_dialog(self):
        Label(self.form, text="Znáš správnou odpověď?", justify=LEFT,
              padx=20, font=("Serif", "20")).grid(row=1, columnspan=2, sticky=W+E+N, pady=40)
        self.ch = []
        tdesc = ["Je to síť krychle a všechny protilehlé strany dávají součet 7",
                 "Je to síť krychle ale některé protilehlé strany dávají jiný součet",
                 "Tohle není žádná krychle ale jen náhodný shluk čtverečků!"
                 ]
        b = Button(self.form, text=tdesc[0], command=lambda: self.handle_buttons(0))
        b.grid(row=2, columnspan=2,  sticky=W)
        self.ch.append(b)
        b = Button(self.form, text=tdesc[1], command=lambda: self.handle_buttons(1))
        b.grid(row=3, columnspan=2,  sticky=W)
        self.ch.append(b)
        b = Button(self.form, text=tdesc[2], command=lambda: self.handle_buttons(2))
        b.grid(row=4, columnspan=2,  sticky=W)
        self.ch.append(b)

    def handle_buttons(self, ch):
        print("choice = {c}, category = {k}".format(c=ch+1, k=self.parent.category))
        if (ch+1) == self.parent.category:
            self.parent.info.add_ra()
        else:
            self.parent.info.add_wa()
        self.parent.get_question()

    def on_off_buttons(self,on=True):
        for i in range(3):
            if on:
                self.ch[i]['state']='normal'
            else:
                self.ch[i]['state']=DISABLED



class PanelInfo:

    def __init__(self, root_form, main_cl):
        """
        :param canvas: where to draw info
        """
        self.root_form = root_form
        self.main_cl = main_cl
        h=300
        self.canvas = Canvas(root_form, width=300, height=h)
        self.canvas.grid(row=0, columnspan=2, sticky=W+E+N, pady=40)
        self.n_right_answer = [0, "Správných odpovědí: {n}",
                               self.canvas.create_text(300 / 2, h / 4, text="")]
        self.update_text(self.n_right_answer)
        self.n_wrong_answer = [0, "Chybných odpovědí: {n}",
                               self.canvas.create_text(300 / 2, 2*h / 4, text="")]
        self.update_text(self.n_wrong_answer)
        self.time_bar = [200]
        self.time_bar.append(self.canvas.create_rectangle(50, 3*h/4,self.time_bar[0]+50,3*200/2+30,fill="black"))
        self.canvas.after(100, self.update_time_bar)


    def update_time_bar(self):
        self.time_bar[0] -= 2
        self.canvas.coords(self.time_bar[1],50, 3*300/4,self.time_bar[0]+50,3*200/2+30)
        print("cas {t}".format(t=self.time_bar[0]))
        if self.time_bar[0] > 0:
            self.canvas.after(2000, self.update_time_bar)
        else:
            self.canvas.create_text(50,30, text="Konec testu!")
            self.main_cl.n_attempt['state'] = 'normal'
            self.main_cl.dialog.on_off_buttons(False)
            GeometrieTest.communication.add_data("krychle", 100*self.n_right_answer[0]*pow(0.3,self.n_wrong_answer[0]))


    def update_text(self, txt):
        self.canvas.itemconfigure(txt[2], text=txt[1].format(n=txt[0]))

    def add_ra(self):
        """increase number of right answers"""
        self.n_right_answer[0] += 1
        self.update_text(self.n_right_answer)

    def add_wa(self):
        """increase number of wrong answers"""
        self.n_wrong_answer[0] += 1
        self.update_text(self.n_wrong_answer)


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

        master.title("Testík")
        # redis

        login_data = Identity(master)
        master.wait_window(login_data.top)
        GeometrieTest.communication = login_data.redis
        if not login_data.redis_ok or login_data.closed_window:
            sys.exit("Nefunkcni REDIS!")

        # kontrolni tisk
        print('Name: ', login_data.name)
        print('Surname: ', login_data.surname)
        self.name = (login_data.name, login_data.surname)

        # tkinter
        self.frameL = Frame(master)
        self.frameL.pack(padx=20, pady=20, side=LEFT)
        self.frameR = Frame(master)
        self.frameR.pack(padx=5, pady=10, side=LEFT)
        self.info = PanelInfo(self.frameR, self)
        self.dialog = ShowDialog(self)
        self.n_attempt = Button(self.frameR, text="Další pokus?", fg="red",
                                state=DISABLED, font=("Serif", "10"), command=self.get_new_attempt)
        self.n_attempt.grid(row=5, column=1, pady=20)
        self.sh = self.create_net_place()
        self.category = -1
        self.get_question()

    def create_net_place(self):
        canvas_width = 700
        canvas_height = 700
        canvas = Canvas(self.frameL, width=canvas_width, height=canvas_height)
        canvas.pack()
        sh = ShowNet(canvas, netComb.res_cubes, netComb.res_nocubes)
        return sh

    def get_question(self):
        self.category = random.randint(1, 3)
        self.sh.create_problem(self.category)

    def get_new_attempt(self):
        if hasattr(self, 'n_attempt') and  self.n_attempt['state'] != DISABLED:
            self.dialog.on_off_buttons(True)
            self.n_attempt['state'] = DISABLED
            self.info = PanelInfo(self.frameR, self)
            self.get_question()



def main(): #run mianloop
    root = Tk()
    app = GeometrieTest(root)
    root.mainloop()

if __name__ == '__main__':
    main()


