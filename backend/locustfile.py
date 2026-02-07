import random
import string

from locust import HttpUser, between, task


def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

class AesteloUser(HttpUser):
    wait_time = between(1, 3)
    csrf_token = None  # Store the token here

    def on_start(self):
        self.email = f"{random_string()}@test.com"
        self.password = "password123"

        # 1. Signup
        response = self.client.post("/auth/signup", json={
            "email": self.email,
            "password": self.password,
            "confirm_password": self.password,
        })

        if response.status_code == 201:
            # 2. Login
            login_response = self.client.post("/auth/login-email", json={
                "email": self.email,
                "password": self.password
            })
            
            if login_response.status_code == 200:
                # 3. CRITICAL FIX: Extract CSRF Token from cookies
                # Flask-JWT-Extended usually names the cookie 'csrf_access_token'
                # Note: Check your config.py for the exact name if you changed it.
                for cookie in self.client.cookies:
                    if cookie.name == 'csrf_access_token':
                        self.csrf_token = cookie.value
                        break
                
                if not self.csrf_token:
                    print(f"Login success but CSRF token missing for {self.email}")
            else:
                print(f"Login failed for {self.email}")
                self.interrupt()

    @task(3)
    def view_profile(self):
        # GET requests usually don't need CSRF headers
        self.client.get("/profile/me")

    @task(1)
    def update_bio(self):
        if not self.csrf_token:
            return # Don't try if we don't have the token

        new_bio = f"Hello I am {self.email} and I love coding!"
        
        # 4. Add the Header manually
        self.client.patch(
            "/profile/me", 
            data={"bio": new_bio},
            headers={"X-CSRF-TOKEN": self.csrf_token} # <--- REQUIRED
        )

    @task(5)
    def view_feed(self):
        self.client.get("/post/feed")