# Hello! Welcome to Image Editor. To run my program, activate my virtual
# environemnt "cv" and enter "python image_editor.py" in the command line.

# import packages
import numpy as np
import cv2

def addBorder(image, color):
# function to add a red, green or blue border to an image

    # possible colors
    colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink"]

    # define GBR values of colors
    red = (0, 0, 255)
    orange = (0, 165, 255)
    yellow = (0, 255, 255)
    green = (0, 255, 0)
    blue = (255, 0, 0)
    purple = (255, 0, 255)
    pink = (203,192,255)

    while True:
        # if color is valid
        if color in colors:
            if color == "red":
                BGRcolor = red
            elif color == "orange":
                BGRcolor = orange
            elif color == "yellow":
                BGRcolor = yellow
            elif color == "green":
                BGRcolor = green
            elif color == "blue":
                BGRcolor = blue
            elif color == "purple":
                BGRcolor = purple
            else:
                BGRcolor = pink

            # set four borders
            image[0:image.shape[0], 0:15] = BGRcolor
            image[0:image.shape[0], image.shape[1]-15:image.shape[1]] = BGRcolor
            image[0:15, 0:image.shape[1]] = BGRcolor
            image[image.shape[0]-15:image.shape[0], 0:image.shape[1]] = BGRcolor

            # return image with borders
            return image
        # if color is invalid
        else:
            color = input("Please pick between red, orange, yellow, green, blue, purple, or pink: ")

def countShapes(image, canny):
# function to count the number of shapes in an image

    # find contours
    (contours, _) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    copy = image.copy()
    # draw the contours onto the image
    cv2.drawContours(copy, contours, -1, (255, 0, 255), 2)

    return copy, contours

def canny(image):
# function to find canny edges within an image

    # convert image to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # blue image using Gaussian Blur
    image = cv2.GaussianBlur(image, (5, 5), 0)
    """Ok so this is definitely kind of cheating because I'm making all the bison
     black so the edges within the bison aren't detected since I only want the
     outer edge but Canny detects everything :/ any way I can fix that besides
     cheating like this lol?"""
    (T, thresh) = cv2.threshold(image, 250, 255, cv2.THRESH_BINARY)
    # perform Canny edge detection with two threshold values (min and max) as parameters
    canny = cv2.Canny(thresh, 30, 150)

    return canny

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

def transition(image, title, text):
# transition function that clears the current image, displays the new image, and
# waits for a keypress between every image change
    cv2.destroyAllWindows()
    cv2.imshow(title, image)
    print(text)
    cv2.waitKey(0)

def main():
    # load images
    backgroundImage = cv2.imread("background.png")
    appaImage = cv2.imread("appa.png")
    cupcakeImage = cv2.imread("cupcake.png")
    babyBisonImage = cv2.imread("baby_bison.png")

    # (using a copy of the background) add a background to appaImage
    image = overlay(np.copy(backgroundImage), appaImage)

    # welcome user, display original image
    transition(image, "Original Appa", "Hello! Welcome to image editor. Today we \
will be editing this picture of Appa the flying bison! (Press any key for the \
next step)")

    print("Appa is currently flying in mid-air. Let's add a platform for him to land on. (Press any key to add a platform)")

    # add platform
    platformColor = (13, 26, 40)
    # 230, 375 – top point
    # 545, 380 – bottom point
    # 767, 535 – size of image
    point1 = (int(image.shape[1]*0.28), int(image.shape[0]*0.7))
    point2 = (int(image.shape[1]*0.72), int(image.shape[0]*0.74))
    image = cv2.rectangle(image, point1, point2, platformColor, -1)

    transition(image, "Appa on a Platform", "Awesome! (Press any key for the next step)")

    # (using a copy of image) add cupcake
    imageWithCupcake1 = overlay(np.copy(image), cupcakeImage)

    transition(imageWithCupcake1, "A Cupcake!", "Look, a cupcake! Appa is hungry \
and he wants to eat the cupcake. However, he is facing the wrong way. Let's flip \
him so that he can eat the cupcake. (Press any key to flip Appa)")

    # flip Appa then place him on (unflipped) background again
    image = overlay(backgroundImage, cv2.flip(appaImage, 1))
    # redraw platform
    image = cv2.rectangle(image, point1, point2, platformColor, -1)
    # (using a copy of image) flip image, add cupcake onto flipped image
    imageWithCupcake2 = overlay(np.copy(image), cupcakeImage)

    transition(imageWithCupcake2, "Nom nom", "Yum :) (Press any key to continue)")

    transition(image, "Appa is Lonely :(", "Now, Appa is lonely. Let's find him \
some friends to play with. (Press any key to find Appa some friends)")

    # display baby bison photo
    transition(babyBisonImage, "Baby bison!", "Look! Baby bison! Let's count how \
many there are. (Press any key to count)")

    # (with a copy of image) use canny edge detection to find the edges in the image
    bisonCanny = canny(np.copy(babyBisonImage))
    # use the Canny image to find the contours of the image and how many there are
    bisonCounted, count = countShapes(babyBisonImage, bisonCanny)

    transition(bisonCounted, "Baby Bison Counted", "There are {} baby bison! Let's \
bring them over to Appa. (Press any key to bring them over)".format(len(count)))

    # add baby bison to Appa image
    image = overlay(image, babyBisonImage)

    transition(image, "Appa and friends", "So cute :) (Press any key to continue)")

    # prompt user for border color
    borderColor = input("Now, lets frame our image with a nice border. Please enter \
color you would like the border to be: ").lower()

    # add border
    image = addBorder(image, borderColor)

    transition(image, "Finished!", "Amazing! (Press any key to exit)")

if __name__ == "__main__":
    main()
