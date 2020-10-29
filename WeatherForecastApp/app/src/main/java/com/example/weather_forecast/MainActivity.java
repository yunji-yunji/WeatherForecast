package com.example.weather_forecast;

import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.BatteryManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.io.RandomAccessFile;
import java.util.List;
import java.util.Locale;

import java.text.DecimalFormat;
import java.text.DecimalFormatSymbols;

public class MainActivity extends AppCompatActivity {

    private SensorManager manager;
    private SensorEventListener listener;

    Sensor temperature, humidity, pressure, light;
    float sensor_value;

    TextView txtTemperature, txtHumidity, txtPressure, txtLight;
    Button listButton;

    @Override
    protected void onPostResume() {
        super.onPostResume();
        manager.registerListener(listener, temperature, SensorManager.SENSOR_DELAY_UI);
        manager.registerListener(listener, humidity, SensorManager.SENSOR_DELAY_UI);
        manager.registerListener(listener, pressure, SensorManager.SENSOR_DELAY_UI);
        manager.registerListener(listener, light, SensorManager.SENSOR_DELAY_UI);
    }

    @Override
    protected void onPause() {
        super.onPause();
        manager.unregisterListener(listener);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        txtTemperature = (TextView) findViewById(R.id.temperature);
        txtHumidity = (TextView) findViewById(R.id.humidity);
        txtPressure = (TextView) findViewById(R.id.pressure);
        txtLight = (TextView) findViewById(R.id.light);


        listButton = (Button) findViewById(R.id.listButton);
        listButton.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View view) {
                // TODO : Change Activity to Manager Activity
                Intent intent = new Intent(MainActivity.this, BluetoothActivity.class);
//                intent.putExtra(“text”,String.valueOf(editText.getText()));
                startActivity(intent);
            }
        });

        manager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);

        // 1. 온도
        temperature = manager.getDefaultSensor(Sensor.TYPE_AMBIENT_TEMPERATURE);
//        temperature = manager.getDefaultSensor(Sensor.TYPE_TEMPERATURE);
//         2. 습도
        humidity = manager.getDefaultSensor(Sensor.TYPE_RELATIVE_HUMIDITY);
        // 3. 압력
        pressure = manager.getDefaultSensor(Sensor.TYPE_PRESSURE);
        // 4. 밝기
        light = manager.getDefaultSensor(Sensor.TYPE_LIGHT);

        listener = new SensorEventListener() {

            @Override
            public void onSensorChanged(SensorEvent event) {
                switch(event.sensor.getType()) {

                    case Sensor.TYPE_AMBIENT_TEMPERATURE:
                        sensor_value = event.values[0];
                        txtTemperature.setText("TEMPERATURE " + String.valueOf(sensor_value));
                        break;

                    case Sensor.TYPE_RELATIVE_HUMIDITY:
                        sensor_value = event.values[0];
                        txtHumidity.setText("HUMIDITY " + String.valueOf(sensor_value));
                        break;

                    case Sensor.TYPE_PRESSURE:
                        sensor_value = event.values[0];
                        txtPressure.setText("PRESSURE " + String.valueOf(sensor_value));
                        break;

                    case Sensor.TYPE_LIGHT:
                        sensor_value = event.values[0];
                        txtLight.setText("LIGHT " + String.valueOf(sensor_value));
                }
            }

            @Override
            public void onAccuracyChanged(Sensor sensor, int accuracy) {

            }
        };
    }
}
