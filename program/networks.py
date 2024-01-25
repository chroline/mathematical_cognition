import tensorflow as tf
from autokeras import CUSTOM_OBJECTS

digits_classifier = tf.keras.models.load_model('../trained_models/digits_classifier')
addition_memory = tf.keras.models.load_model('../trained_models/addition_memory', custom_objects=CUSTOM_OBJECTS)
multiplication_memory = tf.keras.models.load_model('../trained_models/multiplication_memory',
                                                   custom_objects=CUSTOM_OBJECTS)
