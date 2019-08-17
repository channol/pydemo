#!/usr/bin/python3

import sys,os,re,time
from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return 'Hello, world!'

@app.route('/')
def index():
    return 'index page'

@app.route('/user/<username>')
def show_user_profile(username):
    return 'user %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'post %s' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return 'subpath %s' % subpath
