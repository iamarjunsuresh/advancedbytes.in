#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import os
import logging
import urllib
import jinja2
import random
import json
from google.appengine.ext import ndb
from google.appengine.api import mail
import pyclbr
import hashlib
from _random import Random
from random import random
from setuptools.command.egg_info import overwrite_arg
from email import email
from random import randint
from unjumbleme import userbase, points


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=False)


class gsdp_downloads(ndb.Model):
    version=ndb.StringProperty()
    tmode=ndb.StringProperty()
class nlot(ndb.Model):
    date = ndb.DateTimeProperty(auto_now_add=True)
    email = ndb.StringProperty()
    lotno = ndb.StringProperty()
class mousexy(ndb.Model):
    x = ndb.DateTimeProperty(auto_now_add=True)
    id = ndb.StringProperty()
    y = ndb.StringProperty()

class lotdetails(ndb.Model):
    date = ndb.DateTimeProperty(auto_now_add=True)
    winneremail = ndb.StringProperty()
    lotno = ndb.StringProperty()


class moneydetails(ndb.Model):
    date = ndb.DateTimeProperty(auto_now_add=True)
    winneremail = ndb.StringProperty()
    money = ndb.StringProperty()
    desc = ndb.StringProperty()

    def add(self, email, des, mon):
        self.winneremail = email
        self.desc = des
        self.money = str(mon)
        self.put()
        nb = money().query().filter(money.email == email)
        d = nb.fetch(1)
        d[0].money = str(float(d[0].money) + mon)
        d[0].put();


class users(ndb.Model):
    name = ndb.StringProperty()
    mobile = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()
#class quesnow(ndb.model):


#   ques=ndb.StringProperty()
#  a3=ndb.StringProperty()
# a1=ndb.StringProperty()
# a2=ndb.StringProperty()
# a4=ndb.StringProperty()
# a=ndb.StringProperty()

class usernow(ndb.Model):
    email = ndb.StringProperty()
    kid = ndb.StringProperty()


class money(ndb.Model):
    email = ndb.StringProperty()
    money = ndb.StringProperty(default='10')


class csh(ndb.Model):
    des = ndb.StringProperty()
    email = ndb.StringProperty()


def p(f):
    logging.debug("value of my var is %s", str(f))


def cidvalidation(cidss):
    return '123@g.'
    k = usernow.query(usernow.kid == cidss)
    logging.info(k.get())
    fent = k.get()
    if fent is not None:
        return fent.email
    else:
        return False


class selectlotwinner(webapp2.RequestHandler):
    def get(self):
        n = lotdetails.query().filter(lotdetails.winneremail == "")
        nn = n.get()
        logging.info(nn.lotno)
        queryfortoday = nlot.query().filter(nlot.lotno == nn.lotno)
        queryresult = queryfortoday.fetch(100)
        rando = len(queryresult)
        if rando != 0:
            logging.info(rando)
            randomwinner = randint(0, rando - 1)
            nn.winneremail = queryresult[randomwinner].email
            nn.put()

        else:
            nn.winneremail = 'NoWinner'
            nn.put()
        newlot = lotdetails()
        newlot.lotno = str(int(nn.lotno) + 1)
        newlot.winneremail = ""
        newlot.put()


class ntial(webapp2.RedirectHandler):
    def get(self):
        #createlot()
        pass


def createlot():
    newlot = lotdetails()
    newlot.lotno = '1'
    newlot.winneremail = ""
    newlot.put()


class my(webapp2.RequestHandler):
    def get(self):
        #self.response.write(self.request.cookies.get('cid'))
        user = cidvalidation(self.request.cookies.get('cid'))

        if user == False:
            self.redirect('./')
        else:
            q = users.query().filter(users.email == user)
            usee = q.fetch(1)
            mn = money.query().filter(users.email == user)
            m = mn.fetch(1)
            template = JINJA_ENVIRONMENT.get_template('html/hme.html')
            f = open('html/my-earn.html')
            myearn = f.read()
            template_values=[]
            if usee!=[]:
                template_values = {'name': usee[0].name, 'g': m[0].money, 'content': myearn}
            self.response.write(template.render(template_values))


