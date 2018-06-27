import os, cv2
import numpy as np
import matplotlib.pyplot as plt

from sklearn.utils import shuffle
from sklearn.cross_validation import train_test_split

from keras import backend as K

K.set_image_dim_ordering('th')

from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD, RMSprop, adam


# %%
class char74kClassify:
    def __init__(self):
        self.img_rows = 28
        self.img_cols = 28
        self.num_channel = 1
        self.num_epoch = 3
        self.model = Sequential()
        # Define the number of classes
        self.num_classes = 10
        self.PATH = os.path.dirname(os.path.realpath(__file__))

        self.loadData()

    def loadDataSet(self):
        data_path = self.PATH + '/../DataSet/data'
        data_dir_list = os.listdir(data_path)

        img_data_list = []
        j = 0
        nombre = []
        print('Loading dataset ...')
        for dataset in data_dir_list:
            img_list = os.listdir(data_path + '/' + dataset)
            nombre.append(j)
            j = 0
            for img in img_list:
                input_img = cv2.imread(data_path + '/' + dataset + '/' + img)
                input_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
                input_img_resize = cv2.resize(input_img, (28, 28))
                img_data_list.append(input_img_resize)
                j += 1

        img_data = np.array(img_data_list)
        img_data = img_data.astype('float32')
        img_data /= 255

        if self.num_channel == 1:
            if K.image_dim_ordering() == 'th':
                img_data = np.expand_dims(img_data, axis=1)
            else:
                img_data = np.expand_dims(img_data, axis=4)

        else:
            if K.image_dim_ordering() == 'th':
                img_data = np.rollaxis(img_data, 3, 1)

        # %%
        USE_SKLEARN_PREPROCESSING = False

        if USE_SKLEARN_PREPROCESSING:
            # using sklearn for preprocessing
            from sklearn import preprocessing

            def image_to_feature_vector(image, size=(28, 28)):
                # resize the image to a fixed size, then flatten the image into
                # a list of raw pixel intensities
                return cv2.resize(image, size).flatten()

            img_data_list = []
            for dataset in data_dir_list:
                img_list = os.listdir(data_path + '/' + dataset)
                for img in img_list:
                    input_img = cv2.imread(data_path + '/' + dataset + '/' + img)
                    input_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
                    input_img_flatten = image_to_feature_vector(input_img, (28, 28))
                    img_data_list.append(input_img_flatten)

            img_data = np.array(img_data_list)
            img_data = img_data.astype('float32')
            img_data_scaled = preprocessing.scale(img_data)

            if K.image_dim_ordering() == 'th':
                img_data_scaled = img_data_scaled.reshape(img_data.shape[0], self.num_channel, self.img_rows,
                                                          self.img_cols)

            else:
                img_data_scaled = img_data_scaled.reshape(img_data.shape[0], self.img_rows, self.img_cols,
                                                          self.num_channel)

            if K.image_dim_ordering() == 'th':
                img_data_scaled = img_data_scaled.reshape(img_data.shape[0], self.num_channel, self.img_rows,
                                                          self.img_cols)

            else:
                img_data_scaled = img_data_scaled.reshape(img_data.shape[0], self.img_rows, self.img_cols,
                                                          self.num_channel)

        if USE_SKLEARN_PREPROCESSING:
            img_data = img_data_scaled

        # %%
        # Assigning Labels


        num_of_samples = img_data.shape[0]
        labels = np.ones((num_of_samples,), dtype='int64')

        labels[0:1015] = 0
        labels[1015:2031] = 1
        labels[2031:3047] = 2
        labels[3047:4063] = 3
        labels[4063:5079] = 4
        labels[5079:6095] = 5
        labels[6095:7111] = 6
        labels[7111:8127] = 7
        labels[8127:9143] = 8
        labels[9143:10159] = 9

        # convert class labels to on-hot encoding
        Y = np_utils.to_categorical(labels, self.num_classes)

        # Shuffle the dataset
        x, y = shuffle(img_data, Y, random_state=2)
        # Split the dataset
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(x, y, test_size=0.2, random_state=2)

        input_shape = img_data[0].shape
        print(input_shape)


    def loadModel(self):


        print("Loading Model...")
        self.model.add(Convolution2D(32, 3, 3, border_mode='same', input_shape=(1,28,28)))
        self.model.add(Activation('relu'))
        self.model.add(Convolution2D(32, 3, 3))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.5))

        self.model.add(Convolution2D(64, 3, 3))
        self.model.add(Activation('relu'))
        # self.Model.add(Convolution2D(64, 3, 3))
        # self.Model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.5))

        self.model.add(Flatten())
        self.model.add(Dense(64))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(self.num_classes))
        self.model.add(Activation('softmax'))

        # sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        # self.Model.compile(loss='categorical_crossentropy', optimizer=sgd,metrics=["accuracy"])
        self.model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=["accuracy"])

        # Viewing self.model_configuration

        # self.Model.summary()
        # self.Model.get_config()
        # self.Model.layers[0].get_config()
        # self.Model.layers[0].input_shape
        # self.Model.layers[0].output_shape
        # self.Model.layers[0].get_weights()
        # np.shape(self.Model.layers[0].get_weights()[0])
        # self.Model.layers[0].trainable

    def loadData(self):

        self.loadModel()
        # %%
        # Training

        if os.path.isfile(self.PATH + '/../Model/char74k.h5'):
            self.model.load_weights(self.PATH + '/../Model/char74k.h5')
        else:
            self.loadDataSet()

            self.model.fit(self.X_train, self.y_train, batch_size=16, nb_epoch=self.num_epoch, verbose=1, validation_data=(self.X_test, self.y_test))
            self.model.save(self.PATH + '/../Model/char74k.h5')
        print("Model loaded")

    def classifyImage(self, img):
        # img = cv2.imread(path)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (28, 28))
        img = np.array(img)
        img = img.astype('float32')
        img /= 255

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

        # Predicting the test image
        return self.model.predict_classes(img)[0]

    def resize_image(self, image):
        img = cv2.resize(image, (28, 28))
        arr = np.array(img)

        # convert to gray scale
        if len(arr.shape) > 2:
            arr = np.mean(arr, 2)

        # flatten
        arr = arr.flatten()
        return arr


if __name__ == '__main__':
    model = char74kClassify()
    PATH = os.path.dirname(os.path.realpath(__file__))
    img = cv2.imread(r"C:\Users\Uporabnik\Desktop\fax\2.Letnik\python\Sudoku-Solver\DataSet\data\Sample004\img004-00002.png")
    cv2.imshow("img", img)
    cv2.waitKey(0)
    print(model.classifyImage(img))