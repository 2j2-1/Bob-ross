from os import listdir
import cv2
file_path = "raw_data/"
base_save_path = "preprocessed_data/"
file_names = sorted(listdir(file_path))
def validate_files(file_path):
	validate_image_count = 0
	for image_path in file_names:
		try:
			image = cv2.imread(file_path + image_path)
			assert image is not None, "Corrupt"
			assert image.shape == (337, 450, 3), "Resolution"
			save_path = "{}{}.png".format(base_save_path, validate_image_count)
			saveFile(save_path,image)
			validate_image_count += 1
		except AssertionError as e:
			print("{} {}".format(e, image_path))
		cv2.destroyAllWindows()

def saveFile(save_path,image):
	cv2.imwrite(save_path,image)

validate_files(file_path)