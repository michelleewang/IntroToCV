# import packages
import numpy as np
import cv2

def overlay(background, overlay):
# function to "overlay" an image onto another image using masks
# NOTE: IMAGES MUST BE THE SAME SIZE!!!

    # choose region to put the overlay image, roi = region of interest
    rows,cols,channels = overlay.shape
    roi = background[0:rows, 0:cols]

    # create an inverse mask for the overlay, use thresholding to 'black out'
    # parts of the image that are white (the background)
    overlaygray = cv2.cvtColor(overlay,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(overlaygray, 250, 255, cv2.THRESH_BINARY_INV)
    mask_inv = cv2.bitwise_not(mask)

    # black out the area where the overlay will be on the background image
    background_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
    # extract overlay image region from the image (black out the background)
    overlay_fg = cv2.bitwise_and(overlay,overlay,mask = mask)

    # add two images togethe using bitwise add(), black areas in both images will be filled
    result = cv2.add(background_bg,overlay_fg)
    background[0:rows, 0:cols] = result

    return result

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

def transition(image, title, text):
# transition function that clears the current image, displays the new image, and
# waits for a keypress between every image change
    cv2.destroyAllWindows()
    cv2.imshow(title, image)
    print(text)
    cv2.waitKey(0)

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

transition(image, "Appa with Border", "Nice! Now, Appa is currently flying in \
mid-air. Let's add a platform for him to land on. (Press any key to add a platform)")

# add platform
platformColor = (13, 26, 40)
point1 = (int(image.shape[1]*0.2), int(image.shape[0]*0.84))
point2 = (int(image.shape[1]*0.8), int(image.shape[0]*0.89))
image = cv2.rectangle(image, point1, point2, platformColor, -1)

transition(image, "Appa on a Platform", "Awesome! (Press any key for the next step)")

# (using a copy of image) add cupcake
imageWithCupcake1 = overlay(np.copy(image), cupcakeImage)

transition(imageWithCupcake1, "A Cupcake!", "Look, a cupcake! Appa is hungry and \
he wants to eat the cupcake. However, he is facing the wrong way. Let's flip him \
so that he can eat the cupcake. (Press any key to flip Appa)")

# (using a copy of image) flip image, add cupcake onto flipped image
imageWithCupcake2 = overlay(cv2.flip(np.copy(image), 1), cupcakeImage)

transition(imageWithCupcake2, "Yum!", "Yum :)")

# flip original image
image = cv2.flip(image, 1)

transition(image, "Appa is Lonely :(", "Now, Appa is lonely. Let's give him some \
friends to play with.")



# Save the image -- OpenCV handles converting filetypes automatically
#cv2.imwrite("newimage.jpg", image)
