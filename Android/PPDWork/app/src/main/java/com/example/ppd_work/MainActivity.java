package com.example.ppd_work;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.bluetooth.BluetoothGattCharacteristic;
import android.bluetooth.BluetoothGattDescriptor;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    private Context mContext;

    private BroadcastReceiver receiver = new MyBroadcastReceiver();

    private BluetoothLEService BTLEService;
    private HttpService HTTPServiceObject;

    private TextView globalResultTextView;

    private int BLOODPRESSURE_DEVICE = 0;
    private int CHOLESTEROL_DEVICE = 1;

    private int BLOODPRESSURE = 0;
    private int CHOLESTEROL = 0;

    private String TAG = "Main";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mContext = getApplicationContext();

        /* Register a receiver for action BTLE_SERVICE_FINISHED.
        Called when data is collected from BT device. */
        IntentFilter filter = new IntentFilter("BTLE_SERVICE_FINISHED_BP");
        filter.addAction("BTLE_SERVICE_FINISHED_CHL");
        filter.addAction("BTLE_NO_FIND");
        filter.addAction("HTTP_PREDICTION_RESULT");
        filter.addAction("HTTP_ERROR");
        registerReceiver(receiver, filter);

        // Permission needed for using BT.
        ActivityCompat.requestPermissions(this,new String[]{Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION}, 1001); //Any number

        Button btnGetBP = findViewById(R.id.GetBPData);
        Button btnGetChl = findViewById(R.id.GetCHLData);
        Button btnPredict = findViewById(R.id.predict);
        Button btnGlblPredict = findViewById(R.id.globalPredict);
        final TextView resultTextView = findViewById(R.id.prediction);
        globalResultTextView = findViewById(R.id.textViewGR);

        // Get the blood pressure from the blood pressure module.
        btnGetBP.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                synchronized (this) {

                    BTLEService = new BluetoothLEService(mContext, BLOODPRESSURE_DEVICE);

                    // Once the data is received we are thrown into receiver object.
                    BTLEService.start();
                }

            }
        });

        // Get the cholesterol value from the cholesterol module.
        btnGetChl.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                synchronized (this) {

                    BTLEService = new BluetoothLEService(mContext, CHOLESTEROL_DEVICE);

                    // Once the data is received we are thrown into receiver object.
                    BTLEService.start();
                }
            }
        });

        btnPredict.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                // Features:
                double age = 58;
                double gender = 1;
                double ecg = 0;

                double[] features = new double[5];

                features[0] = age;
                features[1] = gender;
                features[2] = ecg;
                features[3] = BLOODPRESSURE;
                features[4] = CHOLESTEROL;


                // Prediction:
                NeuralNet clf = new NeuralNet("relu", "logistic");
                int estimation = clf.predict(features);

                Log.i(TAG, "Prediction: " + estimation);

                resultTextView.setText("Prediction: " + estimation);
            }
        });

        // Do prediction on server.
        btnGlblPredict.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                // Start a Http service
                HTTPServiceObject = new HttpService(mContext);

                // Send data to server. A broadcast is sent when results are ready.
                long id = 951127;
                HTTPServiceObject.start(1,1,1,1,1,1, 951127);

            }
        });
    }

    public class MyBroadcastReceiver extends BroadcastReceiver {
        private static final String TAG = "MyBroadcastReceiver";
        @Override
        public void onReceive(Context context, Intent intent) {
            Log.d(TAG, "onReceive");
            String action = intent.getAction();
            if(action.equals("BTLE_SERVICE_FINISHED_BP")){
                BLOODPRESSURE = BTLEService.getData();
                Log.d(TAG, "Data received from BP device. Value: " + BTLEService.getData());
                BTLEService = null;
                Toast.makeText(mContext, "Data received from blood pressure device", Toast.LENGTH_LONG).show();
            }else if(action.equals("BTLE_SERVICE_FINISHED_CHL")){
                CHOLESTEROL = BTLEService.getData();
                Log.d(TAG, "Data received from CHL device. Value: " + BTLEService.getData());
                BTLEService = null;
                Toast.makeText(mContext, "Data received from cholesterol device", Toast.LENGTH_LONG).show();
            }else if(action.equals("BTLE_NO_FIND")){
                Log.d(TAG, "Did not find the device");
                Toast.makeText(mContext, "Did not find the device", Toast.LENGTH_LONG).show();
            }else if(action.equals("HTTP_PREDICTION_RESULT")){
                int prediction = HTTPServiceObject.getPrediction();
                float predictionProb = HTTPServiceObject.getPredictionProb();

                Log.d(TAG, "HTTP prediction result ready. Result: " + prediction +
                        "Predict prob: " + predictionProb);

                String text = "Result: " + prediction + "Predict prob: " + predictionProb;
                globalResultTextView.setText(text);

                Toast.makeText(mContext, "Result received.", Toast.LENGTH_LONG).show();
            }else if(action.equals("HTTP_ERROR")){
                Toast.makeText(mContext, "Http error.", Toast.LENGTH_LONG).show();
            }

        }
    }
}
