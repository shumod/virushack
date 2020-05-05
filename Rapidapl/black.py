import cv2
def variance_of_laplacian(image):
	return cv2.Laplacian(image, cv2.CV_64F).var()

threshold = 100.0
imagePath =".\\dumps\\22.png"
image = cv2.imread(imagePath)
text = "Not black"
if ((cv2.sumElems(image)[0] == 0) & (cv2.sumElems(image)[1] == 0) & (cv2.sumElems(image)[2] == 0)):
	text = "Black"
print(text)
key = cv2.waitKey(0)