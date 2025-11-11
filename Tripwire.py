import cv2

# Load and resize image
img = cv2.imread("cam1.jpg")
TARGET_WIDTH, TARGET_HEIGHT = 640, 480
img = cv2.resize(img, (TARGET_WIDTH, TARGET_HEIGHT))
clone = img.copy()

wire_start = None
wire_end = None
click_count = 0

def draw_tripwire(event, x, y, flags, param):
    global wire_start, wire_end, click_count, img

    if event == cv2.EVENT_LBUTTONDOWN:
        if click_count == 0:
            wire_start = (x, y)
            click_count = 1
        elif click_count == 1:
            wire_end = (x, y)
            click_count = 2

            # Draw line (tripwire)
            cv2.line(img, wire_start, wire_end, (0, 0, 255), 2)

            # Draw coordinate text
            coord_text = f"{wire_start} to {wire_end}"
            cv2.putText(img, coord_text, (wire_start[0], wire_start[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            print(f"Tripwire coordinates: {coord_text}")

            # Save to text file
            with open("tripwire_coords.txt", "w") as f:
                f.write(f"{wire_start[0]},{wire_start[1]},{wire_end[0]},{wire_end[1]}")

# Set up window and callback
cv2.namedWindow("Define Tripwire")
cv2.setMouseCallback("Define Tripwire", draw_tripwire)

while True:
    cv2.imshow("Define Tripwire", img)
    key = cv2.waitKey(1)
    if key == ord("r"):  # Reset wire
        img = clone.copy()
        click_count = 0
        wire_start = None
        wire_end = None
    elif key == ord("q"):
        break

cv2.destroyAllWindows()
