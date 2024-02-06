import os
import cv2
import psycopg2
import numpy as np
import pandas as pd
from PIL import Image
from psycopg2 import connect
from tensorflow.keras.models import load_model
from Database import DB
from tensorflow.keras.utils import load_img, img_to_array
from keras_vggface import utils

_MODEL_PATH = "models/model.h5"
_COMPARING_DATA_PATH = "./comparing_dataset"
_TARGET_SIZE = (224,224)
_THRESHOLD_VALUE= 0.85

def contrastive_loss(y_true, y_pred):
    square_pred = tf.math.square(y_pred)
    margin_square = tf.math.square(tf.math.maximum(margin - (y_pred), 0))
    return tf.math.reduce_mean(
        (1 - y_true) * square_pred + (y_true) * margin_square
    )

class FaceSimilarity:

    def __init__(self, inputImageFromRobot):
        self.inputImageFromRobot = utils.preprocess_input(img_to_array(inputImageFromRobot), version=1)
        self.model = load_model(_MODEL_PATH, custom_objects={"contrastive_loss": contrastive_loss})

    def expandInputImageDims(self, number):
        self.inputImageFromRobot = np.tile(self.inputImageFromRobot, (number,1,1,1))

    def loadImagesFromDatabase(self):
        response = {}
        query = "SELECT * FROM meta_data"
        imageData = DB.execute(query)
        totalCount = len(imageData)
        self.expandInputImageDims(totalCount)
        if imageData is not None:
            for item in imageData:
                imageName = os.path.join(item[1], item[2])
                image = self.preprocessImage(imageName)
                response[item[1] + "_" + str(item[0])] = image
        return response

    def preprocessImage(self, imagePath):
        path = os.path.join(_COMPARING_DATA_PATH, imagePath)
        image = cv2.imread(path)
        image = img_to_array(image)
        return utils.preprocess_input(image, version=1)

    def findMeanForPerdiction(self, keys, prediction):
        keys = [key.split('_')[0] for key in keys]
        df = pd.DataFrame({"keys": keys, "predictions": prediction})
        df_sorted = df.groupby('keys').apply(lambda x: x.nlargest(3, 'predictions')).reset_index(drop=True)
        mean_predictions = df_sorted.groupby("keys")['predictions'].mean()
        # print(mean_predictions)
        return mean_predictions.idxmax(), mean_predictions.max()


    def predict(self):
        prediction = None
        response = "Oops, No match found!"
        imagesPair = self.loadImagesFromDatabase()
        dataset = [self.inputImageFromRobot, np.array(list(imagesPair.values()))]
        if len(imagesPair.keys()) > 0:
            prediction = self.model.predict(dataset)
        if prediction is not None:
            prediction = prediction.flatten()
            # df = pd.DataFrame({"keys": list(imagesPair.keys()), "predictions": prediction})
            # print(df)
            if (not all(v == 0 for v in prediction)):
                keys = list(imagesPair.keys())
                predictedName, predictedValue = self.findMeanForPerdiction(keys, prediction)
                if predictedValue >= _THRESHOLD_VALUE:
                    response = "Hello {}, nice to meet you. Hope you're doing well.".format(predictedName)
        return response