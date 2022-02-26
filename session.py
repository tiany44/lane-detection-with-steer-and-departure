import math
from lane_detection_lib import *

lane_detection = LaneDetection()

################################################################################
######## START - MAIN FUNCTION #################################################
################################################################################

# Read the input image
image = lane_detection.readVideo()

################################################################################
#### START - LOOP TO PLAY THE INPUT IMAGE ######################################
while True:

    _, frame = image.read()


    # Apply perspective warping by calling the "perspectiveWarp()" function
    # Then assign it to the variable called (birdView)
    # Provide this function with:
    # 1- an image to apply perspective warping (frame)
    birdView, birdViewL, birdViewR, minverse = lane_detection.perspectiveWarp(frame)


    # Apply image processing by calling the "processImage()" function
    # Then assign their respective variables (img, hls, grayscale, thresh, blur, canny)
    # Provide this function with:
    # 1- an already perspective warped image to process (birdView)
    img, hls, grayscale, thresh, blur, canny = lane_detection.processImage(birdView)
    imgL, hlsL, grayscaleL, threshL, blurL, cannyL = lane_detection.processImage(birdViewL)
    imgR, hlsR, grayscaleR, threshR, blurR, cannyR = lane_detection.processImage(birdViewR)


    # Plot and display the histogram by calling the "get_histogram()" function
    # Provide this function with:
    # 1- an image to calculate histogram on (thresh)
    hist, leftBase, rightBase = lane_detection.plotHistogram(thresh)
    # print(rightBase - leftBase)
    plt.plot(hist)
    # plt.show()


    ploty, left_fit, right_fit, left_fitx, right_fitx = lane_detection.slide_window_search(thresh, hist)
    plt.plot(left_fit)
    # plt.show()


    draw_info = lane_detection.general_search(thresh, left_fit, right_fit)
    # plt.show()


    curveRad, curveDir = lane_detection.measure_lane_curvature(ploty, left_fitx, right_fitx)


    # Filling the area of detected lanes with green
    meanPts, result = lane_detection.draw_lane_lines(frame, thresh, minverse, draw_info)


    deviation, directionDev = lane_detection.offCenter(meanPts, frame)


    # TR = WB/tan(a)
    # a = arctan(WB/TR)

    steering_angle = math.atan(2.69/curveRad)

    # Adding text to our final image
    finalImg = lane_detection.addText(result, curveRad, curveDir, deviation, directionDev, steering_angle)

    # Displaying final image
    cv2.imshow("Final", finalImg)


    # Wait for the ENTER key to be pressed to stop playback
    if cv2.waitKey(1) == 13:
        break