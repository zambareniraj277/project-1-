users = {}

def get_user(username):
    return users.get(username)

def add_user(username, password):
    users[username] = {'username': username, 'password': password}

reset_tokens = {}

def store_reset_token(email, token):
    reset_tokens[email] = token

def get_reset_token(email):
    return reset_tokens.get(email)

def get_email_from_token(token):
    for email, stored_token in reset_tokens.items():
        if stored_token == token:
            return email
    return None

def update_password(username, password):
    if username in users:
        users[username]['password'] = password
