import cv2
import matplotlib.pyplot as plt

# simply counts the peanut(s) on the screen and shows the result on the screen as a text.
def findCountrsInImage(image):
  contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

  contours_count = 0
  for cnt in contours:
    area = cv2.contourArea(cnt)
    area_min = 200
    area_max = 100000
    color = (0, 0, 255)
    if area_min < area < area_max:
      cv2.drawContours(img, [cnt], -1, color, -1)
      contours_count += 1

  return contours_count
def resultText(contours_count):
  width = img.shape[1]
  mid_width = int(width / 2)

  cv2.putText(img, f'Total: {contours_count}', (mid_width, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)

def plotDrawImage(x, y, img, title):
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  loc[x, y].imshow(img)
  loc[y, y].set_title(title)

img = cv2.imread("../resources/peanut.png")
img = cv2.resize(img, (600, 400))
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

blurred = cv2.blur(imgGray, (12, 12), 0)
_, thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY_INV)

masked = cv2.bitwise_and(img, img, mask=thresh)
cv2.imshow("masked", masked)

canny = cv2.Canny(thresh, 20, 200)

contours_count = findCountrsInImage(thresh)
resultText(contours_count)

f, loc = plt.subplots(2, 2)

plotDrawImage(0, 0, img, 'result image')
plotDrawImage(0, 1, canny, 'canny')
plotDrawImage(1, 0, thresh, 'thresh')
plotDrawImage(1, 1, imgGray, 'gray')

plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()