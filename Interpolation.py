from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
import random
import glob

try:
    os.mkdir('Interpolation')
except:
    print('already existing')

try:
    os.mkdir('Interpolation')
except:
    print('already existing')

im0 = Image.open("Interpolation/image0.png")
tab0 = np.array(im0)
im1 = Image.open("Interpolation/image1.png")
tab1 = np.array(im1)

width, height = len(tab0[0]), len(tab0)

tab0 = np.array([[int(tab0[i][j][0]/255) for j in range(width)] for i in range(height)])
tab1 = np.array([[int(tab1[i][j][0]/255) for j in range(width)] for i in range(height)])


def quick_show(tab):
    x, y = [], []
    for i in range(height):
        for j in range(width):
            if tab[i][j] == 0:
                x.append(j)
                y.append(height-i)
    plt.plot(np.array(x), np.array(y))
    plt.show()


def blacks(tab):
    return [(i, j) for i in range(height) for j in range(width) if tab[i][j] == 0]


def distance(p, q):
    return np.sqrt((p[0]-q[0])**2 + (p[1]-q[1])**2)


def closest(p, tab_blacks):
    min_dist = np.sqrt(width**2 + height**2)
    min_rank = 0
    for rank in range(len(tab_blacks)):
        q = tab_blacks[rank]
        d = distance(p, q)
        if d < min_dist:
            min_rank, min_dist = rank, d
    return [tab_blacks[min_rank], min_rank, min_dist]


def association_tab(tab0_blacks, tab1_blacks):
    length = min(len(tab0_blacks), len(tab1_blacks))
    tab0_blacks = tab0_blacks[:length]
    tab1_blacks = tab1_blacks[:length]
    links = [0]*length
    cur = 0
    while length > 0:
        p = tab0_blacks[cur]
        [q, rank] = closest(p, tab1_blacks)[:2]
        tab1_blacks.pop(rank)
        links[cur] = q
        length -= 1
        cur += 1
    return links


def reconstitution(tab_blacks):
    tab = [[1 for j in range(width)] for i in range(height)]
    for p in tab_blacks:
        if 0 <= p[0] <= height-1 and 0 <= p[1] <= width-1:
            tab[p[0]][p[1]] = 0
    return tab


def intermediate(tab0_blacks, tab1_blacks):
    tab1_blacks = association_tab(tab0_blacks, tab1_blacks)
    length = len(tab1_blacks)
    new_tab = [(int((tab0_blacks[i][0]+tab1_blacks[i][0]) / 2), int((tab0_blacks[i][1]+tab1_blacks[i][1]) / 2)) for i in range(length)]
    return new_tab


def save_picture(tab, name, location):
    matrix = np.array([[[float(tab[i][j])] * 3 for j in range(width)] for i in range(height)])
    matplotlib.image.imsave(location + "/" + name + ".png", matrix)


##############################################################################################


im_rot0 = Image.open("Interpolation/image1.png")
tab0_rot = np.array(im_rot0)
im_rot1 = Image.open("Interpolation/image0.png")
tab1_rot = np.array(im_rot1)

tab0_rot = np.array([[int(tab0_rot[i][j][0]/255) for j in range(width)] for i in range(height)])
tab1_rot = np.array([[int(tab1_rot[i][j][0]/255) for j in range(width)] for i in range(height)])


def rotation(theta, tab_blacks, bary):
    tab_rot = []
    for p in tab_blacks:
        q0, q1 = p[0] - bary[0], p[1] - bary[1]
        q0_temp = q0
        q1_temp = q1
        q0 = np.cos(theta) * q0_temp - np.sin(theta) * q1_temp
        q1 = np.sin(theta) * q0_temp + np.cos(theta) * q1_temp
        q0, q1 = int(q0 + bary[0]), int(q1 + bary[1])
        tab_rot.append([(q0, q1), p])
    return tab_rot


def translation(u, tab_blacks):
    tab_trans = []
    for i in range(len(tab_blacks)):
        p, p0 = tab_blacks[i][0], tab_blacks[i][1]
        q0, q1 = int(p[0] + u[0]), int(p[1] + u[1])
        tab_trans.append([(q0, q1), p0])
    return tab_trans


def dist_images(tab0_blacks, tab1_blacks):
    s = 0
    for p in tab0_blacks:
        s += closest(p, tab1_blacks)[2] ** 2
    return np.sqrt(s)


def barycenter(tab_blacks):
    x, y = 0, 0
    for p in tab_blacks:
        x += p[0]
        y += p[1]
    n = len(tab_blacks)
    return (int(x/n), int(y/n))


