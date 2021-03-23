# Petstagram

A simple pet themed instagram clone!  With Petstagram, you can create a user, post images, and check out posts from other users in a feed.


### Local Deployment

To launch this app on your local environment, clone this repository:

```
git clone https://github.com/Kou-kun42/petstagram.git
```

Navigate to the project folder and then set up a python virtual environment using:

```
python3 -m venv env
```

Activate it:

```
source env/bin/activate
```

Next, install all the required packages:

```
pip3 install -r requirements.txt
```

Add a .env file to the root of the project directory with the following key names
```bash
SQLALCHEMY_DATABASE_URI=sqlite:///database.db

SECRET_KEY={Your auth session secret key}
(You can create and use any strong password of your choosing)
```

Finally, launch the app:

```
python3 app.py
```


