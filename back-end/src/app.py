from flask import Flask, escape, request, jsonify
from flask_cors import CORS, cross_origin
import tensorflow as tf
import os
app = Flask(__name__)
CORS(app)
gpus = tf.config.experimental.list_physical_devices('GPU')
print(gpus)
class Model(tf.keras.Model):

  def __init__(self):
    super(Model, self).__init__()
    self.conv1 = tf.keras.layers.Conv2D(32, 3, activation='relu', bias_initializer='he_normal')
    self.conv2 = tf.keras.layers.Conv2D(64, 3, activation='relu', bias_initializer='he_normal')
    self.max0 = tf.keras.layers.MaxPool2D(2,2)
    self.conv3 = tf.keras.layers.Conv2D(64, 3, activation='relu', padding="same")
    self.conv4 = tf.keras.layers.Conv2D(64, 3, activation='relu', padding="same")
    self.conv5 = tf.keras.layers.Conv2D(128, 3, activation='relu')
    self.conv6 = tf.keras.layers.Conv2D(128, 3, activation='relu', padding="same")
    self.conv7 = tf.keras.layers.Conv2D(128, 3, activation='relu', padding="same")
    self.conv8 = tf.keras.layers.Conv2D(256, 3, activation='relu')
    self.conv9 = tf.keras.layers.Conv2D(256, 3, activation='relu', padding="same")
    self.conv10 = tf.keras.layers.Conv2D(256, 3, activation='relu', padding="same")
    self.conv11 = tf.keras.layers.Conv2D(512, 3, activation='relu')
    self.conv12 = tf.keras.layers.Conv2D(512, 3, activation='relu', padding="same")
    self.conv13 = tf.keras.layers.Conv2D(512, 3, activation='relu', padding="same")
    self.flatten = tf.keras.layers.Flatten()
    self.d1 = tf.keras.layers.Dense(1000, activation='relu', use_bias= True)
    self.b1 = tf.keras.layers.BatchNormalization(trainable=True)
    self.d2 = tf.keras.layers.Dense(1, activation='sigmoid',  use_bias= True)

  def call(self, x):
    x = tf.reshape(x, [-1, 50, 50, 3])
    x = self.conv1(x)
    x = self.conv2(x)
    x = self.b1(x)
    x = self.conv3(x)
    x = self.max0(x)
    x = self.flatten(x)
    x = self.d1(x)
    x = self.d2(x)
    return x
  
  def get_model():
    return Model(name='cnn')


model = Model()

model.load_weights('../trained_model')
cwd = os.getcwd()

def parse_image(img):
    image = tf.io.read_file(img)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.image.resize(image, [50, 50])
    os.unlink(img)
    return image

if __name__ == '__main__':
    app.run(host='0.0.0.0')

@app.route('/', methods = ['POST', 'GET'])
def main():
    if request.method == 'POST':
        file = request.files["file"]
        file.save(cwd + file.filename)
        image = parse_image(cwd + file.filename)
        pred = model(image)
        return jsonify({'pred':round(pred.numpy()[0][0]*100, 2)})



    if request.method == 'GET':
        return f'Flask'
