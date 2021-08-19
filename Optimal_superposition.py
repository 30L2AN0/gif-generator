from PIL import Image
import numpy as np
import os
import matplotlib

try:
    os.mkdir('ITC')
except:
    print('already existing')


imA = Image.open("ITC/imageA.png")
tabA = np.array(imA)
width, height = len(tabA[0]), len(tabA)
tabA = np.array([[int(tabA[i][j][0]/255) for j in range(width)] for i in range(height)])
tabA_bl = [[i, j] for i in range(height) for j in range(width) if tabA[i][j] == 0]
width, height = len(tabA[0]), len(tabA)


A = np.array(tabA_bl).transpose()
# A = np.array([[1, -1], [2, 2], [-2, 3]]).transpose()


N = len(A[0])
d = len(A)


theta = np.pi / 6
R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
t = np.array([[-height/5, width/4]] * N).transpose()
B = R.dot(A) + t

centroid_A = 1/N * np.array([[sum(A[i])] * N for i in range(d)])
centroid_B = 1/N * np.array([[sum(B[i])] * N for i in range(d)])

H = (A - centroid_A).dot((B - centroid_B).transpose())
U, S, V = np.linalg.svd(H, full_matrices=True)
R_found = V.dot(U.transpose())
t_found = centroid_B - R.dot(centroid_A)

if __name__ == '__main__':
    print(R)
    print(R_found)
    print(t)
    print(t_found)
