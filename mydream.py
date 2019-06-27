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
import os
import jinja2
from google.appengine.ext import ndb
import urllib2
import xml.etree.ElementTree as ET
import re
from google.appengine.api import mail
from google.appengine.api.mail import EmailMessage
import pyjade;
import json


class somedata(ndb.Model):
    data=ndb.StringProperty()
class pointerxy(ndb.Model):
    ip=ndb.StringProperty()
    date=ndb.DateTimeProperty(auto_now_add=True)
    x=ndb.IntegerProperty()
    y=ndb.IntegerProperty()
class gatescore(ndb.Model):
    rollno=ndb.StringProperty()
    branch=ndb.StringProperty()
    mark=ndb.FloatProperty()
    nodehtml=ndb.TextProperty()
    date=ndb.DateTimeProperty(auto_now_add=True)

class articles(ndb.Model):
    title=ndb.StringProperty()
    entry=ndb.TextProperty()
    date=ndb.DateTimeProperty(auto_now_add=True)
    link=ndb.StringProperty()
    id=ndb.StringProperty()

class google_feedback(ndb.Model):
    title=ndb.StringProperty()
    feed=ndb.StringProperty()
    email=ndb.StringProperty()
    date=ndb.DateProperty(auto_now_add=True)
class messagetouser(ndb.Model):
	message=ndb.StringProperty()
	date=ndb.DateProperty(auto_now_add=True)

class gsdp_downloads(ndb.Model):
    version=ndb.StringProperty()
    tmode=ndb.StringProperty()
    ua=ndb.StringProperty()
class linkcount(ndb.Model):
	count=ndb.IntegerProperty()

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape','pyjade.ext.jinja.PyJadeExtension'],
    autoescape=False)
def getusermessage():
	messtr=''
	mes=messagetouser.query().order(-messagetouser.date).fetch(10)
	for i in range(0,len(mes)):
		messtr=messtr+mes[i].message+"</br>"
	messtr='<span style="color:red;">'+ messtr+'</span>'

	return messtr


class homepage(webapp2.RequestHandler):
    def get(self):
        ua=self.request.headers.get('User-Agent')
        if ismobile(ua)==False:
            temp = JINJA_ENVIRONMENT.get_template('html/pc-homepage.html')
            self.response.write(temp.render(message=getusermessage()))
        else:
            temp = JINJA_ENVIRONMENT.get_template('html/mobile-home.html')
            self.response.write(temp.render())
'''
	 #upload_post("sample", "good morning",'1')
        temp=JINJA_ENVIRONMENT.get_template('html/homepage.html')
        articlearray=articles.query().order(-articles.date).fetch(10);
        template_values=[]
        if articlearray==[]:
            pass
        else:
            for i in range(0,len(articlearray)):
                stri=articlearray[i].entry
                #stri=stri[:500]
                dict_obj=dict(heading=articlearray[i].title,entry=stri,link=articlearray[i].link)
                template_values.append(dict_obj)


        self.response.write(temp.render(posts=template_values))
'''
def render_jade(kk,content):
        template=JINJA_ENVIRONMENT.get_template("html/pc-base.jade")
        kk.response.write(template.render())
class addmessageclass(webapp2.RequestHandler):
	def get(self):
		mestr=self.request.get('str')
		messnode=messagetouser()
		messnode.message=mestr
		messnode.put()

class sendmail(webapp2.RequestHandler):
    def get(self):
	em=EmailMessage(sender='Admin<'+self.request.get('semail')+'>',to="User<"+self.request.get('remail')+">",        subject=self.request.get('sub'),html=self.request.get('body'))
	em.send()

class listpage(webapp2.RequestHandler):
    def get(self):
        #upload_post("sample", "good morning",'1')
        temp=JINJA_ENVIRONMENT.get_template('html/articleslist.html')
        articlearray=articles.query().fetch(100);
        template_values=[]
        if articlearray==[]:
            pass
        else:
            for i in range(0,len(articlearray)):
                dict_obj=dict(link=articlearray[i].link,title=articlearray[i].title)
                template_values.append(dict_obj)


        self.response.write(temp.render(links=template_values))

class articlepage(webapp2.RequestHandler):
    def get(self):
        id=self.request.get('id')
        temp=JINJA_ENVIRONMENT.get_template('html/articlemain.html')
        articlearray=articles.query().filter(articles.link==id).fetch(1);
        template_values=[]
        if articlearray==[]:
            self.error(404)
        else:
            template_values={'heading':articlearray[0].title,'entry':articlearray[0].entry}
            self.response.write(temp.render(post=template_values))
