"""
UA-mnist train CNN. Test accuracy: 0.78

"""

from __future__ import print_function
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import numpy
import json
from sklearn.model_selection import train_test_split
from data_reader import read_data
import os.path

data = json.load(open("config.json"))

if os.path.isfile(data["features_path"]+"/.npy"):           # Check if we already have numpy with our data
    dataset = numpy.load(data["features_path"] + "/.npy")
else:
    dataset = read_data()   # Create and read numpy data (see data_reader.py)

X = numpy.asarray([img[0] for img in dataset])
y = numpy.asarray([img[2] for img in dataset])

x_train, x_test, y_train, y_test = train_test_split(X, y)   # Divide our data on train and test samples

# print train and test shapes
# print("x_train:", x_train.shape, "\nx_test:", x_test.shape, "\ny_test:", y_test.shape)

batch_size = 128
num_classes = 72    # Write number of classes 72
epochs = 12

# input image dimensions
img_rows, img_cols = 27, 35     # Set size of our images


if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test))
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])



