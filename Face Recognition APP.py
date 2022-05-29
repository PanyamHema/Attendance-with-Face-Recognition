{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 1. Setup"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1.1 Install Dependencies"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "!pip install tensorflow==2.4.1 tensorflow-gpu==2.4.1 opencv-python matplotlib"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1.2 Import Dependencies"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import standard dependencies\n",
    "import cv2\n",
    "import os\n",
    "import random\n",
    "import numpy as np\n",
    "from matplotlib import pyplot as plt"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import tensorflow dependencies - Functional API\n",
    "from tensorflow.keras.models import Model\n",
    "from tensorflow.keras.layers import Layer, Conv2D, Dense, MaxPooling2D, Input, Flatten\n",
    "import tensorflow as tf"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1.3 Set GPU Growth"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Avoid OOM errors by setting GPU Memory Consumption Growth\n",
    "gpus = tf.config.experimental.list_physical_devices('GPU')\n",
    "for gpu in gpus: \n",
    "    tf.config.experimental.set_memory_growth(gpu, True)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1.4 Create Folder Structures"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Setup paths\n",
    "POS_PATH = os.path.join('data', 'positive')\n",
    "NEG_PATH = os.path.join('data', 'negative')\n",
    "ANC_PATH = os.path.join('data', 'anchor')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Make the directories\n",
    "os.makedirs(POS_PATH)\n",
    "os.makedirs(NEG_PATH)\n",
    "os.makedirs(ANC_PATH)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 2. Collect Positives and Anchors"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2.1 Untar Labelled Faces in the Wild Dataset"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# http://vis-www.cs.umass.edu/lfw/"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Uncompress Tar GZ Labelled Faces in the Wild Dataset\n",
    "!tar -xf lfw.tgz"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Move LFW Images to the following repository data/negative\n",
    "for directory in os.listdir('lfw'):\n",
    "    for file in os.listdir(os.path.join('lfw', directory)):\n",
    "        EX_PATH = os.path.join('lfw', directory, file)\n",
    "        NEW_PATH = os.path.join(NEG_PATH, file)\n",
    "        os.replace(EX_PATH, NEW_PATH)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2.2 Collect Positive and Anchor Classes"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import uuid library to generate unique image names\n",
    "import uuid"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "os.path.join(ANC_PATH, '{}.jpg'.format(uuid.uuid1()))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Establish a connection to the webcam\n",
    "cap = cv2.VideoCapture(4)\n",
    "while cap.isOpened(): \n",
    "    ret, frame = cap.read()\n",
    "   \n",
    "    # Cut down frame to 250x250px\n",
    "    frame = frame[120:120+250,200:200+250, :]\n",
    "    \n",
    "    # Collect anchors \n",
    "    if cv2.waitKey(1) & 0XFF == ord('a'):\n",
    "        # Create the unique file path \n",
    "        imgname = os.path.join(ANC_PATH, '{}.jpg'.format(uuid.uuid1()))\n",
    "        # Write out anchor image\n",
    "        cv2.imwrite(imgname, frame)\n",
    "    \n",
    "    # Collect positives\n",
    "    if cv2.waitKey(1) & 0XFF == ord('p'):\n",
    "        # Create the unique file path \n",
    "        imgname = os.path.join(POS_PATH, '{}.jpg'.format(uuid.uuid1()))\n",
    "        # Write out positive image\n",
    "        cv2.imwrite(imgname, frame)\n",
    "    \n",
    "    # Show image back to screen\n",
    "    cv2.imshow('Image Collection', frame)\n",
    "    \n",
    "    # Breaking gracefully\n",
    "    if cv2.waitKey(1) & 0XFF == ord('q'):\n",
    "        break\n",
    "        \n",
    "# Release the webcam\n",
    "cap.release()\n",
    "# Close the image show frame\n",
    "cv2.destroyAllWindows()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.imshow(frame[120:120+250,200:200+250, :])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 2.x NEW - Data Augmentation"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "def data_aug(img):\n",
    "    data = []\n",
    "    for i in range(9):\n",
    "        img = tf.image.stateless_random_brightness(img, max_delta=0.02, seed=(1,2))\n",
    "        img = tf.image.stateless_random_contrast(img, lower=0.6, upper=1, seed=(1,3))\n",
    "        # img = tf.image.stateless_random_crop(img, size=(20,20,3), seed=(1,2))\n",
    "        img = tf.image.stateless_random_flip_left_right(img, seed=(np.random.randint(100),np.random.randint(100)))\n",
    "        img = tf.image.stateless_random_jpeg_quality(img, min_jpeg_quality=90, max_jpeg_quality=100, seed=(np.random.randint(100),np.random.randint(100)))\n",
    "        img = tf.image.stateless_random_saturation(img, lower=0.9,upper=1, seed=(np.random.randint(100),np.random.randint(100)))\n",
    "            \n",
    "        data.append(img)\n",
    "    \n",
    "    return data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import uuid"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [],
   "source": [
    "img_path = os.path.join(ANC_PATH, '924e839c-135f-11ec-b54e-a0cec8d2d278.jpg')\n",
    "img = cv2.imread(img_path)\n",
    "augmented_images = data_aug(img)\n",
    "\n",
    "for image in augmented_images:\n",
    "    cv2.imwrite(os.path.join(ANC_PATH, '{}.jpg'.format(uuid.uuid1())), image.numpy())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "for file_name in os.listdir(os.path.join(POS_PATH)):\n",
    "    img_path = os.path.join(POS_PATH, file_name)\n",
    "    img = cv2.imread(img_path)\n",
    "    augmented_images = data_aug(img) \n",
    "    \n",
    "    for image in augmented_images:\n",
    "        cv2.imwrite(os.path.join(POS_PATH, '{}.jpg'.format(uuid.uuid1())), image.numpy())"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 3. Load and Preprocess Images"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3.1 Get Image Directories"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 172,
   "metadata": {},
   "outputs": [],
   "source": [
    "anchor = tf.data.Dataset.list_files(ANC_PATH+'\\*.jpg').take(3000)\n",
    "positive = tf.data.Dataset.list_files(POS_PATH+'\\*.jpg').take(3000)\n",
    "negative = tf.data.Dataset.list_files(NEG_PATH+'\\*.jpg').take(3000)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 173,
   "metadata": {},
   "outputs": [],
   "source": [
    "dir_test = anchor.as_numpy_iterator()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 174,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "b'data\\\\anchor\\\\a004ebfe-135f-11ec-9f91-a0cec8d2d278.jpg'\n"
     ]
    }
   ],
   "source": [
    "print(dir_test.next())"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3.2 Preprocessing - Scale and Resize"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "def preprocess(file_path):\n",
    "    \n",
    "    # Read in image from file path\n",
    "    byte_img = tf.io.read_file(file_path)\n",
    "    # Load in the image \n",
    "    img = tf.io.decode_jpeg(byte_img)\n",
    "    \n",
    "    # Preprocessing steps - resizing the image to be 100x100x3\n",
    "    img = tf.image.resize(img, (100,100))\n",
    "    # Scale image to be between 0 and 1 \n",
    "    img = img / 255.0\n",
    "\n",
    "    # Return image\n",
    "    return img"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 176,
   "metadata": {
    "scrolled": true,
    "tags": []
   },
   "outputs": [],
   "source": [
    "img = preprocess('data\\\\anchor\\\\a4e73462-135f-11ec-9e6e-a0cec8d2d278.jpg')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 177,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "1.0"
      ]
     },
     "execution_count": 177,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "img.numpy().max() "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 178,
   "metadata": {},
   "outputs": [
    {
     "ename": "NameError",
     "evalue": "name 'dataset' is not defined",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mNameError\u001b[0m                                 Traceback (most recent call last)",
      "\u001b[1;32m~\\AppData\\Local\\Temp/ipykernel_6884/2569123063.py\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[1;32m----> 1\u001b[1;33m \u001b[0mdataset\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mmap\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mpreprocess\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[1;31mNameError\u001b[0m: name 'dataset' is not defined"
     ]
    }
   ],
   "source": [
    "dataset.map(preprocess)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3.3 Create Labelled Dataset"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 179,
   "metadata": {},
   "outputs": [],
   "source": [
    "# (anchor, positive) => 1,1,1,1,1\n",
    "# (anchor, negative) => 0,0,0,0,0"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 180,
   "metadata": {},
   "outputs": [],
   "source": [
    "positives = tf.data.Dataset.zip((anchor, positive, tf.data.Dataset.from_tensor_slices(tf.ones(len(anchor)))))\n",
    "negatives = tf.data.Dataset.zip((anchor, negative, tf.data.Dataset.from_tensor_slices(tf.zeros(len(anchor)))))\n",
    "data = positives.concatenate(negatives)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 181,
   "metadata": {},
   "outputs": [],
   "source": [
    "samples = data.as_numpy_iterator()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 182,
   "metadata": {},
   "outputs": [],
   "source": [
    "exampple = samples.next()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 183,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(b'data\\\\anchor\\\\5b0483e2-33a9-11ec-9085-a0cec8d2d278.jpg',\n",
       " b'data\\\\positive\\\\7dfdedca-33a9-11ec-ad17-a0cec8d2d278.jpg',\n",
       " 1.0)"
      ]
     },
     "execution_count": 183,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "exampple"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3.4 Build Train and Test Partition"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 184,
   "metadata": {},
   "outputs": [],
   "source": [
    "def preprocess_twin(input_img, validation_img, label):\n",
    "    return(preprocess(input_img), preprocess(validation_img), label)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 185,
   "metadata": {},
   "outputs": [],
   "source": [
    "res = preprocess_twin(*exampple)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 186,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.image.AxesImage at 0x1cd229c4198>"
      ]
     },
     "execution_count": 186,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.imshow(res[1])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "1.0"
      ]
     },
     "execution_count": 19,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "res[2]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 187,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Build dataloader pipeline\n",
    "data = data.map(preprocess_twin)\n",
    "data = data.cache()\n",
    "data = data.shuffle(buffer_size=10000)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 188,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Training partition\n",
    "train_data = data.take(round(len(data)*.7))\n",
    "train_data = train_data.batch(16)\n",
    "train_data = train_data.prefetch(8)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 189,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Testing partition\n",
    "test_data = data.skip(round(len(data)*.7))\n",
    "test_data = test_data.take(round(len(data)*.3))\n",
    "test_data = test_data.batch(16)\n",
    "test_data = test_data.prefetch(8)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 4. Model Engineering"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4.1 Build Embedding Layer"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 190,
   "metadata": {},
   "outputs": [],
   "source": [
    "inp = Input(shape=(100,100,3), name='input_image')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 191,
   "metadata": {},
   "outputs": [],
   "source": [
    "c1 = Conv2D(64, (10,10), activation='relu')(inp)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 192,
   "metadata": {},
   "outputs": [],
   "source": [
    "m1 = MaxPooling2D(64, (2,2), padding='same')(c1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 193,
   "metadata": {},
   "outputs": [],
   "source": [
    "c2 = Conv2D(128, (7,7), activation='relu')(m1)\n",
    "m2 = MaxPooling2D(64, (2,2), padding='same')(c2)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 194,
   "metadata": {},
   "outputs": [],
   "source": [
    "c3 = Conv2D(128, (4,4), activation='relu')(m2)\n",
    "m3 = MaxPooling2D(64, (2,2), padding='same')(c3)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 195,
   "metadata": {},
   "outputs": [],
   "source": [
    "c4 = Conv2D(256, (4,4), activation='relu')(m3)\n",
    "f1 = Flatten()(c4)\n",
    "d1 = Dense(4096, activation='sigmoid')(f1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 196,
   "metadata": {},
   "outputs": [],
   "source": [
    "mod = Model(inputs=[inp], outputs=[d1], name='embedding')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 197,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Model: \"embedding\"\n",
      "_________________________________________________________________\n",
      "Layer (type)                 Output Shape              Param #   \n",
      "=================================================================\n",
      "input_image (InputLayer)     [(None, 100, 100, 3)]     0         \n",
      "_________________________________________________________________\n",
      "conv2d_8 (Conv2D)            (None, 91, 91, 64)        19264     \n",
      "_________________________________________________________________\n",
      "max_pooling2d_6 (MaxPooling2 (None, 46, 46, 64)        0         \n",
      "_________________________________________________________________\n",
      "conv2d_9 (Conv2D)            (None, 40, 40, 128)       401536    \n",
      "_________________________________________________________________\n",
      "max_pooling2d_7 (MaxPooling2 (None, 20, 20, 128)       0         \n",
      "_________________________________________________________________\n",
      "conv2d_10 (Conv2D)           (None, 17, 17, 128)       262272    \n",
      "_________________________________________________________________\n",
      "max_pooling2d_8 (MaxPooling2 (None, 9, 9, 128)         0         \n",
      "_________________________________________________________________\n",
      "conv2d_11 (Conv2D)           (None, 6, 6, 256)         524544    \n",
      "_________________________________________________________________\n",
      "flatten_2 (Flatten)          (None, 9216)              0         \n",
      "_________________________________________________________________\n",
      "dense_4 (Dense)              (None, 4096)              37752832  \n",
      "=================================================================\n",
      "Total params: 38,960,448\n",
      "Trainable params: 38,960,448\n",
      "Non-trainable params: 0\n",
      "_________________________________________________________________\n"
     ]
    }
   ],
   "source": [
    "mod.summary()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 198,
   "metadata": {},
   "outputs": [],
   "source": [
    "def make_embedding(): \n",
    "    inp = Input(shape=(100,100,3), name='input_image')\n",
    "    \n",
    "    # First block\n",
    "    c1 = Conv2D(64, (10,10), activation='relu')(inp)\n",
    "    m1 = MaxPooling2D(64, (2,2), padding='same')(c1)\n",
    "    \n",
    "    # Second block\n",
    "    c2 = Conv2D(128, (7,7), activation='relu')(m1)\n",
    "    m2 = MaxPooling2D(64, (2,2), padding='same')(c2)\n",
    "    \n",
    "    # Third block \n",
    "    c3 = Conv2D(128, (4,4), activation='relu')(m2)\n",
    "    m3 = MaxPooling2D(64, (2,2), padding='same')(c3)\n",
    "    \n",
    "    # Final embedding block\n",
    "    c4 = Conv2D(256, (4,4), activation='relu')(m3)\n",
    "    f1 = Flatten()(c4)\n",
    "    d1 = Dense(4096, activation='sigmoid')(f1)\n",
    "    \n",
    "    \n",
    "    return Model(inputs=[inp], outputs=[d1], name='embedding')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 199,
   "metadata": {},
   "outputs": [],
   "source": [
    "embedding = make_embedding()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 200,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Model: \"embedding\"\n",
      "_________________________________________________________________\n",
      "Layer (type)                 Output Shape              Param #   \n",
      "=================================================================\n",
      "input_image (InputLayer)     [(None, 100, 100, 3)]     0         \n",
      "_________________________________________________________________\n",
      "conv2d_12 (Conv2D)           (None, 91, 91, 64)        19264     \n",
      "_________________________________________________________________\n",
      "max_pooling2d_9 (MaxPooling2 (None, 46, 46, 64)        0         \n",
      "_________________________________________________________________\n",
      "conv2d_13 (Conv2D)           (None, 40, 40, 128)       401536    \n",
      "_________________________________________________________________\n",
      "max_pooling2d_10 (MaxPooling (None, 20, 20, 128)       0         \n",
      "_________________________________________________________________\n",
      "conv2d_14 (Conv2D)           (None, 17, 17, 128)       262272    \n",
      "_________________________________________________________________\n",
      "max_pooling2d_11 (MaxPooling (None, 9, 9, 128)         0         \n",
      "_________________________________________________________________\n",
      "conv2d_15 (Conv2D)           (None, 6, 6, 256)         524544    \n",
      "_________________________________________________________________\n",
      "flatten_3 (Flatten)          (None, 9216)              0         \n",
      "_________________________________________________________________\n",
      "dense_5 (Dense)              (None, 4096)              37752832  \n",
      "=================================================================\n",
      "Total params: 38,960,448\n",
      "Trainable params: 38,960,448\n",
      "Non-trainable params: 0\n",
      "_________________________________________________________________\n"
     ]
    }
   ],
   "source": [
    "embedding.summary()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4.2 Build Distance Layer"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Siamese L1 Distance class\n",
    "class L1Dist(Layer):\n",
    "    \n",
    "    # Init method - inheritance\n",
    "    def __init__(self, **kwargs):\n",
    "        super().__init__()\n",
    "       \n",
    "    # Magic happens here - similarity calculation\n",
    "    def call(self, input_embedding, validation_embedding):\n",
    "        return tf.math.abs(input_embedding - validation_embedding)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 202,
   "metadata": {},
   "outputs": [],
   "source": [
    "l1 = L1Dist()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 203,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "ename": "NameError",
     "evalue": "name 'anchor_embedding' is not defined",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mNameError\u001b[0m                                 Traceback (most recent call last)",
      "\u001b[1;32m~\\AppData\\Local\\Temp/ipykernel_6884/3877395630.py\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[1;32m----> 1\u001b[1;33m \u001b[0ml1\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0manchor_embedding\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mvalidation_embedding\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[1;31mNameError\u001b[0m: name 'anchor_embedding' is not defined"
     ]
    }
   ],
   "source": [
    "l1(anchor_embedding, validation_embedding)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4.3 Make Siamese Model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 204,
   "metadata": {},
   "outputs": [],
   "source": [
    "input_image = Input(name='input_img', shape=(100,100,3))\n",
    "validation_image = Input(name='validation_img', shape=(100,100,3))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 205,
   "metadata": {},
   "outputs": [],
   "source": [
    "inp_embedding = embedding(input_image)\n",
    "val_embedding = embedding(validation_image)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 206,
   "metadata": {},
   "outputs": [],
   "source": [
    "siamese_layer = L1Dist()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 207,
   "metadata": {},
   "outputs": [],
   "source": [
    "distances = siamese_layer(inp_embedding, val_embedding)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 208,
   "metadata": {},
   "outputs": [],
   "source": [
    "classifier = Dense(1, activation='sigmoid')(distances)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 209,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<KerasTensor: shape=(None, 1) dtype=float32 (created by layer 'dense_6')>"
      ]
     },
     "execution_count": 209,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "classifier"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 210,
   "metadata": {},
   "outputs": [],
   "source": [
    "siamese_network = Model(inputs=[input_image, validation_image], outputs=classifier, name='SiameseNetwork')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 211,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Model: \"SiameseNetwork\"\n",
      "__________________________________________________________________________________________________\n",
      "Layer (type)                    Output Shape         Param #     Connected to                     \n",
      "==================================================================================================\n",
      "input_img (InputLayer)          [(None, 100, 100, 3) 0                                            \n",
      "__________________________________________________________________________________________________\n",
      "validation_img (InputLayer)     [(None, 100, 100, 3) 0                                            \n",
      "__________________________________________________________________________________________________\n",
      "embedding (Functional)          (None, 4096)         38960448    input_img[0][0]                  \n",
      "                                                                 validation_img[0][0]             \n",
      "__________________________________________________________________________________________________\n",
      "l1_dist_4 (L1Dist)              (None, 4096)         0           embedding[0][0]                  \n",
      "                                                                 embedding[1][0]                  \n",
      "__________________________________________________________________________________________________\n",
      "dense_6 (Dense)                 (None, 1)            4097        l1_dist_4[0][0]                  \n",
      "==================================================================================================\n",
      "Total params: 38,964,545\n",
      "Trainable params: 38,964,545\n",
      "Non-trainable params: 0\n",
      "__________________________________________________________________________________________________\n"
     ]
    }
   ],
   "source": [
    "siamese_network.summary()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 212,
   "metadata": {},
   "outputs": [],
   "source": [
    "def make_siamese_model(): \n",
    "    \n",
    "    # Anchor image input in the network\n",
    "    input_image = Input(name='input_img', shape=(100,100,3))\n",
    "    \n",
    "    # Validation image in the network \n",
    "    validation_image = Input(name='validation_img', shape=(100,100,3))\n",
    "    \n",
    "    # Combine siamese distance components\n",
    "    siamese_layer = L1Dist()\n",
    "    siamese_layer._name = 'distance'\n",
    "    distances = siamese_layer(embedding(input_image), embedding(validation_image))\n",
    "    \n",
    "    # Classification layer \n",
    "    classifier = Dense(1, activation='sigmoid')(distances)\n",
    "    \n",
    "    return Model(inputs=[input_image, validation_image], outputs=classifier, name='SiameseNetwork')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 213,
   "metadata": {},
   "outputs": [],
   "source": [
    "siamese_model = make_siamese_model()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 214,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Model: \"SiameseNetwork\"\n",
      "__________________________________________________________________________________________________\n",
      "Layer (type)                    Output Shape         Param #     Connected to                     \n",
      "==================================================================================================\n",
      "input_img (InputLayer)          [(None, 100, 100, 3) 0                                            \n",
      "__________________________________________________________________________________________________\n",
      "validation_img (InputLayer)     [(None, 100, 100, 3) 0                                            \n",
      "__________________________________________________________________________________________________\n",
      "embedding (Functional)          (None, 4096)         38960448    input_img[0][0]                  \n",
      "                                                                 validation_img[0][0]             \n",
      "__________________________________________________________________________________________________\n",
      "distance (L1Dist)               (None, 4096)         0           embedding[2][0]                  \n",
      "                                                                 embedding[3][0]                  \n",
      "__________________________________________________________________________________________________\n",
      "dense_7 (Dense)                 (None, 1)            4097        distance[0][0]                   \n",
      "==================================================================================================\n",
      "Total params: 38,964,545\n",
      "Trainable params: 38,964,545\n",
      "Non-trainable params: 0\n",
      "__________________________________________________________________________________________________\n"
     ]
    }
   ],
   "source": [
    "siamese_model.summary()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 5. Training"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5.1 Setup Loss and Optimizer"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 215,
   "metadata": {},
   "outputs": [],
   "source": [
    "binary_cross_loss = tf.losses.BinaryCrossentropy()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 216,
   "metadata": {},
   "outputs": [],
   "source": [
    "opt = tf.keras.optimizers.Adam(1e-4) # 0.0001"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5.2 Establish Checkpoints"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 217,
   "metadata": {},
   "outputs": [],
   "source": [
    "checkpoint_dir = './training_checkpoints'\n",
    "checkpoint_prefix = os.path.join(checkpoint_dir, 'ckpt')\n",
    "checkpoint = tf.train.Checkpoint(opt=opt, siamese_model=siamese_model)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5.3 Build Train Step Function"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 218,
   "metadata": {},
   "outputs": [],
   "source": [
    "test_batch = train_data.as_numpy_iterator()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 219,
   "metadata": {},
   "outputs": [],
   "source": [
    "batch_1 = test_batch.next()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 220,
   "metadata": {},
   "outputs": [],
   "source": [
    "X = batch_1[:2]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 221,
   "metadata": {},
   "outputs": [],
   "source": [
    "y = batch_1[2]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 222,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([1., 0., 1., 1., 1., 1., 1., 1., 0., 1., 0., 1., 0., 1., 1., 1.],\n",
       "      dtype=float32)"
      ]
     },
     "execution_count": 222,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "y"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 56,
   "metadata": {
    "collapsed": true,
    "jupyter": {
     "outputs_hidden": true
    },
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "\u001b[1;31mInit signature:\u001b[0m\n",
       "\u001b[0mtf\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mlosses\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mBinaryCrossentropy\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m\n",
       "\u001b[0m    \u001b[0mfrom_logits\u001b[0m\u001b[1;33m=\u001b[0m\u001b[1;32mFalse\u001b[0m\u001b[1;33m,\u001b[0m\u001b[1;33m\n",
       "\u001b[0m    \u001b[0mlabel_smoothing\u001b[0m\u001b[1;33m=\u001b[0m\u001b[1;36m0\u001b[0m\u001b[1;33m,\u001b[0m\u001b[1;33m\n",
       "\u001b[0m    \u001b[0mreduction\u001b[0m\u001b[1;33m=\u001b[0m\u001b[1;34m'auto'\u001b[0m\u001b[1;33m,\u001b[0m\u001b[1;33m\n",
       "\u001b[0m    \u001b[0mname\u001b[0m\u001b[1;33m=\u001b[0m\u001b[1;34m'binary_crossentropy'\u001b[0m\u001b[1;33m,\u001b[0m\u001b[1;33m\n",
       "\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
       "\u001b[1;31mSource:\u001b[0m        \n",
       "\u001b[1;32mclass\u001b[0m \u001b[0mBinaryCrossentropy\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mLossFunctionWrapper\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\n",
       "\u001b[0m  \u001b[1;34m\"\"\"Computes the cross-entropy loss between true labels and predicted labels.\n",
       "\n",
       "  Use this cross-entropy loss when there are only two label classes (assumed to\n",
       "  be 0 and 1). For each example, there should be a single floating-point value\n",
       "  per prediction.\n",
       "\n",
       "  In the snippet below, each of the four examples has only a single\n",
       "  floating-pointing value, and both `y_pred` and `y_true` have the shape\n",
       "  `[batch_size]`.\n",
       "\n",
       "  Standalone usage:\n",
       "\n",
       "  >>> y_true = [[0., 1.], [0., 0.]]\n",
       "  >>> y_pred = [[0.6, 0.4], [0.4, 0.6]]\n",
       "  >>> # Using 'auto'/'sum_over_batch_size' reduction type.\n",
       "  >>> bce = tf.keras.losses.BinaryCrossentropy()\n",
       "  >>> bce(y_true, y_pred).numpy()\n",
       "  0.815\n",
       "\n",
       "  >>> # Calling with 'sample_weight'.\n",
       "  >>> bce(y_true, y_pred, sample_weight=[1, 0]).numpy()\n",
       "  0.458\n",
       "\n",
       "   >>> # Using 'sum' reduction type.\n",
       "  >>> bce = tf.keras.losses.BinaryCrossentropy(\n",
       "  ...     reduction=tf.keras.losses.Reduction.SUM)\n",
       "  >>> bce(y_true, y_pred).numpy()\n",
       "  1.630\n",
       "\n",
       "  >>> # Using 'none' reduction type.\n",
       "  >>> bce = tf.keras.losses.BinaryCrossentropy(\n",
       "  ...     reduction=tf.keras.losses.Reduction.NONE)\n",
       "  >>> bce(y_true, y_pred).numpy()\n",
       "  array([0.916 , 0.714], dtype=float32)\n",
       "\n",
       "  Usage with the `tf.keras` API:\n",
       "\n",
       "  ```python\n",
       "  model.compile(optimizer='sgd', loss=tf.keras.losses.BinaryCrossentropy())\n",
       "  ```\n",
       "  \"\"\"\u001b[0m\u001b[1;33m\n",
       "\u001b[0m\u001b[1;33m\n",
       "\u001b[0m  \u001b[1;32mdef\u001b[0m \u001b[0m__init__\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mself\u001b[0m\u001b[1;33m,\u001b[0m\u001b[1;33m\n",
       "\u001b[0m               \u001b[0mfrom_logits\u001b[0m\u001b[1;33m=\u001b[0m\u001b[1;32mFalse\u001b[0m\u001b[1;33m,\u001b[0m\u001b[1;33m\n",
       "\u001b[0m               \u001b[0mlabel_smoothing\u001b[0m\u001b[1;33m=\u001b[0m\u001b[1;36m0\u001b[0m\u001b[1;33m,\u001b[0m\u001b[1;33m\n",
       "\u001b[0m               \u001b[0mreduction\u001b[0m\u001b[1;33m=\u001b[0m\u001b[0mlosses_utils\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mReductionV2\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mAUTO\u001b[0m\u001b[1;33m,\u001b[0m\u001b[1;33m\n",
       "\u001b[0m               \u001b[0mname\u001b[0m\u001b[1;33m=\u001b[0m\u001b[1;34m'binary_crossentropy'\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\n",
       "\u001b[0m    \u001b[1;34m\"\"\"Initializes `BinaryCrossentropy` instance.\n",
       "\n",
       "    Args:\n",
       "      from_logits: Whether to interpret `y_pred` as a tensor of\n",
       "        [logit](https://en.wikipedia.org/wiki/Logit) values. By default, we\n",
       "          assume that `y_pred` contains probabilities (i.e., values in [0, 1]).\n",
       "          **Note - Using from_logits=True may be more numerically stable.\n",
       "      label_smoothing: Float in [0, 1]. When 0, no smoothing occurs. When > 0,\n",
       "        we compute the loss between the predicted labels and a smoothed version\n",
       "        of the true labels, where the smoothing squeezes the labels towards 0.5.\n",
       "        Larger values of `label_smoothing` correspond to heavier smoothing.\n",
       "      reduction: (Optional) Type of `tf.keras.losses.Reduction` to apply to\n",
       "        loss. Default value is `AUTO`. `AUTO` indicates that the reduction\n",
       "        option will be determined by the usage context. For almost all cases\n",
       "        this defaults to `SUM_OVER_BATCH_SIZE`. When used with\n",
       "        `tf.distribute.Strategy`, outside of built-in training loops such as\n",
       "        `tf.keras` `compile` and `fit`, using `AUTO` or `SUM_OVER_BATCH_SIZE`\n",
       "        will raise an error. Please see this custom training [tutorial](\n",
       "          https://www.tensorflow.org/tutorials/distribute/custom_training)\n",
       "        for more details.\n",
       "      name: (Optional) Name for the op. Defaults to 'binary_crossentropy'.\n",
       "    \"\"\"\u001b[0m\u001b[1;33m\n",
       "\u001b[0m    \u001b[0msuper\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mBinaryCrossentropy\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mself\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m__init__\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m\n",
       "\u001b[0m        \u001b[0mbinary_crossentropy\u001b[0m\u001b[1;33m,\u001b[0m\u001b[1;33m\n",
       "\u001b[0m        \u001b[0mname\u001b[0m\u001b[1;33m=\u001b[0m\u001b[0mname\u001b[0m\u001b[1;33m,\u001b[0m\u001b[1;33m\n",
       "\u001b[0m        \u001b[0mreduction\u001b[0m\u001b[1;33m=\u001b[0m\u001b[0mreduction\u001b[0m\u001b[1;33m,\u001b[0m\u001b[1;33m\n",
       "\u001b[0m        \u001b[0mfrom_logits\u001b[0m\u001b[1;33m=\u001b[0m\u001b[0mfrom_logits\u001b[0m\u001b[1;33m,\u001b[0m\u001b[1;33m\n",
       "\u001b[0m        \u001b[0mlabel_smoothing\u001b[0m\u001b[1;33m=\u001b[0m\u001b[0mlabel_smoothing\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\n",
       "\u001b[0m    \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mfrom_logits\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mfrom_logits\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
       "\u001b[1;31mFile:\u001b[0m           d:\\youtube\\faceid\\faceid\\lib\\site-packages\\tensorflow\\python\\keras\\losses.py\n",
       "\u001b[1;31mType:\u001b[0m           type\n",
       "\u001b[1;31mSubclasses:\u001b[0m     \n"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "tf.losses.BinaryCrossentropy??"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 223,
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "@tf.function\n",
    "def train_step(batch):\n",
    "    \n",
    "    # Record all of our operations \n",
    "    with tf.GradientTape() as tape:     \n",
    "        # Get anchor and positive/negative image\n",
    "        X = batch[:2]\n",
    "        # Get label\n",
    "        y = batch[2]\n",
    "        \n",
    "        # Forward pass\n",
    "        yhat = siamese_model(X, training=True)\n",
    "        # Calculate loss\n",
    "        loss = binary_cross_loss(y, yhat)\n",
    "    print(loss)\n",
    "        \n",
    "    # Calculate gradients\n",
    "    grad = tape.gradient(loss, siamese_model.trainable_variables)\n",
    "    \n",
    "    # Calculate updated weights and apply to siamese model\n",
    "    opt.apply_gradients(zip(grad, siamese_model.trainable_variables))\n",
    "        \n",
    "    # Return loss\n",
    "    return loss"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5.4 Build Training Loop"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 224,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import metric calculations\n",
    "from tensorflow.keras.metrics import Precision, Recall"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 225,
   "metadata": {},
   "outputs": [],
   "source": [
    "def train(data, EPOCHS):\n",
    "    # Loop through epochs\n",
    "    for epoch in range(1, EPOCHS+1):\n",
    "        print('\\n Epoch {}/{}'.format(epoch, EPOCHS))\n",
    "        progbar = tf.keras.utils.Progbar(len(data))\n",
    "        \n",
    "        # Creating a metric object \n",
    "        r = Recall()\n",
    "        p = Precision()\n",
    "        \n",
    "        # Loop through each batch\n",
    "        for idx, batch in enumerate(data):\n",
    "            # Run train step here\n",
    "            loss = train_step(batch)\n",
    "            yhat = siamese_model.predict(batch[:2])\n",
    "            r.update_state(batch[2], yhat)\n",
    "            p.update_state(batch[2], yhat) \n",
    "            progbar.update(idx+1)\n",
    "        print(loss.numpy(), r.result().numpy(), p.result().numpy())\n",
    "        \n",
    "        # Save checkpoints\n",
    "        if epoch % 10 == 0: \n",
    "            checkpoint.save(file_prefix=checkpoint_prefix)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5.5 Train the model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 226,
   "metadata": {},
   "outputs": [],
   "source": [
    "EPOCHS = 50"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 227,
   "metadata": {
    "scrolled": true,
    "tags": []
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      " Epoch 1/50\n",
      "Tensor(\"binary_crossentropy/weighted_loss/value:0\", shape=(), dtype=float32)\n",
      "Tensor(\"binary_crossentropy/weighted_loss/value:0\", shape=(), dtype=float32)\n",
      "262/263 [============================>.] - ETA: 0sTensor(\"binary_crossentropy/weighted_loss/value:0\", shape=(), dtype=float32)\n",
      "263/263 [==============================] - 43s 163ms/step\n",
      "0.85728246 0.94401914 0.9959616\n",
      "\n",
      " Epoch 2/50\n",
      "263/263 [==============================] - 41s 156ms/step\n",
      "0.1616693 0.9791073 0.99806386\n",
      "\n",
      " Epoch 3/50\n",
      "263/263 [==============================] - 40s 152ms/step\n",
      "0.025755242 0.98856056 0.99807507\n",
      "\n",
      " Epoch 4/50\n",
      "263/263 [==============================] - 40s 150ms/step\n",
      "0.21595995 0.99035215 0.99757046\n",
      "\n",
      " Epoch 5/50\n",
      "263/263 [==============================] - 39s 150ms/step\n",
      "5.019956e-05 0.9961959 0.9966698\n",
      "\n",
      " Epoch 6/50\n",
      " 46/263 [====>.........................] - ETA: 32s"
     ]
    },
    {
     "ename": "KeyboardInterrupt",
     "evalue": "",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mKeyboardInterrupt\u001b[0m                         Traceback (most recent call last)",
      "\u001b[1;32m~\\AppData\\Local\\Temp/ipykernel_6884/1690291132.py\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[1;32m----> 1\u001b[1;33m \u001b[0mtrain\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mtrain_data\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mEPOCHS\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[1;32m~\\AppData\\Local\\Temp/ipykernel_6884/1294751870.py\u001b[0m in \u001b[0;36mtrain\u001b[1;34m(data, EPOCHS)\u001b[0m\n\u001b[0;32m     13\u001b[0m             \u001b[1;31m# Run train step here\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     14\u001b[0m             \u001b[0mloss\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mtrain_step\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mbatch\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m---> 15\u001b[1;33m             \u001b[0myhat\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0msiamese_model\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mpredict\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mbatch\u001b[0m\u001b[1;33m[\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;36m2\u001b[0m\u001b[1;33m]\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m     16\u001b[0m             \u001b[0mr\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mupdate_state\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mbatch\u001b[0m\u001b[1;33m[\u001b[0m\u001b[1;36m2\u001b[0m\u001b[1;33m]\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0myhat\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     17\u001b[0m             \u001b[0mp\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mupdate_state\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mbatch\u001b[0m\u001b[1;33m[\u001b[0m\u001b[1;36m2\u001b[0m\u001b[1;33m]\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0myhat\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32mD:\\YouTube\\FaceID\\faceid\\lib\\site-packages\\tensorflow\\python\\keras\\engine\\training.py\u001b[0m in \u001b[0;36mpredict\u001b[1;34m(self, x, batch_size, verbose, steps, callbacks, max_queue_size, workers, use_multiprocessing)\u001b[0m\n\u001b[0;32m   1627\u001b[0m           \u001b[1;32mfor\u001b[0m \u001b[0mstep\u001b[0m \u001b[1;32min\u001b[0m \u001b[0mdata_handler\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0msteps\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m   1628\u001b[0m             \u001b[0mcallbacks\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mon_predict_batch_begin\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mstep\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m-> 1629\u001b[1;33m             \u001b[0mtmp_batch_outputs\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mpredict_function\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0miterator\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m   1630\u001b[0m             \u001b[1;32mif\u001b[0m \u001b[0mdata_handler\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mshould_sync\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m   1631\u001b[0m               \u001b[0mcontext\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0masync_wait\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32mD:\\YouTube\\FaceID\\faceid\\lib\\site-packages\\tensorflow\\python\\eager\\def_function.py\u001b[0m in \u001b[0;36m__call__\u001b[1;34m(self, *args, **kwds)\u001b[0m\n\u001b[0;32m    826\u001b[0m     \u001b[0mtracing_count\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mexperimental_get_tracing_count\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    827\u001b[0m     \u001b[1;32mwith\u001b[0m \u001b[0mtrace\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mTrace\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_name\u001b[0m\u001b[1;33m)\u001b[0m \u001b[1;32mas\u001b[0m \u001b[0mtm\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 828\u001b[1;33m       \u001b[0mresult\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_call\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m*\u001b[0m\u001b[0margs\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;33m**\u001b[0m\u001b[0mkwds\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    829\u001b[0m       \u001b[0mcompiler\u001b[0m \u001b[1;33m=\u001b[0m \u001b[1;34m\"xla\"\u001b[0m \u001b[1;32mif\u001b[0m \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_experimental_compile\u001b[0m \u001b[1;32melse\u001b[0m \u001b[1;34m\"nonXla\"\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    830\u001b[0m       \u001b[0mnew_tracing_count\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mexperimental_get_tracing_count\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32mD:\\YouTube\\FaceID\\faceid\\lib\\site-packages\\tensorflow\\python\\eager\\def_function.py\u001b[0m in \u001b[0;36m_call\u001b[1;34m(self, *args, **kwds)\u001b[0m\n\u001b[0;32m    860\u001b[0m       \u001b[1;31m# In this case we have not created variables on the first call. So we can\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    861\u001b[0m       \u001b[1;31m# run the first trace but we should fail if variables are created.\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 862\u001b[1;33m       \u001b[0mresults\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_stateful_fn\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m*\u001b[0m\u001b[0margs\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;33m**\u001b[0m\u001b[0mkwds\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    863\u001b[0m       \u001b[1;32mif\u001b[0m \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_created_variables\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    864\u001b[0m         raise ValueError(\"Creating variables on a non-first call to a function\"\n",
      "\u001b[1;32mD:\\YouTube\\FaceID\\faceid\\lib\\site-packages\\tensorflow\\python\\eager\\function.py\u001b[0m in \u001b[0;36m__call__\u001b[1;34m(self, *args, **kwargs)\u001b[0m\n\u001b[0;32m   2941\u001b[0m        filtered_flat_args) = self._maybe_define_function(args, kwargs)\n\u001b[0;32m   2942\u001b[0m     return graph_function._call_flat(\n\u001b[1;32m-> 2943\u001b[1;33m         filtered_flat_args, captured_inputs=graph_function.captured_inputs)  # pylint: disable=protected-access\n\u001b[0m\u001b[0;32m   2944\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m   2945\u001b[0m   \u001b[1;33m@\u001b[0m\u001b[0mproperty\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32mD:\\YouTube\\FaceID\\faceid\\lib\\site-packages\\tensorflow\\python\\eager\\function.py\u001b[0m in \u001b[0;36m_call_flat\u001b[1;34m(self, args, captured_inputs, cancellation_manager)\u001b[0m\n\u001b[0;32m   1917\u001b[0m       \u001b[1;31m# No tape is watching; skip to running the function.\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m   1918\u001b[0m       return self._build_call_outputs(self._inference_function.call(\n\u001b[1;32m-> 1919\u001b[1;33m           ctx, args, cancellation_manager=cancellation_manager))\n\u001b[0m\u001b[0;32m   1920\u001b[0m     forward_backward = self._select_forward_and_backward_functions(\n\u001b[0;32m   1921\u001b[0m         \u001b[0margs\u001b[0m\u001b[1;33m,\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32mD:\\YouTube\\FaceID\\faceid\\lib\\site-packages\\tensorflow\\python\\eager\\function.py\u001b[0m in \u001b[0;36mcall\u001b[1;34m(self, ctx, args, cancellation_manager)\u001b[0m\n\u001b[0;32m    558\u001b[0m               \u001b[0minputs\u001b[0m\u001b[1;33m=\u001b[0m\u001b[0margs\u001b[0m\u001b[1;33m,\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    559\u001b[0m               \u001b[0mattrs\u001b[0m\u001b[1;33m=\u001b[0m\u001b[0mattrs\u001b[0m\u001b[1;33m,\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 560\u001b[1;33m               ctx=ctx)\n\u001b[0m\u001b[0;32m    561\u001b[0m         \u001b[1;32melse\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    562\u001b[0m           outputs = execute.execute_with_cancellation(\n",
      "\u001b[1;32mD:\\YouTube\\FaceID\\faceid\\lib\\site-packages\\tensorflow\\python\\eager\\execute.py\u001b[0m in \u001b[0;36mquick_execute\u001b[1;34m(op_name, num_outputs, inputs, attrs, ctx, name)\u001b[0m\n\u001b[0;32m     58\u001b[0m     \u001b[0mctx\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mensure_initialized\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     59\u001b[0m     tensors = pywrap_tfe.TFE_Py_Execute(ctx._handle, device_name, op_name,\n\u001b[1;32m---> 60\u001b[1;33m                                         inputs, attrs, num_outputs)\n\u001b[0m\u001b[0;32m     61\u001b[0m   \u001b[1;32mexcept\u001b[0m \u001b[0mcore\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_NotOkStatusException\u001b[0m \u001b[1;32mas\u001b[0m \u001b[0me\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     62\u001b[0m     \u001b[1;32mif\u001b[0m \u001b[0mname\u001b[0m \u001b[1;32mis\u001b[0m \u001b[1;32mnot\u001b[0m \u001b[1;32mNone\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;31mKeyboardInterrupt\u001b[0m: "
     ]
    }
   ],
   "source": [
    "train(train_data, EPOCHS)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "tags": []
   },
   "source": [
    "# 6. Evaluate Model"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 6.1 Import Metrics"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 228,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import metric calculations\n",
    "from tensorflow.keras.metrics import Precision, Recall"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 6.2 Make Predictions"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 229,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Get a batch of test data\n",
    "test_input, test_val, y_true = test_data.as_numpy_iterator().next()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 230,
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "y_hat = siamese_model.predict([test_input, test_val])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 231,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1]"
      ]
     },
     "execution_count": 231,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Post processing the results \n",
    "[1 if prediction > 0.5 else 0 for prediction in y_hat ]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 232,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([1., 1., 1., 0., 1., 1., 0., 0., 1., 0., 0., 0., 0., 1., 0., 1.],\n",
       "      dtype=float32)"
      ]
     },
     "execution_count": 232,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "y_true"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 6.3 Calculate Metrics"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 233,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "1.0"
      ]
     },
     "execution_count": 233,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Creating a metric object \n",
    "m = Recall()\n",
    "\n",
    "# Calculating the recall value \n",
    "m.update_state(y_true, y_hat)\n",
    "\n",
    "# Return Recall Result\n",
    "m.result().numpy()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 234,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "1.0"
      ]
     },
     "execution_count": 234,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Creating a metric object \n",
    "m = Precision()\n",
    "\n",
    "# Calculating the recall value \n",
    "m.update_state(y_true, y_hat)\n",
    "\n",
    "# Return Recall Result\n",
    "m.result().numpy()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 235,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "1.0 0.99889135\n"
     ]
    }
   ],
   "source": [
    "r = Recall()\n",
    "p = Precision()\n",
    "\n",
    "for test_input, test_val, y_true in test_data.as_numpy_iterator():\n",
    "    yhat = siamese_model.predict([test_input, test_val])\n",
    "    r.update_state(y_true, yhat)\n",
    "    p.update_state(y_true,yhat) \n",
    "\n",
    "print(r.result().numpy(), p.result().numpy())"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 6.4 Viz Results"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 236,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 720x576 with 2 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "# Set plot size \n",
    "plt.figure(figsize=(10,8))\n",
    "\n",
    "# Set first subplot\n",
    "plt.subplot(1,2,1)\n",
    "plt.imshow(test_input[0])\n",
    "\n",
    "# Set second subplot\n",
    "plt.subplot(1,2,2)\n",
    "plt.imshow(test_val[0])\n",
    "\n",
    "# Renders cleanly\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 7. Save Model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 237,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Save weights\n",
    "siamese_model.save('siamesemodelv2.h5')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "L1Dist"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "WARNING:tensorflow:No training configuration found in the save file, so the model was *not* compiled. Compile it manually.\n"
     ]
    }
   ],
   "source": [
    "# Reload model \n",
    "siamese_model = tf.keras.models.load_model('siamesemodelv2.h5', \n",
    "                                   custom_objects={'L1Dist':L1Dist, 'BinaryCrossentropy':tf.losses.BinaryCrossentropy})"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 239,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([[2.7295970e-05],\n",
       "       [8.7373185e-01],\n",
       "       [1.1476276e-06],\n",
       "       [9.9997568e-01],\n",
       "       [9.9490523e-01],\n",
       "       [2.8164588e-06],\n",
       "       [2.9260066e-06],\n",
       "       [1.0000000e+00]], dtype=float32)"
      ]
     },
     "execution_count": 239,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Make predictions with reloaded model\n",
    "siamese_model.predict([test_input, test_val])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 240,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Model: \"SiameseNetwork\"\n",
      "__________________________________________________________________________________________________\n",
      "Layer (type)                    Output Shape         Param #     Connected to                     \n",
      "==================================================================================================\n",
      "input_img (InputLayer)          [(None, 100, 100, 3) 0                                            \n",
      "__________________________________________________________________________________________________\n",
      "validation_img (InputLayer)     [(None, 100, 100, 3) 0                                            \n",
      "__________________________________________________________________________________________________\n",
      "embedding (Functional)          (None, 4096)         38960448    input_img[0][0]                  \n",
      "                                                                 validation_img[0][0]             \n",
      "__________________________________________________________________________________________________\n",
      "l1_dist_6 (L1Dist)              (None, 4096)         0           embedding[0][0]                  \n",
      "                                                                 embedding[1][0]                  \n",
      "__________________________________________________________________________________________________\n",
      "dense_7 (Dense)                 (None, 1)            4097        l1_dist_6[0][0]                  \n",
      "==================================================================================================\n",
      "Total params: 38,964,545\n",
      "Trainable params: 38,964,545\n",
      "Non-trainable params: 0\n",
      "__________________________________________________________________________________________________\n"
     ]
    }
   ],
   "source": [
    "# View model summary\n",
    "siamese_model.summary()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 8. Real Time Test"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 8.1 Verification Function"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "application_data\\verification_images"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "os.listdir(os.path.join('application_data', 'verification_images'))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "os.path.join('application_data', 'input_image', 'input_image.jpg')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "for image in os.listdir(os.path.join('application_data', 'verification_images')):\n",
    "    validation_img = os.path.join('application_data', 'verification_images', image)\n",
    "    print(validation_img)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "def verify(model, detection_threshold, verification_threshold):\n",
    "    # Build results array\n",
    "    results = []\n",
    "    for image in os.listdir(os.path.join('application_data', 'verification_images')):\n",
    "        input_img = preprocess(os.path.join('application_data', 'input_image', 'input_image.jpg'))\n",
    "        validation_img = preprocess(os.path.join('application_data', 'verification_images', image))\n",
    "        \n",
    "        # Make Predictions \n",
    "        result = model.predict(list(np.expand_dims([input_img, validation_img], axis=1)))\n",
    "        results.append(result)\n",
    "    \n",
    "    # Detection Threshold: Metric above which a prediciton is considered positive \n",
    "    detection = np.sum(np.array(results) > detection_threshold)\n",
    "    \n",
    "    # Verification Threshold: Proportion of positive predictions / total positive samples \n",
    "    verification = detection / len(os.listdir(os.path.join('application_data', 'verification_images'))) \n",
    "    verified = verification > verification_threshold\n",
    "    \n",
    "    return results, verified"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 8.2 OpenCV Real Time Verification"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "True\n"
     ]
    }
   ],
   "source": [
    "cap = cv2.VideoCapture(4)\n",
    "while cap.isOpened():\n",
    "    ret, frame = cap.read()\n",
    "    frame = frame[120:120+250,200:200+250, :]\n",
    "    \n",
    "    cv2.imshow('Verification', frame)\n",
    "    \n",
    "    # Verification trigger\n",
    "    if cv2.waitKey(10) & 0xFF == ord('v'):\n",
    "        # Save input image to application_data/input_image folder \n",
    "#         hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)\n",
    "#         h, s, v = cv2.split(hsv)\n",
    "\n",
    "#         lim = 255 - 10\n",
    "#         v[v > lim] = 255\n",
    "#         v[v <= lim] -= 10\n",
    "        \n",
    "#         final_hsv = cv2.merge((h, s, v))\n",
    "#         img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)\n",
    "\n",
    "        cv2.imwrite(os.path.join('application_data', 'input_image', 'input_image.jpg'), frame)\n",
    "        # Run verification\n",
    "        results, verified = verify(siamese_model, 0.5, 0.5)\n",
    "        print(verified)\n",
    "    \n",
    "    if cv2.waitKey(10) & 0xFF == ord('q'):\n",
    "        break\n",
    "cap.release()\n",
    "cv2.destroyAllWindows()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "36"
      ]
     },
     "execution_count": 17,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "np.sum(np.squeeze(results) > 0.9)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[array([[0.9944859]], dtype=float32),\n",
       " array([[0.9999912]], dtype=float32),\n",
       " array([[0.9999943]], dtype=float32),\n",
       " array([[0.9999951]], dtype=float32),\n",
       " array([[0.99993753]], dtype=float32),\n",
       " array([[0.9082498]], dtype=float32),\n",
       " array([[0.9999846]], dtype=float32),\n",
       " array([[0.9834683]], dtype=float32),\n",
       " array([[0.87159216]], dtype=float32),\n",
       " array([[0.7328309]], dtype=float32),\n",
       " array([[0.74533516]], dtype=float32),\n",
       " array([[0.949607]], dtype=float32),\n",
       " array([[0.7501703]], dtype=float32),\n",
       " array([[0.60669833]], dtype=float32),\n",
       " array([[0.93921214]], dtype=float32),\n",
       " array([[0.9813106]], dtype=float32),\n",
       " array([[0.9848625]], dtype=float32),\n",
       " array([[0.89696234]], dtype=float32),\n",
       " array([[0.98896575]], dtype=float32),\n",
       " array([[0.99082947]], dtype=float32),\n",
       " array([[0.7747197]], dtype=float32),\n",
       " array([[0.99999297]], dtype=float32),\n",
       " array([[0.99986887]], dtype=float32),\n",
       " array([[0.9999764]], dtype=float32),\n",
       " array([[0.90808266]], dtype=float32),\n",
       " array([[0.8795649]], dtype=float32),\n",
       " array([[0.9634782]], dtype=float32),\n",
       " array([[0.9790052]], dtype=float32),\n",
       " array([[0.98665583]], dtype=float32),\n",
       " array([[0.98852533]], dtype=float32),\n",
       " array([[0.9995832]], dtype=float32),\n",
       " array([[1.]], dtype=float32),\n",
       " array([[0.9905027]], dtype=float32),\n",
       " array([[0.99841905]], dtype=float32),\n",
       " array([[0.96080494]], dtype=float32),\n",
       " array([[0.8443497]], dtype=float32),\n",
       " array([[0.9721696]], dtype=float32),\n",
       " array([[0.80732024]], dtype=float32),\n",
       " array([[0.79700935]], dtype=float32),\n",
       " array([[0.94146115]], dtype=float32),\n",
       " array([[0.9694269]], dtype=float32),\n",
       " array([[0.902836]], dtype=float32),\n",
       " array([[0.9999974]], dtype=float32),\n",
       " array([[0.9999436]], dtype=float32),\n",
       " array([[0.83173716]], dtype=float32),\n",
       " array([[0.9837488]], dtype=float32),\n",
       " array([[0.9999938]], dtype=float32),\n",
       " array([[0.9960765]], dtype=float32),\n",
       " array([[0.8436094]], dtype=float32),\n",
       " array([[0.78270465]], dtype=float32)]"
      ]
     },
     "execution_count": 18,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "results"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "faceid",
   "language": "python",
   "name": "faceid"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}