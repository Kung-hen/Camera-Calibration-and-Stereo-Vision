# import cv2
# import numpy as np
# import os
# import glob
# import matplotlib.pyplot as plt


# def show_WORDS(letters, path):
#     # path = self.folder_path+"/*bmp"
#     fs = cv2.FileStorage('{}'.format(path), cv2.FILE_STORAGE_READ)
#     text = str('{}'.format(letters))
#     row = 8
#     column = 11
#     CHECKERBOARD = (column, row)
#     shift = np.array([
#         [7, 5], [4, 5], [1, 5], [7, 2], [4, 2], [1, 2]
#     ])
#     obj_points = []
#     im_points = []

#     criteria = (cv2.TERM_CRITERIA_EPS +
#                 cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

#     points3D = np.zeros((1, column*row, 3), np.float32)
#     points3D[0, :, :2] = np.mgrid[0:column, 0:row].T.reshape(-1, 2)

#     image_folder = glob.glob('Q2_Image/*.bmp')
#     for files in image_folder:
#         image = cv2.imread(files)
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         ret, corners = cv2.findChessboardCorners(
#             gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
#         if ret == True:
#             obj_points.append(points3D)
#             corners2 = cv2.cornerSubPix(
#                 gray, corners, (11, 11), (-1, -1), criteria)
#             im_points.append(corners2)

#             ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
#                 obj_points, im_points, gray.shape[::-1], None, None)
#             ret, rvecs, tvecs = cv2.solvePnP(points3D, corners2, mtx, dist)

#             for v, n in enumerate(text):
#                 ch = fs.getNode(n).mat()
#                 number_of_points = 2*len(ch[:])
#                 ch1 = np.resize(ch, (number_of_points, 3))

#                 for i, x in enumerate(ch1):
#                     ch1[i, 0], ch1[i, 1] = (
#                         ch1[i, 0] + shift[v, 0], ch1[i, 1]+shift[v, 1])

#                 # Project 3D points to image plane
#                 chessboard_corners = np.float32(ch1)
#                 imgpts, jac = cv2.projectPoints(
#                     chessboard_corners, rvecs, tvecs, mtx, dist)
#                 imgpts = imgpts.astype(int)
#                 imgpts = np.ravel(imgpts)
#                 q = []
#                 for i, n in enumerate(imgpts):
#                     q.append(n)
#                     if len(q) == 4:
#                         image = cv2.line(
#                             image, (q[0], q[1]), (q[2], q[3]), (0, 0, 255), 10)
#                         q.clear()

#         image = cv2.resize(image, (900, 900))
#         cv2.imshow('img', image)

#         cv2.waitKey(1000)

#     cv2.destroyAllWindows()
