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


def create_account(form):
    err = []
    if "user" in form and "pass" in form and "pass2" in form:
        user = form['user'].value
        password = form['pass'].value
        password2 = form['pass2'].value
        if checkIfNameExists(user):
            err += ["User exists: " + user]
        elif password != password2:
            err += ["Passwords do not match!"]
        elif not valid(user):
            err += ["Username contains invalid characters"]
        else:
            print password, user
            f = open('data/users.txt', 'a')
            password = md5Pass(password + user)
            f.write(user + "," + password + "\n")
            f.close()
            return "<h2>Your account, " + user + ', was created successfully! login here: \
                                    <a href="./login.py">login page</a></h2><br>'
    else:
        err += ['Invalid form submission, please fill in all fields</h2>']
    return err


def notFilledIn():
    return '''You need to create an account using the form found <a href="create.html">here</a>\n'''


def render_errors(errors):
    return '</br>'.join(['<h3>' + err + '</h3>' for err in errors]) + '</br>'


def main():
    form = cgi.FieldStorage()
    if len(form) == 0:
        print open('render/create.html', 'r').read()
    else:
        acc = create_account(form)
        if acc[0:10] == '<h2>Your a':
            print open('render/account_created.html', 'r').read().replace('%Message Filler%', acc)
        else:
            print open('render/create.html', 'r').read().replace('<!--Message Filler-->', render_errors(acc))


main()
