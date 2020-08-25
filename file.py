from flask import Flask
from pyresparser import ResumeParser
from simple_salesforce import Salesforce
from pyresparser import ResumeParser
import requests
import os
import json

app = Flask(__name__)
 
 
@app.route('/<id>')
def hello_world(id):
   sf = Salesforce(
   username='targetrecruitsalesforce@talan.com', 
   password='oumawejouma11', 
   security_token='CQxJHyrAmFoBXBsI31XNnoYD')
   sessionId = sf.session_id
   instance = sf.sf_instance
   print ('sessionId: ' + sessionId)
   #r = requests.get("https://vast-escarpment-63477.herokuapp.com/")
   #print(r.content)
   attachment = sf.query("SELECT Id, Name,ParentId FROM Attachment where Id='" + id + "' LIMIT 1")
   #SELECT Id, Name, Body ,ParentId, Parent.Type FROM Attachment where Parent.Type = 'Contact'
   filename=attachment['records'][0]['Name']
   fileid=attachment['records'][0]['Id']
   fileparentid=attachment['records'][0]['ParentId']
   print('filename: ' + filename)
   print('fileid: ' + fileid)
   response = requests.get('https://' + instance + '/services/data/v39.0/sobjects/Attachment/' + fileid + '/body',
                           headers = { 'Content-Type': 'application/text', 'Authorization': 'Bearer ' + sessionId })

   f1 = open(filename, "wb")
   f1.write(response.content)
   f1.close()
   print('output file: '  + os.path.realpath(f1.name))
   response.close()
   data = ResumeParser(os.path.realpath(f1.name)).get_extracted_data()
   # Parse JSON into an object with attributes corresponding to dict keys.
   cand_dict=json.dumps(data)
   print(cand_dict)
   x = json.loads(cand_dict)

   #print (x["name"])
   class candidate:
     def __init__(self, name, email,skills):
       self.name = name
       self.email = email
       self.skills = skills

   c1 = candidate(x["name"], x["email"],x["skills"])
   print(c1.name)
   print(c1.email)
   print(c1.skills)

   a=json.dumps(c1.name)
   a =a.replace('"', '')

   c=json.dumps(c1.email)
   c =c.replace('"', '')
   c=c.lstrip()
   c=c.lstrip()
   print (c)
   b=json.dumps(c1.skills)
   b =b.replace('"', '')
   b =b.replace('[', '')
   b =b.replace(']', '')
  
   #sf.Contact.create({'LastName':a,'Email':c, 'Skills__c':b,'Record_Typess__c':'Candidat'})
   sf.Contact.update(fileparentid,{'Skills__c':b})
   return b
 
if __name__ == '__main__':
 app.run() 
