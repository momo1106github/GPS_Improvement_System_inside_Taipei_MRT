import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import sys

CLASS = {"ON_MRT": 0, "AT_STATION": 1}

def scene_recognition(img):
    if not img: 
        return None

    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = tensorflow.keras.models.load_model('./model/converted_keras/keras_model.h5', compile=False)

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(img)

    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    #turn the image into a numpy array
    image_array = np.asarray(image)

    # display the resized image
    # image.show()

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    
    print (prediction, prediction[0][CLASS["AT_STATION"]], prediction[0][CLASS["ON_MRT"]])
    return prediction[0][CLASS["AT_STATION"]] > prediction[0][CLASS["ON_MRT"]]        

if __name__ == '__main__':
    scene_recognition(sys.argv[1])