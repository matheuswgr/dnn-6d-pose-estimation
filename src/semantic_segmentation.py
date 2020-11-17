# -*- coding: utf-8 -*-
"""6Dpose-CNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1d8LnEwfEVd98INTtp19qj6Nu-MqmaRq9
"""

import tensorflow as tf
tf.test.gpu_device_name()

from glob import glob
import numpy as np
import tensorflow as tf
from google.colab import drive
drive.mount('/content/drive')

dataset_path = "/content/drive/My Drive/"
training_data = "LINEMOD/cam/JPEGImages/"
val_data = "LINEMOD/cam/JPEGImages/"
TRAINSET_SIZE = len(glob(dataset_path + training_data + "*.jpg"))
print(f"The Training Dataset contains {TRAINSET_SIZE} images.")

VALSET_SIZE = len(glob(dataset_path + val_data + "*.jpg"))
print(f"The Validation Dataset contains {VALSET_SIZE} images.")

# Image size that we are going to use
IMG_SIZE = (480,640)
# Our images are RGB (3 channels)
N_CHANNELS = 3
# Scene Parsing has 150 classes + `not labeled`
N_CLASSES = 2

def parse_image(img_path: str) -> dict:
    image = tf.io.read_file(img_path)
    image = tf.image.decode_png(image, channels=3)
    image = tf.image.convert_image_dtype(image, tf.uint8)

    # For one Image path:
    # .../trainset/images/training/ADE_train_00000001.jpg
    # Its corresponding annotation path is:
    # .../trainset/annotations/training/ADE_train_00000001.png
    mask_path = tf.strings.regex_replace(img_path, "JPEGImages/00", "mask/")
    mask_path = tf.strings.regex_replace(mask_path, "jpg", "png")
    mask = tf.io.read_file(mask_path)
    # The masks contain a class index for each pixels
    mask = tf.image.decode_png(mask, channels=1)
    # In scene parsing, "not labeled" = 255
    # But it will mess up with our N_CLASS = 150
    # Since 255 means the 255th class
    # Which doesn't exist
    mask = tf.where(mask == 255, np.dtype('uint8').type(1), mask)
    # Note that we have to convert the new value (0)
    # With the same dtype than the tensor itself

    return {'image': image, 'segmentation_mask': mask}

@tf.function
def normalize(input_image: tf.Tensor, input_mask: tf.Tensor) -> tuple:
    input_image = tf.cast(input_image, tf.float32) / 255.0
    return input_image, input_mask

@tf.function
def load_image_train(datapoint: dict) -> tuple:
    
    input_image = tf.image.resize(datapoint['image'], (IMG_SIZE[0], IMG_SIZE[1]))
    input_mask = tf.image.resize(datapoint['segmentation_mask'], (IMG_SIZE[0], IMG_SIZE[1]))

    if tf.random.uniform(()) > 0.5:
        input_image = tf.image.flip_left_right(input_image)
        input_mask = tf.image.flip_left_right(input_mask)

    input_image, input_mask = normalize(input_image, input_mask)

    return input_image, input_mask

@tf.function
def load_image_test(datapoint: dict) -> tuple:
    input_image = tf.image.resize(datapoint['image'], (IMG_SIZE[0], IMG_SIZE[1]))
    input_mask = tf.image.resize(datapoint['segmentation_mask'], (IMG_SIZE[0], IMG_SIZE[1]))

    input_image, input_mask = normalize(input_image, input_mask)

    return input_image, input_mask


BATCH_SIZE = 16

# for reference about the BUFFER_SIZE in shuffle:
# https://stackoverflow.com/questions/46444018/meaning-of-buffer-size-in-dataset-map-dataset-prefetch-and-dataset-shuffle
BUFFER_SIZE = 1000
SEED=1
AUTOTUNE = tf.data.experimental.AUTOTUNE
train_dataset = tf.data.Dataset.list_files(dataset_path + training_data + "*.jpg", seed=SEED)
train_dataset = train_dataset.map(parse_image)

val_dataset = tf.data.Dataset.list_files(dataset_path + val_data + "*.jpg", seed=SEED)
val_dataset =val_dataset.map(parse_image)

dataset = {"train": train_dataset, "val": val_dataset}

# -- Train Dataset --#
dataset['train'] = dataset['train'].map(load_image_train, num_parallel_calls=tf.data.experimental.AUTOTUNE)
dataset['train'] = dataset['train'].shuffle(buffer_size=BUFFER_SIZE, seed=SEED)
dataset['train'] = dataset['train'].repeat()
dataset['train'] = dataset['train'].batch(BATCH_SIZE)
dataset['train'] = dataset['train'].prefetch(buffer_size=AUTOTUNE)

#-- Validation Dataset --#
dataset['val'] = dataset['val'].map(load_image_test)
dataset['val'] = dataset['val'].repeat()
dataset['val'] = dataset['val'].batch(BATCH_SIZE)
dataset['val'] = dataset['val'].prefetch(buffer_size=AUTOTUNE)

print(dataset['train'])
print(dataset['val'])

