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
    // EXAMPLE ONLY - RESET HIGHEST AT 500°C
    public Double closestTemperature = 500.0;
    public Long resetTime = 0L;

    public String getAmbientTemperature(int averageRunningTemp, int period)
    {
        // CHECK MINUTES PASSED ( STOP CONSTANT LOW VALUE )
        Boolean passed30 = ((System.currentTimeMillis() - resetTime) > ((1000 * 60)*period));
        if (passed30)
        {
            resetTime = System.currentTimeMillis();
            closestTemperature = 500.0;
        }

        // FORMAT DECIMALS TO 00.0°C
        DecimalFormatSymbols dfs = new DecimalFormatSymbols(Locale.US);
        dfs.setDecimalSeparator('.');
        DecimalFormat decimalFormat = new DecimalFormat("##.0", dfs);

        // READ CPU & BATTERY
        try
        {
            // BYPASS ANDROID RESTRICTIONS ON THERMAL ZONE FILES & READ CPU THERMAL

            RandomAccessFile restrictedFile = new RandomAccessFile("sys/class/thermal/thermal_zone1/temp", "r");
            Double cpuTemp = (Double.parseDouble(restrictedFile.readLine()) / 1000);

            // RUN BATTERY INTENT
            Intent batIntent = this.registerReceiver(null, new IntentFilter(Intent.ACTION_BATTERY_CHANGED));
            // GET DATA FROM INTENT WITH BATTERY
            Double batTemp = (double) batIntent.getIntExtra(BatteryManager.EXTRA_TEMPERATURE, 0) / 10;

            // CHECK IF DATA EXISTS
            if (cpuTemp != null)
            {
                // CPU FILE OK - CHECK LOWEST TEMP
                if (cpuTemp - averageRunningTemp < closestTemperature)
                    closestTemperature = cpuTemp - averageRunningTemp;
            }
            else if (batTemp != null)
            {
                // BAT OK - CHECK LOWEST TEMP
                if (batTemp - averageRunningTemp < closestTemperature)
                    closestTemperature = batTemp - averageRunningTemp;
            }
            else
            {
                // NO CPU OR BATTERY TEMP FOUND - RETURN 0°C
                closestTemperature = 0.0;
            }
        }
        catch (Exception e)
        {
            // NO CPU OR BATTERY TEMP FOUND - RETURN 0°C
            closestTemperature = 0.0;
        }
        // FORMAT & RETURN
        return decimalFormat.format(closestTemperature);
    }


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

//        My Average Heat was 11°C higher than the real temperature --> 11 being Average Temperature
//        30 being Next Reset Time ( Period of minimum check )
//        String temper = getAmbientTemperature(9, 30);
//        Log.d("온도@@@@@ ", temper );

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

        if (temperature == null) {
            Log.d("온도센서가 ", String.valueOf(temperature) );
        }

        if (humidity == null) {
            Log.d("습도센서가 ", String.valueOf(humidity) );
        }

        listener = new SensorEventListener() {

            @Override
            public void onSensorChanged(SensorEvent event) {
//                Log.d("이벤트.센",String.valueOf(event.sensor) );
//                Log.d("이벤트.value",String.valueOf(event.values) );
//                Log.d("이벤트.timestamp",String.valueOf(event.timestamp) );

                switch(event.sensor.getType()) {

                    case Sensor.TYPE_AMBIENT_TEMPERATURE:
                        sensor_value = event.values[0];
//                        Log.d("온도 이벤트긴하다.",String.valueOf(sensor_value) );
//                        if(temperature == null) {
//                            txtTemperature.setText("온도 센서 없음");
//                        }
    //                    sensor_value = event.values[0] + event.values[1] + event.values[2];
    //                    float[] tmp = event.values;
                        txtTemperature.setText("TEMPERATURE " + String.valueOf(sensor_value));
                        break;

                    case Sensor.TYPE_RELATIVE_HUMIDITY:
                        Log.d("도 이벤트긴하다.",String.valueOf(sensor_value) );

                        if(humidity == null) {
                            txtHumidity.setText("습도 센서 없음");
                        }
                        sensor_value = event.values[0];
                        txtHumidity.setText("HUMIDITY " + String.valueOf(sensor_value));
                        break;

                    case Sensor.TYPE_PRESSURE:
                        sensor_value = event.values[0];
//                        String res = "PRESSURE" + sensor_value;
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
