import cv2
img = cv2.imread('./resource/img.png')
new = cv2.resize(img, (150,420), fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
cv2.imwrite('./resource/img.png', new)