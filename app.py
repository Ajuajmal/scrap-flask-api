from flask import Flask, request, jsonify,render_template

from bs4 import BeautifulSoup
import requests
import pickle
import boto3

import json
import os
from os import path
import re




LINKEDIN_MAIL = os.environ.get("LINKEDIN_MAIL")
LINKEDIN_PASSWORD = os.environ.get("LINKEDIN_PASSWORD")
S3_ACCESS_KEY = os.environ.get("S3_ACCESS_KEY")
S3_SECRET_KEY = os.environ.get("S3_SECRET_KEY")
S3_BUCKET = os.environ.get("S3_BUCKET")
S3_FILE_NAME = os.environ.get("S3_FILE_NAME")

app = Flask(__name__)


SERVER_ERROR = [{"server-error":"can't establish connection ,try again, after some time"}]
SERVER_ERROR_DATA = [{"server-error":"failed to fetch data, try again, after some time"}]

def connect_s3():
    s3_client = boto3.client('s3',aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY)

    return s3_client

def save_cookies(requests_cookiejar):
    s3_client = connect_s3()
    cookie_object=pickle.dumps(requests_cookiejar)
    upload_response = s3_client.put_object(
    Bucket= S3_BUCKET,
    Body=cookie_object,
    Key= S3_FILE_NAME
    )

def load_cookies():
    s3_client = connect_s3()
    try:
        cookie_req = s3_client.get_object(
    Bucket=S3_BUCKET,
    Key=S3_FILE_NAME)
        cookies = pickle.loads(cookie_req['Body'].read())
        return cookies
    except:
        return "nofiles"



def login_linkedin():
    client = requests.Session()
    HOMEPAGE_URL = 'https://www.linkedin.com'
    LOGIN_URL = 'https://www.linkedin.com/uas/login-submit'
    html = client.get(HOMEPAGE_URL).content
    soup = BeautifulSoup(html, "html.parser")
    try:
        csrf = soup.find('input', dict(name='loginCsrfParam'))['value']
    except:
        return "csrf :error"

    try:
        login_information = {
            'session_key':LINKEDIN_MAIL,
            'session_password':LINKEDIN_PASSWORD,
            'loginCsrfParam': csrf,
        }
        client.post(LOGIN_URL, data=login_information)
        save_cookies(client.cookies)
    except:
        return "login:error"
    return "success"

def scrapper(link,user_req_data):
    cookies = load_cookies()
    if cookies == "nofiles":
        login = login_linkedin()
        if login == "success":
            cookies = load_cookies()
        else:
            return(SERVER_ERROR)
    url = link
    html = requests.get(url,cookies=cookies)
    if not html.status_code == 200:
        login = login_linkedin()
        cookies = load_cookies()
        html = requests.get(url,cookies=cookies)
        if not login == "success" or not html.status_code == 200:
            return(SERVER_ERROR)
    soup = BeautifulSoup(html.content , "html.parser")
    data = soup.find_all('code')
    if data == []:
        return(SERVER_ERROR_DATA)
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
