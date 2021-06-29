import matplotlib.pyplot as plt
import numpy as np
import os
from tensorflow.keras.datasets import mnist
from tensorflow.keras.layers import *
from tensorflow.keras.models import Sequential

OUT_DIR = './OUT_img/'
img_shape = (28, 28, 1)
epoch = 100000
batch_size = 128
noise = 100
sample_interval = 100

(X_train , _), (_, _) = mnist.load_data()   # y값, 검증 데이터 없음
print(X_train.shape)

X_train = X_train / 127.5 - 1       # -1에서 1 사이의 값을 가짐
X_train = np.expand_dims(X_train, axis=3)       # 차원 하나 늘림. 4번째 차원 생성. reshape와 동일
print(X_train.shape)

#build generator
generator_model = Sequential()
generator_model.add(Dense(128, input_dim=noise))      # 랜덤하게 만들어진 잡음 100개
generator_model.add(LeakyReLU(alpha=0.01))      # activation function=LeakyReLU / alpha 값은 음수에서의 기울기. 양수에서는 기울기 1
generator_model.add(Dense(784, activation='tanh'))
generator_model.add(Reshape(img_shape))         # 최종 출력 28*28*1
print(generator_model.summary())        # 제너레이터 모델은 홀로 학습이 안 됨. 컴파일 불필요.

#build discriminator
discriminator_model = Sequential()
discriminator_model.add(Flatten(input_shape=img_shape))     # generator가 만든 이미지를 펼치기 위해 flatten 사용
discriminator_model.add(Dense(128))
discriminator_model.add(LeakyReLU(alpha=0.01))      # 데이터가 -1에서 1 값, 즉 음수 값이 있기 때문에 LeakyReLU 사용. 음수 값에서도 미세한 기울기가 있어 학습이 가능.
# LeakyReLU 다른 방식
# lrelu = LeakyReLU(alpha=0.01
# discriminator_model.add(Dense(128, activation=lrelu))
discriminator_model.add(Dense(1, activation='sigmoid'))       # 진품, 가품 여부만 알면 되므로 출력은 1개
print(discriminator_model.summary())

discriminator_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])       # 이진분류기이므로 loss는 바이너리 크로스엔트로피
discriminator_model.trainable = False   # 해당 모델이 학습을 안 하도록. forward만 가능, backward 불가

#build GAN
gan_model = Sequential()
gan_model.add(generator_model)
gan_model.add(discriminator_model)
print(gan_model.summary())
gan_model.compile(loss='binary_crossentropy', optimizer='adam')

real = np.ones((batch_size, 1))     # 1 128개
print(real)
fake = np.zeros((batch_size, 1))    # 0 128개
print(fake)

for itr in range(epoch):        # 10만번 반복
    idx = np.random.randint(0, X_train.shape[0], batch_size)    # 0부터 59999까지 batch_size 개수만큼 뽑아냄
    real_imgs = X_train[idx]            # 이미지 128장

    z = np.random.normal(0, 1, (batch_size, noise))     # 제너레이터에게 입력으로 줄 잡음 데이터. 평균은 0 표준편차 1인 랜덤 값으로 standardization과 동일. 100개짜리 128 세트.
    fake_imgs = generator_model.predict(z)      # 이미지 128장

    d_hist_real = discriminator_model.train_on_batch(real_imgs, real)      # model.fit 대신 model.train_on_batch. 랜덤 이미지 128장과 전부 1로 채워진 정답지 주고 학습.
    d_hist_fake = discriminator_model.train_on_batch(fake_imgs, fake)      # discriminator 모델에 generator가 생성한 fake 이미지 128장을 주고 loss값 계산.

    d_loss, d_acc = 0.5 * np.add(d_hist_real, d_hist_fake)      # 두 결과의 평균

    z = np.random.normal(0, 1, (batch_size, noise))
    gan_hist = gan_model.train_on_batch(z, real)        # 간 모델 학습할 때 generator만 학습되고 discriminator는 학습 안 됨. z= 배치 real=라벨
                                                            # 간 모델은 출력이 1이 나오게 학습해야 함

    if itr % sample_interval == 0:        # 100 에포크마다 한 번씩 이미지 그리기
        print('%d [D loss: %f], acc.: %.2f%%] [G loss: %f]'%(itr, d_loss, d_acc*100, gan_hist))
        row = col = 4
        z = np.random.normal(0, 1, (row * col, noise))        # 4*4=16개 잡음
        fake_imgs = generator_model.predict(z)
        fake_imgs = 0.5 * fake_imgs + 0.5           # ?????
        _, axs = plt.subplots(row, col, figsize=(row, col), sharey=True, sharex=True)      # 가로 4, 세로 4 크기의 이미지 16장 그리기
        cnt = 0
        for i in range(row):
            for j in range(col):
                axs[i, j].imshow(fake_imgs[cnt, :, :, 0], cmap='gray')
                axs[i, j].axis('off')       # x, y 눈금 없애기
                cnt += 1
        path = os.path.join(OUT_DIR, 'img-{}'.format(itr + 1))
        plt.savefig(path)
        plt.close()