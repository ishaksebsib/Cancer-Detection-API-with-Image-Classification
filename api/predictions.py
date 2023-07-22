import cv2
import tensorflow as tf


def predictBloodCancer(image_path, model):

    # process the image
    img = cv2.imread(image_path)
    resize = tf.image.resize(img, (224, 224))

    # predicit the result
    result = model.predict(resize.numpy().reshape(1, 224, 224, 3))
    final = {}
    if result[0][0] < result[0][1]:
        final["is_cancer"] = False
        final["confidence"] = round(result[0][1]*100, 6)
    else:
        final["is_cancer"] = True
        final["confidence"] = round(result[0][0]*100, 6)
    return final
