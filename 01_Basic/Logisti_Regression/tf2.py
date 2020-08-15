import os
# For Mac User...
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import numpy as np

import tensorflow as tf
from tensorflow.keras import models, layers, optimizers, losses, utils, datasets

tf.random.set_seed(777)

print("Packge Loaded!")
# %%
EPOCHS = 500
BATCH_SIZE = 128

# Data Loading
(train_x, train_y), (test_x, test_y) = datasets.mnist.load_data()
train_x, test_x = np.reshape(train_x/255., [-1, 784]), np.reshape(test_x/255., [-1, 784])
# 0 : digit < 5
# 1 : digit >= 5
train_y, test_y = np.greater_equal(train_y, 5)[..., np.newaxis], np.greater_equal(test_y, 5)[..., np.newaxis]


print("Train Data's Shape : ", train_x.shape, train_y.shape)
print("Test Data's Shape : ", test_x.shape, test_y.shape)

train_ds = tf.data.Dataset.from_tensor_slices(
    (train_x, train_y)).shuffle(10000).batch(BATCH_SIZE)

test_ds = tf.data.Dataset.from_tensor_slices(
    (test_x, test_y)).shuffle(10000).batch(BATCH_SIZE)

# plt.plot(x, y, 'r.')
# plt.show()
print("Data Prepared!")

# %%
class LinearRegression(models.Model):
    def __init__(self):
        super(LinearRegression, self).__init__()
        self.d = layers.Dense(1, input_shape=(1, ), activation='sigmoid')

    def call(self, x):
        return self.d(x)

# Create an instance of the model
model = LinearRegression()

loss_object = losses.BinaryCrossentropy()

optimizer = optimizers.Adam()

# %%
for epoch in range(EPOCHS):
    for batch_x, batch_y in train_ds:
        with tf.GradientTape() as tape:
            predictions = model(batch_x, training=True)
            loss = loss_object(batch_y, predictions)
            gradients = tape.gradient(loss, model.trainable_variables)
            optimizer.apply_gradients(zip(gradients, model.trainable_variables))

    print("{:5}|{:10.6f}".format(epoch+1, loss))