import cv2
from os import listdir
from os.path import isfile
import csv
from sklearn.cluster import MiniBatchKMeans
import numpy


class Label(object):

    preprocessed_file_path = "preprocessed_data/"
    labeled_file_path = "labeled_data/"

    def threshold(self):
        isFile = isfile("threshold.csv")
        if isFile:
            with open('threshold.csv', mode='r') as file:
                reader = csv.reader(file)
                mydict = dict((rows[0], int(rows[1])) for rows in reader)

        for image_path in listdir(self.preprocessed_file_path):
            
            min_value = mydict.get(image_path, 60)
            
            image = cv2.imread(self.preprocessed_file_path + image_path)

            ret, thresh1 = cv2.threshold(
                image, min_value, 255, cv2.THRESH_BINARY)

            while 1:
                cv2.imshow("Original", image)
                cv2.imshow("Labeled", thresh1)
                k = cv2.waitKey(33)
                if k == 27 or k == ord(' '):
                    break
                elif k == ord('s'):
                    mydict[image_path] = min_value
                    self.saveFile(image_path, thresh1)
                    break
                elif k == ord('a'):
                    min_value -= 1
                    ret, thresh1 = cv2.threshold(
                        image, min_value, 255, cv2.THRESH_BINARY)
                elif k == ord('d'):
                    min_value += 1
                    ret, thresh1 = cv2.threshold(
                        image, min_value, 255, cv2.THRESH_BINARY)

            if k == 27:
                print(mydict)
                with open('threshold.csv', 'w') as csvfile:
                    for data in mydict:
                        csvfile.write("{},{}\n".format(data, mydict[data]))
                break

    def cluster(self):
        for image_path in listdir(self.preprocessed_file_path):
            image = cv2.imread(self.preprocessed_file_path + image_path)
            (h, w) = image.shape[:2]
            image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            image = image.reshape((image.shape[0] * image.shape[1], 3))
            clt = MiniBatchKMeans(n_clusters=8)
            labels = clt.fit_predict(image)
            quant = clt.cluster_centers_.astype("uint8")[labels]
            quant = quant.reshape((h, w, 3))
            image = image.reshape((h, w, 3))
            quant = cv2.cvtColor(quant, cv2.COLOR_LAB2BGR)
            image = cv2.cvtColor(image, cv2.COLOR_LAB2BGR)
            self.saveFile(image_path, numpy.hstack([image, quant]))

    def saveFile(self, save_path, image):
        print(save_path)
        cv2.imwrite(self.labeled_file_path + save_path, image)

label = Label()
label.cluster()
