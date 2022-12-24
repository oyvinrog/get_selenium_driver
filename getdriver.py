"""


Every time Chrome is updated, the chromedriver must be updated as well. That is a pain in the **.
Also, when you upgrade Python, you must download the chromedriver again. That is also a pain in the **.

This script will get the Windows chromedriver for Chrome. No need to download it manually

Example of use:

    import getdriver
    
    getdriver.get_chromedriver()

Note: This script will only work on Windows. It will not work on Linux or Mac.


"""

import os
import winreg
import zipfile
import sys

from selenium import webdriver
import requests
from bs4 import BeautifulSoup

def get_python_root():
    """Get Python installation folder"""
    # get python installation folder. 
    # we will add the chromedriver to the python scripts folder, because that is already in PATH
    python_root = os.path.join( sys.exec_prefix,"scripts")
    return python_root


def get_chromedriver():
    """Get the Windows chromedriver for chrome. No need to download it manually"""
    # abort if chromedriver.exe is already in the folder
    

    # Get python installation folder. We will move the executable there
    root_folder = get_python_root()
    # create the folder if it does not exist
    if not os.path.isdir(root_folder):
        os.mkdir(root_folder)
        print("Created folder",root_folder)
    
    # create full_path_exe with root folder, BIN and chromedriver.exe
    full_path_exe = os.path.join(root_folder,"chromedriver.exe")

    if os.path.isfile(full_path_exe):
        print("chromedriver.exe already exists")
        return "chromedriver.exe"

    # get chromedriver.exe from https://chromedriver.chromium.org/downloads
    # and put it in the same folder as this file
    # download the latest chrome driver and unzip
    # put the chromedriver.exe in the same folder as this file

    response = requests.get("https://chromedriver.chromium.org/downloads")
    # get version of chrome on this machine
    # https://stackoverflow.com/questions/33225947/can-a-python-script-get-chrome-browser-version-number

    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r"Software\Google\Chrome\BLBeacon")
    version = winreg.QueryValueEx(key, "version")[0]
    major_version = version.split(".")[0]

    print(f"Your version of chrome is {version} and the major version is {major_version}")
    print(f"Getting the latest chromedriver version for chrome version {major_version}")
    # get the latest chromedriver version
    soup = BeautifulSoup(response.text, 'html.parser')
    # find the matching version
    no_link_found = True
    for link in soup.find_all('a'):

        if f"ChromeDriver {major_version}" in link.text:
            print(link.get('href'))
            no_link_found = False
            # append chromedriver_win32.zip to the link, and remove "index.html?path="
            link = link.get('href').replace("index.html?path=","") + "chromedriver_win32.zip"
            
            # download the file
            r = requests.get(link, allow_redirects=True)
            
            full_path_zip = os.path.join(root_folder,"chromedriver_win32.zip")
            open(full_path_zip, 'wb').write(r.content)
            # unzip the file, and move it to the same folder as this file
            with zipfile.ZipFile(full_path_zip, 'r') as zip_ref:
                zip_ref.extractall(root_folder)
                

            # delete the zip file
            os.remove(full_path_zip)

            print("chromedriver.exe downloaded and unzipped to " + full_path_exe)

            break

    if no_link_found:
        print("No chromedriver found for your version of chrome. Please download the latest chromedriver from https://chromedriver.chromium.org/downloads and put it in the same folder as this file")
        exit()


if __name__ == "__main__":
    get_chromedriver()
