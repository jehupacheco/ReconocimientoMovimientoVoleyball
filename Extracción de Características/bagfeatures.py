import os
import cv2
import numpy as np
import tensorflow as tf
import functools
import time

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

def input_fn(data):
    print('yep')
    x = tf.constant(data , tf.float32)
    return (x, None)

def bagOfFeatures(size, features):
    print('Bag Features was asked for {} clusters'.format(size))
    print('Features with shape: {}'.format(features.shape))
    index = int(time.perf_counter() * 10000000)
    classifier = tf.contrib.learn.KMeansClustering(size, '/home/a20122064/tmp/log-{}'.format(index))
    classifier.fit(input_fn=functools.partial(input_fn, data=features), max_steps=2000)
    clusters = classifier.clusters()
    a = clusters.flatten()
    print('Normal clusters have shape {}'.format(clusters.shape))
    print('Flattened clusters have shape {}'.format(a.shape))
    return a

# https://gist.github.com/alfredplpl/6901429
