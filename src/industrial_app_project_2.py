import cv2
import numpy as np

def n(x):
  pass

cv2.namedWindow("Mask Settings")
cv2.resizeWindow("Mask Settings", 500, 250)

cv2.namedWindow("Threshold Settings")
cv2.resizeWindow("Threshold Settings", 500, 70)

cv2.createTrackbar("Thresh-Min", "Threshold Settings", 0, 255, n)
cv2.createTrackbar("Thresh-Max", "Threshold Settings", 0, 255, n)

cv2.createTrackbar("Lower-H", "Mask Settings", 0, 180, n)
cv2.createTrackbar("Lower-S", "Mask Settings", 0, 255, n)
cv2.createTrackbar("Lower-V", "Mask Settings", 0, 255, n)

cv2.createTrackbar("Upper-H", "Mask Settings", 0, 180, n)
cv2.createTrackbar("Upper-S", "Mask Settings", 0, 255, n)
cv2.createTrackbar("Upper-V", "Mask Settings", 0, 255, n)

# ##################################################################################

cv2.setTrackbarPos("Thresh-Min", "Threshold Settings", 221)
cv2.setTrackbarPos("Thresh-Max", "Threshold Settings", 255)

cv2.setTrackbarPos("Lower-H", "Mask Settings", 82)
cv2.setTrackbarPos("Lower-S", "Mask Settings", 0)
cv2.setTrackbarPos("Lower-V", "Mask Settings", 149)

cv2.setTrackbarPos("Upper-H", "Mask Settings", 180)
cv2.setTrackbarPos("Upper-S", "Mask Settings", 255)
cv2.setTrackbarPos("Upper-V", "Mask Settings", 255)


def findCountrsInImage(frameImg, showImage):
  contours, hierarchy = cv2.findContours(frameImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
  hull = []

  contours_count = 0
  print("Count of eggs: ", len(contours))

  bg = np.zeros((frameImg.shape[0], frameImg.shape[1], 3), np.uint8)

  for i in range(0, len(contours)):
    contour = contours[i]
    hull.append(cv2.convexHull(contour, False))
    area = cv2.contourArea(contour)
    rRect = cv2.minAreaRect(contour)

    area_min = 100
    area_max = 100000
    color = (0, 0, 255)
    if (area_min < area < area_max):
      center = rRect[0]

      x_coor = int(center[0])
      y_coor = int(center[1])
      cv2.putText(showImage, f'*', (x_coor - 15, y_coor + 5), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 255, 0), 2, cv2.LINE_AA)

      epsilon = 0.01 * cv2.arcLength(contours[i], True)
      approx = cv2.approxPolyDP(contours[i], epsilon, True)
      cv2.drawContours(bg, [approx], -1, (0, 0, 255), 3)

      x, y, w, h = cv2.boundingRect(contours[i])
      cv2.rectangle(showImage, (x - 20, y), (x + w, y + h), (0, 255, 0), 2)

    contours_count += 1

  cv2.imshow("approx", bg)
  return contours_count

def resultText(contours_count):
  cv2.putText(frame, f'Count of eggs: {contours_count}', (0, 50), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 255, 0), 1,
              cv2.LINE_AA)


cap = cv2.VideoCapture("../resources/eggsVideo.mp4")

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

  lh = cv2.getTrackbarPos("Lower-H", "Mask Settings")
  ls = cv2.getTrackbarPos("Lower-S", "Mask Settings")
  lv = cv2.getTrackbarPos("Lower-V", "Mask Settings")
  uh = cv2.getTrackbarPos("Upper-H", "Mask Settings")
  us = cv2.getTrackbarPos("Upper-S", "Mask Settings")
  uv = cv2.getTrackbarPos("Upper-V", "Mask Settings")

  lower_b = np.array([lh, ls, lv])
  upper_b = np.array([uh, us, uv])

  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

  mask = cv2.inRange(hsv, lowerb=lower_b, upperb=upper_b)

  bitwise_and = cv2.bitwise_and(frame, frame, mask=mask)
  maskedEggs = bitwise_and.copy()

  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
  morphClose = cv2.morphologyEx(thresholdImg, cv2.MORPH_CLOSE, kernel)
  _, thresholdImg = cv2.threshold(morphClose, tmin, tmax, cv2.THRESH_TOZERO)

  contours_count = findCountrsInImage(thresholdImg, maskedEggs)

  resultText(contours_count)

  cv2.imshow("video", frame)
  cv2.imshow("thresh", thresholdImg)
  cv2.imshow("blurred", frameBlurred)
  cv2.imshow("edges", edges)
  cv2.imshow("bitwise_and", bitwise_and)
  cv2.imshow("mask", mask)
  cv2.imshow("masked eggs", maskedEggs)

  key = cv2.waitKey(30)

  if key == ord('q'):
    break
  if key == ord('p'):
    cv2.waitKey(-1)

cap.release()
cv2.destroyAllWindows()
