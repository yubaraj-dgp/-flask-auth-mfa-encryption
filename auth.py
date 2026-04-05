users = {"admin1": "1234", "admin2": "12345"}

def login(username, password):
    return users.get(username) == password