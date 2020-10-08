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

public class MainActivity extends AppCompatActivity {

    TextView regRedirect,forgotPass;
    Button loginBtn;
    EditText logEmail,logPass;
    private FirebaseAuth mAuth;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        checkLoginStatus();
        init();

    }

    public void checkLoginStatus() {
        // Check if user is signed in (non-null) and update UI accordingly.
        FirebaseUser user = FirebaseAuth.getInstance().getCurrentUser();
        if (user != null) {
            Intent loggedIn = new Intent(MainActivity.this,HomePage.class);
            finish();
            //Log.d("FireBase Login (Login class)","User is logged check redirection if MainActivity doesnt start");
            startActivity(loggedIn);
        } else {
            //Log.d("Firebase Login (Login class)","User is not logged in continue for Login auth");
        }
    }

    private void init() {

        logEmail = findViewById(R.id.log_email);
        logPass = findViewById(R.id.log_pass);
        loginBtn = findViewById(R.id.btn_login);
        regRedirect = findViewById(R.id.reg_redirect);
        forgotPass = findViewById(R.id.for_pass);

        mAuth = FirebaseAuth.getInstance();

        regRedirect.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent redReg = new Intent(MainActivity.this,Register.class);
                finish();
                startActivity(redReg);
            }
        });

        forgotPass.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent forgot = new Intent(MainActivity.this,ForgotPassword.class);
                finish();
                startActivity(forgot);
            }
        });

        loginBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                loginUser();
            }
        });

    }


    private void loginUser() {

        String email,password;

        email = logEmail.getText().toString().trim();
        password = logPass.getText().toString().trim();

        if(email.isEmpty()){
            Toast.makeText(this,"Email cannot be empty",Toast.LENGTH_SHORT).show();
            return;
        }
        if(password.isEmpty()){
            Toast.makeText(this,"Email cannot be empty",Toast.LENGTH_SHORT).show();
            return;
        }

        mAuth.signInWithEmailAndPassword(email, password)
                .addOnCompleteListener(this, new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task) {
                        if (task.isSuccessful()) {
                            // Sign in success, update UI with the signed-in user's information
                            Log.d("Firebase User (Login)", "signInWithEmail:success");
                            FirebaseUser user = mAuth.getCurrentUser();
                            goToMain();
                        } else {
                            // If sign in fails, display a message to the user.
                            Log.d("Firebase User (Login)", "signInWithEmail:failure", task.getException());
                            Toast.makeText(MainActivity.this, "Authentication failed.", Toast.LENGTH_SHORT).show();
                        }
                    }
                });

    }

    private void goToMain() {

        Intent goToMain = new Intent(MainActivity.this,HomePage.class);
        finish();
        startActivity(goToMain);
    }

}