class admin(webapp2.RequestHandler):
    def get(self):
        id=self.request.get('id')
        temp=JINJA_ENVIRONMENT.get_template('html/admin.html')
        self.response.write(temp.render())
    def post(self):
    	if(self.request.get('user')=='arjun' and self.request.get('password')=="trilon258"):
    	    template=JINJA_ENVIRONMENT.get_template('html/admin_edit.html')
    	    response=urllib2.urlopen("http://www.yashveer.heck.in/rss.xml")

    	    xml=ET.fromstring(response.read())
    	    items = []
            for i in range(4,13):
                n_item = dict(title=xml[0][i][0].text,content=xml[0][i][3].text,ind=str(i),dat=xml[0][i][2].text)
                items.append(n_item)
            self.response.write(template.render(posts=items))
class downloadclass(webapp2.RequestHandler):
    def get(self):
        ua = self.request.headers.get('User-Agent')
        if ismobile(ua) == True:
            temp = JINJA_ENVIRONMENT.get_template('html/mobile-download.html')
            self.response.write(temp.render())
        else:
            template = JINJA_ENVIRONMENT.get_template('html/pc-download.html')
            self.response.write(template.render(message=getusermessage()))

def ismobile(ua):
    reg_b = re.compile("(android|bb\\d+|meego).+mobile|avantgo|bada\\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\\.(browser|link)|vodafone|wap|windows ce|xda|xiino",re.I | re.M)
    reg_v = re.compile("1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\\-(n|u)|c55\\/|capi|ccwa|cdm\\-|cell|chtm|cldc|cmd\\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\\-s|devi|dica|dmob|do(c|p)o|ds(12|\\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\\-|_)|g1 u|g560|gene|gf\\-5|g\\-mo|go(\\.w|od)|gr(ad|un)|haie|hcit|hd\\-(m|p|t)|hei\\-|hi(pt|ta)|hp( i|ip)|hs\\-c|ht(c(\\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\\-(20|go|ma)|i230|iac( |\\-|\\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\\/)|klon|kpt |kwc\\-|kyo(c|k)|le(no|xi)|lg( g|\\/(k|l|u)|50|54|\\-[a-w])|libw|lynx|m1\\-w|m3ga|m50\\/|ma(te|ui|xo)|mc(01|21|ca)|m\\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\\-2|po(ck|rt|se)|prox|psio|pt\\-g|qa\\-a|qc(07|12|21|32|60|\\-[2-7]|i\\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\\-|oo|p\\-)|sdk\\/|se(c(\\-|0|1)|47|mc|nd|ri)|sgh\\-|shar|sie(\\-|m)|sk\\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\\-|v\\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\\-|tdg\\-|tel(i|m)|tim\\-|t\\-mo|to(pl|sh)|ts(70|m\\-|m3|m5)|tx\\-9|up(\\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\\-|your|zeto|zte\\-",re.I | re.M)
    b = reg_b.search(ua)
    v = reg_v.search(ua[0:4])
    if b or v:
        return True
    else:
        return False
class google_suggestion(webapp2.RequestHandler):
    def get(self):
        ua=self.request.headers.get('User-Agent')
        if ismobile(ua)==False:
            temp = JINJA_ENVIRONMENT.get_template('html/pc-suggestion.html')
            self.response.write(temp.render())
        else:
            temp = JINJA_ENVIRONMENT.get_template('html/mobile-suggestion.html')
            self.response.write(temp.render())

    def post(self):
        nod=google_feedback()
        nod.title=self.request.get('fb_title')
        nod.feed=self.request.get('fb_feed')
	nod.email=self.request.get('fb_email')
        mail.send_mail(sender='Arjun Suresh<123arjunsuresh@gmail.com>',to="Arjun Suresh <123arjunsuresh@gmail.com>",          subject="Addon Suggestion from user",body='Dear arjun,'+'\n'+nod.title+'\n from '+nod.email+'\n\n\n'+nod.feed);
        nod.put()
        self.redirect("/")
class install_version(webapp2.RequestHandler):


    def get(self):
        if self.request.get('ver') and self.request.get('tmode'):
            node=gsdp_downloads();
            node.version=self.request.get('ver')
            node.tmode=self.request.get('tmode')
            node.ua=self.request.headers.get('User-Agent')
            node.put()
        ua = self.request.headers.get('User-Agent')
        if ismobile(ua) == True:
            temp = JINJA_ENVIRONMENT.get_template('html/mobile-changelog.html')
            self.response.write(temp.render())
        else:
            temp = JINJA_ENVIRONMENT.get_template('html/pc-version.html')
            self.response.write(temp.render(message=getusermessage()))

