import requests 
from bs4 import BeautifulSoup
import time
from urllib3.exceptions import InsecureRequestWarning
import datetime


username = ''
password = ''

login_url = 'https://agnigarh.iitg.ac.in:1442/login?a'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Connection": "close"
}

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def logout(session):
    session.get('https://agnigarh.iitg.ac.in:1442/logout?030403030f050d06',verify=False)
    print("[*] Logged out!..")

def login(session, login_url, username, password):
    response = session.get(login_url, headers=headers,verify=False)
    
    soup = BeautifulSoup(response.text, 'html.parser')  

    magic = soup.find('input', attrs={'name':'magic'})['value']
    redirect_url = soup.find('input', {'name':'4Tredir'})['value']

    login_data = {
        '4Tredir': redirect_url,
        'magic': magic,
        'username': username, 
        'password': password
    }
    
    response = session.post(login_url, data=login_data, headers=headers,verify=False)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    keepalive_url = soup.find('script').text.split('"')[1]
    
    return session, keepalive_url

def keepalive_session(session, keepalive_url):
    try:
        while True:
            response = session.get(keepalive_url, headers=headers,verify=False)
            print("[*] Auto-refreshed")
            time.sleep(10)
    except KeyboardInterrupt:
        print("[*] Logging Out!!")
        logout(session)
        exit()
    except requests.exceptions.ConnectionError:
        print("[*] Connection  Error!!")
        logout(session)
    except:
        pass
    


curtime = datetime.datetime.now()
while True:
    time.sleep(1)
    diff = (datetime.datetime.now()- curtime).total_seconds()
    print(diff)
    session = requests.Session() 
    session, keepalive_url = login(session, login_url, username, password)
    keepalive_session(session, keepalive_url)
    if diff > 10:
        print("AWAKEEEEE")
        logout(session)
        session = requests.Session() 
        session, keepalive_url = login(session, login_url, username, password)
        keepalive_session(session, keepalive_url) 
        
    curtime = datetime.datetime.now()

