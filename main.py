import cv2
import numpy as np
from sklearn.cluster import KMeans

path = "tables/4.jpg"

# Read the image
image = cv2.imread(path)

# Initialize parameters T and TH
T = 100
TH = 100
threshold_value = 10
les_y = []
les_x = []
sorted_data_les_y = []
sorted_data_les_x = []
filtered_data_les_y = []
filtered_data_les_x = []

# Create a window and display the image
cv2.namedWindow("Table Lines")
cv2.imshow("Table Lines", image)


# Callback function for trackbar T
def update_T(value):
    global T
    T = value
    update_lines()

# Callback function for trackbar TH
def update_TH(value):
    global TH
    TH = value
    update_lines()

def update_threshold_value(value):
    global threshold_value
    threshold_value = value
    update_lines()

# Callback function to update lines based on T and TH
def update_lines():
    global image, threshold_value, T, TH, les_y, les_x, sorted_data_les_y, sorted_data_les_x, filtered_data_les_y, filtered_data_les_x

    print('************************************************')
    try :
        image = cv2.imread(path)
        _, gray = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)

        # Reset les_y and les_x
        les_y = []
        les_x = []

        #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Perform edge detection
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        # Hough Line Transform
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=5)

        # Extract line endpoints and convert to a format suitable for clustering
        line_points = np.array([[line[0][0], line[0][1], line[0][2], line[0][3]] for line in lines])

        # Use k-means clustering to group lines
        num_clusters = 2  # You can adjust this based on the number of connected line groups you expect
        kmeans = KMeans(n_clusters=num_clusters)
        kmeans.fit(line_points)
        labels = kmeans.labels_

        # Draw lines and color them based on clusters
        for i, line in enumerate(lines):
            x1, y1, x2, y2 = line[0]
            color = (0, 0, 255) if labels[i] == 0 else (255, 0, 0)
            if abs(x2 - x1) < 10:
                cv2.line(image, (x1, y1), (x2, y2), color, 2)
                les_y.append(x1)
            if abs(y2 - y1) < 10:
                if abs(x1 - x2) > 90:
                    cv2.line(image, (x1, y1), (x2, y2), color, 2)
                    les_x.append(y1)

        # Update lines if T is changed
        if T != sorted_data_les_y:
            # Sort the list in ascending order
            sorted_data_les_y = sorted(les_y)

        # Initialize a new list to store filtered elements
        filtered_data_les_y = [sorted_data_les_y[0]]

        # Iterate through the sorted list and add elements to the new list if the distance is greater than or equal to T
        for i in range(1, len(sorted_data_les_y)):
            if sorted_data_les_y[i] - filtered_data_les_y[-1] >= T:
                filtered_data_les_y.append(sorted_data_les_y[i])

        print(filtered_data_les_y)
        print("\n")

        image = cv2.imread(path)
        _, image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)


        # Draw vertical lines on the image
        vertical_line_positions = filtered_data_les_y
        for x in vertical_line_positions:
            cv2.line(image, (x, 0), (x, image.shape[0]), (0, 0, 255), 5)

        # Update lines if TH is changed
        if TH != sorted_data_les_x:
            # Sort the list in ascending order
            sorted_data_les_x = sorted(les_x)
    except:
        pass

    # Initialize a new list to store filtered elements
    try :
        filtered_data_les_x = [sorted_data_les_x[0]]
    except:
        pass

    # Iterate through the sorted list and add elements to the new list if the distance is greater than or equal to TH
    for i in range(1, len(sorted_data_les_x)):
        if sorted_data_les_x[i] - filtered_data_les_x[-1] >= TH:
            filtered_data_les_x.append(sorted_data_les_x[i])

    print(filtered_data_les_x)

    # Draw horizontal lines on the image
    horizontal_line_positions = filtered_data_les_x
    for y in horizontal_line_positions:
        cv2.line(image, (0, y), (image.shape[1], y), (0, 0, 255), 2)

    ####################
    # Apply thresholding

    thresholded = image

    # Resize the image for display
    height, width = thresholded.shape[:2]
    max_dim = 900  # You can adjust the maximum dimension for display
    if max(height, width) > max_dim:
        scale_factor = max_dim / max(height, width)
        thresholded = cv2.resize(thresholded, None, fx=scale_factor, fy=scale_factor)

    ############

    # Display the updated image
    cv2.imshow("Table Lines", thresholded)





# Create trackbars for T and TH
cv2.createTrackbar("T", "Table Lines", T, 100, update_T)
cv2.createTrackbar("TH", "Table Lines", TH, 100, update_TH)
cv2.createTrackbar("thresholded", "Table Lines", threshold_value, 255, update_threshold_value)

# Initial lines update
update_lines()

# Wait for user input and close on 'esc' key
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # 'esc' key to exit
        break

cv2.destroyAllWindows()
