import pyrebase

config = {
    "apiKey": "AIzaSyAr54bCYMwvqBdLHNjKF5HsvoJx29MlmGo",
    "authDomain": "martlet-inno.firebaseapp.com",
    "databaseURL": "https://martlet-inno.firebaseio.com/",
    "storageBucket": "martlet-inno.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

if __name__ == '__main__':
    # data to save
    data = {
        "name2": "Mortimer 'Morty' Smith"
    }

    # Pass the user's idToken to the push method
    results = db.child("sensors").update(data)
    print(results)
