import numpy as np
import struct
import sys
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import matplotlib.pyplot as plt
import cv2


def main():

    w = 1600
    h = 400

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('lidar-point-cloud.avi',fourcc, 10.0, (w,h))


    for ii in range(240, 300, 1):
        cur_frame = cv2.imread("azimuth{}.png".format(ii))
        out.write(cur_frame)

    for ii in reversed(range(270, 300, 1)):
        cur_frame = cv2.imread("azimuthr{}.png".format(ii))
        out.write(cur_frame)

    for jj in range(250,270,1):
        cur_frame = cv2.imread("elev{}.png".format(jj))
        out.write(cur_frame)

    for jj in reversed(range(220,270,1)):
        cur_frame = cv2.imread("elev{}.png".format(jj))
        out.write(cur_frame)

    out.release()

if __name__ == "__main__":
    main()
