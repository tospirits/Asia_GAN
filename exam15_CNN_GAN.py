import matplotlib.pyplot as plt
import numpy as np
import os
from tensorflow.keras.datasets import mnist
from tensorflow.keras.layers import *
from tensorflow.keras.models import Sequential

OUT_DIR = './CNN_OUT_img/'
if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)
img_shape = (28, 28, 1)
epoch = 5000    # 성능이 좋은 대신 시간이 오래 걸리므로 에포크 수 감소
batch_size = 128
noise = 100
sample_interval = 100

(X_train , _), (_, _) = mnist.load_data()
print(X_train.shape)

X_train = X_train / 127.5 - 1
X_train = np.expand_dims(X_train, axis=3)
print(X_train.shape)

#build generator
generator_model = Sequential()
generator_model.add(Dense(256*7*7, input_dim=noise))
generator_model.add(Reshape((7,7,256)))     # shape를 하나의 튜플로 묶어서 줘야 함.  7 * 7 = 256개?

generator_model.add(Conv2DTranspose(128, kernel_size=3, strides=2, padding='same'))     # Conv2DTranspose는 Conv2D와 유사하면서 generator 모델에서 쓰는 레이어
                                                                                        # Upsampling이 묶여 있어 Upsampling 먼저 하고 그 다음 Convolution하는 레이어
generator_model.add(BatchNormalization())       # 값이 계속 커지면 안 되므로 정규화
generator_model.add(LeakyReLU(alpha=0.01))

generator_model.add(Conv2DTranspose(64, kernel_size=3, strides=1, padding='same'))      # strides는 kernel의 이동 간격. 이 값이 커지면 padding이 있어도 이미지 사이즈가 줄어듦
generator_model.add(BatchNormalization())       # 값이 계속 커지면 안 되므로 정규화           # (위에 이어서) strides 1 주면 이미지가 줄어들지 않음
generator_model.add(LeakyReLU(alpha=0.01))

generator_model.add(Conv2DTranspose(1, kernel_size=3, strides=2, padding='same'))       # strides=2는 MaxPool 사이즈가 2*2였다는 뜻. Conv2DTranspose로 다시 2배의 크기가 됨
generator_model.add(Activation('tanh'))     # -1에서 1 사이의 값

generator_model.summary()       # 제너레이터 모델은 홀로 학습이 안 됨. 컴파일 불필요.

#build discriminator
discriminator_model = Sequential()
discriminator_model.add(Conv2D(32, kernel_size=3, strides=2, padding='same', input_shape=img_shape))
discriminator_model.add(LeakyReLU(alpha=0.01))

discriminator_model.add(Conv2D(64, kernel_size=3, strides=2, padding='same'))
#discriminator_model.add(BatchNormalization())
discriminator_model.add(LeakyReLU(alpha=0.01))

discriminator_model.add(Conv2D(128, kernel_size=3, strides=2, padding='same'))
#discriminator_model.add(BatchNormalization())
discriminator_model.add(LeakyReLU(alpha=0.01))

discriminator_model.add(Flatten())
discriminator_model.add(Dense(1, activation='sigmoid'))
discriminator_model.summary()

discriminator_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
discriminator_model.trainable = False

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

# CNN의 경우 discriminator model이 gan model보다 학습이 잘 돼서 성과가 낮음
for itr in range(epoch):        # 10만번 반복
    idx = np.random.randint(0, X_train.shape[0], batch_size)    # 0부터 59999까지 batch_size 개수만큼 뽑아냄
    real_imgs = X_train[idx]            # 이미지 128장

    z = np.random.normal(0, 1, (batch_size, noise))     # 제너레이터에게 입력으로 줄 잡음 데이터. 평균은 0 표준편차 1인 랜덤 값으로 standardization과 동일. 100개짜리 128 세트.
    fake_imgs = generator_model.predict(z)      # 이미지 128장

    d_hist_real = discriminator_model.train_on_batch(real_imgs, real)      # model.fit 대신 model.train_on_batch. 랜덤 이미지 128장과 전부 1로 채워진 정답지 주고 학습.
    d_hist_fake = discriminator_model.train_on_batch(fake_imgs, fake)      # discriminator 모델에 generator가 생성한 fake 이미지 128장을 주고 loss값 계산.

    d_loss, d_acc = 0.5 * np.add(d_hist_real, d_hist_fake)      # 두 결과의 평균

    z = np.random.normal(0, 1, (batch_size, noise))     # 제너레이터에게 입력으로 줄 잡음 데이터         // standardization과 동일
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