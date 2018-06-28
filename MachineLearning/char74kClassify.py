import os
import cv2
import numpy as np
from keras import backend as K
K.set_image_dim_ordering('th')
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D


class Char74kClassify:
    def __init__(self):
        self.img_rows = 28
        self.img_cols = 28
        self.num_channel = 1
        self.num_epoch = 10
        self.model = Sequential()
        # Define the number of classes
        self.num_classes = 10
        self.PATH = os.path.dirname(os.path.realpath(__file__))

        self._LoadData()

    def _LoadModel(self):
        print("Loading Model...")
        self.model.add(Convolution2D(32, 3, 3, border_mode='same', input_shape=(1,self.img_rows,self.img_cols)))
        self.model.add(Activation('relu'))
        self.model.add(Convolution2D(32, 3, 3))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.5))

        self.model.add(Convolution2D(64, 3, 3))
        self.model.add(Activation('relu'))

        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.5))

        self.model.add(Flatten())
        self.model.add(Dense(64))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(self.num_classes))
        self.model.add(Activation('softmax'))

        self.model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=["accuracy"])

    def _LoadData(self):
        self._LoadModel()
        self._LoadFileModel()


    def _LoadFileModel(self):
        # Training
        if os.path.isfile(self.PATH + '/../Model/char74k.h5'):
            self.model.load_weights(self.PATH + '/../Model/char74k.h5')
            print("Model loaded")
            return True
        else:
            raise Exception("Model not founded in directory /Model")

    def _Resizing(self, img):
        img = cv2.resize(img, (28, 28))
        return img

    def _ImgToArray(self, img):
        img = np.array(img)
        img = img.astype('float32')
        img /= 255
        return img

    def _Reshaping(self, img):
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


    def ClassifyImage(self, img):
        img = self._Resizing(img)
        img = self._Reshaping(img)

        # Predicting the test image
        return self.model.predict_classes(img)[0]


if __name__ == '__main__':
    model = Char74kClassify()
    PATH = os.path.dirname(os.path.realpath(__file__))
    img = cv2.imread("..\..\DataSet\data\Sample004\img004-00002.png")
    # cv2.imshow("img", img)
    # cv2.waitKey(0)
    print(model.ClassifyImage(img))