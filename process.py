from os import listdir
import cv2
import numpy
preprocessed_file_path= "preprocessed_data/"
labeled_file_path= "labeled_data/"
train_file_path = "training_data/"

def combine():    
    for image_path in listdir(preprocessed_file_path):
        processed_image_path = preprocessed_file_path + image_path
        labeled_image_path = labeled_file_path + image_path
        processed_image = cv2.imread(processed_image_path)
        labeled_image = cv2.imread(labeled_image_path)
        if processed_image.shape[2] == 4:
                processed_image = processed_image[:,:,:3]
        if labeled_image.shape[2] == 4:
                labeled_image = labeled_image[:,:,:3]
        try:
            concat = numpy.concatenate([processed_image,labeled_image],axis = 1)
            cv2.imwrite(train_file_path + image_path, concat)
        except:
            print(image_path)
            cv2.imshow("og",processed_image)
            cv2.imshow("label",labeled_image)
        