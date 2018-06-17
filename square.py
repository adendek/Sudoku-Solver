import cv2
import time
import numpy as np

"""
sudo apt-get install python-opencv
sudo apt-get install python-matplotlib
"""

##################
DELAY = 0.02
USE_CAM = 1
IS_FOUND = 0

MORPH = 7
CANNY = 250

_width = 600.0
_height = 420.0
_margin = 0.0

# setup initial location of window
r, h, c, w = 250, 90, 400, 125  # simply hardcoded the values
track_window = (c, r, w, h)

video_capture = cv2.VideoCapture(0)
corners = np.array(
    [
        [[_margin, _margin]],
        [[_margin, _height + _margin]],
        [[_width + _margin, _height + _margin]],
        [[_width + _margin, _margin]]
    ]
)

pts_dst = np.array(corners, np.float32)
out = None
while True:
    if USE_CAM:
        ret, rgb = video_capture.read()
    else:
        ret = 1
        rgb = cv2.imread("opencv.jpg", 1)

    if ret:
        gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

        gray = cv2.bilateralFilter(gray, 1, 10, 120)

        edges = cv2.Canny(gray, 10, CANNY)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (MORPH, MORPH))

        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        key = cv2.waitKey(1)
        h, contours, hierarchy = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cont in contours:
            if cv2.contourArea(cont) > 5000:

                arc_len = cv2.arcLength(cont, True)

                approx = cv2.approxPolyDP(cont, 0.1 * arc_len, True)

                if len(approx) == 4:
                    IS_FOUND = True
                    pts_src = np.array(approx, np.float32)
                    h, status = cv2.findHomography(pts_src, pts_dst)
                    out = cv2.warpPerspective(rgb, h, (int(_width + _margin * 2), int(_height + _margin * 2)))
                    cv2.drawContours(rgb, [approx], -1, (255, 0, 0), 3)

                else:
                    pass

        # cv2.imshow( 'closed', closed )
        # cv2.imshow( 'gray', gray )

        cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
        cv2.imshow('edges', edges)  # edges

        cv2.namedWindow('rgb', cv2.WINDOW_NORMAL)
        cv2.imshow('rgb', rgb)  # rgb picture

        if IS_FOUND:
            # rectangle coordinates are in pts_src
            print("rectangle found")
            cv2.namedWindow('out', cv2.WINDOW_NORMAL)
            cv2.imshow('out', out)
            if key%256 == 32:
                img_name = "opencv_frame_{}.png".format(0)
                cv2.imwrite(img_name, out)
                print("{} written!".format(img_name))
        if cv2.waitKey(27) & 0xFF == ord('q'):  # press q for quiting
            break

        time.sleep(DELAY)

    else:
        break

if USE_CAM:
    video_capture.release()
cv2.destroyAllWindows()