class screenshot(webapp2.RequestHandler):
    def get(self):
        ua = self.request.headers.get('User-Agent')
        if ismobile(ua)==True:
            temp = JINJA_ENVIRONMENT.get_template('html/mobile-screenshot.html')
            self.response.write(temp.render())
        else:
            temp = JINJA_ENVIRONMENT.get_template('html/pc-screenshot.html')
            self.response.write(temp.render(message=getusermessage()))
class dsu_main(webapp2.RequestHandler):
    def get(self):
        file=open("html/dsumain.html")
        html=file.read()
        self.response.write(html)
class jayalakshmi(webapp2.RequestHandler):
	def get(self):
		file=open("html/jaya2017.html")
		html=file.read()
		self.response.write(html)

class crithothegame(webapp2.RequestHandler):
    def get(self):
    	html=open("html/crithogame.html")
    	self.response.write(html.read())

class plotscatter(webapp2.RequestHandler):
    def get(self):
    	html=open("html/plot.html")
    	self.response.write(html.read())

class admin_edit(webapp2.RequestHandler):
    def post(self):
        title=self.request.get('title')
        content=self.request.get('content')
        id=self.request.get('date')
        que=linkcount.query().fetch(1)
        if que==[]:
            linkco=linkcount()
            linkco.count=11
            linkco.put()
            link=10
        else:
            link=que[0].count
            que[0].count=que[0].count+1
            que[0].put()
        upload_post(title, content, link, id)
class geturl(webapp2.RequestHandler):
    def get(self):
	import urllib2
	response = urllib2.urlopen(self.request.get('url'))
	html = response.read()
	self.response.write(html)
class gate2018(webapp2.RequestHandler):
    def get(self):
		self.response.headers['Access-Control-Allow-Origin'] = '*'
		self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
		self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
		html=open("html/gate2018/index.php")
    		self.response.write(html.read())
class pointerclass(webapp2.RequestHandler):
    def get(self):
        html=open("html/pointer.html")
        self.response.write(html.read())


class pointerapiclass(webapp2.RequestHandler):
    def get(self):
        if self.request.get('get')=="true":
            res=[{"x":zz.x,"y":zz.y} for zz in pointerxy.query().fetch()]
            #res=[x;x.date=str(x.date) for x in res]
            self.response.write(json.dumps(res))
        else:
            x=self.request.get('x')
            y=self.request.get('y')
            prevrec=pointerxy.query(pointerxy.ip==self.request.remote_addr).fetch()
            if(len(prevrec)==0):
                pn=pointerxy()
                pn.x=int(x)
                pn.y=int(y)
                pn.ip=self.request.remote_addr
                pn.put()
            else:
                prevrec[0].x=int(x)
                prevrec[0].y=int(y)
                prevrec[0].put()

class adtxt(webapp2.RequestHandler):
    def get(self):
        self.response.write("google.com, pub-7934673545282018, DIRECT, f08c47fec0942fa0")
class gate2018logmarks(webapp2.RequestHandler):
	def post(self):
		branch=self.request.get('branch')
		mark=float(self.request.get('mark'))
		sc=gatescore()
		idd=self.request.get('id')
		sc.branch=branch
		sc.mark=mark
		sc.nodehtml=self.request.get('ans')
		sc.rollno=idd
		sc.put()






def upload_post(title,content,link,id):
    if articles.query().filter(articles.id==id).fetch(1)==[]:
        article=articles()
        article.title=title
        article.entry=content
        article.link=str(link)
        article.id=id
        article.put()
#('/signup',Rec),('/sigd',Sigd)
app = webapp2.WSGIApplication([
                                  ('/', homepage)
                                  ,('/plot',plotscatter),('/suggest',google_suggestion),('/sendmail',sendmail),('/addmessage',addmessageclass),('/version',install_version),('/crithogamev2',crithothegame),('/screenshot',screenshot),('/pointer',pointerclass),('/pointerapi',pointerapiclass),('/download',downloadclass),('/article',articlepage),('/articles',listpage),('/admin',admin),('/geturl',geturl),('/gate2018/',gate2018),('/gate2018',gate2018),('/gate2018logmark/',gate2018logmarks),('/admin_edit',admin_edit),('/dsu/',dsu_main)],
                              debug=True)
