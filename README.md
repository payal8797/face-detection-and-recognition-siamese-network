Face Similarity System for Nao Robot using Siamese networks

Abstract: This report presents the development of a face detection and recognition system using deep learning models for integration with the Nao Robot. The system utilizes the CelebA dataset to create 400,000 image pairs with an equal positive-negative ratio. The detection module is based on the YOLOv8 model pretrained on COCO and fine-tuned on the WIDER faces dataset. For face recognition, a Siamese model with VGG16 as the feature extractor, pretrained on the "Labeled Faces in the Wild" dataset, is employed. The Nao Robot interacts with the control center VM (CC) through an API, allowing it to capture images, process them, and receive the predicted results. The system achieves accurate face detection and recognition, enabling the Nao Robot to identify known individuals and respond accordingly.

Dataset:
●	The CelebA dataset of cropped faces is processed to create 400,000 image pairs with an equal positive-negative ratio.
●	Positive pairs indicate the same celebrity with different face orientations, while negative pairs consist of randomly selected different celebrities.
●	The data is split into an 80% training dataset, a 10% validation dataset, and a 10% testing dataset.
●	An additional support dataset is created with 45 cropped face images from 5 new classes not present in the training dataset.

Detection Module:
●	The face detection module is based on the YOLOv8 model, pretrained on the COCO dataset, and fine-tuned on the WIDER faces dataset.
●	During inference, the PyTorch model is converted to the ONNX format.
●	The module takes RGB images of size 640x480 pixels from the control center API and crops them to 224x224x3 pixels for further analysis.

Recognition Module:
●	The face recognition module utilizes a Siamese model with VGG16 as the feature extractor, pretrained on the "Labeled Faces in the Wild" dataset.
●	The complete model is fine-tuned on the training dataset mentioned earlier.
●	During inference, the Keras model takes two cropped face images of size 224x224x3 pixels and returns a similarity score between them.
●	At runtime, each image from the support dataset is compared with the input image from the Nao Robot.
●	The module selects the top three predictions for each class and returns the best label based on the maximum similarity score, calculated using the mean of the top three predictions.

Nao Robot Integration:
●	The Nao Robot is connected to the control center VM (CC) to enable the integration of the face detection and recognition system.
●	Various modules including LEDs, Posture, AutonomousLife, Camera, and TextToSpeech are initialized.
●	The robot performs posture correction, pause motion, and moving as required.
●	Images are captured by the robot at a rate of 4 images per 2 seconds and stored remotely in the control center.
●	An API request is then sent to the control center for image processing and retrieval of the predicted results.
●	The response from the control center is vocalized using the TextToSpeech module of the Nao Robot.
●	The execution of the system can be stopped upon completion of the task.

API:
●	The API receives a Get Request from the control center, specifying the image name for processing.
●	The requested image is downloaded from the control center for further analysis.
●	The face image is cropped using the previously described face detection module.
●	If the module fails to detect a face, the API downloads the next image and repeats the face detection process.
●	If no face is found in any of the images, the API returns the response "Face not found."
●	If a face is detected, the cropped image is sent to the recognition module for further analysis.
●	The recognition module compares the input face with known faces and returns the name of the recognized person if the similarity score exceeds the predefined threshold of 85%.
●	If the person is not known, the API returns the response "Unknown person."

Conclusion: The developed face detection and recognition system demonstrates accurate performance in identifying known individuals and detecting unknown faces. The integration of the system with the Nao Robot enables personalized interactions and appropriate responses. By utilizing the YOLOv8 model for face detection and the Siamese model with VGG16 for face recognition, reliable results are achieved. Further enhancements may include dataset expansion, model optimization, and exploring additional functionalities to augment the system's capabilities.


