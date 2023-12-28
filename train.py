import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.preprocessing.image import ImageDataGenerator
from keras.layers.convolutional import Conv2D, MaxPooling2D
import matplotlib.pyplot as plt


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
epochs = 13
batch_size = 32
num_classes = len(labels)

# Data Augmentation
datagen = ImageDataGenerator(
    rescale=1./255,
    #rotation_range=2,
    #width_shift_range=0.01,
    #height_shift_range=0.01,
    #horizontal_flip=False,
    #vertical_flip=False
)

train_generator = datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    color_mode='grayscale',
    batch_size=batch_size,
    class_mode='categorical'
)

validation_generator = datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    color_mode='grayscale',
    batch_size=batch_size,
    class_mode='categorical')

test_generator = datagen.flow_from_directory(
    test_data_dir,
    target_size=(img_width, img_height),
    color_mode='grayscale',
    batch_size=batch_size,
    class_mode='categorical')

# Model Architecture
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(img_width, img_height, 1)),
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

#print(model.summary())
# Compile the model
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# Train the model
history = model.fit(
          train_generator,
          steps_per_epoch= train_generator.samples // batch_size,
          epochs=epochs,
          validation_data=validation_generator,
          validation_steps= validation_generator.samples // batch_size)

# Save the model
model.save('model.h5')

# Evaluate the model
score = model.evaluate(test_generator, verbose=1)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

# Plot fitting history
plt.plot(range(1, epochs+1), history.history['accuracy'], label='Train')
plt.plot(range(1,epochs+1), history.history['val_accuracy'], label='Validation')
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.savefig('accuracy.png')
plt.show()
