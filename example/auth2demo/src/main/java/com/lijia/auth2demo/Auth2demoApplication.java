package com.lijia.auth2demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.security.oauth2.client.EnableOAuth2Sso;
@EnableOAuth2Sso
@SpringBootApplication
public class Auth2demoApplication {

	public static void main(String[] args) {
		SpringApplication.run(Auth2demoApplication.class, args);
	}

}
