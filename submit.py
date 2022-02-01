import os
from contextlib import redirect_stdout
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

#click safety
def click(ele):
	webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	ele.click()

#for selectBox
def select(path,s):
	global webdriver
	ele = webdriver.find_element_by_xpath(path)
	sle = Select(ele)
	sle.select_by_value(s)

def init():
	global webdriver
	options = Options()
	options.add_argument('--headless')
	options.add_argument('--disable-gpu')
	options.add_argument("--log-level=3")
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	try:
		webdriver = webdriver.Chrome(executable_path=r"C:\Users\yutak\program\AtcoderJudgeSystem\chromedriver.exe", chrome_options=options)
	except:
		pass
	webdriver.set_window_size(1000,1000)
	webdriver.get("https://atcoder.jp/login?continue=https%3A%2F%2Fatcoder.jp%2F")

	#getURL
	url = sys.argv[1]
	#url = 'https://atcoder.jp/contests/abc169/tasks/abc169_a'

	time.sleep(0.5)
	return url

def login():
	user = "user"
	password = "password"
	webdriver.find_element_by_xpath('//*[@id="username"]').send_keys(user)
	webdriver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
	loginButton = webdriver.find_element_by_xpath('//*[@id="submit"]')
	click(loginButton)
	time.sleep(1.5)

def getCode():
	#atcoder.py needs to exist in corrent directory
	with open("atcoder.py", mode="r", encoding='utf-8') as f:
		x = f.read()
	#print(x)
	return x.replace("\t","  ")

def submit(url,code):
	#init
	contestURL=url
	webdriver.get(contestURL)
	time.sleep(0.5)

	#select Programming Language
	try:
		select('//*[@id="select-lang"]/select',"4006")
	except:
		select('//*[@id="select-lang"]/select',"3023")

	#change editer
	editer = webdriver.find_element_by_xpath('//*[@id="main-container"]/div[1]/div[2]/form/div[2]/div[2]/p[2]/button')
	click(editer)
	#enter SourceCode
	textarea = webdriver.find_element_by_xpath('//*[@id="sourceCode"]/textarea')
	textarea.send_keys(code)
	#submit
	submitButton = webdriver.find_element_by_xpath('//*[@id="submit"]')
	click(submitButton)

def getRes():
	time.sleep(1)

	#result pass
	path = webdriver.find_elements_by_class_name("table-bordered")[0].find_elements(By.TAG_NAME,"tbody")[0].find_elements(By.TAG_NAME,"tr")[0].find_elements(By.TAG_NAME,"td")

	for i in range(1,100):
		path = webdriver.find_elements_by_class_name("table-bordered")[0].find_elements(By.TAG_NAME,"tbody")[0].find_elements(By.TAG_NAME,"tr")[0].find_elements(By.TAG_NAME,"td")
		#print(path[7].text)
		if path[7].text!="詳細":
			return path[6].text
		time.sleep(1)
	return "No Return"


def test():
	print(getCode())

def main():
	#init
	url = init()
	#init()

	#login
	login()

	#getSourceCode(formated)
	code = getCode()

	#enter and submit
	submit(url,code)

	res = getRes()
	print(res)
	#print("RESULT")

	webdriver.close()
	webdriver.quit()

main()

#x = submit.webdriver.find_element_by_xpath('//*[@id="main-container"]/div[1]/div[3]/div[2]/div[2]/table/tbody/tr[1]/td[7]/span')