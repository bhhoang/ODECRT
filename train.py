from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.preprocessing.image import ImageDataGenerator
from keras.layers.convolutional import Conv2D, MaxPooling2D
import matplotlib.pyplot as plt
import os
from sklearn.decomposition import PCA
from PIL import Image
from sklearn.preprocessing import MinMaxScaler
import cv2
import numpy as np

# Character Labels
labels = [str(i) for i in range(10)] + \
         [chr(i) for i in range(ord('A'), ord('Z')+1)] + \
         [chr(i) for i in range(ord('a'), ord('z')+1)]
# Image Dimensions for resizing
img_width, img_height = 128, 128
# Processed data directories
train_data_dir = 'dataset/train'
validation_data_dir = 'dataset/valid'
test_data_dir = 'dataset/test'
# Hyperparameters
epochs = 15
batch_size = 32
num_classes = len(labels)

# Data Augmentation
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=1,
    width_shift_range=0.01,
    height_shift_range=0.01,
    horizontal_flip=False,
    vertical_flip=False
)


# Create labels for training data
train_labels = []
i = 0
for folder in os.listdir(train_data_dir):
    label = [0]*num_classes
    label[i] = 1
    for _ in os.listdir(os.path.join(train_data_dir, folder)):
        train_labels.append(label)
    i += 1
train_labels = np.array(train_labels)

# Create labels for validation data
validation_labels = []
j = 0
for valid_img in os.listdir(validation_data_dir):
    label = [0]*num_classes
    label[j] = 1
    for _ in os.listdir(os.path.join(validation_data_dir, valid_img)):
        validation_labels.append(label)
    j += 1
validation_labels = np.array(validation_labels)

# Create labels for test data
test_labels = []
k = 0
for test_img in os.listdir(test_data_dir):
    label = [0]*num_classes
    label[k] = 1
    for _ in os.listdir(os.path.join(test_data_dir, test_img)):
        test_labels.append(label)
    k += 1
test_labels = np.array(test_labels)


train = []
for folder in os.listdir(train_data_dir):
    for img in os.listdir(os.path.join(train_data_dir, folder)):
        img = cv2.imread(os.path.join(train_data_dir, folder, img), cv2.IMREAD_GRAYSCALE)
        img = Image.fromarray(img)
        img = img.resize((img_width, img_height))
        img = np.array(img)
        scaler = MinMaxScaler()
        img = scaler.fit_transform(img)
        pca = PCA(n_components=56)
        img = pca.fit_transform(img)
        img = np.expand_dims(img, axis=-1)
        if img is not None:
            train.append(img)
train = np.array(train)
train_generator = datagen.flow(train, train_labels, batch_size=batch_size)

validation = []
for valid_img in os.listdir(validation_data_dir):
    for img in os.listdir(os.path.join(validation_data_dir, valid_img)):
        img = cv2.imread(os.path.join(validation_data_dir, valid_img, img), cv2.IMREAD_GRAYSCALE)
        img = Image.fromarray(img)
        img = img.resize((img_width, img_height))
        img = np.array(img)
        scaler = MinMaxScaler()
        img = scaler.fit_transform(img)
        pca = PCA(n_components=56)
        img = pca.fit_transform(img)
        img = np.expand_dims(img, axis=-1)
        if img is not None:
            validation.append(img)
validation = np.array(validation)
validation_generator = datagen.flow(validation, validation_labels, batch_size=batch_size)

test = []
for test_img in os.listdir(test_data_dir):
    for img in os.listdir(os.path.join(test_data_dir, test_img)):
        img = cv2.imread(os.path.join(test_data_dir, test_img, img), cv2.IMREAD_GRAYSCALE)
        img = Image.fromarray(img)
        img = img.resize((img_width, img_height))
        img = np.array(img)
        scaler = MinMaxScaler()
        img = scaler.fit_transform(img)
        pca = PCA(n_components=56)
        img = pca.fit_transform(img)
        img = np.expand_dims(img, axis=-1)
        if img is not None:
            test.append(img)
test = np.array(test)
test_generator = datagen.flow(test, test_labels, batch_size=batch_size)

# Model Architecture
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(128, 56, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),

    Flatten(),
    Dense(310, activation='relu'),
    Dropout(0.1),
    Dense(num_classes, activation='softmax')
])

# Compile the model
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
print(model.summary())

# Train the model
history = model.fit(
          train_generator,
          steps_per_epoch= train_generator.n // batch_size,
          epochs=epochs,
          validation_data=validation_generator,
          validation_steps= validation_generator.n // batch_size)


# Save the model
model.save('model.h5')

# Evaluate the model
score = model.evaluate(test_generator, verbose=1)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

# Plot fitting history
plt.plot(range(1, epochs+1), history.history['accuracy'], label='Train')
plt.plot(range(1, epochs+1), history.history['val_accuracy'], label='Validation')
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.savefig('accuracy.png')
plt.show()