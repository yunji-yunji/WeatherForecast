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
#  Load Data
#########################################################################

X_Train_Set_Load = pd.read_csv("./Data/x_train.csv", names=['기온', '습도', '이슬점', '기압']);
print(X_Train_Set_Load.head(5));
print("Load X\n\n");

Y_Train_Set_Load = pd.read_csv("./Data/y_train.csv", names=['기온', '습도', '이슬점', '기압']);
print(Y_Train_Set_Load.head(5));
print("Load Y\n\n");

# load data shape (10103, 4) : 4개 feature를 가지는 10103개의 항목.

# divide int train data and test data
# 2000
X_Train_Set = X_Train_Set_Load[6000:7500]
Y_Train_Set = Y_Train_Set_Load[6000:7500]
X_Test_Set = X_Train_Set_Load[7500:8000]
Y_Test_Set = Y_Train_Set_Load[7500:8000]

# 10,000
# X_Train_Set = X_Train_Set_Load[:8000]
# Y_Train_Set = Y_Train_Set_Load[:8000]
# X_Test_Set = X_Train_Set_Load[8000:10000]
# Y_Test_Set = Y_Train_Set_Load[8000:10000]

#########################################################################
#  Make Neural Network
#########################################################################

Weather_Forecast_Model = Sequential();

# Add Hidden Layers
Hidden_Layer1 = Dense(8, input_dim=4, activation='linear');
Weather_Forecast_Model.add(Hidden_Layer1);

Hidden_Layer2 = Dense(8, activation='linear');
Weather_Forecast_Model.add(Hidden_Layer2);

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
#  Setting learning parameters
#########################################################################
Weather_Forecast_Model.compile(loss='mean_squared_logarithmic_error', optimizer='adam', metrics=['accuracy', 'mse', 'mae']);
early_stopping = EarlyStopping(monitor='loss', patience=100);

#########################################################################
#  Train Model
#########################################################################
Weather_Forecast_Model.fit(X_Train_Set, Y_Train_Set, epochs=500, batch_size=500, callbacks=[early_stopping]);

#########################################################################
#  Evaluate Performance
#########################################################################
print("\n Accuracy: %.4f" % (Weather_Forecast_Model.evaluate(X_Test_Set,Y_Test_Set)[1]));

# Print Predict Result
Test_Forecast_List = Weather_Forecast_Model.predict(X_Test_Set.head(5));
for i in range(5):
    print(Test_Forecast_List[i]);

y_hat = Weather_Forecast_Model.predict(X_Test_Set, batch_size=1);

print(Y_Train_Set.values.shape)     # 1500, 4
print(y_hat.shape)                  # 500, 4
print(Y_Test_Set.values.shape)      # 500, 4

#########################################################################
#  Plot
#########################################################################
# x axis
a_axis = np.arange(0, len(Y_Train_Set))
b_axis = np.arange(len(Y_Train_Set), len(Y_Train_Set) + len(y_hat))

# y axis
title = ['Temperature', 'Humidity', 'Dew point', 'Pressure']
plt.figure(figsize=(14,10))
for i, t in enumerate(title):
    print(i, t)
    # plt.subplot(2, 2, i+1)
    plt.title(t, fontsize=16)

    # input # : 2000
    plt.plot(a_axis, Y_Train_Set.values.reshape(1500, 4)[:, i], linewidth=0.4)
    plt.plot(b_axis, y_hat.reshape(500, 4)[:, i], color='green', label='Predicted', linewidth=0.4)
    plt.plot(b_axis, Y_Test_Set.values.reshape(500, 4)[:, i], color='red', label='Actual', linewidth=0.4)

    # input # : 10,000
    # plt.plot(a_axis, Y_Train_Set.values.reshape(8000, 4)[:, i], linewidth=0.4)
    # plt.plot(b_axis, y_hat.reshape(2000, 4)[:, i], color='green', label='Predicted', linewidth=0.4)
    # plt.plot(b_axis, Y_Test_Set.values.reshape(2000, 4)[:, i], color='red', label='Actual', linewidth=0.4)

    plt.legend(prop={'size': 8})
    plt.interactive(False)
    plt.show(block=True)

#########################################################################
#  Save Model
#########################################################################
model = input("\n\nInput Model Name: ");
Weather_Forecast_Model.save(model);

Weather_Forecast_Model.summary();

print("\nSAVE");