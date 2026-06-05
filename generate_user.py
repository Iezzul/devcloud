from faker import Faker
import pandas as pd
import random

fake = Faker()

user = []

for i in range(20):

    username = fake.user_name()
    email = f"{username}{random.randint(1000, 9999)}@yopmail.com"
    
    user.append(
        {
            "username": username,
            "email": email,
            'password': "Password123!"
        }
    )
df = pd.DataFrame(user)

df.to_excel(
    "users.xlsx",
    index=False
)

print("users.xlsx created")