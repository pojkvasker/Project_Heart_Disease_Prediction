package com.example.ppd_work;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCallback;
import android.bluetooth.BluetoothGattCharacteristic;
import android.bluetooth.BluetoothGattDescriptor;
import android.bluetooth.BluetoothManager;
import android.bluetooth.BluetoothProfile;
import android.bluetooth.le.BluetoothLeScanner;
import android.bluetooth.le.ScanCallback;
import android.bluetooth.le.ScanResult;
import android.content.Context;
import android.content.Intent;
import android.os.Handler;
import android.util.Log;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.util.List;
import java.util.UUID;

public class BluetoothLEService extends AppCompatActivity {

    private int BLOODPRESSURE_DEVICE = 0;
    private int CHOLESTEROL_DEVICE = 1;
    private int DEVICE;
    private Context mContext;
    private String Address;

    private int dataReturned = 0;

    private int connectionState = STATE_DISCONNECTED;

    private static final int STATE_DISCONNECTED = 0;
    private static final int STATE_CONNECTING = 1;
    private static final int STATE_CONNECTED = 2;

    private static final int BOND_BONDED = 12;
    private static final int BOND_BONDING = 11;
    private static final int BOND_NONE = 10;

    /**
     * UUIDs for the BT device.
     */
    private UUID SERVICE_UUID;
    private UUID CHAR_UUID;

    /**
     * Our UUID.
     */
    private UUID CLIENT_CHARACTERISTIC_CONFIG_UUID = convertFromInteger(0x2902);


    /**
     * Bluetooth things.
     */
    private BluetoothAdapter btA;
    private BluetoothLeScanner btScan;
    private boolean mScanning;
    private String TAG = "BTLEService";
    private BluetoothGatt btGatt;
    private BluetoothDevice BPdevice;


    public BluetoothLEService(Context context, int inDEVICE){

        mContext = context;

        DEVICE = inDEVICE;

        // Get default adapter.
        btA = BluetoothAdapter.getDefaultAdapter();

        // Get a Le scanner object to enable scan.
        btScan = btA.getBluetoothLeScanner();

        if(DEVICE == BLOODPRESSURE_DEVICE){
            Address = "90:E2:02:BE:56:40"; // Address of BP device.
            SERVICE_UUID = convertFromInteger(0xAAA0);
            CHAR_UUID = convertFromInteger(0xFFE1);
        }else if(DEVICE == CHOLESTEROL_DEVICE){
            Address = "90:E2:02:A0:2B:07"; // Address of Cholesterol device.
            SERVICE_UUID = convertFromInteger(0xAAA0);
            CHAR_UUID = convertFromInteger(0xFFE1);
        }else{
            //Error
        }

    }

    /**
     * Collects the data from the remote device.
     */
    public synchronized void start(){

        // Start BT, if it is not all ready started.
        startBT();

        // Start the BT train.
        scanLeDevice(true);
    }

    public int getData(){
        return dataReturned;
    }

