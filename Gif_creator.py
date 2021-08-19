from tkinter import *

root = Tk()
cnv = Canvas(root, width=400, height=400)
cnv.pack()

old = None


def rayon(r):
    global old
    r = int(r)
    cnv.delete(old)
    old = cnv.create_oval(200-r, 200-r, 200+r, 200+r)


curseur = Scale(root, orient="horizontal", command=rayon, from_=0, to=200)
curseur2 = Scale(root, orient="horizontal", command=rayon, from_=0, to=200)
curseur3 = Scale(root, orient="horizontal", command=rayon, from_=0, to=200)
curseur.pack()
curseur2.pack()
curseur3.pack()

root.mainloop()
