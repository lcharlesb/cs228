import pickle


database = pickle.load(open('userData/database.p','rb'))

userName = raw_input('Please enter your name: ')
if userName in database:
    print('welcome back ' + userName + '.')
    userEntry = database[userName]
    incrementMe = userEntry['logins']
    incrementMe += 1
    userEntry['logins'] = incrementMe
else:
    database[userName] = {'logins': 1}
    print('welcome ' + userName + '.')

print(database)

pickle.dump(database, open('userData/database.p','wb'))
