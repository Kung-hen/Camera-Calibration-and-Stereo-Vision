# from turtle import widthnp
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog
from UI import Ui_Form
import cv2
import glob
import os
import numpy as np
import matplotlib.pyplot as plt


row = 8
column = 11
CHECKERBOARD = (row, column)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

obj_points = []
im_points = []

points3D = np.zeros((1, row * column, 3), np.float32)
points3D[0, :, :2] = np.mgrid[0:row, 0:column].T.reshape(-1, 2)


class Form_controller(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setup_control()

    def setup_control(self):
        self.ui.pushButton_14.clicked.connect(self.open_folder)
        self.ui.pushButton_2.clicked.connect(self.open_image_L)
        self.ui.pushButton_3.clicked.connect(self.open_image_R)
        self.ui.pushButton_4.clicked.connect(self.Find_corner)
        self.ui.pushButton_5.clicked.connect(self.find_intrinsic)
        self.ui.comboBox.currentIndexChanged.connect(self.combolbox)
        self.ui.pushButton_15.clicked.connect(self.find_extrinsic)
        self.ui.pushButton_6.clicked.connect(self.find_dis)
        self.ui.pushButton_13.clicked.connect(self.show_re)
        self.ui.pushButton_8.clicked.connect(self.HOR_WORD)
        self.ui.pushButton_9.clicked.connect(self.VER_ACT)
        self.ui.pushButton_12.clicked.connect(self.stero)

    def refreshShow(self):
        height, width, channel = self.img.shape
        bytesPerLine = 3*width
        self.qImg = QImage(self.img.data, width, height,
                           bytesPerLine, QImage.Format_RGB888).rgbSwapped()

    def refreshShow_2(self):
        height, width, channel = self.img_2.shape
        bytesPerLine = 3*width
        self.qImg = QImage(self.img.data, width, height,
                           bytesPerLine, QImage.Format_RGB888).rgbSwapped()

    def open_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory(
            self, "Open folder", "./")
        # self.image_folder = glob.glob("{}".format(self.folder_path+"/*bmp"))
        # for files in self.image_folder:
        #     image = cv2.imread(files)
        #     print(image)
        # cv2.destroyAllWindows()

    def open_image_L(self):
        filename_L, filetype_L = QFileDialog.getOpenFileName(
            self, "Open File", "./")
        self.img = cv2.imread(filename_L, -1)
        self.refreshShow()
        # cv2.imshow("img", self.img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def open_image_R(self):
        filename_R, filetype_R = QFileDialog.getOpenFileName(
            self, "Open File", "./")
        self.img_2 = cv2.imread(filename_R, -1)
        self.refreshShow_2()
        # cv2.imshow("img", self.img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def Find_corner(self):
        self.image_folder = glob.glob('{}'.format(self.folder_path+"/*bmp"))
        for files in self.image_folder:
            image = cv2.imread(files)

            ret, cor = cv2.findChessboardCorners(image, CHECKERBOARD)
            if ret == True:
                cv2.drawChessboardCorners(image, CHECKERBOARD, cor, ret)
                image = cv2.resize(image, (900, 900))
                cv2.imshow('corners', image)
                cv2.waitKey(500)
        cv2.destroyAllWindows()

    def find_intrinsic(self):
        self.image_folder = glob.glob("{}".format(self.folder_path+"/*bmp"))
        for files in self.image_folder:
            image = cv2.imread(files)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(
                gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
            if ret == True:
                obj_points.append(points3D)
                corners2 = cv2.cornerSubPix(
                    gray, corners, (11, 11), (-1, -1), criteria)
                im_points.append(corners2)

        ret, cam_mtx, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(
            obj_points, im_points, gray.shape, None, None)
        # 轉至 gray.shape[::-1]
        print('Intrinsic Matrix of image:\n', cam_mtx)

    def combolbox(self):
        obj_points = []
        im_points = []

        points3D = np.zeros((1, row * column, 3), np.float32)
        points3D[0, :, :2] = np.mgrid[0:row, 0:column].T.reshape(-1, 2)
        # Loop
        image_folder = glob.glob('{}'.format(self.folder_path+"/*bmp"))
        for files in image_folder:
            image = cv2.imread(files)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(
                gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
            if ret == True:
                obj_points.append(points3D)
                corners2 = cv2.cornerSubPix(
                    gray, corners, (11, 11), (-1, -1), criteria)
                im_points.append(corners2)

        ret, cam_mtx, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(
            obj_points, im_points, gray.shape[::-1], None, None)

        rvecs = np.array(rvecs)
        r_mtx = np.zeros([len(image_folder), 3, 3])

        for idx, n in enumerate(rvecs):
            matrix, jacobian = cv2.Rodrigues(n)
            r_mtx[idx, :, :] = matrix

        ext_mtx = np.append(r_mtx, tvecs, axis=2)
        num = int(self.ui.comboBox.currentText())
        print('Extrinsic Matrix of image', num,
              ':\n', ext_mtx[num-1, :, :])

    def find_extrinsic(self):
        pass

    def find_dis(self):
        obj_points = []
        im_points = []

        points3D = np.zeros((1, row * column, 3), np.float32)
        points3D[0, :, :2] = np.mgrid[0:row, 0:column].T.reshape(-1, 2)
        # Loop
        image_folder = glob.glob('{}'.format(self.folder_path+"/*bmp"))
        for files in image_folder:
            image = cv2.imread(files)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(
                gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
            if ret == True:
                obj_points.append(points3D)
                corners2 = cv2.cornerSubPix(
                    gray, corners, (11, 11), (-1, -1), criteria)
                im_points.append(corners2)

        ret, cam_mtx, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(
            obj_points, im_points, gray.shape[::-1], None, None)
        print("Distortion:\n", distCoeffs)

    def show_re(self):
        image_folder = glob.glob('{}'.format(self.folder_path+"/*bmp"))
        for files in image_folder:
            image = cv2.imread(files)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(
                gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
            if ret == True:
                obj_points.append(points3D)
                corners2 = cv2.cornerSubPix(
                    gray, corners, (11, 11), (-1, -1), criteria)
                im_points.append(corners2)

            ret, cam_mtx, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(
                obj_points, im_points, gray.shape[::-1], None, None)
            corrected_im = cv2.undistort(image, cam_mtx, distCoeffs)
            bundle = np.concatenate((image, corrected_im), axis=1)
            bundle = cv2.resize(bundle, (1800, 900))
            cv2.imshow('Distorted vs Undistorted Image', bundle)
            cv2.waitKey(2000)
            cv2.destroyAllWindows()

    def HOR_WORD(self):
        f = self.ui.plainTextEdit.toPlainText()
        self.show_WORDS(
            f, 'Q2_lib/alphabet_lib_onboard.txt')

    def VER_ACT(self):
        f = self.ui.plainTextEdit.toPlainText()
        self.show_WORDS(f, 'Q2_lib/alphabet_lib_vertical.txt')

    def stero(self):

        right, left = self.img, self.img_2
        gray_l = cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)
        gray_r = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)
        rg = cv2.resize(right, (699, 476))
        lg = cv2.resize(left, (699, 476))
        stereo = cv2.StereoBM_create(16, 7)
        self.disp = stereo.compute(gray_l, gray_r).astype(np.float32)/(16)
        plt.imshow(self.disp, "gray")
        plt.show()
        r, l = self.img, self.img_2
        r = cv2.resize(r, (699, 476))
        l = cv2.resize(l, (699, 476))
        cv2.imshow('left', l)
        param = [l, r]
        cv2.setMouseCallback('left', self.click_event, param)
        while True:
            cv2.imshow('left', l)
            if cv2.waitKey(0):
                break
        cv2.destroyAllWindows()

    def click_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            left_copy = param[0].copy()
            right_copy = param[1].copy()
            cv2.circle(left_copy, (x, y), 5, (255, 0, 0), -1)
            cv2.imshow("left", left_copy)
            cv2.circle(
                right_copy, (int(x - self.disp[y][x]), y), 5, (0, 255, 0), -1)
            cv2.imshow("right", right_copy)

    def show_WORDS(self, letters, path):
        # path = self.folder_path+"/*bmp"
        fs = cv2.FileStorage('{}'.format(path), cv2.FILE_STORAGE_READ)
        text = str('{}'.format(letters))
        row = 8
        column = 11
        CHECKERBOARD = (column, row)
        shift = np.array([
            [7, 5], [4, 5], [1, 5], [7, 2], [4, 2], [1, 2]
        ])
        obj_points = []
        im_points = []

        criteria = (cv2.TERM_CRITERIA_EPS +
                    cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        points3D = np.zeros((1, column*row, 3), np.float32)
        points3D[0, :, :2] = np.mgrid[0:column, 0:row].T.reshape(-1, 2)

        image_folder = glob.glob('{}'.format(self.folder_path+"/*bmp"))
        for files in image_folder:
            image = cv2.imread(files)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(
                gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
            if ret == True:
                obj_points.append(points3D)
                corners2 = cv2.cornerSubPix(
                    gray, corners, (11, 11), (-1, -1), criteria)
                im_points.append(corners2)

                ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
                    obj_points, im_points, gray.shape[::-1], None, None)
                ret, rvecs, tvecs = cv2.solvePnP(points3D, corners2, mtx, dist)

                for v, n in enumerate(text):
                    ch = fs.getNode(n).mat()  # lines
                    number_of_points = 2*len(ch[:])
                    ch1 = np.resize(ch, (number_of_points, 3))

                    for i, x in enumerate(ch1):
                        ch1[i, 0], ch1[i, 1] = (
                            ch1[i, 0] + shift[v, 0], ch1[i, 1]+shift[v, 1])

                    # Project 3D points to image plane
                    chessboard_corners = np.float32(ch1)
                    imgpts, jac = cv2.projectPoints(
                        chessboard_corners, rvecs, tvecs, mtx, dist)
                    imgpts = imgpts.astype(int)
                    imgpts = np.ravel(imgpts)
                    q = []
                    for i, n in enumerate(imgpts):
                        q.append(n)
                        if len(q) == 4:
                            image = cv2.line(
                                image, (q[0], q[1]), (q[2], q[3]), (0, 0, 255), 10)
                            q.clear()

            image = cv2.resize(image, (900, 900))
            cv2.imshow('img', image)

            cv2.waitKey(1000)

        cv2.destroyAllWindows()
