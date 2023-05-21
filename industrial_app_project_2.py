import cv2
import numpy as np

def n(x):
    pass

cv2.namedWindow("Mask Settings")
cv2.resizeWindow("Mask Settings", 500, 250)

cv2.namedWindow("Threshold Settings")
cv2.resizeWindow("Threshold Settings", 500, 250)

cv2.createTrackbar("Thresh-Min", "Threshold Settings", 0, 255, n)
cv2.createTrackbar("Thresh-Max", "Threshold Settings", 0, 255, n)

cv2.createTrackbar("Lower-H", "Mask Settings", 0, 180, n)
cv2.createTrackbar("Lower-S", "Mask Settings", 0, 255, n)
cv2.createTrackbar("Lower-V", "Mask Settings", 0, 255, n)

cv2.createTrackbar("Upper-H", "Mask Settings", 0, 180, n)
cv2.createTrackbar("Upper-S", "Mask Settings", 0, 255, n)
cv2.createTrackbar("Upper-V", "Mask Settings", 0, 255, n)


# ##################################################################################

cv2.setTrackbarPos("Thresh-Min", "Threshold Settings", 222)
cv2.setTrackbarPos("Thresh-Max", "Threshold Settings", 255)

cv2.setTrackbarPos("Lower-H", "Mask Settings", 154)
cv2.setTrackbarPos("Lower-S", "Mask Settings", 118)
cv2.setTrackbarPos("Lower-V", "Mask Settings", 144)

cv2.setTrackbarPos("Upper-H", "Mask Settings", 180)
cv2.setTrackbarPos("Upper-S", "Mask Settings", 255)
cv2.setTrackbarPos("Upper-V", "Mask Settings", 255)

def findCountrsInImage(frame, showImage):
  contours, _ = cv2.findContours(thresholdImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
  contours_count = 0
  print("Count of eggs: ", len(contours))

  for i in range(0, len(contours)):
    contour = contours[i]
    area = cv2.contourArea(contour)
    rRect = cv2.minAreaRect(contour)

    area_min = 10
    area_max = 100000
    color = (0, 0, 255)
    if(area_min < area < area_max):
      cv2.drawContours(masked, contour, -1, color, 2)

      center = rRect[0]

      x_coor = int(center[0])
      y_coor = int(center[1])

      cv2.putText(masked, f'*', (x_coor - 15, y_coor + 5), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 255, 0), 2, cv2.LINE_AA)

    contours_count += 1

  return contours_count

def resultText(contours_count):
  cv2.putText(frame, f'Count of egges: {contours_count}', (0, 50), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 255, 0), 1, cv2.LINE_AA)

cap = cv2.VideoCapture("eggsVideo.mp4")

while True:
  ret, frame = cap.read()
  frame = cv2.resize(frame, (300, 450))

  if ret == 0:
    break

  frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  frameBlurred = cv2.medianBlur(frameGray, 11)

  thresholdImg = frameBlurred.copy()
  edges = cv2.Canny(thresholdImg, 100, 200)

  tmin = cv2.getTrackbarPos("Thresh-Min", "Threshold Settings")
  tmax = cv2.getTrackbarPos("Thresh-Max", "Threshold Settings")

  _, thresholdImg = cv2.threshold(thresholdImg, tmin, tmax, cv2.THRESH_TOZERO)

  lh = cv2.getTrackbarPos("Lower-H", "Mask Settings")
  ls = cv2.getTrackbarPos("Lower-S", "Mask Settings")
  lv = cv2.getTrackbarPos("Lower-V", "Mask Settings")
  uh = cv2.getTrackbarPos("Upper-H", "Mask Settings")
  us = cv2.getTrackbarPos("Upper-S", "Mask Settings")
  uv = cv2.getTrackbarPos("Upper-V", "Mask Settings")

  lower_b = np.array([lh, ls, lv])
  upper_b = np.array([uh, us, uv])
  mask = cv2.inRange(frame, lowerb=lower_b, upperb=upper_b)
  masked = cv2.bitwise_and(frame, frame, mask=mask)


  contours_count = findCountrsInImage(thresholdImg, masked)
  resultText(contours_count)

  cv2.imshow("video", frame)
  cv2.imshow("thresh", thresholdImg)
  cv2.imshow("blurred", frameBlurred)
  cv2.imshow("edges", edges)
  cv2.imshow("masked", masked)

  key = cv2.waitKey(30)

  if key == ord('q'):
    break
  if key == ord('p'):
    cv2.waitKey(-1)

cap.release()
cv2.destroyAllWindows()