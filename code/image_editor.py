# command line
# python load_display_save.py --image ../images/trex.png

# import packages
import numpy as np
import cv2

def flip(image):
    return cv2.flip(image, 1)

def overlay(image1, image2):
# function to add a cupcake image to the original image
    #280, 195
    return image1

def drawRectangle(image, color, point1, poin2):
    cv2.rectangle(image, point1, point2, color, -1)
    return image

def addBorder(image, color):
# function to add a red, green or blue border to an image

    red = (0, 0, 255)
    green = (0, 255, 0)
    blue = (255, 0, 0)

    while True:
        # if color is valid
        if color == "red" or color == "green" or color == "blue":
            if color == "red":
                BGRColor = red
            elif color == "green":
                BGRColor = green
            else:
                BGRColor = blue
            # set four borders
            image[0:image.shape[0], 0:5] = BGRColor
            image[0:image.shape[0], image.shape[1]-5:image.shape[1]] = BGRColor
            image[0:5, 0:image.shape[1]] = BGRColor
            image[image.shape[0]-5:image.shape[0], 0:image.shape[1]] = BGRColor

            # return image with borders
            return image
        # if color is invalid
        else:
            color = input("Please pick between red, green, and blue: ")

# welcome user
print("Hello! Welcome to image editor. Today we will be editing this picture of \
Appa the flying bison! (Press any key for the next step)")

# load image
image = cv2.imread("/Users/michellewang/Desktop/IntroToCV/images/appa.png")

# display image, wait for keypress
cv2.imshow("Original Appa", image)
cv2.waitKey(0)

# prompt user for border color
borderColor = input("First, let's add a border. Please enter color you would like \
the border to be. You may choose red, green, or blue: ").lower()

# add border
image = addBorder(image, borderColor)

# clear original, display updated image, wait for keypress to add platform
cv2.destroyAllWindows()
cv2.imshow("Appa with Border", image)
print("Nice! Now, Appa is currently flying in mid-air. Let's add a platform for \
him to land on. (Press any key to add a platform)")
cv2.waitKey(0)

# add platform
platformColor = (13, 26, 40)
point1 = (95, 280)
point2 = (395, 295)
image = drawRectangle(image, platformColor, point1, point2)

# clear original, display updated image, wait for keypress
cv2.destroyAllWindows()
cv2.imshow("Appa on platform", image)
print("Awesome! (Press any key for the next step)")
cv2.waitKey(0)

# add cupcake
cupcakeImage = cv2.imread("/Users/michellewang/Desktop/IntroToCV/images/cupcake.png", cv2.IMREAD_UNCHANGED)
image = overlay(image, cupcakeImage)

# clear original, display updated image, wait for keypress to flip image
cv2.destroyAllWindows()
cv2.imshow("A cupcake!", image)
print("Look, a cupcake! Appa is hungry and he wants to eat the cupcake. However, \
he is facing the wrong way. Let's flip him so that he can eat the cupcake. \
(Press any key to flip Appa)")
cv2.waitKey(0)

# flip image
image = flip(image)
# clear original, display updated image, wait for keypress
cv2.destroyAllWindows()
cv2.imshow("A cupcake!", image)
print("Yum :)")
cv2.waitKey(0)


# Save the image -- OpenCV handles converting filetypes automatically
#cv2.imwrite("newimage.jpg", image)
