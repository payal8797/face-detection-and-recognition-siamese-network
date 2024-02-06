from PIL import Image
import time
import io
import sys
import os
import numpy as np
import cv2
import requests
from YoloFace import YoloFace
from FaceSimilarity import FaceSimilarity

_YOLO_PATH = "models/detect.onnx"

class RobotCommServer:

    def PredictionProcedure(self, request):

        #Initialization of variables and downloading the image form server for processing.
        response = "Oops, No image detected!"
        retry = 1
        try:
            image_name = request.get("image_name")
            base_path = "SERVER BASE URL FOR IMAGE."
            image_path = base_path + image_name
            # print("image Path:", image_path)
            result = requests.get(image_path)
            nparr = np.fromstring(result.content, np.uint8)
            image = cv2.imdecode(nparr, flags=1)

            #Loading the YoloFace model class to detect the face in the input image and return a cropped face in response.
            faceDetector = YoloFace(_YOLO_PATH, conf_thres=0.6, iou_thres=0.6)
            image = np.array(image)
            image = faceDetector.detect_image(image)

            #If Yolo model class will return the cropped image then based on that we are calling the Face similarity class to predict the similarity.
            if len(image) > 0:
                cv2.imwrite("./cropped/"+image_name, image)
                retry = 0
                facePrediction = FaceSimilarity(image)
                response = facePrediction.predict()
        except Exception as e:
            print("error", e)
            pass
        return response, retry