    /**
     * Function to start the BT. THIS METHOD SHOULD BE REWRITTEN.
     */
    private void startBT(){
        if (!btA.isEnabled()) {
            Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableBtIntent, 1);
            // TODO: Solution is temporary. While loop is used to hold it here while we wait for user.
            while(!btA.isEnabled()){}
            Log.i("test","BT started");
        }
    }

    /**
     * Function used to start the scan and stop the scan after SCAN_PERIOD seconds.
     * When the LE scan finds a device we are thrown into mScanCallback.
     * @param enable
     */
    private void scanLeDevice(final boolean enable) {
        final long SCAN_PERIOD = 5000; // 5 seconds
        Handler mHandler = new Handler();
        if (enable) {
            // Stops scanning after a pre-defined scan period.
            mHandler.postDelayed(new Runnable() {
                @Override
                public void run() {
                    mScanning = false;
                    btScan.stopScan(mScanCallback);
                    /* If we get here and we are not connected, we have not find our device.
                     TODO: Rewrite this method of telling whether the device has been found or not.
                       The method is not bullet proof. */
                    if(connectionState != STATE_CONNECTED) {
                        Intent intent = new Intent("BTLE_NO_FIND");
                        mContext.sendBroadcast(intent);
                    }
                }
            }, SCAN_PERIOD);

            mScanning = true;
            btScan.startScan(mScanCallback);
        } else {
            mScanning = false;
            btScan.stopScan(mScanCallback);
        }
    }

    /**
     * Function called when scanLEDevice() finds something?
     */
    private ScanCallback mScanCallback = new ScanCallback() {
        @Override
        public void onScanResult(int callbackType, ScanResult result) {
            super.onScanResult(callbackType, result);
            String deviceAddress = result.getDevice().getAddress();
            Log.i(TAG,"Device address: " + deviceAddress);
            if(deviceAddress.equals(Address)){ // The address of the module we are looking for.
                Log.i(TAG,"Found device");
                // We found the device we where looking for, stop the scan.
                btScan.stopScan(mScanCallback);
                // Save the found device.
                BPdevice = result.getDevice();
                // Start connecting process.
                connect(BPdevice);
            }
        }

        @Override
        public void onBatchScanResults(List<ScanResult> results) {
            super.onBatchScanResults(results);
            Log.d(TAG,"Batch result?");
            //
        }

        @Override
        public void onScanFailed(int errorCode) {
            super.onScanFailed(errorCode);
            Log.e(TAG,"Scan did not start");
        }
    };

    /**
     * Function that starts connecting procedure. Called from ScanCallback.
     * @param BTDevice_OfInterest
     */
    private void connect(BluetoothDevice BTDevice_OfInterest){

        // This throws us into gattCallback.
        btGatt = BTDevice_OfInterest.connectGatt(this, false, gattCallback);
    }

    /**
     * GattCallback. We are sent here from the connectGatt function.
     * Here we can decide what happens when we have a connection state change,
     * services discovered, characteristic read, etc.
     */
    private final BluetoothGattCallback gattCallback = new BluetoothGattCallback() {
        @Override
        public void onConnectionStateChange(BluetoothGatt gatt, int status, int newState) {
            super.onConnectionStateChange(gatt, status, newState);
            String intentAction;
            if (newState == BluetoothProfile.STATE_CONNECTED) {
                connectionState = STATE_CONNECTED;
                Log.i(TAG, "Connected to GATT server.");
                Log.i(TAG, "Attempting to start service discovery:" +
                        btGatt.discoverServices());

            }else if (newState == BluetoothProfile.STATE_DISCONNECTED) {
                connectionState = STATE_DISCONNECTED;
                Log.i(TAG, "Disconnected from GATT server.");
            }
        }

        /**
         * When we have discovered services, which we do when we connect to the BT LE device,
         * we want to send a command to the BT LE device.
         * Because we need to be bonded when we send the command when need to wait for the user to
         * enter the pin to bond the devices.
         * @param gatt
         * @param status
         */
        @Override
        public void onServicesDiscovered(BluetoothGatt gatt, int status) {
            if (status == BluetoothGatt.GATT_SUCCESS) {
                Log.i(TAG,"onServicesDiscovered");

                // Synchronized because we want to hold at the while loop.
                synchronized (this){

                    while(BPdevice.getBondState() == BOND_BONDING){}

                    // We start the information exchange.
                    BluetoothGattCharacteristic characteristic =
                            gatt.getService(SERVICE_UUID)
                                    .getCharacteristic(CHAR_UUID);

                    gatt.setCharacteristicNotification(characteristic, true);

                    BluetoothGattDescriptor descriptor =
                            characteristic.getDescriptor(CLIENT_CHARACTERISTIC_CONFIG_UUID);

                    descriptor.setValue(
                            BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE);

                    // This command throws us into descriptor write.
                    gatt.writeDescriptor(descriptor);
                }

            } else {
                Log.w(TAG, "onServicesDiscovered received: " + status);
            }
        }

        @Override
        public void onDescriptorWrite(BluetoothGatt gatt, BluetoothGattDescriptor descriptor, int status){

            BluetoothGattCharacteristic characteristic =
                    gatt.getService(SERVICE_UUID)
                            .getCharacteristic(CHAR_UUID);

            // A is our key that the remote device also has. When it receives 'A' it sends data back.
            characteristic.setValue("A".getBytes());
            gatt.writeCharacteristic(characteristic);

            Log.i(TAG,"Descriptor Write");
        }

        @Override
        public void onCharacteristicChanged(BluetoothGatt gatt, BluetoothGattCharacteristic characteristic) {
            // The connected BT LE device has changed a value of the characteristic --> read that data.
            processData(characteristic);
        }
    };

    /**
     * Store the read data and close the gatt.
     * @param characteristic
     */
    private synchronized void processData(BluetoothGattCharacteristic characteristic) {
        dataReturned = Integer.parseInt(characteristic.getStringValue(0));
        Log.i(TAG,"Value: " + dataReturned);

        Intent intent = new Intent();

        if(DEVICE == BLOODPRESSURE_DEVICE) {
            intent.setAction("BTLE_SERVICE_FINISHED_BP");
        }else if(DEVICE == CHOLESTEROL_DEVICE) {
            intent.setAction("BTLE_SERVICE_FINISHED_CHL");
        }
        // Send broadcast that we have received the data.
        mContext.sendBroadcast(intent);

        // We have gotten our value - close the connection.
        btGatt.close();
    }

    /**
     * Converts an int to a UUID.
     * @param i
     * @return UUID
     */
    private UUID convertFromInteger(int i) {
        final long MSB = 0x0000000000001000L;
        final long LSB = 0x800000805f9b34fbL;
        long value = i & 0xFFFFFFFF;
        return new UUID(MSB | (value << 32), LSB);
    }

}
