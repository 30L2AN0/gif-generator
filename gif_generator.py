from PIL import ImageDraw, ImageTk
import PIL.Image
from tkinter import *
from PIL import Image
from PIL import ImageFilter
from PIL.ImageFilter import (BLUR)
import glob
import numpy as np
import os
import cv2
import Interpolation
import shutil

try:
    os.mkdir('gif')
except:
    shutil.rmtree('gif')
    os.mkdir('gif')
    print('file cleared')

root0 = Tk()


# Drawing functions


def draw_dot(event, position, canvas, draw):
    x, y = event.x, event.y
    canvas.create_oval(x, y, x, y, fill="black")
    draw.point((x, y), fill="black")
    position.append((x, y))


def draw_line(event, position, canvas, draw):
    x, y = event.x, event.y
    if position:
        (x0, y0) = position[0]
        canvas.create_line(x0, y0, x, y, fill="black")
        draw.line([(x0, y0), (x, y)], fill="black")
        position.pop()
    position.append((x, y))
    return


def reset_drawing_line(position):
    position.pop()


# Processes functions


def drawing_process(image_number, drawing_root):
    width0, height0 = 500, 500
    canvas = Canvas(drawing_root, width=width0, height=height0, background="white")
    canvas.pack(side=TOP, padx=5, pady=5)

    image = PIL.Image.new('RGB', (width0, height0), "white")
    draw = ImageDraw.Draw(image)

    def finalize_drawing():
        drawing_root.quit()
        image.save('gif/image' + str(image_number) + '.png')
        canvas.destroy()
        button.destroy()

    def finalize_drawing_by_push(event):
        finalize_drawing()

    position0 = []
    canvas.bind("<Button-1>", lambda event: draw_dot(event, position0, canvas, draw))
    canvas.bind("<B1-Motion>", lambda event: draw_line(event, position0, canvas, draw))
    canvas.bind("<ButtonRelease-1>", lambda event: reset_drawing_line(position0))
    drawing_root.bind('<Return>', finalize_drawing_by_push)
    button = Button(drawing_root, text="Finish", command=finalize_drawing)
    button.pack()

    drawing_root.mainloop()


def choice_process(root):
    photo = PhotoImage(file='Interface_pictures/NEW_DRAWING.png')
    canvas = Label(root, image=photo)
    canvas.pack()
    stop_drawing = [True]

    def accept_or_refuse_by_click(event):
        x, y = event.x, event.y
        if 164 <= x <= 249 and 236 <= y <= 282:
            canvas.destroy()
            stop_drawing.append(False)
            root.quit()
        if 334 <= x <= 419 and 233 <= y <= 282:
            canvas.destroy()
            root.quit()

    def accept_by_push(event):
        canvas.destroy()
        stop_drawing.append(False)
        root.quit()

    def refuse_by_push(event):
        canvas.destroy()
        root.quit()

    root.bind('<Return>', accept_by_push)
    root.bind('<BackSpace>', refuse_by_push)
    canvas.bind("<ButtonRelease-1>", lambda event: accept_or_refuse_by_click(event))

    root.mainloop()

    return stop_drawing[-1]


# Main functions


def main_loop(root):
    drawing_number = -1
    while True:
        drawing_number += 1
        drawing_process(drawing_number, root)
        stop_drawing = choice_process(root)
        if stop_drawing:
            return drawing_number


def main_function(root):
    photo = PhotoImage(file='Interface_pictures/START_DRAWING.png')
    canvas = Label(root, image=photo)
    canvas.pack()

    number_of_drawings = [1]

    def enter_app_by_click(event):
        x, y = event.x, event.y
        if 238 <= x <= 322 and 238 <= y <= 284:
            canvas.destroy()
            number_of_drawings[0] = main_loop(root) + 1
            root.quit()

    def enter_app_by_push(event):
        canvas.destroy()
        number_of_drawings[0] = main_loop(root) + 1
        root.quit()

    root.bind('<Return>', enter_app_by_push)
    canvas.bind("<ButtonRelease-1>", lambda event: enter_app_by_click(event))

    root.mainloop()

    return number_of_drawings[0]


