# -*- coding: utf-8 -*-
"""Ana.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1shdANlfZ7CFPXdWdDuiQ5d_Duxlm206l
"""

import zipfile

# specify the path to the zip file in your Google Drive
zip_path = '/content/drive/MyDrive/AnaData_val.zip'

# specify the path to the folder where you want to unzip the dataset
extract_path = '/content/dataset/'

# extract the contents of the zip file to the extract_path folder
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

import tensorflow as tf
from tensorflow import keras
from keras.layers import Dense, Rescaling, Conv2D, MaxPooling2D, Dropout, Flatten
from keras.callbacks import EarlyStopping
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os
from keras.preprocessing.image import ImageDataGenerator
from google.colab import drive

# DATA SOURCE -----------------------------------------

batch_size = 25

train_data_dir = r'/content/dataset/dataset/training_set'
validation_data_dir = r'/content/dataset/dataset/validation_test'

train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=15,
        zoom_range=0.1
)

validation_datagen = ImageDataGenerator(
        rescale=1./255
)

train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(250, 250),
        batch_size=batch_size,
        class_mode='categorical')

validation_generator = validation_datagen.flow_from_directory(
        validation_data_dir,
        target_size=(250, 250),
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False)

valid_dataset = keras.preprocessing.image_dataset_from_directory(
    directory= r'/content/dataset/dataset/validation_test',
    image_size=(250,250),
    batch_size=batch_size,
    label_mode='categorical'
)

model.to_json()

#IA GOOGLE

from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions

model_transfer = VGG16(weights='imagenet', include_top=True)

from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions

model_transfer = VGG16(weights='imagenet', include_top=True)
base_model = keras.applications.VGG16(
    weights='imagenet',
    input_shape=(250, 250, 3),
    include_top=False)

base_model.trainable = False

inputs = keras.Input(shape=(250, 250, 3))

x = base_model(inputs, training=False)
x = keras.layers.GlobalAveragePooling2D()(x)

x = keras.layers.Dense(256, activation='relu')(x)
outputs = keras.layers.Dense(2, activation='softmax')(x)

model_transfer = keras.Model(inputs, outputs)

model_transfer.compile(loss=tf.keras.losses.categorical_crossentropy,
                      optimizer=tf.keras.optimizers.Adam(1e-3),
                      metrics=['accuracy'])

epochs = 5

es = EarlyStopping(monitor='val_accuracy', mode='max', verbose=1, patience=10, restore_best_weights=True)

h = model_transfer.fit(
        train_generator,
        epochs=epochs, 
        validation_data=validation_generator,
        callbacks = [es]
)

img = keras.preprocessing.image.load_img(
    r'/content/dataset/dataset/test_set/dogs/dog.4006.jpg', target_size=(150,150)
)
img_array = keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0) 

predictions = model_transfer.predict(img_array)
predictions_transfer = model_transfer.predict(img_array)

print(train_generator.class_indices)
print(np.argmax(predictions[0]))
print(np.argmax(predictions_transfer[0]))
class_names = list(train_generator.class_indices.keys())
print()

if(np.argmax(predictions_transfer[0]) == 0):
        print("I see a picture of " + class_names[0])
else:
        print("I see a picture of " + class_names[1])

# EVALUATION ------------------------------------------

