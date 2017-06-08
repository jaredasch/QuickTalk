#!/usr/bin/python
print "Content-Type: text/html"
print ""

import cgi, cgitb, os, random, hashlib

cgitb.enable()


def md5Pass(password):
    m = hashlib.md5()
    m.update(password)
    return m.hexdigest()


def checkIfNameExists(user):
    text = open('data/users.txt', 'r').readlines()
    for line in text:
        if line.split(",")[0] == user:
            return True
    return False


def valid(s):  # Add more password validation
    for c in s:
        if not (c >= 'a' and c <= 'z' or c >= 'A' and c <= 'Z' or c >= '0' and c <= '9'):
            return False
    return True

def validPassword(password):
    return 4 < len(password) < 25

def validUser(user):
    return valid(user) and 4 < len(user) < 25

def create_account(form):
    err = []
    if "user" in form and "pass" in form and "pass2" in form and "name" in form:
        user = form['user'].value
        password = form['pass'].value
        password2 = form['pass2'].value
        name = form['name'].value
        if checkIfNameExists(user):
            return open('render/signup.html', 'r').read().replace('<!--ERRORS-->',
                                                                 '<p class = "error">User ' + user + ' already exists</p>')
        elif password != password2:
            return open('render/signup.html', 'r').read().replace('<!--ERRORS-->',
                                                                 '<p class = "error">Passwords do not match</p>')
        elif not validUser(user):
            return open('render/signup.html', 'r').read().replace('<!--ERRORS-->',
                                                                 '<p class = "error">Username contains invalid characters</p>')
        elif not validPassword(password):
            return open('render/signup.html', 'r').read().replace('<!--ERRORS-->',
                                                                 '<p class = "error">Password is too long or too short</p>')
        else:
            f = open('data/users.txt', 'a')
            password = md5Pass(password + user)
            f.write(user + ',' + password + "," + name + "\n")
            f.close()
            return open('render/account_created.html', 'r').read().replace('%USER%', user)
    else:
        return open('render/signup.html', 'r').read().replace('<!--ERRORS-->',
                                                             '<p class = "error">Invalid form submission, please fill in all fields</p>')


def notFilledIn():
    return '''You need to create an account using the form found <a href="signup.html">here</a>\n'''


def render_errors(errors):
    return '</br>'.join(['<h3>' + err + '</h3>' for err in errors]) + '</br>'


def main():
    form = cgi.FieldStorage()
    if len(form) == 0:
        print open('render/signup.html', 'r').read()
    else:
        print create_account(form)



main()
