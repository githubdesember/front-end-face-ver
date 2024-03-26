import cv2 as cv

# Global variables to store the coordinates of the selected region
start_x, start_y, end_x, end_y = -1, -1, -1, -1
drawing = False

def select_roi(event, x, y, flags, param):
    global start_x, start_y, end_x, end_y, drawing

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        start_x, start_y = x, y
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing:
            end_x, end_y = x, y
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        end_x, end_y = x, y
        print("Selected Region Coordinates: ", start_x, start_y, end_x, end_y)

# Read an image
img = cv.imread('resource/bg.jpg')

# Create a window and set mouse callback
cv.namedWindow('Select ROI')
cv.setMouseCallback('Select ROI', select_roi)

while True:
    clone = img.copy()

    if not drawing and start_x != -1 and start_y != -1 and end_x != -1 and end_y != -1:
        cv.rectangle(clone, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

    cv.imshow('Select ROI', clone)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
