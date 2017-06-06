#!/usr/bin/python
print "Content-Type: text/html"
print ""


import random
import cgi, cgitb, os

cgitb.enable()

form = cgi.FieldStorage()

def authenticate():
    if 'user' in form and 'magicnumber' in form:
        # get the data from form, and IP from user.
        user = form['user'].value
        magicnumber = form['magicnumber'].value
        IP = 'NULL'
        if 'REMOTE_ADDR' in os.environ:
            IP = os.environ["REMOTE_ADDR"]
        # compare with file
        text = open('data/loggedin.txt').readlines()
        for line in text:
            line = line.strip().split(",")
            if line[0] == user:  # when you find the right user name
                if line[1] == magicnumber and line[2] == IP:
                    return True
                else:
                    return False
        return False  # in case user not found
    return False  # no/missing fields passed into field storage


# either returns ?user=__&magicnumber=__  or an empty string.
def securefields():
    if 'user' in form and 'magicnumber' in form:
        user = form['user'].value
        magicnumber = form['magicnumber'].value
        return "?user=" + user + "&magicnumber=" + magicnumber
    return ""


# makes a link, link will include secure features if the user is logged in
def makeLink(page, text):
    return '<a href="' + page + securefields() + '">' + text + '</a><br>'


def loggedIn():
    return '''
This part is super secret!<br>
My secret? I hate fleas... even at flea markets.<br>
'''


def notLoggedIn():
    return '''You need to login to see more. You can log in here: <a href="login.html">here</a>\n'''


def main():
    isLoggedIn = authenticate()
    if not isLoggedIn:
        print open('login.html', 'r').read()
    else:
        print open('home.index.html','r').read().replace('%secure_fields%', securefields())
    # body += "<hr>other stuff can go here<hr>\n"
    #
    # # determine if the user is properly logged in once.
    #
    #
    # # use this to determine if you want to show "logged in " stuff, or regular stuff
    # if isLoggedIn:
    #     body += loggedIn()
    # else:
    #     body += notLoggedIn()
    #
    # # anyone can see this
    # body += "<hr>other stuff can go here<hr>\n"
    #
    # # attach a logout link only if logged in
    # if isLoggedIn:
    #     body += makeLink("logout.py", "Click here to log out") + "<br>"
    #
    # # make links that include logged in status when the user is logged in
    # body += makeLink("page1.py", "here is page one") + '<br>'
    # body += makeLink("page2.py", "here is page two") + '<br>'
    #
    # # finally print the entire page.
    # print header() + body + footer()


main()