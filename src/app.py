from flask import Flask

app=Flask(__name__)

@app.get("/")
def index ():
    return "Hello World"

@app.get("/hello")
def say_hello():
    return {"message": "Hello World"}