def contenttemplate(self, files, boolctr):
    user = cidvalidation(self.request.cookies.get('cid'))
    if user == False:
        self.redirect('./')
    else:
        q = users.query().filter(users.email == user)
        usee = q.fetch(1)
        mn = money.query().filter(users.email == user)

        m = mn.fetch(1)
        template = JINJA_ENVIRONMENT.get_template('html/hme.html')
        if boolctr == 1:
            f = open('html/' + files + '.html')
            myearn = f.read()
        else:
            myearn = files
        template_values = {'name': usee[0].name, 'g': m[0].money, 'content': myearn}
        return template.render(template_values)
        pass


class ed(webapp2.RequestHandler):
    def get(self):
        d = cidvalidation(self.request.cookies.get('cid'))
        if d == False:
            self.redirect('./')
        else:
            q = users.query().filter(users.email == d)
            usee = q.fetch(1)
            mn = money.query().filter(users.email == d)
            m = mn.fetch(1)
            template = JINJA_ENVIRONMENT.get_template('html/hme.html')
            dedit = JINJA_ENVIRONMENT.get_template('html/dedit.html')
            valueedit = {'name': usee[0].name, 'email': usee[0].email, 'p': usee[0].password, 'mob': usee[0].mobile}
            #f=open('html/dedit.html')
            #s=f.read()
            template_values = {'name': usee[0].name, 'g': m[0].money, 'content': dedit.render(valueedit)}
            self.response.write(template.render(template_values))

    def post(self):
        d = cidvalidation(self.request.cookies.get('cid'))
        if d == False:
            self.redirect('./')
        else:

            q = users.query().filter(users.email == d)
            usee = q.fetch(1)
            mn = money.query().filter(users.email == d)
            m = mn.fetch(1)
            usee[0].name = self.request.get('n')
            usee[0].password = self.request.get('p')
            usee[0].put()
            template = JINJA_ENVIRONMENT.get_template('html/hme.html')
            dedit = JINJA_ENVIRONMENT.get_template('html/dedit.html')
            valueedit = {'name': usee[0].name, 'email': usee[0].email, 'p': usee[0].password, 'mob': usee[0].mobile}
            template_values = {'name': usee[0].name, 'g': m[0].money, 'content': dedit.render(valueedit)}
            self.response.write(template.render(template_values))


class MainHandler(webapp2.RequestHandler):
    def get(self):
        f = open('html/homepage.html')
        s = f.read()
        self.response.write(s)


class Sign(webapp2.RequestHandler):
    def get(self):
        f = open('html/sign.html')
        s = f.read()
        self.response.write(s)


class poyi(webapp2.RequestHandler):
    def get(self):
        k = cidvalidation(self.request.cookies.get('cid'))
        if k == False:
            self.redirect('../')
        else:
            u = usernow.query().filter(usernow.email == k)
            ud = u.fetch(1)
            ud[0].key.delete()
            self.redirect('../')


class Sigd(webapp2.RequestHandler):
    def post(self):

        user = self.request.get('username')
        passw = self.request.get('password')
        q = users.query().filter(users.email == user)
        usee = q.fetch(1)
        if usee:
            if usee[0].password == passw:
                hashintermediate = hashlib.sha224('nsadsad' + user + str(random()))
                idf = hashintermediate.hexdigest()
                fd = usernow(id=user)
                fd.email = user

                fd.kid = idf
                fd.put()
                self.response.set_cookie('cid', idf, max_age=3655, overwrite=True)

                self.redirect('./here')

        else:
            f = open('html/error in sign.html')
            s = f.read()
            self.response.write(s)


class lot(webapp2.RequestHandler):
    def post(self):
        user = cidvalidation(self.request.cookies.get('cid'))
        newn = nlot(id=1)
        newn.email = user
        n = lotdetails.query().filter(lotdetails.winneremail == "")
        nn = n.get()
        if nn is None:
            newn.lotno = '1'
        else:
            newn.lotno = nn.lotno
        newn.put()
        self.response.write(contenttemplate(self, 'lot', 1))

    def get(self):
        self.response.write(contenttemplate(self, 'lot', 1))


class signe(webapp2.RequestHandler):
    def get(self):
        f = open('html/log.html')
        s = f.read()
        self.response.write(s)


