

# Plot ad hoc mnist instances
import numpy
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras.optimizers import Adadelta
from keras.losses import categorical_crossentropy
import numpy as np
from PIL import Image
import cv2
import os

class classifyKeras():

    def __init__(self):
        self.prepareModel()

    def prepareModel(self):
        seed = 7
        numpy.random.seed(seed)

        img_width, img_height = 28, 28

        (self.X_train, self.y_train), (self.X_test, self.y_test) = mnist.load_data()
        # reshape to be [samples][pixels][width][height]
        self.X_train = self.X_train.reshape(self.X_train.shape[0], 28, 28, 1).astype('float32')
        self.X_test = self.X_test.reshape(self.X_test.shape[0], 28, 28, 1).astype('float32')
        # normalize inputs from 0-255 to 0-1
        self.X_train = self.X_train / 255
        self.X_test = self.X_test / 255
        # one hot encode outputs
        self.y_train = np_utils.to_categorical(self.y_train)
        self.y_test = np_utils.to_categorical(self.y_test)
        num_classes = self.y_test.shape[1]

        self.model = self.createModel(num_classes)

        if (os.path.isfile('../Model/Model.h5')):
            self.model.load_weights('../Model/Model.h5')
        else:
            self.model.fit(self.X_train, self.y_train,
                      batch_size=128,
                      epochs=12,
                      verbose=1,
                      validation_data=(self.X_test, self.y_test))
            self.model.save('../Model/Model.h5')

    def createModel(self, num_classes):
        # create Model
        model = Sequential()
        model.add(Conv2D(32, kernel_size=(3, 3),
                         activation='relu',
                         input_shape=(28, 28, 1)))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(num_classes, activation='softmax'))
        # Compile Model
        model.compile(loss=categorical_crossentropy,
                      optimizer=Adadelta(),
                      metrics=['accuracy'])
        return model

    def resize_image(self, image):
        img = cv2.resize(image, (28,28))
        arr = np.array(img)

        # convert to gray scale
        if len(arr.shape) > 2:
            arr = np.mean(arr, 2)

        # flatten
        arr = arr.flatten()
        return arr

    def predict(self, img):
        arr = self.resize_image(img)
        arr = arr.reshape(1, 28, 28, 1)
        predicted_classes = self.model.predict_classes(arr)
        return predicted_classes[0]

    def evaluateModel(self):
        loss_and_metrics = self.model.evaluate(self.X_test, self.y_test, verbose=2)
        print("Test Loss", loss_and_metrics[0])
        print("Test Accuracy", loss_and_metrics[1])

if __name__ == '__main__':
    model = classifyKeras()
    print(model.predict(cv2.imread("./number-five.png")))


