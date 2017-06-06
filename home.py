#!/usr/bin/python
print "Content-Type: text/html"
print ""

import random
import cgi, cgitb, os

cgitb.enable()

# the field storage is a global variable.
# Since your page has exactly one, you can
# just acccess it from anywhere in the program.
form = cgi.FieldStorage()


def authenticate():
    if 'user' in form and 'magicnumber' in form:
        # get the data from form, and IP from user.
        user = form.getvalue('user')
        magicnumber = form.getvalue('magicnumber')
        IP = 'NULL'
        if 'REMOTE_ADDR' in os.environ:
            IP = os.environ["REMOTE_ADDR"]
        # compare with file
        text = open('data/loggedin.txt').read().split("\n")
        for line in text:
            line = line.split(",")
            if line[0] == user:  # when you find the right user name
                if line[1] == magicnumber and line[2] == IP:
                    return True
                else:
                    return False
        return False  # in case user not found
    return False  # no/missing fields passed into field storage


# either returns ?user=__&magicnumber=__  or an empty string.
def secure_fields():
    if 'user' in form and 'magicnumber' in form:
        user = form.getvalue('user')
        magicnumber = form.getvalue('magicnumber')
        return "?user=" + user + "&magicnumber=" + magicnumber
    return ""


def update_posts():
    html = ''
    posts = open('data/posts.txt', 'r').readlines()
    for i in posts:
        html += '<p>' + i.split(',', 1)[1] + ' --- ' + i.split(',', 1)[0] + '</p></br>'
    return html


def main():
    is_logged_in = authenticate()
    if not is_logged_in:
        print open('render/login.html', 'r').read()
    else:
        name = secure_fields().split('&')[0].split('=')[1]
        number = secure_fields().split('&')[1].split('=')[1]
        template = open('render/home.html', 'r').read()
        template = template.replace('%secure_fields%', secure_fields()).replace('%auth_number%', number).replace('%user%', name).replace('<!--POSTS-->', update_posts())
        print template

main()