def auto_superposition(tab0_blacks, tab1_blacks):
    min_dist = dist_images(tab0_blacks, tab1_blacks)
    final_tab1_bl = [p for p in tab1_blacks]
    min_height = int(-height/4)
    max_height = int(height/4)
    min_width = int(-width/4)
    max_width = int(width/4)
    iterations = 50
    path = (0, 0)
    bary = barycenter(final_tab1_bl)
    for i in range(iterations):
        theta = random.uniform(-np.pi, np.pi)
        new_tab1_bl = rotation(theta, tab1_blacks, bary)
        vect = (path[0] + random.randint(min_height, max_height), path[1] + random.randint(min_width, max_width))
        new_tab1_bl = translation(vect, new_tab1_bl)
        new_tab1_bl_core = [row[0] for row in new_tab1_bl]
        save_picture(reconstitution(new_tab1_bl_core), str(i), "Interpolation")
        dist = dist_images(tab0_blacks, new_tab1_bl_core)
        if dist < min_dist:
            min_dist = dist
            final_tab1_bl = [p for p in new_tab1_bl]
            v_size = max_height - min_height
            h_size = max_width - min_width
            path = vect
            min_height += int(v_size/15)
            max_height -= int(v_size/15)
            min_width += int(h_size/15)
            max_width -= int(h_size/15)

    fin_tab1_bl_core = [row[0] for row in final_tab1_bl]
    save_picture(reconstitution(fin_tab1_bl_core), "final", "Interpolation")
    return [final_tab1_bl, min_dist]


def closest_mvt(p, tab_bl):
    min_dist = np.sqrt(width**2 + height**2)
    min_rank = 0
    for rank in range(len(tab_bl)):
        q = tab_bl[rank][0]
        d = distance(p, q)
        if d < min_dist:
            min_rank, min_dist = rank, d
    return [tab_bl[min_rank][1], min_rank]


def association_mvt(tab0_bl, final_tab1_bl):
    length = min(len(tab0_bl), len(final_tab1_bl))
    tab0_bl = tab0_bl[:length]
    tab1_bl = final_tab1_bl[:length]
    links = [0]*length
    cur = 0
    while length > 0:
        p = tab0_bl[cur]
        [q, rank] = closest_mvt(p, tab1_bl)
        tab1_bl.pop(rank)
        links[cur] = q
        length -= 1
        cur += 1
    return links


def intermediate_mvt(tab0_bl, final_tab1_bl, nb_of_inter):
    tab1_bl = association_mvt(tab0_bl, final_tab1_bl)
    length = len(tab1_bl)
    new_tabs = []
    N = nb_of_inter + 2
    for k in range(1, N-1):
        new_tab = [(int((tab0_bl[i][0] * k + tab1_bl[i][0] * (N-k)) / N),
                    int((tab0_bl[i][1] * k + tab1_bl[i][1] * (N-k)) / N)) for i in range(length)]
        new_tabs.append(new_tab)
    return new_tabs


if __name__ == '__main__':
    """imA = Image.open("Interpolation/imageA.png")
    tabA = np.array(imA)
    tabA = np.array([[int(tabA[i][j][0] / 255) for j in range(width)] for i in range(height)])
    tabA_bl = blacks(tabA)
    tabB_bl = rotation(np.pi/6, tabA_bl, (height/2, width/2))
    tabB_bl = [row[0] for row in translation((-height/5, width/4), tabB_bl)]
    tabB = reconstitution(tabB_bl)
    save_picture(tabB, "imageB", "Interpolation")"""

    """tab0_bl_rot, tab1_bl_rot = blacks(tab0_rot), blacks(tab1_rot)
    res_bl_rot = rotation(np.pi/2, tab0_bl_rot)
    res_bl_rot = [row[0] for row in translation((height/5, -width/5), res_bl_rot)]
    res_rot = reconstitution(res_bl_rot)
    save_picture(res_rot, "blabla", "Interpolation")"""

    tab0_bl, tab1_bl = blacks(tab0_rot), blacks(tab1_rot)
    final_tab1_bl = auto_superposition(tab0_bl, tab1_bl)[0]
    N = 10
    intermeds = intermediate_mvt(tab0_bl, final_tab1_bl, N)
    for i in range(N):
        intermed = intermeds[i]
        save_picture(reconstitution(intermed), "intermed"+str(i), "Interpolation")

    """frames = []
    imgs = glob.glob('Interpolation/special_file/*.png')
    for i in range(len((imgs))):
        new_frame = Image.open(imgs[i])
        frames.append(new_frame)

    frames[0].save('Interpolation/special_file/thrown_ball.gif',
                   format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=300, loop=0)"""

