import cv2
import numpy as np
import sys

def main():
  path = sys.argv[1]

  if path == None:
    print("Please enter a valid path!")
    return

  img = cv2.imread(path)
  width = np.float32(img.shape[0] / 2)
  height = np.float32(img.shape[1] / 2)

  img = cv2.resize(img, (300, 450))

  grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  blurredImg = cv2.medianBlur(grayImg, 9)

  thresholdImg = blurredImg.copy()
  edges = cv2.Canny(thresholdImg, 100, 200)


  _, thresholdImg = cv2.threshold(thresholdImg, 220, 255, cv2.THRESH_TOZERO )
  contours, hierarchy = cv2.findContours(thresholdImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


  print("Count of eggs: ", len(contours))
  outImg = np.zeros(thresholdImg.shape, dtype=np.uint8)

  # cv2.drawContours(img, contours, 6, (255, 0, 0), 2, cv2.LINE_AA)

  for i in range(0, len(contours)):
    contour = contours[i]
    area = cv2.contourArea(contour)
    rRect = cv2.minAreaRect(contour)
    area_min = 100
    area_max = 100000
    color = (0, 0, 255)
    if area_min < area < area_max:
      cv2.drawContours(img, contours, -1, (255, 0, 0), 2, cv2.LINE_AA)

    center = rRect[0]

    x_coor = int(center[0])
    y_coor = int(center[1])

    cv2.putText(img, f'{i + 1}', (x_coor, y_coor), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 255, 0), 2, cv2.LINE_AA)

  cv2.imshow("org", img)
  cv2.imshow("grayImg", grayImg)
  cv2.imshow("thresholdImg", thresholdImg)
  cv2.imshow("edges", edges)

  cv2.waitKey(0)
  cv2.destroyAllWindows()



if __name__ == "__main__":
    main()