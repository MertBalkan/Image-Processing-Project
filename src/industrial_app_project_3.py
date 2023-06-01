import cv2
import numpy as np
import sys

contours_count = 0


def n(x):
    pass


def findCountrsInImage(frameImg, showImage, frame):
    contours, hierarchy = cv2.findContours(
        frameImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    try:
        hierarchy = hierarchy[0]
    except:
        hierarchy = []
    hull = []
    global contours_count

    print("Count of eggs: ", contours_count)
    bg = np.zeros((frameImg.shape[0], frameImg.shape[1], 3), np.uint8)

    for contour, hier in zip(contours, hierarchy):
        (x, y, w, h) = cv2.boundingRect(contour)
        if x > 65 and x < 70:
            contours_count += 1

    resultText(contours_count, frame)

    for i in range(0, len(contours)):
        contour = contours[i]
        hull.append(cv2.convexHull(contour, False))
        area = cv2.contourArea(contour)

        area_min = 100
        area_max = 1000

        color = (255, 0, 255)
        if (area_min < area < area_max):
            M = cv2.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            cv2.circle(showImage, (cX, cY), 5, color, -1)

            epsilon = 0.01 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            cv2.drawContours(bg, [approx], -1, (0, 0, 255), 3)

            ellipse = cv2.fitEllipse(contour)
            cv2.ellipse(showImage, ellipse, (0, 255, 0), 3)

    # cv2.namedWindow("approx", cv2.WINDOW_NORMAL)
    # cv2.imshow("approx", bg)
    return contours_count


def resultText(contours_count, frame):
    cv2.putText(frame, f'Count of eggs: {contours_count}', (0, 50), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 255, 0), 1,
                cv2.LINE_AA)


def main():
    try:
        path = sys.argv[1]
    except:
        print("Please enter a valid path")
        return

    cap = cv2.VideoCapture(path)  # ../resources/eggsVideo.mp4

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

    cv2.setTrackbarPos("Lower-H", "Mask Settings", 0)
    cv2.setTrackbarPos("Lower-S", "Mask Settings", 0)
    cv2.setTrackbarPos("Lower-V", "Mask Settings", 149)

    cv2.setTrackbarPos("Upper-H", "Mask Settings", 180)
    cv2.setTrackbarPos("Upper-S", "Mask Settings", 33)
    cv2.setTrackbarPos("Upper-V", "Mask Settings", 255)

    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (300, 450))

        roi = frame[0:, 0:80]

        if ret == 0:
            break

        frameGray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        frameBlurred = cv2.medianBlur(frameGray, 13)

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

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lowerb=lower_b, upperb=upper_b)

        bitwise_and = cv2.bitwise_and(roi, roi, mask=mask)
        maskedEggs = bitwise_and.copy()

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (14, 14))
        morphClose = cv2.morphologyEx(mask, cv2.MORPH_RECT, kernel)
        _, thresholdImg = cv2.threshold(
            morphClose, tmin, tmax, cv2.THRESH_BINARY)

        contours_count = findCountrsInImage(thresholdImg, roi, frame)

        cv2.line(frame, (50, 0), (50, 500), (0, 255, 255), 2)
        cv2.line(frame, (70, 0), (70, 500), (0, 255, 255), 2)

        roi = cv2.resize(roi, (50, 400))

        cv2.namedWindow("final", cv2.WINDOW_NORMAL)
        # cv2.namedWindow("thresh", cv2.WINDOW_NORMAL)
        # cv2.namedWindow("roi", cv2.WINDOW_NORMAL)
        # cv2.namedWindow("blurred", cv2.WINDOW_NORMAL)
        # cv2.namedWindow("edges", cv2.WINDOW_NORMAL)
        # cv2.namedWindow("bitwise_and", cv2.WINDOW_NORMAL)
        # cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
        # cv2.namedWindow("masked eggs", cv2.WINDOW_NORMAL)
        #
        cv2.imshow("final", frame)
        # cv2.imshow("thresh", thresholdImg)
        # cv2.imshow("blurred", frameBlurred)
        # cv2.imshow("edges", edges)
        # cv2.imshow("bitwise_and", bitwise_and)
        # cv2.imshow("mask", mask)
        # cv2.imshow("masked eggs", maskedEggs)
        # cv2.imshow("roi", roi)

        key = cv2.waitKey(30)

        if key == ord('q'):
            break
        if key == ord('p'):
            cv2.waitKey(-1)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
