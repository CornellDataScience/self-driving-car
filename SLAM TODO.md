Initialize only takes current & reference frames (See [Here](https://github.com/raulmur/ORB_SLAM/blob/master/src/Initializer.cc), line 44)

* Find matching points from keypoints
* Use matching points to construct matrices
  * A homography and the fundamental matrix
  * Based on scores, use one or the other
* Use matrices to guess camera rotation and translation
* Use camera position guesses to calculate 3D map points

(Above 2 are simultaneous, see `checkRT` in above link)



Once initialized we can create initial map using 

We can then iteratively compare new frames to current map

- Much more complicated then it sounds though