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

img_result = img.copy()     # 이미지 복사
dets = detector(img)        # 얼굴의 좌표, 얼굴이 여러개면 각각의 좌표를 반환
if len(dets) == 0:
    print('cannot find faces!')
else:
    fig, ax = plt.subplots(1, figsize=(16, 10))
    for det in dets:
        x, y, w, h = det.left(), det.top(), det.width(), det.height()       # 왼쪽 끝, 위쪽 끝, 너비, 높이
        rect = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor='r', facecolor='none')        # linewidth는 표시선의 굵기, edgecolor는 선의 색깔, facecolor는 채우기
        ax.add_patch(rect)
    ax.imshow(img_result)
    plt.show()

fig, ax = plt.subplots(1, figsize=(16, 10))
objs = dlib.full_object_detections()
for detection in dets:
    s = sp(img, detection)      # 모델이 5개 랜드마크 위치 예측
    objs.append(s)
    for point in s.parts():
        circle = patches.Circle((point.x, point.y), radius=3, edgecolor='r', facecolor='r')     # radius는 원의 지름
        ax.add_patch(circle)
ax.imshow(img_result)
plt.show()

faces = dlib.get_face_chips(img, objs, size=256, padding=0.3)
fig, axes = plt.subplots(1, len(faces)+1, figsize=(20, 16))
axes[0].imshow(img)
for i, face in enumerate(faces):
    axes[i+1].imshow(face)
plt.show()