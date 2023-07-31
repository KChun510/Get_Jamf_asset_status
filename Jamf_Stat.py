from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import csv



driver = webdriver.Chrome()
#You need to paste the url, to companys jamf server
driver.get("url-to-Jamf")
wait = WebDriverWait(driver, 10)




#This login function is used to get paste okta verify, you can delete "login()" function and sighn in mannually
def login():
	
	time.sleep(2)

	user = wait.until(EC.presence_of_element_located((By.ID, "input28"))).send_keys("user_name")
	
	pass_word = wait.until(EC.presence_of_element_located((By.ID, "input36"))).send_keys("your_pass")


	sighn_in_butt = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Sign in']"))).click()

	wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Select")))
	select_butts = driver.find_elements(By.LINK_TEXT, "Select") 
	
	select_butts[1].click()





def navigate():

	save_arr = []

	serial_numbs = parse_serial_numb()

	computers_butt = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='computers.html']"))).click()
	prestage_butt = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='computerEnrollmentPrestage.html']"))).click()
	"""
	DEP_US = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='computerEnrollmentPrestage.html?id=1&o=r']")))
	"""


	#DEP_US = driver.find_element(By.XPATH, "//a[@href='computerEnrollmentPrestage.html?id=1&o=r']")
	driver.get("https://jss.corp.creditkarma.com/computerEnrollmentPrestage.html?id=1&o=r")



	iframe = wait.until(EC.presence_of_element_located((By.XPATH ,"//iframe[@src='legacy/computerEnrollmentPrestage.html?id=1&o=r']")))
	driver.switch_to.frame(iframe)


	#scope = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='javascript:changeTab('COMPUTER_DEP_PRESTAGE_TAB_SCOPE')']"))).click()
	
	

	a_tags = driver.find_elements(By.TAG_NAME, 'a')
	scope_tag = a_tags[1]

	print(scope_tag.get_attribute("href"))

	wait.until(EC.element_to_be_clickable(scope_tag)).click()

	#search_button = driver.find_elements(By.TAG_NAME, 'input')
	search_button = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Filter Results']")))

	count = 1
	print(f"the len of {len(serial_numbs)}")
	for group in serial_numbs:
		print(f"{count} of {len(serial_numbs)} checked")
		count += 1
		print(f"This is the group serial {group}")
		if (group[0] == ''):
			save_arr.append('')
			
			index += 1
			continue
		else:
			tmp = ''
			text = []
			for single in group:
				for index in range(30):
					search_button.send_keys(Keys.BACK_SPACE)

				search_button.send_keys(single)

				time.sleep(.5)


				status = driver.find_elements(By.TAG_NAME, "td")



				time.sleep(.5)

				for word in status[2700:]:
					if(word.text):
						text += [word.text]


				
				for word in text:
					if (word == 'Not Assigned' or word == 'Assigned'):
						tmp += single + ' - ' + word + '                   '
						break
					elif(word == 'No matching records found'):
						tmp += single + ' - ' + 'Not Found' + '                   '
						break



			save_arr.append(tmp)

	return save_arr



def parse_serial_numb():
	serial_numbs = []
	with open('serial_numbs_test.csv', 'r' ,newline='') as csvfile:
	    user_csv = csv.reader(csvfile, delimiter=',', quotechar='|')
	    for row in user_csv:
	    	print(row)
	    	row = row[0].split('-')
	    	serial_numbs += [row]

	


	csvfile.close()
	return serial_numbs



def write_to_csv():
	serial_numbs = navigate()
	with open('jamf_output_test.csv', 'w' ,newline='') as csvfile:
		serial_numb_csv = csv.writer(csvfile, delimiter=',', quotechar='|')
		for strings in serial_numbs:
			serial_numb_csv.writerow([strings])




	

			
login()
write_to_csv()





driver.quit()
driver.close() 


