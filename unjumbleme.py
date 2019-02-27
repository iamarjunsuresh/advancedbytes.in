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
import datetime
from _random import Random
from random import random
from setuptools.command.egg_info import overwrite_arg
from email import email
from random import randint

class openhashes(ndb.Model):
    hash=ndb.IntegerProperty()
    expiry=ndb.DateTimeProperty()
class userbase(ndb.Model):
    name=ndb.StringProperty()
    mobileno=ndb.StringProperty()
    deviceid=ndb.IntegerProperty()
    uuid=ndb.StringProperty()
    country=ndb.StringProperty()
class points(ndb.Model):
    score=ndb.IntegerProperty()
    deviceid=ndb.IntegerProperty()
    name=ndb.StringProperty()
    country=ndb.StringProperty()
    ver=ndb.StringProperty()
class usercount(ndb.Model):
    count=ndb.IntegerProperty()   
    
#class quesnow(ndb.model):
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=False)

def exi(self,h):
    s=openhashes.query(openhashes.hash==h)
    ni=s.fetch(1)
    if ni==[]:
        return False
    else:
        return True
    
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("hello")
class getdeviceid(webapp2.RequestHandler):
    def get(self):
        user = self.request.get('name')
        passw = self.request.get('mobileno')
        uuid=self.request.get('uid')
        country=self.request.get('cntry')
        a=usercount.query().fetch(1)
        if a==[]:
            deviceid=1
            ab=usercount(count=1)
            ab.put()
        else:
            deviceid=a[0].count+1
            a[0].count=deviceid
            a[0].put()
        
        users=userbase()
        users.name=user
        users.mobileno=passw
        users.uuid=uuid
        users.country=country
        users.deviceid=deviceid
        users.put()
        
        self.response.write(deviceid)
class score(webapp2.RequestHandler):   
    def get(self):
        h=self.request.get('h')
        score=self.request.get('score')
        auth=self.request.get('auth')
        deviceid=self.request.get('device')
        version=self.request.get('ver')
        #self.response.write(auth+deviceid+score+'arjunsuresh')
        if exi(self,int(auth))==False:
            self.response.write("Score submission unsuccessful");
            return
            
        fetchedquery=openhashes.query(openhashes.hash==int(auth)).fetch(1)
        if fetchedquery[0].expiry<datetime.datetime.now():
            self.response.write("Score submission unsuccessful");
            return
        hasha=hashlib.sha256(auth+deviceid+score+'arjunsuresh')
        if hasha.hexdigest()!=h:
            self.response.write("Score submission unsuccessful");
            return
        if version=='1.4.0.0':
            self.response.write('Sorry try updating the app');
            return
            
        fetchs=points().query(points.deviceid==int(deviceid)).fetch(1)
        if fetchs==[]:
		    submit=points()
        else:
            submit=fetchs[0]
        submit.score=int(score)
        submit.deviceid=int(deviceid)
        fetchuser=userbase().query(userbase.deviceid==int(deviceid)).fetch(1)
        submit.name=fetchuser[0].name
        submit.country=fetchuser[0].country
        submit.ver=version
        submit.put()
        self.response.write("score submitted. See leadersboard");
            
            
class leadersboard(webapp2.RequestHandler):
    def get(self):
        #template=JINJA_ENVIRONMENT.get_template('html/leader.html')
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
        self.response.write(json.dumps(leaders))	
        
class auth(webapp2.RequestHandler):
    def get(self):
        openhash=openhashes()
        k=randint(0,10000)
        openhash.hash=k
        openhash.expiry=datetime.datetime.now()+datetime.timedelta(seconds=600)
        openhash.put()
        
        self.response.write(k)

app = webapp2.WSGIApplication([
                                  ('/app', MainHandler),('/app/auth',auth),('/app/register',getdeviceid),('/app/score',score),('/app/leadersboard',leadersboard)],
                              debug=True)