import io
import numpy as np
from matplotlib import pyplot as plt
import cv2
from PIL import Image, ImageFilter

# Load the image
image_path = 'images\star.jpg'
image = cv2.imread(image_path)

text_area1 = (0, 0, 2499,500)  # Example coordinates, you may need to change these
text_area2 = (0, 480, 580, 910)  # Example coordinates, you may need to change these
text_area3 = (0, 1000, 290, 3499)  # Example coordinates, you may need to change these
text_area4 = (0, 3250,2499, 3499)


image = cv2.rectangle(image, (0, 0), (2499, 475), (255, 255, 255), -1)
image = cv2.rectangle(image, (0, 480), (580, 910), (255, 255, 255), -1)
image = cv2.rectangle(image, (0, 1000), (290, 3499), (255, 255, 255), -1)
image = cv2.rectangle(image, (0, 1500), (260, 2000), (255, 255, 255), -1)
image = cv2.rectangle(image, (0, 3250), (2499, 3499), (255, 255, 255), -1)
blurred_image_path = 'images\starr.jpg'
cv2.imwrite(blurred_image_path, image)
plt.imshow(image)
plt.show()
cv2.waitKey(0)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.medianBlur(gray, 5)
circles = cv2.HoughCircles(
    gray,
    cv2.HOUGH_GRADIENT,
    dp=1,
    minDist=30,
    param1=75,
    param2=13,
    minRadius=8,
    maxRadius=20
)

note_line_1=[]
note_line_2=[]
note_line_3=[]
note_line_4=[]
note_line_5=[]
note_line_6=[]
note1 = []
note2 = []
note3 = []  
note4 = []
note5 = []
note6 = []
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # 绘制外圆
        print(i)
        cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # 绘制圆心
        cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)
        if(i[1]>500 and i[1]<750):
                note_line_1.append(i)
        elif(i[1]>750 and i[1]<1000):
            note_line_2.append(i)
        elif(i[1]>1000 and i[1]<1250):
            note_line_3.append(i)
        elif(i[1]>1250 and i[1]<1500):
            note_line_4.append(i)
        elif(i[1]>1500 and i[1]<1750):
            note_line_5.append(i)
        elif(i[1]>1750 and i[1]<2000 and i[0]<2275):
            note_line_6.append(i)
        else:
            continue
plt.imshow(image)
plt.show()
note_line_1.sort(key=lambda x: x[0]+x[1])
note_line_2.sort(key=lambda x: x[0]+x[1])
note_line_3.sort(key=lambda x: x[0]+x[1])  
note_line_4.sort(key=lambda x: x[0]+x[1])
note_line_5.sort(key=lambda x: x[0]+x[1])
note_line_6.sort(key=lambda x: x[0]+x[1])
for i in note_line_1:
    note1.append(int(i[0]))
for i in note_line_2:
    note2.append(int(i[0]))
for i in note_line_3:
    note3.append(int(i[0]))
for i in note_line_4:
    note4.append(int(i[0]))
for i in note_line_5:
    note5.append(int(i[0]))
for i in note_line_6:
    note6.append(int(i[0]))       
    
print('1:   ',   note_line_1)
print('2:   ',   note_line_2)
print('3:   ',   note_line_3)  
print('4:   ',   note_line_4)
print('5:   ',   note_line_5)
print('6:   ',   note_line_6)