def gif_creator(root):
    number_of_drawings = main_function(root)

    photo = PhotoImage(file='Interface_pictures/CHOOSE_TIME.png')
    canvas = Label(root, image=photo)
    canvas.pack()

    size = [1]

    def get_size(s):
        size.pop()
        size.append(s)

    def affect_size():
        root.quit()
        canvas.destroy()
        slider.destroy()
        button.destroy()

    def affect_size_by_push(event):
        affect_size()

    slider = Scale(root, orient='horizontal', command=get_size, from_=1, to=15, resolution=0.1, tickinterval=1,
                   length=500, label='Length (sec)')
    slider.pack()
    button = Button(root, text="Finish", command=affect_size)
    button.pack()
    root.bind('<Return>', affect_size_by_push)

    root.mainloop()

    photo = PhotoImage(file='Interface_pictures/IMAGES_PLACEMENT.png')
    canvas = Label(root, image=photo)
    canvas.pack()

    def next_slide():
        root.quit()
        canvas.destroy()
        button.destroy()

    def next_slide_by_push(event):
        next_slide()

    button = Button(root, text="Fine!", command=next_slide)
    button.pack()
    root.bind('<Return>', next_slide_by_push)

    root.mainloop()

    sliders = []
    sliders_values = [0 for i in range(number_of_drawings)]

    for i in range(number_of_drawings):
        slider = Scale(root, orient='horizontal', from_=0, to=size[0],
                       resolution=0.1, tickinterval=1, length=500, label='Position of Image n°' + str(i) + ' (sec)')
        sliders.append(slider)
        sliders[i].pack()

    def affect_placements():
        root.quit()
        for j in range(number_of_drawings):
            sliders_values[j] = sliders[j].get()
            sliders[j].destroy()
        button.destroy()

    def affect_placements_by_push(event):
        affect_placements()

    button = Button(root, text="Finish", command=affect_placements)
    button.pack()
    root.bind('<Return>', affect_placements_by_push)

    root.mainloop()

    times = [int(float(size[0])), sliders_values]
    times[0] *= 10
    for i in range(len(times[1])):
        times[1][i] *= 10

    frames = []
    imgs = glob.glob('gif/*.png')
    for i in range(times[0] + 1):
        if i in times[1]:  # si l'image existe
            time = times[1].index(i)
            new_frame = Image.open(imgs[time])
        else:
            if (i + 1) in times[1]:  # si la suivante existe on anticipe le brouillé de la suivante
                time = times[1].index(i + 1)
                new_frame = Image.open(imgs[time])
                new_frame = new_frame.filter(ImageFilter.BLUR)
            else:  # sinon on prend le brouillé de la précédente.
                new_frame = new_frame.filter(ImageFilter.BLUR)
        frames.append(new_frame)

    # Save into a GIF file that loops forever
    frames[0].save('gif/output.gif',
                   format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=1, loop=0)

    """frames = []
    imgs = glob.glob('gif/*.png')
    sorted_pics = sorted([(times[1][i], i) for i in range(len(times[1]))])
    N = len(sorted_pics)
    couples = [[(i, i+1), sorted_pics[i+1][0] - sorted_pics[i][0] - 1] for i in range(N-1)]
    # couples += [[(N-1, 0), sorted_pics[0][0] + times[0] - sorted_pics[N-1][0] - 1]]
    for i in range(N-1):
        couple = couples[i]

        im0 = Image.open(imgs[sorted_pics[couple[0][1]][1]])
        tab0 = np.array(im0)
        im1 = Image.open(imgs[sorted_pics[couple[0][0]][1]])
        tab1 = np.array(im1)

        width, height = len(tab0[0]), len(tab0)

        tab0 = np.array([[int(tab0[i][j][0] / 255) for j in range(width)] for i in range(height)])
        tab1 = np.array([[int(tab1[i][j][0] / 255) for j in range(width)] for i in range(height)])

        tab0_bl, tab1_bl = Interpolation.blacks(tab0), Interpolation.blacks(tab1)
        final_tab1_bl = Interpolation.auto_superposition(tab0_bl, tab1_bl)[0]
        n = int(couple[1])
        intermeds = Interpolation.intermediate_mvt(tab0_bl, final_tab1_bl, n)

        frames.append(im1)

        for j in range(n):
            intermed = intermeds[j]
            Interpolation.save_picture(Interpolation.reconstitution(intermed),
                                       "image" + str(i) + str(j), "gif")
            new_frame = Image.open("gif/image" + str(i) + str(j) + ".png")
            frames.append(new_frame)

        frames.append(im0)

    # Save into a GIF file that loops forever
    frames[0].save('gif/gif_interpolation.gif',
                   format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=1, loop=0)"""


if __name__ == '__main__':
    gif_creator(root0)
