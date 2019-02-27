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

class balance_openhashes(ndb.Model):
    hash=ndb.IntegerProperty()
    expiry=ndb.DateTimeProperty()
class balance_userbase(ndb.Model):
    name=ndb.StringProperty()
    mobileno=ndb.StringProperty()
    deviceid=ndb.IntegerProperty()
    uuid=ndb.StringProperty()
    country=ndb.StringProperty()
class balance_points(ndb.Model):
    score=ndb.IntegerProperty()
    deviceid=ndb.IntegerProperty()
    name=ndb.StringProperty()
    country=ndb.StringProperty()
    ver=ndb.StringProperty()
    mode=ndb.StringProperty()
class balance_usercount(ndb.Model):
    count=ndb.IntegerProperty()   
    

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=False)

def exi(self,h):
    s=balance_openhashes.query(balance_openhashes.hash==h)
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
        a=balance_usercount.query().fetch(1)
        if a==[]:
            deviceid=1
            ab=balance_usercount(count=1)
            ab.put()
        else:
            deviceid=a[0].count+1
            a[0].count=deviceid
            a[0].put()
        
        users=balance_userbase()
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
        m=self.request.get('mode')
        #self.response.write(auth+deviceid+score+'arjunsuresh')
        if exi(self,int(auth))==False:
            self.response.write("Score submission unsuccessful-openhash does not exist");
            return
            
        fetchedquery=balance_openhashes.query(balance_openhashes.hash==int(auth)).fetch(1)
        if fetchedquery[0].expiry<datetime.datetime.now():
            self.response.write("Score submission unsuccessful-openhash expired");
            return
       # hasha=hashlib.sha256(auth+deviceid+score+'arjunsureshbalance')
       # if hasha.hexdigest()!=h:
        #    self.response.write("Score submission unsuccessful-hash errror");
         #   return
       
            
        fetchs=balance_points().query(balance_points.deviceid==int(deviceid)).filter(balance_points.mode==m).fetch(1)
        if fetchs==[]:
		    submit=balance_points()
        else:
            submit=fetchs[0]
        submit.score=int(score)
        submit.deviceid=int(deviceid)
        fetchuser=balance_userbase().query(balance_userbase.deviceid==int(deviceid)).fetch(1)
        if fetchuser==[]:
            self.response.write("some error occured")
            return
        submit.name=fetchuser[0].name
        submit.country=fetchuser[0].country
        submit.ver=version
        submit.mode=m
        submit.put()
        self.response.write("score submitted. See leadersboard")
class checkexists(webapp2.RequestHandler):
    def get(self):
        con=self.request.get('did')
        fetchedq=balance_userbase.query(balance_userbase.uuid==con).fetch(1)
        if len(fetchedq)==0:
            self.response.write("-1")
        else:
            self.response.write(fetchedq[0].deviceid)
            fet=balance_points.query(balance_points.deviceid==fetchedq[0].deviceid).filter(balance_points.mode=="Normal").fetch(1)
            if len(fet)==0:
                self.response.write(",0,")
            else:
                self.response.write(","+str(fet[0].score)+",")
            fet=balance_points.query(balance_points.deviceid==fetchedq[0].deviceid).filter(balance_points.mode=="Inverted").fetch(1)
            if len(fet)==0:
                self.response.write("0")
            else:
                self.response.write(str(fet[0].score))
class leadersboard(webapp2.RequestHandler):
    def get(self):
        #template=JINJA_ENVIRONMENT.get_template('html/leader.html')
        #con=self.request.get('cntry')
        mod=self.request.get('mode')
        if mod=='':
            mod='Normal'

        leaders=[]
        leader=balance_points.query().filter(balance_points.mode==mod).order(-balance_points.score).fetch(100)
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
        openhash=balance_openhashes()
        k=randint(0,10000)
        openhash.hash=k
        openhash.expiry=datetime.datetime.now()+datetime.timedelta(seconds=600)
        openhash.put()
        
        self.response.write(k)

app = webapp2.WSGIApplication([
                                  ('/app/balance/', MainHandler),('/app/balance/auth',auth),('/app/balance/register',getdeviceid),('/app/balance/checkexists',checkexists),('/app/balance/score',score),('/app/balance/leadersboard',leadersboard)],
                              debug=True)
