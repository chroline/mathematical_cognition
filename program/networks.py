from os import path

import tensorflow as tf
from autokeras import CUSTOM_OBJECTS

DIRNAME = path.dirname(path.abspath(__file__))

digits_classifier = tf.keras.models.load_model(path.join(DIRNAME, '../trained_models/digits_classifier'))
addition_memory = tf.keras.models.load_model(path.join(DIRNAME, '../trained_models/addition_memory'),
                                             custom_objects=CUSTOM_OBJECTS)
multiplication_memory = tf.keras.models.load_model(
    path.join(DIRNAME, '../trained_models/multiplication_memory'),
    custom_objects=CUSTOM_OBJECTS)
