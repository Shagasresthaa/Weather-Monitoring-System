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
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;

public class Register extends AppCompatActivity {

    TextView logRedirect;
    Button regBtn;
    EditText regEmail,regPass,regConfPass;
    private FirebaseAuth mAuth;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        checkLoginStatus();
        init();

    }

    public void checkLoginStatus() {
        // Check if user is signed in (non-null) and update UI accordingly.
        FirebaseUser user = FirebaseAuth.getInstance().getCurrentUser();
        if (user != null) {
            Intent loggedIn = new Intent(Register.this,MainActivity.class);
            finish();
            //Log.d("FireBase Login (Register class)","User is logged check redirection if MainActivity doesnt start");
            startActivity(loggedIn);
        } else {
            //Log.d("Firebase Login (Register class)","User is not logged in continue for registration");
        }
    }

    private void init() {

        mAuth = FirebaseAuth.getInstance();

        logRedirect = findViewById(R.id.red_login);
        regBtn = findViewById(R.id.btn_register);
        regEmail = findViewById(R.id.reg_email);
        regPass = findViewById(R.id.reg_pass);
        regConfPass = findViewById(R.id.reg_pass_conf);

        logRedirect.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent logRedirect = new Intent(Register.this,MainActivity.class);
                finish();
                startActivity(logRedirect);
            }
        });

        regBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                userRegister();
            }
        });
    }

    private void userRegister() {

        String email,cpassword,password,firstName,lastName;

        email = regEmail.getText().toString().trim();
        password = regPass.getText().toString().trim();
        cpassword = regConfPass.getText().toString().trim();

        if(email.isEmpty()){
            Toast.makeText(Register.this, "Email cant be empty", Toast.LENGTH_SHORT).show();
            return;
        }
        else if(password.isEmpty()){
            Toast.makeText(Register.this, "Password cant be empty", Toast.LENGTH_SHORT).show();
            return;
        }
        else if(!(password.equals(cpassword))){
            Toast.makeText(Register.this, "Passwords doesnt match please check password", Toast.LENGTH_SHORT).show();
            return;
        }

        mAuth.createUserWithEmailAndPassword(email, password)
                .addOnCompleteListener(this, new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task) {
                        if (task.isSuccessful()) {
                            // Sign in success, update UI with the signed-in user's information
                            //Log.d("Firebase user", "createUserWithEmail:success");
                            FirebaseUser user = mAuth.getCurrentUser();
                            backToLogin();
                        } else {
                            // If sign in fails, display a message to the user.
                            //Log.w("Firebase user", "createUserWithEmail:failure", task.getException());
                            Toast.makeText(Register.this, "Authentication failed.", Toast.LENGTH_SHORT).show();
                        }

                    }
                });

    }

    private void backToLogin() {
        Intent btlogin = new Intent(Register.this,MainActivity.class);
        finish();
        startActivity(btlogin);
    }

}