/*
Weather Monitoring System using cost effective Weather nodes
Copyright (C) 2020  Shaga Sresthaa

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>

The full text of the GNU General Public License version 3 can be found in the
source code root directory as COPYING.txt.
*/

package com.example.weathermonitor;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;

public class ForgotPassword extends AppCompatActivity {

    TextView logRedirectF;
    EditText resetEmail;
    Button reset;
    private FirebaseAuth mAuth;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_forgot_password);

        checkLoginStatus();
        init();
    }

    public void checkLoginStatus() {
        // Check if user is signed in (non-null) and update UI accordingly.
        FirebaseUser user = FirebaseAuth.getInstance().getCurrentUser();
        if (user != null) {
            Intent loggedIn = new Intent(ForgotPassword.this,MainActivity.class);
            finish();
            //Log.d("FireBase Login (ForgotPassword class)","User is logged check redirection if MainActivity does'nt start");
            startActivity(loggedIn);
        } else {
            //Log.d("Firebase Login (ForgotPassword class)","User is not logged in continue for registration");
        }
    }

    private void init() {

        logRedirectF = findViewById(R.id.ret_log);
        resetEmail = findViewById(R.id.res_em);
        reset = findViewById(R.id.btn_reset);

        mAuth = FirebaseAuth.getInstance();

        reset.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                resetEmailSendVerification();
            }
        });

        logRedirectF.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent returnToLogin = new Intent(ForgotPassword.this,MainActivity.class);
                finish();
                startActivity(returnToLogin);
            }
        });

    }

    private void resetEmailSendVerification() {

        String email = resetEmail.getText().toString().trim();

        if(email.isEmpty()){
            Toast.makeText(ForgotPassword.this,"Email cant be empty",Toast.LENGTH_SHORT).show();
            return;
        }

        mAuth.sendPasswordResetEmail(email)
                .addOnCompleteListener(new OnCompleteListener<Void>() {
                    @Override
                    public void onComplete(@NonNull Task<Void> task) {
                        if (task.isSuccessful()) {
                            Toast.makeText(ForgotPassword.this,"Password reset email has been sent",Toast.LENGTH_SHORT).show();
                            sendToLogin();
                        } else {
                            Toast.makeText(ForgotPassword.this,"Failed to send reset email", Toast.LENGTH_SHORT).show();
                        }
                    }
                });

    }

    private void sendToLogin() {

        Intent send = new Intent(ForgotPassword.this,MainActivity.class);
        finish();
        startActivity(send);

    }

}