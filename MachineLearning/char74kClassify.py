import os, cv2
import numpy as np
import matplotlib.pyplot as plt

from sklearn.utils import shuffle
from sklearn.cross_validation import train_test_split

from keras import backend as K
from Common.validationFunctions import Validator
from Common.Errors import InappropriateArgsError
K.set_image_dim_ordering('th')

import keras



class Char74kClassify:
    def __init__(self):
        self.img_rows = 28
        self.img_cols = 28
        self.num_channel = 1
        # Define the number of classes
        self.num_classes = 10
        self.PATH = os.path.dirname(os.path.realpath(__file__))

        self._load_data()

    def _load_model(self, path):
        if Validator.is_type(path, str):
            if os.path.isfile(path):
                print("Loading Model...")
                with open(path, "r") as f:
                    json_str = f.read()
                f.close()
                self.model = keras.models.model_from_json(json_str)
                return True
            else:
                raise InappropriateArgsError("Model not founded in directory")
        else:
            raise InappropriateArgsError("Input not valid")


    def _load_data(self):

        self._load_model(self.PATH +"/../Model/model.json")
        self._load_file_weight(self.PATH + '/../Model/char74k.h5')


    def _load_file_weight(self, path):
        # Training

        if Validator.is_type(path, str):
            if os.path.isfile(path):
                self.model.load_weights(path)
                print("Model loaded")
                return True
            else:
                raise InappropriateArgsError("Model not founded in directory")
        else:
            raise InappropriateArgsError("Input not valid")

    def _resizing(self, img):
        if Validator.is_type(img, np.ndarray):
            img = cv2.resize(img, (28, 28))
            return img
        else:
            raise InappropriateArgsError("Input not valid")

    def _img_to_array(self, img):
        if Validator.is_type(img, np.ndarray):
            img = np.array(img)
            img = img.astype('float32')
            img /= 255
            return img
        else:
            raise InappropriateArgsError("Input not valid")

    def _reshaping(self, img):
        if isinstance(img, np.ndarray):
            if self.num_channel == 1:
                if K.image_dim_ordering() == 'th':
                    img = np.expand_dims(img, axis=0)
                    img = np.expand_dims(img, axis=0)
                else:
                    img = np.expand_dims(img, axis=3)
                    img = np.expand_dims(img, axis=0)

            else:
                if K.image_dim_ordering() == 'th':
                    img = np.rollaxis(img, 2, 0)
                    img = np.expand_dims(img, axis=0)
                else:
                    img = np.expand_dims(img, axis=0)

            return img
        else:
            raise InappropriateArgsError("Input not valid")

    def classify_image(self, img):
        if Validator.is_type(img, np.ndarray):
                img = self._resizing(img)
                img = self._reshaping(img)

                # Predicting the test image
                return self.model.predict_classes(img)[0]
        else:
            raise InappropriateArgsError("Input not valid")


if __name__ == '__main__':
    model = Char74kClassify()
    PATH = os.path.dirname(os.path.realpath(__file__))
    img = cv2.imread("..\..\DataSet\data\Sample004\img004-00002.png")
    print(model.classify_image(img))