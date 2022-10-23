from datetime import datetime
import tensorflow as tf
from tensorflow import keras
import numpy as np


class Brain(object):
    __model = None


    def __init__(self, state_shape, action_shape):

        # create model
        learning_rate = 0.001
        # init = tf.keras.initializers.HeUniform()
        init = tf.keras.initializers.random_normal()
        model = keras.Sequential()
        model.add(keras.layers.Dense(state_shape, activation='relu', kernel_initializer=init))
        model.add(keras.layers.Dense(16, activation='relu', kernel_initializer=init))
        model.add(keras.layers.Dense(32, activation='relu', kernel_initializer=init))
        model.add(keras.layers.Dense(action_shape, activation='linear', kernel_initializer=init))
        model.compile(loss=tf.keras.losses.Huber(), optimizer=tf.keras.optimizers.Adam(lr=learning_rate), metrics=['accuracy'])
        self.__model = model
    

    def save(self) -> None:
        str_time = datetime.now()
        self.__model.save_weights("./data/neural_weights/model_" + str_time + ".h5")
    

    def load(self, path) -> None:
        self.__model.load_weights(path)
    

    def pulse(self, state) -> tuple:
        res = tuple(self.__model.predict(np.array([state]), verbose=0)[0])
        return res
