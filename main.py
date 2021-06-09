import os, random, sys, time
# from urllib.parse import urlparse
from selenium import webdriver
from bs4 import BeautifulSoup
import pdb
import re
browser = webdriver.Chrome('driver/chromedriver.exe')
browser.get('https://www.linkedin.com/login')
browser.maximize_window()
file = open('config.txt')
lines = file.readlines()
username = lines[0]
password = lines[1]
elementID = browser.find_element_by_id('username')
elementID.send_keys(username)
elementID = browser.find_element_by_id('password')
elementID.send_keys(password)
elementID.submit()
visitingProfileID = '/my-items/posted-jobs/'
fullLink = 'https://www.linkedin.com' + visitingProfileID
browser.get(fullLink)
visitedProfiles = []
profilesQueued = []
time.sleep(5)
job_list = browser.find_elements_by_class_name('reusable-search__result-container')
for items in job_list:
    # import pdb;pdb.set_trace()
    # job_post = items.find_element_by_class_name('entity-result')
    # print (job_post.text)
    items.click()
    time.sleep(5)
    applicant_list = browser.find_elements_by_class_name('hiring-applicants__list-item')
    for applicant in applicant_list:
        with open('candidate_list.txt', 'a') as fopen:
            applicant.click()
            # pdb.set_trace()
            rating = browser.find_elements_by_class_name('hiring-rating-dropdown__good-fit')
            if not rating:
                continue
            applicant_name = applicant.text.split('\n')[0]
            time.sleep(2)
            # more_button = browser.find_element_by_class_name('hiring_applicant_more').click()
            more_button = browser.find_element_by_xpath('//*[contains(@data-control-name,"hiring_applicant_more")]')
            more_button.click()
            time.sleep(2)
            try:
                applicant_details_hidden = browser.find_element_by_class_name('artdeco-dropdown__content-inner').text
            except:
                print('exception occurred')
            email_re = re.compile('.*Email applicant at (.*)')
            phone_re = re.compile('Copy phone number (.*) to clipboard')
            email_id = email_re.findall(applicant_details_hidden)[0]
            phone_num = phone_re.findall(applicant_details_hidden)[0]
            try:
                browser.find_element_by_xpath('//*[contains(@data-control-name,"hiring_applicant_resume_pdf_download")]').send_keys('\n')
                time.sleep(5)
                resume_status = 'Yes'
            except:
                resume_status='No'
            fopen.write('Name:{0} Email:{1} Mobile:{2} Resume:{3}\n'.format(str(applicant_name),
                                                                            str(email_id), str(phone_num), str(resume_status)))
        # print(applicant_details_hidden.text)
print('script complete')
