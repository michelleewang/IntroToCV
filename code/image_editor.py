# import packages
import numpy as np
import cv2

def flipHorizontally(image):
# function to flip/reflect an image horizontally

    return cv2.flip(image, 1)

def overlay(background, overlay):
# function to "overlay" an image onto another image using masks
# NOTE: IMAGES MUST BE THE SAME SIZE!!!

    # choose region to put the overlay image, roi = region of interest
    rows,cols,channels = overlay.shape
    roi = background[0:rows, 0:cols ]

    # create an inverse mask for the overlay
    overlaygray = cv2.cvtColor(overlay,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(overlaygray, 250, 255, cv2.THRESH_BINARY_INV)
    mask_inv = cv2.bitwise_not(mask)

    # black out the area where the overlay will be on the background image
    background_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
    # extract overlay image region from the image (black out the background)
    overlay_fg = cv2.bitwise_and(overlay,overlay,mask = mask)

    # add two images togethe using bitwise add(), black areas in both images will be filled
    out_img = cv2.add(background_bg,overlay_fg)
    background[0:rows, 0:cols ] = out_img

    return out_img

def drawRectangle(image, color, point1, point2):
# function to draw a rectangle
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

    return image

# welcome user
print("Hello! Welcome to image editor. Today we will be editing this picture of \
Appa the flying bison! (Press any key for the next step)")

# load images
image = cv2.imread("/Users/michellewang/Desktop/IntroToCV/images/appa.png")
cupcakeImage = cv2.imread("/Users/michellewang/Desktop/IntroToCV/images/cupcake.png")

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
point1 = (int(image.shape[1]*0.2), int(image.shape[0]*0.84))
print(point1)
point2 = (int(image.shape[1]*0.8), int(image.shape[0]*0.89))
print(point2)
image = drawRectangle(image, platformColor, point1, point2)

# clear original, display updated image, wait for keypress to add cupcake
cv2.destroyAllWindows()
cv2.imshow("Appa on platform", image)
print("Awesome! (Press any key for the next step)")
cv2.waitKey(0)

# create a copy of both images to edit
imageCopy = np.copy(image)

# add cupcake
imageWithCupcake = overlay(imageCopy, cupcakeImage)

# clear original, display updated image, wait for keypress to flip image
cv2.destroyAllWindows()
cv2.imshow("A cupcake!", imageWithCupcake)
print("Look, a cupcake! Appa is hungry and he wants to eat the cupcake. However, \
he is facing the wrong way. Let's flip him so that he can eat the cupcake. \
(Press any key to flip Appa)")
cv2.waitKey(0)

# flip image and add cupcake again
image = overlay(flipHorizontally(image), cupcakeImage)

# clear original, display updated image, wait for keypress
cv2.destroyAllWindows()
cv2.imshow("A cupcake!", image)
print("Yum :)")
cv2.waitKey(0)


# Save the image -- OpenCV handles converting filetypes automatically
#cv2.imwrite("newimage.jpg", image)
