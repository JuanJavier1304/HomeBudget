import bcrypt

username = "username_test"
password = "74387518"

password_hash = bcrypt.hashpw(
    password.encode(),
    bcrypt.gensalt()
).decode()

print(password_hash)