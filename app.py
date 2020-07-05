from flask import Flask, request, jsonify,render_template
import os

from bs4 import BeautifulSoup
import requests
import json

import re



LINKEDIN_MAIL = os.environ.get("LINKEDIN_MAIL")
LINKEDIN_PASSWORD = os.environ.get("LINKEDIN_PASSWORD")

app = Flask(__name__)

def scrapper(link,user_req_data):
    client = requests.Session()
    HOMEPAGE_URL = 'https://www.linkedin.com'
    LOGIN_URL = 'https://www.linkedin.com/uas/login-submit'
    html = client.get(HOMEPAGE_URL).content
    soup = BeautifulSoup(html, "html.parser")

    try:
        csrf = soup.find('input', dict(name='loginCsrfParam'))['value']
        login_information = {
            'session_key':LINKEDIN_MAIL,
            'session_password':LINKEDIN_PASSWORD,
            'loginCsrfParam': csrf,
        }
        client.post(LOGIN_URL, data=login_information)
        print("Login Successful")
    except:
        print("Failed to Login")
        return([{"server-error":"can't establish connection ,try again, after some time"}])
    url = link
    html = client.get(url).content
    print(html)
    soup = BeautifulSoup(html , "html.parser")
    data = soup.find_all('code')
    print(data)
    if data == []:
        return([{"server-error":"failed to fetch data, try again, after some time"}])
    found = False
    req_data = {}
    for element in data:
        json_object = element.get_text()
        try:
            dict_from_json = json.loads(json_object)
            if 'included' in dict_from_json.keys():
                for values in dict_from_json['included']:
                    if 'birthDateOn' in values.keys():
                        found = True
                        req_data = values
                        print('found at {pos}'.format(pos=data.index(element)))
                        break
            if found:
                break
        except:
            pass

    resp = [{}]
    if found:
        try:
            resp = [{
                user_req_data : req_data[user_req_data]
            }]
            print(req_data['firstName'])
            print(req_data['headline'])
            print(req_data['lastName'])
            print(req_data['summary'])
        except:
            pass
    return resp

@app.route('/api/v1/linkedin/', methods=('GET', 'POST'))
def respond():
    if request.method == 'POST':
        req_data = request.form['data']
        link = request.form['url']
        link_regex = re.compile('((http(s?)://)*([a-zA-Z0-9\-])*\.|[linkedin])[linkedin/~\-]+\.[a-zA-Z0-9/~\-_,&=\?\.;]+[^\.,\s<]')
        validate = link_regex.match(link)
        if validate is None:
            resp = [{
                "invalid_link" : link + "- please check your link one more time and try agian"
            }]
            return jsonify(resp)
        resp = scrapper(link,req_data)
        if resp == [{}]:
            resp = [{
                "No requested data found" : req_data + "- please try again with the keywords headline/firstName/lastName/summary"
            }]
        return jsonify(resp)

    return render_template('api.html')



if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
