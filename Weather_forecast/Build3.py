""" 인공신경망을 이용한 기상예측 프로젝트 """

# import
import numpy as np
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt

from keras.models import Sequential # 신경망 모델 생성자함수
from keras.layers import Embedding, LSTM, GRU, Dense, Dropout
from keras.models import load_model # 신경망 모델 파일 불러오기
from keras.optimizers import Adam
from keras.preprocessing import sequence
from keras.callbacks import EarlyStopping # 학습조기종료

from sklearn.model_selection import train_test_split # 학습용 따로 검증용 분리.

#########################################################################
#  학습 데이터 불러오기
#########################################################################

# X 불러오기
X_Train_Set_Load = pd.read_csv("./Data/X train9.csv", names=['기온', '습도', '이슬점', '기압']);
print(X_Train_Set_Load.head(5));
print("X 불러오기 완료\n\n");

# Y 불러오기
Y_Train_Set_Load = pd.read_csv("./Data/Y train9.csv", names=['기온', '습도', '이슬점', '기압']);
print(Y_Train_Set_Load.head(5));
print("Y 불러오기 완료\n\n");

X_Train_Set = X_Train_Set_Load;
Y_Train_Set = Y_Train_Set_Load;

#학습용 따로 검증용 따로
# X_Train_Set, X_Test_Set, Y_Train_Set, Y_Test_Set = train_test_split(X_Train_Set_Load, Y_Train_Set_Load, test_size=0.25);

# 학습용 데이터와 시험용 데이터
X_Train_Set = X_Train_Set_Load[:500]
Y_Train_Set = Y_Train_Set_Load[:500]
X_Test_Set = X_Train_Set_Load[500:]
Y_Test_Set = Y_Train_Set_Load[500:1000]

# 데이터 가공하기
# # 기온,강수량,풍속,습도,이슬점,현지기압,시정
#
# # 습도 = 습도 * 0.01
# # 기압 = 기압 - 1000
# # 시정 = 시정 * 0.001

#########################################################################
#  신경망 만들기
#########################################################################

# 모델 구조 설계
Weather_Forecast_Model = Sequential();

# 최초 입력층

# mm = GRU(units=8, return_sequences=True, input_dim=4)
# Weather_Forecast_Model.add(mm);
#
# Hidden_Layer32 = Dense(8, activation='linear');
# Weather_Forecast_Model.add(Hidden_Layer32);


# 은닉층 이름이 달라야 추가된다. 같은 것을 계속 추가할 수는 없다.
# # 중간에 ReLU층이 어느 정도 있어야 한다.
Hidden_Layer1 = Dense(8, input_dim=4, activation='linear');
# Hidden_Layer1 = LSTM(8, activation='relu', input_shape=(4,4));

Weather_Forecast_Model.add(Hidden_Layer1);

Hidden_Layer2 = Dense(8, activation='linear');
# Hidden_Layer2 = Dense(4);

Weather_Forecast_Model.add(Hidden_Layer2);
#
Hidden_Layer3 = Dense(4, activation='linear');
Weather_Forecast_Model.add(Hidden_Layer3);

Hidden_Layer4 = Dense(4, activation='linear');
Weather_Forecast_Model.add(Hidden_Layer4);

Hidden_Layer5 = Dense(4, activation='linear');
Weather_Forecast_Model.add(Hidden_Layer5);

Hidden_Layer6 = Dense(4, activation='linear');
Weather_Forecast_Model.add(Hidden_Layer6);

Hidden_Layer7 = Dense(4, activation='linear');
Weather_Forecast_Model.add(Hidden_Layer7);


#########################################################################
#  환경설정 및 학습시작
#########################################################################

# 모델 환경설정
Weather_Forecast_Model.compile(loss='mean_squared_logarithmic_error', optimizer='adam', metrics=['accuracy', 'mse', 'mae']);

# 자동종료 함수
early_stopping = EarlyStopping(monitor='loss', patience=100);

# 모델 학습하기


Weather_Forecast_Model.fit(X_Train_Set, Y_Train_Set, epochs=500, batch_size=500, callbacks=[early_stopping]);
print("\n 정확도: %.4f" % (Weather_Forecast_Model.evaluate(X_Train_Set,Y_Train_Set)[1]));
#
hist = Weather_Forecast_Model.fit(X_Train_Set, Y_Train_Set, epochs=500,batch_size=500)


Test_Forecast_List = Weather_Forecast_Model.predict(X_Train_Set.head(5));

y_hat = Weather_Forecast_Model.predict(X_Train_Set, batch_size=1);

print(Y_Train_Set.values.shape)
print(y_hat.shape)
print(Y_Test_Set.values.shape)

####
a_axis = np.arange(0, len(Y_Train_Set))
b_axis = np.arange(len(Y_Train_Set), len(Y_Train_Set) + len(y_hat))

# print(a_axis)
# print(b_axis)

# 7577, 7577, 2526
print(Y_Train_Set.values)
print(Y_Train_Set.values.reshape(500,4)[:, 0])

plt.figure(figsize=(10,6))
plt.subplot(221)
p1 = plt.plot(a_axis, Y_Train_Set.values.reshape(500,4), 'o-', linewidth=0.1, linestyle='-')
plt.subplot(222)
p2 = plt.plot(b_axis, y_hat.reshape(500,4), 'o-', label='Predicted')
# plt.plot(b_axis, y_hat.reshape(70,4), 'o-', color='red', label='Predicted')
plt.subplot(223)
p3 = plt.plot(b_axis, Y_Test_Set.values.reshape(500,4), 'o-', color='green', alpha=0.2, label='Actual')
plt.interactive(False)
plt.show(block=True)


for i in range(5):
    print(Test_Forecast_List[i]);

# print(hist.history)
# plt.figure(figsize=(10,6))
# plt.plot(hist.history['loss'])
# # plt.plot(hist.history['val_loss'])
# plt.plot(hist.history['accuracy'])
# # plt.plot(hist.history['val_acc'])
# # plt.legend(['loss', 'val_loss', 'accuracy', 'val_acc'])
# plt.legend(['loss', 'accuracy'])
# plt.grid()
# plt.interactive(False)
# plt.show(block=True)


#########################################################################
#  신경망 저장하기
#########################################################################

answer = input("\n\n현재 수치예보모델을 저장하기 >");

# 모델 저장하기
Weather_Forecast_Model.save(answer);
Weather_Forecast_Model.summary();  # 이게 있어야 불러올 때 잘 온다.
print("\n저장완료");