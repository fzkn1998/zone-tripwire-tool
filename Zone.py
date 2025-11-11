import cv2

# Load and resize image
img = cv2.imread("Cam1.jpg")
TARGET_WIDTH, TARGET_HEIGHT = 640, 480
img = cv2.resize(img, (TARGET_WIDTH, TARGET_HEIGHT))
clone = img.copy()

zone_start = None
zone_end = None
drawing = False

def draw_zone(event, x, y, flags, param):
    global zone_start, zone_end, drawing, img

    if event == cv2.EVENT_LBUTTONDOWN:
        zone_start = (x, y)
        drawing = True

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        img = clone.copy()
        cv2.rectangle(img, zone_start, (x, y), (0, 255, 0), 2)

    elif event == cv2.EVENT_LBUTTONUP:
        zone_end = (x, y)
        drawing = False
        cv2.rectangle(img, zone_start, zone_end, (0, 255, 0), 2)

        # Draw coordinate text on image
        coord_text = f"{zone_start} to {zone_end}"
        cv2.putText(img, coord_text, (zone_start[0], zone_start[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        print(f"Zone coordinates: {coord_text}")

        # Save coordinates to a text file
        with open("zone_coords.txt", "w") as f:
            f.write(f"{zone_start[0]},{zone_start[1]},{zone_end[0]},{zone_end[1]}")

# Set up window and mouse callback
cv2.namedWindow("Draw Zone")
cv2.setMouseCallback("Draw Zone", draw_zone)

while True:
    cv2.imshow("Draw Zone", img)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cv2.destroyAllWindows()
