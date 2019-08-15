import time
import ctypes, sys
from datetime import datetime as dt

#this
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
#asks for admin privileages when running the progrmam so I can alter the hosts file
if is_admin():
    # following variables hold the path to where I will make the change and the website that I want to block
    hosts_temp=r"C:\Users\un258\Documents\Demo\hosts"
    hosts_path=r"C:\windows\System32\drivers\etc\hosts"
    redirect = "127.0.0.1"
    website_list = ["www.facebook.com", "facebook.com"]

    #The script runs forever and blocks the website from 0 to 3 am
    while True:
        if dt.now() > dt(dt.now().year,dt.now().month,dt.now().day,0) and dt.now() < dt(dt.now().year,dt.now().month,dt.now().day,3):
            print("Working hours")
            #if it's 3, open the hosts file and write in the websites I wish to block into it
            with open(hosts_path,"r+") as file:
                content = file.read()
                for website in website_list:
                    if website not in content:
                        file.write(redirect + " " + website + "\n")
        #The following block will rewrite the hosts file but without the websites that we want to block
        #which effectively unblocks our websites
        else:
            #if its not 0 - 3 am then do the following
            print("Not working hours")
            #open the hosts file
            with open(hosts_path,"r+") as file:
                #read the lines from file and puts it into content in the form of a list
                content = file.readlines()
                file.seek(0)
                #check each line from text file that is now in our list
                for line in content:
                    #if the line does not contain any of the words listed in our website_list then write it in to hosts file
                    if not any(website in line for website in website_list):
                        #this writes only the lines that doesn't have the website
                        #thanks to file.seek, these new lines are written above the original
                        #the line pointer is now at end of the last written line
                        file.write(line)
                #truncate gets rid of everything after the line pointer, so it erases the original
                file.truncate()

        time.sleep(5)
#This
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
