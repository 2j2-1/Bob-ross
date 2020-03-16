from os import listdir, remove
import cv2


class Preprocess(object):

    file_path = "raw_data/"
    base_save_path = "preprocessed_data/"
    validate_image_count = 0

    def validateFiles(self):

        for image_path in listdir(self.file_path):
            image = cv2.imread(self.file_path + image_path)
            try:
                assert image is not None, "Corrupt"
                assert image.shape == (337, 450, 3), "Resolution"
                save_path = "{}{}".format(
                    self.base_save_path, image_path)
                self.saveFile(save_path, image)
                self.validate_image_count += 1
            except AssertionError as e:
                print("{} {}".format(e, image_path))

    def manualValidate(self,file_path):
        for image_path in listdir(file_path):
            image = cv2.imread(file_path + image_path)
            while 1:
                cv2.imshow(image_path, image)
                
                k = cv2.waitKey(33)
                if k == 27:
                    cv2.destroyAllWindows()
                    break
                elif k == ord('s'):
                    cv2.destroyAllWindows()
                    break
                elif k == ord('d'):
                    cv2.destroyAllWindows()
                    remove(file_path + image_path)
                    break
            if k == 27:
                break

    def reorderFiles(self):
        image_count = 1
        for image_path in sorted(listdir(self.base_save_path), key=lambda x : x[:3]):
            self.saveFile("{}{}.png".format(self.base_save_path,str(image_count).zfill(3)), cv2.imread(self.file_path + image_path))
            image_count += 1
    def saveFile(self,save_path, image):
        print(save_path)
        cv2.imwrite(save_path, image)

pre = Preprocess()
pre.validateFiles()
# pre.manualValidate('preprocessed_data/')
pre.reorderFiles()
