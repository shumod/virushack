import cv2
def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv2.Laplacian(image, cv2.CV_64F).var()
# construct the argument parse and parse the arguments
threshold = 100.0
imagePath =".\\dumps\\22.png"
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
fm = variance_of_laplacian(gray)
text = "Not Blurry"
# if the focus measure is less than the supplied threshold,
# then the image should be considered "blurry"
if fm < threshold:
	text = "Blurry"
# show the image
#cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30),
	#cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
#cv2.imshow("Image", image)
print("{}: {:.2f}".format(text, fm))
key = cv2.waitKey(0)