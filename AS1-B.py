import numpy as np
import cv2
import matplotlib.pyplot as plt
import math

finger_measurements= []
finger_points=[]

#computing the Euclidean distance between two points p1 and p2 in a 2D plane
def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2+ (p1[1]- p2[1])**2)

#this block handles mouse clicks on the image, each left click saves the position 
#in the points list and displays a red circle at that location to visualize 
#the selected point

def mouse_callback(event, x, y,flags,param):
    global finger_points, image_display
    
    if event== cv2.EVENT_LBUTTONDOWN:
        finger_points.append((x, y))

        cv2.circle(image_display, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Image", image_display)

# loading the image
image_path= "C:/Users/PC/Desktop/hand.jpeg"  
image=cv2.imread(image_path)
original_image= image.copy()

#greyscale and Black/White conversion
gray_image= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

cv2.namedWindow("Grayscale Image", cv2.WINDOW_NORMAL)
cv2.imshow("Grayscale Image", gray_image)
cv2.namedWindow("Black and White Image", cv2.WINDOW_NORMAL)
cv2.imshow("Black and White Image", thresh)

#manial measurement

image_display=original_image.copy()
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.imshow("Image", image_display)
cv2.setMouseCallback("Image", mouse_callback)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()

#calculation of measurements
fingers_number= len(finger_points)//6

for i in range(fingers_number):
    p= finger_points[i*6:(i+1)*6]
    
    length= distance(p[0], p[1])
    width_base= distance(p[2], p[3])
    width_mid =distance(p[4], p[5])
    
    finger_measurements.append((length, width_base, width_mid))

finger_lengths= [m[0] for m in finger_measurements]
finger_base_widths= [m[1] for m in finger_measurements]
finger_middle_widths= [m[2] for m in finger_measurements]

avg_finger_length= np.mean(finger_lengths)
avg_finger_base_width=np.mean(finger_base_widths)
avg_finger_middle_width= np.mean(finger_middle_widths)

print("\n--- RESULTS ---")
for i, m in enumerate(finger_measurements):
    print(f"Finger {i+1} :")
    print(f"  Length = {m[0]:.2f} pixels")
    print(f"  Base width = {m[1]:.2f} pixels")
    print(f"  Middle width = {m[2]:.2f} pixels")

print("\n--- Averages ---")
print(f"Average length : {avg_finger_length:.2f} pixels")
print(f"Average base width : {avg_finger_base_width:.2f} pixels")
print(f"Average middle width : {avg_finger_middle_width:.2f} pixels")

#visualization of the measures
 
measured_image=original_image.copy()
for i in range(fingers_number):
    p= finger_points[i*6:(i+1)*6]
    
    #Length: tip to base
    cv2.line(measured_image, p[0], p[1], (0, 255, 0), 2)
    cv2.putText(measured_image, f"L={int(distance(p[0], p[1]))}", 
                (p[0][0], p[0][1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
    
    #base width
    cv2.line(measured_image, p[2], p[3], (255, 0, 0), 2)
    #middle width
    cv2.line(measured_image, p[4], p[5], (0, 0, 255), 2)

#BGR to RGB conversion for matplotlib
measured_rgb_image= cv2.cvtColor(measured_image, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(10, 8))
plt.imshow(measured_rgb_image)
plt.title("Mesures des doigts")
plt.axis("off")
plt.show()

