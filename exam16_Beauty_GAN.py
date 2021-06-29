import dlib     # 디텍트 라이브러리, 이미지 영상에서 특정 대상 찾아냄
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()        # Beauty Gan은 tensorflow 1.x에서 만들어졌으므로 2.x 비활성화 및 1.x 활성화
import numpy as np

detector = dlib.get_frontal_face_detector()     # 이미지에서 얼굴 찾아주는 디텍터
sp = dlib.shape_predictor('./models/shape_predictor_5_face_landmarks.dat')

img = dlib.load_rgb_image('./imgs/12.jpg')
plt.figure(figsize=(16, 10))
plt.imshow(img)
plt.show()