from django.test import TestCase

# Create your tests here.

myurl = 'http://134.64.116.90:8101/smartservice/get.login?c=msgPushService&m= getAppToken'
import requests
r = requests.get(myurl)
print(r)