import matplotlib.pyplot as plt
def display_sample(display_list):
    plt.figure(figsize=(18, 18))

    title = ['Input Image', 'True Mask', 'Predicted Mask']

    for i in range(len(display_list)):
        plt.subplot(1, len(display_list), i+1)
        plt.title(title[i])
        plt.imshow(tf.keras.preprocessing.image.array_to_img(display_list[i]))
        plt.axis('off')
    plt.show()
    
for image, mask in dataset['train'].take(1):
    sample_image, sample_mask = image, mask
    break

display_sample([sample_image[0], sample_mask[0]])

import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
max_filter=512
num_classes = 2
image_shape = (480,640,3)
EPOCHS = 40
BATCH_SIZE = 16
DROPOUT = 0.75
initializer = 'he_normal'
N_CHANNELS=3
#base_model = VGG16(include_top=False, input_shape=image_shape, pooling='avg')
#base_model.trainable = True

# -- Keras Functional API -- #
# -- UNet Implementation -- #
# Everything here is from tensorflow.keras.layers
# I imported tensorflow.keras.layers * to make it easier to read
dropout_rate = 0.5
input_size = (image_shape[0], image_shape[1], N_CHANNELS)

# If you want to know more about why we are using `he_normal`:
# https://stats.stackexchange.com/questions/319323/whats-the-difference-between-variance-scaling-initializer-and-xavier-initialize/319849#319849  
# Or the excellent fastai course:
# https://github.com/fastai/course-v3/blob/master/nbs/dl2/02b_initializing.ipynb
initializer = 'he_normal'

# -- Encoder -- #
# Block encoder 1
inputs = tf.keras.layers.Input(shape=input_size)
conv_enc_1 = tf.keras.layers.Conv2D(max_filter/8, 3, activation='relu', padding='same', kernel_initializer=initializer)(inputs)
conv_enc_1 = tf.keras.layers.Conv2D(max_filter/8, 3, activation = 'relu', padding='same', kernel_initializer=initializer)(conv_enc_1)

