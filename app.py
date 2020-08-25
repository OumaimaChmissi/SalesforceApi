import flask
from flask import request
from pyresparser import ResumeParser
from simple_salesforce import Salesforce
from pyresparser import ResumeParser
import requests
import os
import json


sf = Salesforce(
username='targetrecruitsalesforce@talan.com', 
password='oumawejouma1', 
security_token='P6Hzo0iT1QZdApEdQ6joV9ZrZ')
sessionId = sf.session_id
instance = sf.sf_instance
print ('sessionId: ' + sessionId)

attachment = sf.query("SELECT Id, Name, Body FROM Attachment where Name='output_2.pdf'  LIMIT 1")
#SELECT Id, Name, Body ,ParentId, Parent.Type FROM Attachment where Parent.Type = 'Contact'

filename=attachment['records'][0]['Name']
fileid=attachment['records'][0]['Id']
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
 
print(b)


    

#sf.Contact.create({'LastName':a,'Email':c, 'Skills__c':b,'Record_Typess__c':'Candidat'})


app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def home():
     
        return  a
   
