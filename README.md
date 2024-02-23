# OpenCV-Computer-Vision Practice third



*Discription:*

***1.This is just a small project that we want to practice the camera calibration and stereo vision for 3D reconstruction.***
***2.This topic focuses on image processing to find image contours,calibrate chessboards,create simple AR,and reconstruct reality using stereo vision.***
![image](GUI.png)


**1.Requirements and dependencies**
  * Python 3.7 (https://www.python.org/downloads/)
  * Opencv-contrib-python (3.4.2.17)
  * Matplotlib 3.1.1
  * UI framework: pyqt5 (5.15.1)

**2.Usage:**

1. Downloads whole repository.
2. Run `python start.py` .
3. Input the image.
4. Run the whole code.

**3.Feature:**

1.Find contour

* 1.1 Draw contour :
  
    * Convert the RGB image [Build.jpg](Figures/Building.jpg) into a grayscale image, then smooth it by your own 3x3 Gaussian smoothing filter .
      
      ![image](Figures/Gaussian_result.png)
* 1.2 Count rings :
  
    * Use Sobel edge detection to detect vertical edge by your own 3x3 Sobel X operator.
      
      ![image](Figures/Sobel_X.png)

2.Camera calibration

* 2.1 Find chessboard corners:
  
   * From (430,430) to (215,215).

![image](Figures/Microsoft.png)

* 2.2 Find Intrinsic matrix:
  
   * Xnew = Xold + 215 pixels = 108 + 215 = 323.
   * Ynew = Yold + 215 pixels = 108 + 215 = 323.
   * Point C (108, 108) is center of resized image.
   * Point C’(323, 323) is new center of image. 

![image](Figures/Translate.png)

* 2.3 Find Extrinsic matrix:
  
   * Center: Center of Image.
   * Angle = 45 $^{\circ}$ (counter-clockwise).
   * Scale = 0.5.
   * window size (430,430)

![image](Figures/Rotate.png)
  
* 2.4 Find distortion:
  
   * Old location: ([[50,50],[200,50],[50,200]])
   * New location: ([[10,100],[100,50],[100,250]]) 

![image](Figures/Sharing.png)
* 2.5 Processing result:


3.Augmented reality (AR)

* 3.1 Show the word on board:
  
   * From (430,430) to (215,215).

![image](Figures/Microsoft.png)

* 3.2 Show words vertically:
  
   * From (430,430) to (215,215).

![image](Figures/Microsoft.png)



4.Stereo disparity map
* 4.1 Show the map:
  
   * From (430,430) to (215,215).

![image](Figures/Microsoft.png)