class msd(webapp2.RequestHandler):
    def get(self):
        d = cidvalidation(self.request.cookies.get('cid'))
        if d == False:
            self.redirect('./')
        else:


            q = users.query().filter(users.email == d)
            usee = q.fetch(1)
            mn = money.query().filter(users.email == d)
            m = mn.fetch(1)
            template = JINJA_ENVIRONMENT.get_template('html/hme.html')
            dedit = JINJA_ENVIRONMENT.get_template('html/money.html')

            valueedit = {'mosn': m[0].money}
            template_values = {'name': usee[0].name, 'g': m[0].money, 'content': dedit.render(valueedit)}
            self.response.write(template.render(template_values))


class mouse(webapp2.RedirectHandler):
    def get(self):
        f = open('html/mouse-look.html')
        s = f.read()
        self.response.write(s)
    def post(self):
        x=self.request
class mousehandler(webapp2.RequestHandler):
    def get(self):
        q=mousexy.query().fetch(10);
        if len(q)==0:
            d=[]
            for i in range(0,10):
                an_item = dict(x=randint(0,400),y=randint(0,500))
                d.append(an_item)
                #d={'1':['34','34'],'2':['90','3']}
                
            j=json.dumps(d)
            self.response.write(j)
        else:
            pass
class leader(webapp2.RequestHandler):
    def get(self):
        template=JINJA_ENVIRONMENT.get_template('html/leader.html')
        con=self.request.get('cntry')
        leaders=[]
        leader=points.query().filter(points.country==con).order(-points.score).fetch(100)
        if leader==[]:
            pass
        else:
            lenfetch=len(leader)
            for i in range(0,lenfetch):
                ani=dict(rank=i+1,name=leader[i].name,points=leader[i].score)
                leaders.append(ani)
        self.response.write(template.render(l=leaders))
                
            
class lotwin(webapp2.RedirectHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('html/lotwinner.html')
        usa = []
        query = lotdetails.query().filter()
        
        if query is None:
            pass
        else:
            qs = query.fetch(10)
            a = len(qs)
            for i in range(0, a):
                an_item = dict(date=qs[i].date, email=qs[i].winneremail)
                usa.append(an_item)

        self.response.write(contenttemplate(self, template.render(users=usa), 0))

        pass


class spin(webapp2.RequestHandler):
    def get(self):
        self.response.write(contenttemplate(self, "spin", 1))


class spinwinner(webapp2.RequestHandler):
    def get(self):
        d = cidvalidation(self.request.cookies.get('cid'))
        if d == False:
            self.redirect('./')
        else:
            ema = cidvalidation(self.request.cookies.get('cid'))

            a = [ 0.5,3, 0, 2, 0, 1, 0, 0]
            randomnumber = randint(0, 7)
            s = moneydetails()
            ema = cidvalidation(self.request.cookies.get('cid'))
            if ema is False:
                self.response.write("-1")

            else:
                s.add(ema, "Money Received from spin ", a[randomnumber])
                self.response.write(randomnumber)


class Rec(webapp2.RequestHandler):
    def post(self):
        f = self.request.get('password')
        f1 = self.request.get('word')

        mobile = self.request.get('mob')
        name = self.request.get('nuser')
        email = self.request.get('email')

        if f != f1 or not (mobile.isdigit()) or (not email.count('@') == 1) or not ( email.count('.') == 1):
            self.redirect('./register')

        people = users(id=email)
        people.mobile = mobile
        people.email = email
        people.name = name
        people.password = f
        people.put()

        mon = money(id=email)
        mon.email = email
        mon.money = '10'
        mon.put()
        body = 'Confirm your account using the link below'
        f = open('html/aftersignup.html')
        s = f.read()
        self.response.write(s)

#('/signup',Rec),('/sigd',Sigd)
app = webapp2.WSGIApplication([
                                  ('/', MainHandler), ('/leadersboard',leader),('/lotwinners', lotwin),('/mouse',mouse),('/mousehandle',mousehandler), ('/spinselect', spinwinner),
                                  ('/spin', spin), ('/initial', ntial), ('/selectlotwinner', selectlotwinner),
                                  ('/register', Sign), ('/signup', Rec), ('/lot', lot), ('/sigd', Sigd),
                                  ('/sign', signe), ('/here', my), ('/edit', ed), ('/exit', poyi), ('/mymoney', msd)],
                              debug=True)
