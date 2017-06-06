#!/usr/bin/python
print "Content-Type: text/html"
print ""

import random
import cgi, cgitb, os

cgitb.enable()

form = cgi.FieldStorage()


def authenticate():
    if 'user' in form and 'magicnumber' in form:
        #get the data from form, and IP from user.
        user = form['user'].value
        magicnumber = form['magicnumber'].value
        IP = 'NULL'
        if 'REMOTE_ADDR' in os.environ:
            IP = os.environ["REMOTE_ADDR"]
        #compare with file
        text = open('data/loggedin.txt').readlines()
        for line in text:
            line = line.strip().split(",")
            if line[0]==user:#when you find the right user name
                if line[1]==magicnumber and line[2]==IP:
                    return True
                else:
                    return False
        return False#in case user not found
    return False #no/missing fields passed into field storage


def secure_fields():
    if 'user' in form and 'magicnumber' in form:
        user = form['user'].value
        magicnumber = form['magicnumber'].value
        return "?user=" + user + "&magicnumber=" + magicnumber
    return ""


def main():
    is_logged_in = authenticate()
    if not is_logged_in:
        print open('render/login.html', 'r').read()
    else:
        print open('render/home.html','r').read().replace('%secure_fields%', secure_fields())

main()
