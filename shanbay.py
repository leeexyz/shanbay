
import sys
import requests
import time
import random

login_url = 'https://www.shanbay.com/accounts/login/'
news_url = 'https://www.shanbay.com/api/v1/read/article/news/'
checkin_url = 'http://www.shanbay.com/api/v1/checkin/?for_web=true'

username = sys.argv[1]
password = sys.argv[2]

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',}

s = requests.session()

csrftoken = s.get(login_url).cookies['csrftoken']

print 'Get csrf...'
print 'csrftoken', csrftoken

login_data = {'username': username,
              'password': password,
              #'userid': userid,
              'csrfmiddlewaretoken': csrftoken,}

r = s.post(login_url, data=login_data, headers=headers)
print 'Login successful...'
print requests.utils.dict_from_cookiejar(s.cookies)

auth_token = s.cookies['auth_token']
sessionid = s.cookies['sessionid']
userid = s.cookies['userid']

response = s.get(news_url, data=login_data, headers=headers)
json_r = response.json()

i = 0

if json_r['status_code'] == 0:

   news = json_r['data']['articles']

   for new in news:
       print '--------------'
       if i >= 2:
           checkin_r = s.post(checkin_url, headers = headers) 
           checkin_json = checkin_r.json() 
           print "return mgs is :", checkin_json['data']
           break
       if new['finished']:
           print "Readed..."
           continue

       newid = str(new['id'])

       min_used_seconds = str(new['min_used_seconds'] + random.randint(60,120))

       read_data = {'operation': 'finish',
                    'used_time': min_used_seconds,}
       read_url = 'http://www.shanbay.com/api/v1/read/article/user/' + newid + '/'

       print "reading url is : "
       print read_url
       read_r = s.put(read_url, read_data, headers=headers)
       print read_r, read_r.text
       if read_r.json()['status_code'] == 0:
           i += 1
           print 'Finnish reading.'
           time.sleep(3)
       else:
           print 'Reading failed.'
