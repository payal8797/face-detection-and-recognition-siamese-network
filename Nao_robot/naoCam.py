import os
import requests
from time import sleep
from PIL import Image
from naoqi import ALProxy


class naoCam:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.vm_url = 'SERVER URL FOR REQUEST.'
        self.image_path = "/var/www/html"
        self.video_service = ALProxy("ALVideoDevice", ip, port)

    def get_images(self):
        nameId = self.video_service.subscribeCamera("python_client", 0, 2, 11, 20)

        for i in range(0, 4):
            naoImage = self.video_service.getImageRemote(nameId)
            self.video_service.releaseImage(nameId)
            imageWidth = naoImage[0]
            imageHeight = naoImage[1]
            array = naoImage[6]
            image_string = str(bytearray(array))
            im = Image.frombytes("RGB", (imageWidth, imageHeight), image_string)
            # save as jpeg
            im.save(self.image_path + '/' + 'camImage_' + str(i) + '.jpeg', 'JPEG')
            sleep(0.5)

        self.video_service.unsubscribe(nameId)


    def get_response(self):
        response = "Oops. No image captured"
        imagesList = sorted(os.listdir(self.image_path))
        if len(imagesList) > 0:
            for image in imagesList:
                if "jpeg" in image:
                    payload = {'image_name': image}
                    result = requests.post(self.vm_url, data=payload)
                    print(image, result.content)
                    if result.json()["retry"] is 0:
                        response = result.json()["message"]
                        break

        return response

