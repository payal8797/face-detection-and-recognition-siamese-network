import numpy as np
import pandas as pd
import shutil
import os


# Dataset used is CelebA dataset. You can download it from https://www.kaggle.com/datasets/jessicali9530/celeba-dataset.
# Then run the below script to generate 2 folders, left and right which will then be used for preprocessing



start_labels_limit = 0
end_labels_limit = 4000  #max limit(10177)
base_path = "BASE PATH OF CelebA DATASET"
labels_path = base_path + "/Anno/identity_CelebA.txt"
Images_path = base_path + "/Img/img_align_celeba/img_align_celeba"
left_path = "./left_" + str(start_labels_limit) + "_" + str(end_labels_limit)
right_path = "./right_" + str(start_labels_limit) + "_" + str(end_labels_limit)

if not os.path.exists(left_path):
    os.makedirs(left_path)
    print(f"Directory '{left_path}' created successfully.")
else:
    print(f"Directory '{left_path}' already exists.")

if not os.path.exists(right_path):
    os.makedirs(right_path)
    print(f"Directory '{right_path}' created successfully.")
else:
    print(f"Directory '{right_path}' already exists.")

labels = pd.read_csv(labels_path, sep = " ")
unique_labels = labels['label'].unique().copy()
unique_labels = pd.DataFrame(unique_labels, columns=['label'])
unique_labels = unique_labels[start_labels_limit:end_labels_limit]
df = labels.merge(unique_labels, on="label")
grouped_data = df.groupby('label')

for label, group in grouped_data:
    images = group['image_id'].tolist()
    counter = 1
    if len(images) > 1:
        for i in range(len(images)):

            if i == len(images) - 1 and i % 2 == 0:
                break

            source_file = Images_path + "/" + images[i]
            destination_dir = left_path if i % 2 else right_path
            destination_file_path = destination_dir + "/" + str(label) +"_image_" + str(counter) + '.jpg'

            #Copy image from source to destination
            if not os.path.exists(destination_file_path):
                shutil.copy(source_file, destination_file_path)

            # Check if the move was successful
            if os.path.exists(destination_file_path):
                print("Image moved successfully.")
            else:
                print("Failed to move the image.")

            if i % 2 > 0:
                counter += 1
print("Done :)")
