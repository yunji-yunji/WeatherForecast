#######################################################
"""
    윤지 인공신경망을 이용한 기상예측 프로젝트

"""
########################################################


# 각종 필요한 것들 가져오기
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense
from keras.callbacks import EarlyStopping

import numpy as np
import tensorflow as tf
import pandas as pd


# 신경망 모델 불러오기
def load_model_except():
    answear = input("수치예보모델 불러오기 >");

    try:
        Weather_Forecast_Mode_Local = load_model(answear);
    except:
        print("파일열기 실패\n");
        Weather_Forecast_Mode_Local = -1;

    return Weather_Forecast_Mode_Local;

# 신경망 모델 불러오기

Weather_Forecast_Model = load_model_except();

while(Weather_Forecast_Model == -1):
    Weather_Forecast_Model = load_model_except();


Weather_Forecast_Model.summary();

print("\n\n불러오기 완료\n\n");


# 현재값 입력받기
def load_Data_except():
    answear = input("질의데이터를 불러오기 >");


    try:
        X_data_Local = pd.read_csv(answear, names=['기온', '습도', '이슬점', '기압']);
    except:
        print("파일열기 실패\n");
        X_data_Local = None;

    return X_data_Local;

X_data = load_Data_except();

while(X_data is None):
    X_data = load_Data_except();

print("불러오기 완료\n\n");


# 앞으로의 예측시간
Time_Hour = input("예측시간: ");
Time_Hour = int(Time_Hour);

# 데이터 가공

# # 기온,강수량,풍속,습도,이슬점,현지기압,시정
#
# # 습도 = 습도 * 0.01
# # 기압 = 기압 - 1000
# # 시정 = 시정 * 0.00001
# 예측하려는 yunji data: 34.6, 0, 59,        25.4, 996.5,  1352
# train 7 input data: 0.3,  0, 0.93,    -0.7,   21.3,   0.0392
#X_data.iloc[0,0] = X_data.iloc[0,0] * 0.1;
X_data.iloc[0, 1] = X_data.iloc[0, 1] * 0.01;       # 습도 1
#X_data.iloc[0,4] = X_data.iloc[0,4] * 0.1;
X_data.iloc[0, 3] = (X_data.iloc[0, 3] - 1000);     # 기압  3
# X_data.iloc[0, 4] = X_data.iloc[0, 4] * 0.00001;       # 시정 4

print("입력 데이터");
print(X_data);
print("\n\n\n");

Temp = Weather_Forecast_Model.predict(X_data);

time = 0;
while(time < Time_Hour - 1):
    Temp = Weather_Forecast_Model.predict(Temp);
    time = time + 1;


# 데이터 가공 및 결과 받아오기
Forecast_Temperature = Temp[0][0];


# 강수 : 1미만이면 그냥 없는 것으로 하자 0으로 나눔 예외발생한다.
# if Temp[0][1] < 1:
#     Forecast_Rain = 0;
# else:
#     Forecast_Rain = Temp[0][1];

# Forecast_Wind = Temp[0][2];
Forecast_Humidity = Temp[0][1] * 100;
Forecast_Dew_Point = Temp[0][2];
Forecast_Pressure = (Temp[0][3]) + 1000;
# Forecast_Sight = Temp[0][4] * 100000;


print("기상예보 \n\n");

print("예보 데이터");
print(Temp);
print("\n");

print("기온: ", Forecast_Temperature, "C");
# print("강수량: ", Forecast_Rain, "mm");
# print("풍속: ", Forecast_Wind, "M/s");
print("습도: ", Forecast_Humidity, "%");

print("이슬점: ", Forecast_Dew_Point, "C");
print("기압: ", Forecast_Pressure, "hpa");
# print("시정: ", Forecast_Sight, "Meter");

answear = input("\n\n결과 저장하기 >");

Save_Array = [Forecast_Temperature,
                # Forecast_Rain,
              # Forecast_Wind,
              Forecast_Humidity,Forecast_Dew_Point,Forecast_Pressure];
              # , Forecast_Sight];

Save_File = [ Save_Array];

Forecast_File = pd.DataFrame(Save_File);
Forecast_File.to_csv(answear, header = False, index = False);
print("\n\n 결과저장완료");