plt.plot(h.history['accuracy'])
plt.plot(h.history['val_accuracy'])
plt.plot(h.history['loss'])
plt.title('Model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['training', 'validation','loss'], loc='upper right')
plt.show()

# TRANSFER-LEARNING RESULTS ---------------------------

total_val_samples = validation_generator.n
print("El generador de validación tiene", total_val_samples, "imágenes")

steps = total_val_samples // batch_size

results = np.concatenate([(y, model_transfer.predict(x=x)) for x, y in valid_dataset], axis=1)

predictions = np.argmax(results[0], axis=1)
labels = np.argmax(results[1], axis=1)

cf_matrix = confusion_matrix(labels, predictions)

sns.heatmap(cf_matrix, annot=True, fmt="d", cmap="Blues")

print(classification_report(labels, predictions, digits = 4))

#----------------------------------------------------ANA_PARAMETRICA----------------------------------------------------------------------------------

# Importar las librerías necesarias
import os
import zipfile
from google.colab import drive

# Montar Google Drive en Colab
drive.mount('/content/drive', force_remount=True)

# Función para extraer un archivo .zip y guardar su contenido en la carpeta /content/dataset/
def extraer_zip(ruta_zip, ruta_destino='/content/dataset/'):
  # Extraer el nombre del archivo .zip sin la extensión
  nombre_archivo = os.path.splitext(os.path.basename(ruta_zip))[0]
  # Combinar la ruta de destino con el nombre del archivo
  ruta_archivo = os.path.join(ruta_destino, nombre_archivo)
  # Extraer el contenido del archivo .zip en la ruta de destino
  with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
      zip_ref.extractall(ruta_archivo)
  # Retornar la ruta donde se extrajeron los datos
  return ruta_archivo

# Ejemplo de uso de la función
ruta_zip = '/content/drive/MyDrive/flowers.zip'
ruta_destino = '/content/dataset/'
ruta_datos = extraer_zip(ruta_zip, ruta_destino)

import tensorflow as tf
from tensorflow import keras
from keras.layers import Dense, Rescaling, Conv2D, MaxPooling2D, Dropout, Flatten
from keras.callbacks import EarlyStopping
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os
from keras.preprocessing.image import ImageDataGenerator
from google.colab import drive

# DATA SOURCE -----------------------------------------Primero va esto, para intentar saber el número de clases que se me han pasado

from PIL import Image

batch_size = 25

import os

def buscar_carpeta(ruta_base,name):
    for ruta_actual, carpetas, archivos in os.walk(ruta_base):
        if name in carpetas:
            # Si se encuentra la carpeta "name", se construye la ruta completa a la carpeta
            ruta = os.path.join(ruta_actual, name)
            return ruta
    # Si no se encuentra la carpeta "name", se devuelve None
    return None


train_data_dir = buscar_carpeta('/content/dataset/','train')
validation_data_dir = buscar_carpeta('/content/dataset/','val')
test_data_dir = buscar_carpeta('/content/dataset/','test')

#A partir de la ruta que se ha mandado, buscamos cuantas etiquetas hay en ella
num_classes = len(os.listdir(train_data_dir))

#Dependiendo del número de etiquetas, será un modelo binario o categórico.

if(num_classes == 2):
    mode = 'binary'
    function = tf.keras.losses.binary_crossentropy
else:
    mode = 'categorical'
    function = tf.keras.losses.categorical_crossentropy

#Generador de imagenes

def random_image():
  directory = test_data_dir

  # Obtener la lista de archivos en la carpeta
  files = os.listdir(directory)

  # Seleccionar un archivo aleatorio
  filename = random.choice(files)


  directory_img = os.path.join(directory, filename) # Ruta completa del directorio que contiene las imágenes

  # Obtener una lista de todas las imágenes en el directorio
  images = os.listdir(directory_img)

  # Seleccionar una imagen aleatoria del directorio
  random_image = random.choice(images)
  return os.path.join(directory_img, random_image)


test_datagen = ImageDataGenerator(
          rescale=1./255
)
validation_datagen = ImageDataGenerator(
          rescale=1./255
)

datagen = ImageDataGenerator(
      rotation_range=20,
      width_shift_range=0.2,
      height_shift_range=0.2,
      shear_range=0.2,
      zoom_range=0.2,
      rescale=1./255,
      horizontal_flip=True,
      fill_mode='nearest')

train_generator = datagen.flow_from_directory(
          train_data_dir,
          target_size=(250, 250),
          batch_size=batch_size,
          class_mode=mode)

validation_generator = validation_datagen.flow_from_directory(
          validation_data_dir,
          target_size=(250, 250),
          batch_size=batch_size,
          class_mode=mode,
          shuffle=False)

valid_dataset = keras.preprocessing.image_dataset_from_directory(
      directory= buscar_carpeta('/content/dataset/','val'),
      image_size=(250,250),
      batch_size=batch_size,
      label_mode=mode
)

test_dataset = keras.preprocessing.image_dataset_from_directory(
      directory= buscar_carpeta('/content/dataset/','test'),
      image_size=(250,250),
      batch_size=batch_size,
      label_mode=mode
)

  
print(mode)
print(str(function))
print("La IA ha encontrado " + str(num_classes) + " clases")

from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions
from tensorflow.keras.regularizers import l2

model_transfer = VGG16(weights='imagenet', include_top=True)
base_model = keras.applications.VGG16(
    weights='imagenet',
    input_shape=(250, 250, 3),
    include_top=False)

base_model.trainable = False

inputs = keras.Input(shape=(250, 250, 3))

x = base_model(inputs, training=False)
x = keras.layers.GlobalAveragePooling2D()(x)
#x = keras.layers.Dropout(0.5)(x) # Capa de Dropout



#x = keras.layers.Dense(256, activation='relu', kernel_regularizer=l2(0.01))(x)

x = keras.layers.Dense(256, activation='relu')(x)
outputs = keras.layers.Dense(num_classes, activation='softmax')(x) #OJO CON ESTO, SI CAMBIAS LAS ETIQUETAS CAMBIA EL NUMERO DE OUTPUTS B

model_transfer = keras.Model(inputs, outputs)

model_transfer.compile(loss=function,
                      optimizer=tf.keras.optimizers.Adam(1e-3),
                      metrics=['accuracy'])

epochs = 5

es = EarlyStopping(monitor='val_accuracy', mode='max', verbose=1, patience=10, restore_best_weights=True)

h = model_transfer.fit(
        train_generator,
        epochs=epochs, 
        validation_data=validation_generator,
        callbacks = [es]
)

#Results.
# TRANSFER-LEARNING RESULTS ---------------------------

total_val_samples = validation_generator.n
print("El generador de validación tiene", total_val_samples, "imágenes")

steps = total_val_samples // batch_size

results = np.concatenate([(y, model_transfer.predict(x=x)) for x, y in valid_dataset], axis=1)

predictions = np.argmax(results[0], axis=1)
labels = np.argmax(results[1], axis=1)

cf_matrix = confusion_matrix(labels, predictions)

sns.heatmap(cf_matrix, annot=True, fmt="d", cmap="Blues")

print(classification_report(labels, predictions, digits = 4))

#Results.
# TRANSFER-LEARNING RESULTS ---------------------------
results = np.concatenate([(y, model_transfer.predict(x=x)) for x, y in test_dataset], axis=1)

predictions = np.argmax(results[0], axis=1)
labels = np.argmax(results[1], axis=1)

cf_matrix = confusion_matrix(labels, predictions)

sns.heatmap(cf_matrix, annot=True, fmt="d", cmap="Blues")

print(classification_report(labels, predictions, digits = 4))

# EVALUATION ------------------------------------------

plt.plot(h.history['accuracy'])
plt.plot(h.history['val_accuracy'])
plt.plot(h.history['loss'])
plt.title('Model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['training', 'validation','loss'], loc='upper right')
plt.show()

#Prueba en caliente

import os
import random
from keras.preprocessing import image

def random_image():
  directory = test_data_dir

  # Obtener la lista de archivos en la carpeta
  files = os.listdir(directory)

  # Seleccionar un archivo aleatorio
  filename = random.choice(files)


  directory_img = os.path.join(directory, filename) # Ruta completa del directorio que contiene las imágenes

  # Obtener una lista de todas las imágenes en el directorio
  images = os.listdir(directory_img)

  # Seleccionar una imagen aleatoria del directorio
  random_image = random.choice(images)
  return os.path.join(directory_img, random_image)

picture = random_image();
pil_im = Image.open(picture, 'r')
print(np.asarray(pil_im).shape)
plt.imshow(np.asarray(pil_im))
plt.show()


img = keras.preprocessing.image.load_img(
    picture, target_size=(250,250)
)
img_array = keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0) 

predictions = model_transfer.predict(img_array)
predictions_transfer = model_transfer.predict(img_array)

print(train_generator.class_indices)
print(np.argmax(predictions[0]))
print(np.argmax(predictions_transfer[0]))
class_names = list(train_generator.class_indices.keys())
print()

if np.argmax(predictions_transfer[0]) < len(class_names):
    print("I see a picture of " + class_names[np.argmax(predictions_transfer[0])])
else:
    print("Unknown class")

model_transfer.save('Ana_Flowers.h5')
Ana_flowers = keras.models.load_model('Ana_Flowers.h5')
#Prueba en caliente

import os
import random
from keras.preprocessing import image

def random_image():
  directory = test_data_dir

  # Obtener la lista de archivos en la carpeta
  files = os.listdir(directory)

  # Seleccionar un archivo aleatorio
  filename = random.choice(files)


  directory_img = os.path.join(directory, filename) # Ruta completa del directorio que contiene las imágenes

  # Obtener una lista de todas las imágenes en el directorio
  images = os.listdir(directory_img)

  # Seleccionar una imagen aleatoria del directorio
  random_image = random.choice(images)
  return os.path.join(directory_img, random_image)

picture = random_image();
pil_im = Image.open(picture, 'r')
print(np.asarray(pil_im).shape)
plt.imshow(np.asarray(pil_im))
plt.show()


img = keras.preprocessing.image.load_img(
    picture, target_size=(250,250)
)
img_array = keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0) 

predictions = Ana_flowers.predict(img_array)
predictions_transfer = Ana_flowers.predict(img_array)

print(train_generator.class_indices)
print(np.argmax(predictions[0]))
print(np.argmax(predictions_transfer[0]))
class_names = list(train_generator.class_indices.keys())
print()

if np.argmax(predictions_transfer[0]) < len(class_names):
    print("I see a picture of " + class_names[np.argmax(predictions_transfer[0])])
else:
    print("Unknown class")