# Block encoder 2
max_pool_enc_2 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(conv_enc_1)
conv_enc_2 = tf.keras.layers.Conv2D(max_filter/4, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(max_pool_enc_2)
conv_enc_2 = tf.keras.layers.Conv2D(max_filter/4, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(conv_enc_2)

# Block  encoder 3
max_pool_enc_3 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(conv_enc_2)
conv_enc_3 = tf.keras.layers.Conv2D(max_filter/2, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(max_pool_enc_3)
conv_enc_3 = tf.keras.layers.Conv2D(max_filter/2, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(conv_enc_3)
conv_enc_3 = tf.keras.layers.Conv2D(max_filter/2, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(conv_enc_3)

# Block  encoder 4
max_pool_enc_4 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(conv_enc_3)
conv_enc_4 = tf.keras.layers.Conv2D(max_filter, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(max_pool_enc_4)
conv_enc_4 = tf.keras.layers.Conv2D(max_filter, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(conv_enc_4)
conv_enc_4 = tf.keras.layers.Conv2D(max_filter, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(conv_enc_4)
# -- Encoder -- #

# ----------- #
maxpool = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(conv_enc_4)
conv = tf.keras.layers.Conv2D(max_filter, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(maxpool)
conv = tf.keras.layers.Conv2D(max_filter, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(conv)
conv = tf.keras.layers.Conv2D(max_filter, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(conv)
# ----------- #

#EMBEDDING

emb1_1=tf.keras.layers.Conv2D(max_filter/8, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(conv)
emb1_1=tf.keras.layers.Conv2DTranspose(max_filter/8, 5,strides=(2, 2), activation = 'relu', padding = 'same', kernel_initializer = initializer)(emb1_1)
#emb1_1=tf.keras.layers.Conv2D(max_filter/8, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(emb1_1)

emb1_2=tf.keras.layers.Conv2D(max_filter/8, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(conv_enc_4)

emb1=tf.keras.layers.Add()([emb1_1,emb1_2])
emb1=tf.keras.layers.Conv2D(max_filter/8, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(emb1)

#emb1 = tf.keras.layers.concatenate([emb1_1, emb1_2], axis = 3)
emb1=tf.keras.layers.Conv2DTranspose(max_filter/8, 14,strides=(8, 8), activation = 'relu', padding = 'same', kernel_initializer = initializer)(emb1)
emb1=tf.keras.layers.Conv2D(max_filter/8, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(emb1)
#emb1=tf.keras.layers.Conv2D(max_filter/8, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(emb1)

# -- Decoder -- #
# Block decoder 1
#up_dec_1 = tf.keras.layers.Conv2D(max_filter, 2, activation = 'relu', padding = 'same', kernel_initializer = initializer)(tf.keras.layers.UpSampling2D(size = (2,2))(conv))
#merge_dec_1 = tf.keras.layers.concatenate([conv_enc_4, up_dec_1], axis = 3)
#conv_dec_1 = tf.keras.layers.Conv2D(max_filter, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(merge_dec_1)
#conv_dec_1 = tf.keras.layers.Conv2D(max_filter, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(conv_dec_1)

# Block decoder 2
#up_dec_2 = tf.keras.layers.Conv2D(max_filter/2, 2, activation = 'relu', padding = 'same', kernel_initializer = initializer)(tf.keras.layers.UpSampling2D(size = (2,2))(conv_dec_1))
#merge_dec_2 = tf.keras.layers.concatenate([conv_enc_3, up_dec_2], axis = 3)
#conv_dec_2 = tf.keras.layers.Conv2D(max_filter/2, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(merge_dec_2)
#conv_dec_2 = tf.keras.layers.Conv2D(max_filter/2, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(conv_dec_2)

# Block decoder 3
#up_dec_3 = tf.keras.layers.Conv2D(max_filter/4, 2, activation = 'relu', padding = 'same', kernel_initializer = initializer)(tf.keras.layers.UpSampling2D(size = (2,2))(conv_dec_2))
#merge_dec_3 = tf.keras.layers.concatenate([conv_enc_2, up_dec_3], axis = 3)
#conv_dec_3 = tf.keras.layers.Conv2D(max_filter/4, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(merge_dec_3)
#conv_dec_3 = tf.keras.layers.Conv2D(max_filter/4, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(conv_dec_3)

# Block decoder 4
#up_dec_4 = tf.keras.layers.Conv2D(max_filter/8, 2, activation = 'relu', padding = 'same', kernel_initializer = initializer)(tf.keras.layers.UpSampling2D(size = (2,2))(conv_dec_3))
#merge_dec_4 = tf.keras.layers.concatenate([conv_enc_1, up_dec_4], axis = 3)
#conv_dec_4 = tf.keras.layers.Conv2D(max_filter/8, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(merge_dec_4)
#conv_dec_4 = tf.keras.layers.Conv2D(max_filter/8, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(conv_dec_4)
#conv_dec_4 = tf.keras.layers.Conv2D(2, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(conv_dec_4)
# -- Dencoder -- #

output = tf.keras.layers.Conv2D(num_classes, 1, activation = 'softmax')(emb1)

model = tf.keras.Model(inputs = inputs, outputs = output)
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.00001), loss = tf.keras.losses.SparseCategoricalCrossentropy(),
              metrics=['accuracy'])
model.summary()

def create_mask(pred_mask: tf.Tensor) -> tf.Tensor:
    # pred_mask -> [IMG_SIZE, SIZE, N_CLASS]
    # 1 prediction for each class but we want the highest score only
    # so we use argmax
    pred_mask = tf.argmax(pred_mask, axis=-1)
    # pred_mask becomes [IMG_SIZE, IMG_SIZE]
    # but matplotlib needs [IMG_SIZE, IMG_SIZE, 1]
    pred_mask = tf.expand_dims(pred_mask, axis=-1)
    return pred_mask

def show_predictions(dataset=None, num=1):
    if dataset:
        for image, mask in dataset.take(num):
            pred_mask = model.predict(image[0][tf.newaxis, ...])
            display_sample([image[0], sample_mask[0], create_mask(pred_mask)[0]])
    else:
        # The model is expecting a tensor of the size
        # [BATCH_SIZE, IMG_SIZE, IMG_SIZE, 3]
        # but sample_image[0] is [IMG_SIZE, IMG_SIZE, 3]
        # and we want only 1 inference to be faster
        # so we add an additional dimension [1, IMG_SIZE, IMG_SIZE, 3]
        one_img_batch = sample_image[0][tf.newaxis, ...]
        # one_img_batch -> [1, IMG_SIZE, IMG_SIZE, 3]
        inference = model.predict(one_img_batch)
        # inference -> [1, IMG_SIZE, IMG_SIZE, N_CLASS]
        pred_mask = create_mask(inference)
        # pred_mask -> [1, IMG_SIZE, IMG_SIZE, 1]
        display_sample([sample_image[0], sample_mask[0],
                        pred_mask[0]])
for image, mask in dataset['train'].take(1):
    sample_image, sample_mask = image, mask

show_predictions()

EPOCHS = 40
BATCH_SIZE=16
STEPS_PER_EPOCH = TRAINSET_SIZE // BATCH_SIZE
VALIDATION_STEPS = VALSET_SIZE // BATCH_SIZE
# sometimes it can be very interesting to run some batches on cpu
# because the tracing is way better than on GPU
# you will have more obvious error message
# but in our case, it takes A LOT of time

# On CPU
# with tf.device("/cpu:0"):
#     model_history = model.fit(dataset['train'], epochs=EPOCHS,
#                               steps_per_epoch=STEPS_PER_EPOCH,
#                               validation_steps=VALIDATION_STEPS,
#                               validation_data=dataset['val'])

# On GPU
model_history = model.fit(dataset['train'], epochs=EPOCHS, steps_per_epoch=STEPS_PER_EPOCH)

show_predictions(dataset['val'],num=2)



one_img_batch = sample_image[0][tf.newaxis, ...]
        # one_img_batch -> [1, IMG_SIZE, IMG_SIZE, 3]
inference = model.predict(one_img_batch)
print(np.max(create_mask(inference)))