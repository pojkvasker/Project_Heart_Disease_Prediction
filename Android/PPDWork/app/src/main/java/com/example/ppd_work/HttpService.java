package com.example.ppd_work;

import android.content.Context;
import android.content.Intent;
import android.util.Log;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

public class HttpService {

    private Context mContext;

    private String TAG = "WWW";

    private int ServerSuccess;
    private int Predict;
    private float PredictProb;


    public HttpService(Context context){
        mContext = context;

        ServerSuccess = 0;
        Predict = 0;
        PredictProb = 0;
    }

    public void start(int Age, int Sex, int BP, int Chol, int Ecg, int Exang, int id){

        String url = "http://a4cbb4d5.ngrok.io/phpTest/pingtest.php";
        url += "?Age=" + Age;
        url += "&Sex=" + Sex;
        url += "&BP=" + BP;
        url += "&Chol=" + Chol;
        url += "&Ecg=" + Ecg;
        url += "&Exang=" + Exang;
        url += "&Id=" + id;


        // Instantiate the RequestQueue.
        RequestQueue queue = Volley.newRequestQueue(mContext);

        // Request a string response from the provided URL.
        StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        // Response is what we get from going to the url.
                        String StringResponse = response;
                        Log.d(TAG, StringResponse);
                        Log.i(TAG,"Response is: "+ StringResponse);

                        // Extract the information in the string.
                        parseResponse(StringResponse);
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.e(TAG,"That didn't work!");
                Intent intent = new Intent("HTTP_ERROR");
                mContext.sendBroadcast(intent);
            }
        });

        // Add the request to the RequestQueue.
        queue.add(stringRequest);

    }

    private void parseResponse(String response){
        // Values in response is separated using ",".
        String[] tokens = response.split(", ");

        Log.i(TAG,"0: " + tokens[0]);
        Log.i(TAG,"1: " + tokens[1]);
        Log.i(TAG,"2: " + tokens[2]);

        if(tokens.length == 3) {
            ServerSuccess = Integer.parseInt(tokens[0]);
            Predict = Integer.parseInt(tokens[1]);
            PredictProb = Float.parseFloat(tokens[2]);

            Intent intent = new Intent("HTTP_PREDICTION_RESULT");
            mContext.sendBroadcast(intent);
        }else{
            Log.e(TAG,"Response error");
            Intent intent = new Intent("HTTP_ERROR");
            mContext.sendBroadcast(intent);
        }

    }

    public int getPrediction(){

        return Predict;
    }

    public float getPredictionProb(){

        return PredictProb;
    }
}
