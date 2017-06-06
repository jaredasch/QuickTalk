#!/usr/bin/python
print "Content-Type: text/html"
print ""

import cgi, cgitb, os, random, hashlib

cgitb.enable()

form = cgi.FieldStorage()


def post(data):
    body = data['body'].value
    user = data['user'].value
    file = open('data/posts.txt', 'a')
    file.write(user + ',' + body + '\n')
    file.close()


def secure_fields():
    if 'user' in form and 'magicnumber' in form:
        user = form.getvalue('user')
        magicnumber = form.getvalue('magicnumber')
        return "?user=" + user + "&magicnumber=" + magicnumber
    return ""


def build_post(user, content):
    return '''
        <div class = "post">
            <a href ="profile.py/?user=''' + user + ''''">''' + user + '''</a>
            <div class = "post-body">
                <p class = "post-content">''' + content + '''</p>
            </div>
        </div>
    '''


def update_posts():
    html = ''
    posts = open('data/posts.txt', 'r').readlines()
    for i in posts[::-1]:
        user = i.split(',', 1)[0]
        content = i.split(',', 1)[1]
        html += build_post(user, content)
    return html


def main():
    post(form)
    name = secure_fields().split('&')[0].split('=')[1]
    number = secure_fields().split('&')[1].split('=')[1]
    template = open('render/home.html', 'r').read()
    template = template.replace('%secure_fields%', secure_fields()).replace('%auth_number%', number).replace('%user%',name)
    template = template.replace('<!--POSTS-->', update_posts())
    print template


main()
