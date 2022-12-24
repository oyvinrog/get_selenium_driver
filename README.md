# get_selenium_driver

This script will make sure to set up the Selenium Chrome driver automatically for your Python code. No more worries about Python being upgraded or Chrome version being changed. chromedriver.exe will also be added to the scripts folder on Python Home. Which means that you don't have to add it to your PATH.

Example of use:

    import getdriver
    
    getdriver.get_chromedriver()

Note: This script will only work on Windows. It will not work on Linux or Mac.
