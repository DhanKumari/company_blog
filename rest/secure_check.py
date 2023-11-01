from user import User

users=[User(1,'kannu','12345'),
       User(2,'Dhan','hello')
       
       ]

username_table= {u.username :u for u in users}
userid_table= {u.id :u for u in users}


#auth
def authenticate(username,password):

    user = username_table.get(username,None)
    if user and password == user.password:
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id,None)