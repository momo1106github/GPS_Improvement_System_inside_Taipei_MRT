import cv2
import numpy as np

COLORS = { 
    "G": [169, 255, 133.9], # [160, 100%, 52.5%]
    "R": [348.4, 255, 22.7], # [348.4, 100%, 8.9%]
    "BL": [204, 255, 189], # [204, 100%, 74.1%]
    "BR": [37.5, 191.25, 196.35], # [37.5, 75%, 77%]
    "O": [42, 226.95, 247.35], # [42, 89%, 97%]
    "Y": [51.9, 255, 252.5], # [51.9, 100%, 99%] 
}
DIFF_H = 5
DIFF_S = 100
DIFF_V = 100

def color_recognition(img, colors):
    image = cv2.imread(img)
    
    boundaries = {}
    for color in colors:
        boundaries[color] = [(
            [max(COLORS[color][0] - DIFF_H,   0), max(COLORS[color][1] - DIFF_S,   0), max(COLORS[color][2] - DIFF_V,   0)], 
            [min(COLORS[color][0] + DIFF_H, 255), min(COLORS[color][1] + DIFF_S, 255), min(COLORS[color][2] + DIFF_V, 255)]
        )]
    
    # Scale your BIG image into a small one:
    scalePercent = 0.3

    # Calculate the new dimensions
    width = int(image.shape[1] * scalePercent)
    height = int(image.shape[0] * scalePercent)
    newSize = (width, height)

    # Resize the image:
    image = cv2.resize(image, newSize, None, None, None, cv2.INTER_AREA)

    ratio = {}
    for color, boundary in boundaries.items():
        for (lower, upper) in boundary:
            lowerValues = np.array(lower, dtype=np.uint8)
            upperValues = np.array(upper, dtype=np.uint8)

            # Convert the image to HSV:
            hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Create the HSV mask
            hsvMask = cv2.inRange(hsvImage, lowerValues, upperValues)

            # AND mask & input image:
            hsvOutput = cv2.bitwise_and(image, image, mask=hsvMask)

            # print ("~~",cv2.countNonZero(hsvMask) / (image.size/3))
            ratio[color] = cv2.countNonZero(hsvMask) / (image.size/3)

            # Print the color percent, use 2 figures past the decimal point
            print(f'{color} pixel percentage:', ratio[color])

            # numpy's hstack is used to stack two images horizontally,
            # so you see the various images generated in one figure:
            # cv2.imshow("images", np.hstack([hsvImage, hsvOutput]))
            # cv2.waitKey(0)
    
    return max(ratio.items(), key = lambda k : k[1])