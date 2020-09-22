package com.example.weather_forecast;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import java.util.List;

public class MangerActivity extends AppCompatActivity {
    private SensorManager sensorManager;
    private String sensorString="";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_manger);

        TextView txtSensor = (TextView) findViewById(R.id.listSensor);

        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        List<Sensor> listSensor = sensorManager.getSensorList(Sensor.TYPE_ALL);
        for (int i=0; i<listSensor.size(); i++) {
            Sensor sensor = listSensor.get(i);
            sensorString += i + ". Name: " + sensor.getName() + "\n" +
                    "Vendor: " + sensor.getVendor() + "\n" +
//                    "Version: " + sensor.getVersion() + "\n" +
//                    "Power: " + sensor.getPower() + "\n" +
                    "Type: " + sensor.getType() + "\n" +
                    "toString: " + sensor.toString() + "\n\n";
        }
        txtSensor.setText(sensorString);
        Log.d("센서!!!", sensorString);
    }
}
