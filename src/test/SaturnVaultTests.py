import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import unittest
import random
from selenium.common.exceptions import NoSuchElementException
import re



CHROMEDRIVER_PATH = '/Users/AggregateIQ/workspace/seng426/chromedriver'
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
# driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)
driver = webdriver.Chrome(CHROMEDRIVER_PATH)

url = "http://localhost:8003"
account_u = "p.soell@saturn.com"
account_p = "stickman123"

def input_credentials(s, u, p):
	if s:
		driver.find_element_by_name("site").clear()
		driver.find_element_by_name("site").send_keys(s)
	if u:
		driver.find_element_by_name("login").clear()
		driver.find_element_by_name("login").send_keys(u)
	if p:
		driver.find_element_by_name("password").clear()
		driver.find_element_by_name("password").send_keys(p)

def tick_boxes(lower, upper, digits, special, repeat):
	if lower == 0:
		click_id("field_lower")
	if upper == 0:
		click_id("field_upper")
	if digits == 0:
		click_id("field_digits")
	if special == 0:
		click_id("field_special")
	if special == 1:
		click_id("field_repetition")

def unique(s):
	return len(set(s)) == len(s)

def set_len(l):
	pass_len = driver.find_element_by_id("field_length")
	pass_len.clear()
	pass_len.send_keys(l)

def login(u, p):
	driver.get(url)
	time.sleep(1)
	driver.find_element_by_id("login").click()
	time.sleep(1)
	driver.find_element_by_id("username").send_keys(u)
	driver.find_element_by_id("password").send_keys(p)
	driver.find_element_by_id("password").submit()
	time.sleep(1)

def cleanup():
	del_buttons = driver.find_elements_by_class_name("btn-danger")
	if del_buttons:
		del_buttons[0].click()
		time.sleep(1)
		click_text("Delete")


def check_pass_exists(s):
	tds = driver.find_elements_by_css_selector("table > tbody > tr > td")
	if tds:
		site_name = tds[2].text
		if site_name == s:
			return True
	else:
		return False

def goto_url(dest):
	driver.get(url+dest)

def click_class(c):
	driver.find_element_by_class(c).click()

def click_id(i):
	driver.find_element_by_id(i).click()

def click_text(text):
	driver.find_element_by_xpath("//*[contains(text(), \'"+text+"\')]").click()
	
class TestHeader(unittest.TestCase):
		
	def test_C1(self):
		s = "siteC1"
		u = "cats@cats.com"
		p = "stickman123"
		goto_url("/#/saturn-vault/new")
		time.sleep(1)
		input_credentials(s, u, p)
		time.sleep(1)
		driver.find_element_by_css_selector("form[name='editForm']").submit()
		time.sleep(1)
		result = check_pass_exists(s)
		cleanup()
		self.assertEqual(result, True)


	def test_C2(self):
		s = "siteC2"
		u = "seng426"
		p = "lildaddy"
		goto_url("/#/saturn-vault/new")
		time.sleep(1)
		input_credentials(s, u, p)
		time.sleep(1)
		click_text("Cancel")
		result = check_pass_exists(s)
		if not result:
			cleanup()
		self.assertEqual(result, False)


	def test_C3(self):
		s = "siteC3"
		u = "cats@cats.com"
		p = None
		l = 20
		result = True
		goto_url("/#/saturn-vault/new")
		time.sleep(1)
		input_credentials(s, u, p)
		time.sleep(1)
		click_text("Generate")
		time.sleep(1)
		tick_boxes(1, 0, 0, 0, 0)
		time.sleep(1)
		set_len(str(l))
		click_id("generate_password")
		time.sleep(1)
		password = driver.find_element_by_id("field_password").get_attribute('value')
		time.sleep(1)
		if not re.match(r"[a-z]+", password):
			result = False
		if len(password) != l:
			result = False
		click_text("Use")
		time.sleep(1)
		driver.find_element_by_css_selector("form[name='editForm']").submit()
		time.sleep(1)
		if result:
			result = check_pass_exists(s)
		cleanup()
		self.assertEqual(result, True)


	def test_C4(self):
		s = "siteC4"
		u = "cats@cats.com"
		p = None
		l = 20
		result = True
		goto_url("/#/saturn-vault/new")
		time.sleep(1)
		input_credentials(s, u, p)
		time.sleep(1)
		click_text("Generate")
		time.sleep(1)
		tick_boxes(1, 1, 0, 0, 0)
		time.sleep(1)
		set_len(str(l))
		click_id("generate_password")
		time.sleep(1)
		password = driver.find_element_by_id("field_password").get_attribute('value')
		time.sleep(1)
		if not re.match(r"[a-zA-Z]+", password):
			result = False
		if len(password) != l:
			result = False
		click_text("Use")
		time.sleep(1)
		driver.find_element_by_css_selector("form[name='editForm']").submit()
		time.sleep(1)
		if result:
			result = check_pass_exists(s)
		cleanup()
		self.assertEqual(result, True)
		


	def test_C5(self):
		s = "siteC5"
		u = "cats@cats.com"
		p = None
		l = 20
		result = True
		goto_url("/#/saturn-vault/new")
		time.sleep(1)
		input_credentials(s, u, p)
		time.sleep(1)
		click_text("Generate")
		time.sleep(1)
		tick_boxes(1, 1, 1, 0, 0)
		time.sleep(1)
		set_len(str(l))
		click_id("generate_password")
		time.sleep(1)
		password = driver.find_element_by_id("field_password").get_attribute('value')
		time.sleep(1)
		if not re.match(r"[a-zA-Z0-9]+", password):
			result = False
		if len(password) != l:
			result = False
		click_text("Use")
		time.sleep(1)
		driver.find_element_by_css_selector("form[name='editForm']").submit()
		time.sleep(1)
		if result:
			result = check_pass_exists(s)
		cleanup()
		self.assertEqual(result, True)
		


	def test_C6(self):
		s = "siteC6"
		u = "cats@cats.com"
		p = None
		l = 20
		result = True
		goto_url("/#/saturn-vault/new")
		time.sleep(1)
		input_credentials(s, u, p)
		time.sleep(1)
		click_text("Generate")
		time.sleep(1)
		tick_boxes(1, 1, 1, 1, 0)
		time.sleep(1)
		set_len(str(l))
		click_id("generate_password")
		time.sleep(1)
		password = driver.find_element_by_id("field_password").get_attribute('value')
		time.sleep(1)
		if not re.match(r"[a-zA-Z0-9!@#$%_-]+", password):
			result = False
		if len(password) != l:
			result = False
		click_text("Use")
		time.sleep(1)
		driver.find_element_by_css_selector("form[name='editForm']").submit()
		time.sleep(1)
		if result:
			result = check_pass_exists(s)
		cleanup()
		self.assertEqual(result, True)


	def test_C7(self):
		s = "siteC7"
		u = "cats@cats.com"
		p = None
		l = 20
		result = True
		goto_url("/#/saturn-vault/new")
		time.sleep(1)
		input_credentials(s, u, p)
		time.sleep(1)
		click_text("Generate")
		time.sleep(1)
		tick_boxes(1, 1, 1, 1, 1)
		time.sleep(1)
		set_len(str(l))
		click_id("generate_password")
		time.sleep(1)
		password = driver.find_element_by_id("field_password").get_attribute('value')
		time.sleep(1)
		if not re.match(r"[a-zA-Z0-9!@#$%_-]+", password):
			result = False
		if len(password) != l:
			result = False
		if not unique(password):
			result = False
		click_text("Use")
		time.sleep(1)
		driver.find_element_by_css_selector("form[name='editForm']").submit()
		time.sleep(1)
		if result:
			result = check_pass_exists(s)
		cleanup()
		self.assertEqual(result, True)
		

	def test_C8(self):
		s = "siteC8"
		u = "cats@cats.com"
		p = None
		l = 20
		result = True
		goto_url("/#/saturn-vault/new")
		time.sleep(1)
		input_credentials(s, u, p)
		time.sleep(1)
		click_text("Generate")
		time.sleep(1)
		tick_boxes(1, 1, 1, 1, 1)
		time.sleep(1)
		set_len(str(l))
		click_id("generate_password")
		time.sleep(1)
		click_id("cancel_pass_gen")
		time.sleep(1)
		click_text("Cancel")
		time.sleep(1)
		if result:
			result = check_pass_exists(s)
		self.assertEqual(result, False)


	def test_E1(self):
		s = "siteE1"
		u = "cats@cats.com"
		p = "stickman123"
		s_edit = "siteE1Edit"
		u_edit = "dogs@dogs.com"
		p_edit = "rat123"
		goto_url("/#/saturn-vault/new")
		time.sleep(1)
		input_credentials(s, u, p)
		time.sleep(1)
		driver.find_element_by_css_selector("form[name='editForm']").submit()
		time.sleep(1)
		edit_buttons = driver.find_elements_by_class_name("btn-info")
		edit_buttons[0].click()
		time.sleep(1)
		input_credentials(s_edit, u_edit, p_edit)
		time.sleep(1)
		driver.find_element_by_css_selector("form[name='editForm']").submit()
		time.sleep(1)
		result = check_pass_exists(s_edit)
		time.sleep(1)
		cleanup()
		time.sleep(1)
		self.assertEqual(result, True)


	def test_E2(self):
		s = "siteE2"
		u = "cats@cats.com"
		p = "stickman123"
		s_edit = "siteE2Edit"
		u_edit = "dogs@dogs.com"
		p_edit = "rat123"
		goto_url("/#/saturn-vault/new")
		time.sleep(1)
		input_credentials(s, u, p)
		time.sleep(1)
		driver.find_element_by_css_selector("form[name='editForm']").submit()
		time.sleep(1)
		edit_buttons = driver.find_elements_by_class_name("btn-info")
		edit_buttons[0].click()
		time.sleep(1)
		input_credentials(s_edit, u_edit, p_edit)
		time.sleep(1)
		click_text("Cancel")
		time.sleep(1)
		result = check_pass_exists(s)
		time.sleep(1)
		cleanup()
		time.sleep(1)
		self.assertEqual(result, True)


	def test_E3(self):
		s = "siteE3"
		u = "cats@cats.com"
		p = "stickman123"
		l = 20
		result = True
		goto_url("/#/saturn-vault/new")
		time.sleep(1)
		input_credentials(s, u, p)
		time.sleep(1)
		driver.find_element_by_css_selector("form[name='editForm']").submit()
		time.sleep(1)
		edit_buttons = driver.find_elements_by_class_name("btn-info")
		edit_buttons[0].click()
		time.sleep(1)

		click_text("Generate")
		time.sleep(1)
		tick_boxes(1, 0, 0, 0, 0)
		time.sleep(1)
		set_len(str(l))
		click_id("generate_password")
		time.sleep(1)
		password = driver.find_element_by_id("field_password").get_attribute('value')
		time.sleep(1)
		if not re.match(r"[a-z]+", password):
			result = False
		if len(password) != l:
			result = False
		click_text("Use")
		time.sleep(1)
		password_2 = driver.find_element_by_id("field_password").get_attribute('value')
		if password_2 != password:
			result = False

		driver.find_element_by_css_selector("form[name='editForm']").submit()
		time.sleep(1)
		if result:
			result = check_pass_exists(s)
		cleanup()
		time.sleep(1)
		self.assertEqual(result, True)


	def test_E4(self):
		s = "siteE4"
		u = "cats@cats.com"
		p = "stickman123"
		l = 20
		result = True
		goto_url("/#/saturn-vault/new")
		time.sleep(1)
		input_credentials(s, u, p)
		time.sleep(1)
		driver.find_element_by_css_selector("form[name='editForm']").submit()
		time.sleep(1)
		edit_buttons = driver.find_elements_by_class_name("btn-info")
		edit_buttons[0].click()
		time.sleep(1)

		click_text("Generate")
		time.sleep(1)
		tick_boxes(1, 1, 0, 0, 0)
		time.sleep(1)
		set_len(str(l))
		click_id("generate_password")
		time.sleep(1)
		password = driver.find_element_by_id("field_password").get_attribute('value')
		time.sleep(1)
		if not re.match(r"[a-zA-Z]+", password):
			result = False
		if len(password) != l:
			result = False
		click_text("Use")
		time.sleep(1)
		password_2 = driver.find_element_by_id("field_password").get_attribute('value')
		if password_2 != password:
			result = False

		driver.find_element_by_css_selector("form[name='editForm']").submit()
		time.sleep(1)
		if result:
			result = check_pass_exists(s)
		cleanup()
		time.sleep(1)
		self.assertEqual(result, True)


	def test_E5(self):
		s = "siteE5"
		u = "cats@cats.com"
		p = "stickman123"
		l = 20
		result = True
		goto_url("/#/saturn-vault/new")
		time.sleep(1)
		input_credentials(s, u, p)
		time.sleep(1)
		driver.find_element_by_css_selector("form[name='editForm']").submit()
		time.sleep(1)
		edit_buttons = driver.find_elements_by_class_name("btn-info")
		edit_buttons[0].click()
		time.sleep(1)

		click_text("Generate")
		time.sleep(1)
		tick_boxes(1, 1, 1, 0, 0)
		time.sleep(1)
		set_len(str(l))
		click_id("generate_password")
		time.sleep(1)
		password = driver.find_element_by_id("field_password").get_attribute('value')
		time.sleep(1)
		if not re.match(r"[a-zA-Z0-9]+", password):
			result = False
		if len(password) != l:
			result = False
		click_text("Use")
		time.sleep(1)
		password_2 = driver.find_element_by_id("field_password").get_attribute('value')
		if password_2 != password:
			result = False

		driver.find_element_by_css_selector("form[name='editForm']").submit()
		time.sleep(1)
		if result:
			result = check_pass_exists(s)
		cleanup()
		time.sleep(1)
		self.assertEqual(result, True)


	def test_E6(self):
		s = "siteE6"
		u = "cats@cats.com"
		p = "stickman123"
		l = 20
		result = True
		goto_url("/#/saturn-vault/new")
		time.sleep(1)
		input_credentials(s, u, p)
		time.sleep(1)
		driver.find_element_by_css_selector("form[name='editForm']").submit()
		time.sleep(1)
		edit_buttons = driver.find_elements_by_class_name("btn-info")
		edit_buttons[0].click()
		time.sleep(1)

		click_text("Generate")
		time.sleep(1)
		tick_boxes(1, 1, 1, 1, 0)
		time.sleep(1)
		set_len(str(l))
		click_id("generate_password")
		time.sleep(1)
		password = driver.find_element_by_id("field_password").get_attribute('value')
		time.sleep(1)
		if not re.match(r"[a-zA-Z0-9!@#$%_-]+", password):
			result = False
		if len(password) != l:
			result = False
		click_text("Use")
		time.sleep(1)
		password_2 = driver.find_element_by_id("field_password").get_attribute('value')
		if password_2 != password:
			result = False

		driver.find_element_by_css_selector("form[name='editForm']").submit()
		time.sleep(1)
		if result:
			result = check_pass_exists(s)
		cleanup()
		time.sleep(1)
		self.assertEqual(result, True)


	def test_E7(self):
		s = "siteE7"
		u = "cats@cats.com"
		p = "stickman123"
		l = 20
		result = True
		goto_url("/#/saturn-vault/new")
		time.sleep(1)
		input_credentials(s, u, p)
		time.sleep(1)
		driver.find_element_by_css_selector("form[name='editForm']").submit()
		time.sleep(1)
		edit_buttons = driver.find_elements_by_class_name("btn-info")
		edit_buttons[0].click()
		time.sleep(1)

		click_text("Generate")
		time.sleep(1)
		tick_boxes(1, 1, 1, 1, 1)
		time.sleep(1)
		set_len(str(l))
		click_id("generate_password")
		time.sleep(1)
		password = driver.find_element_by_id("field_password").get_attribute('value')
		time.sleep(1)
		if not re.match(r"[a-zA-Z0-9!@#$%_-]+", password):
			result = False
		if len(password) != l:
			result = False
		if not unique(password):
			result = False
		click_text("Use")
		time.sleep(1)
		password_2 = driver.find_element_by_id("field_password").get_attribute('value')
		if password_2 != password:
			result = False

		driver.find_element_by_css_selector("form[name='editForm']").submit()
		time.sleep(1)
		if result:
			result = check_pass_exists(s)
		cleanup()
		time.sleep(1)
		self.assertEqual(result, True)


	def test_E8(self):
		s = "siteE8"
		u = "cats@cats.com"
		p = "stickman123"
		l = 20
		result = True
		goto_url("/#/saturn-vault/new")
		time.sleep(1)
		input_credentials(s, u, p)
		time.sleep(1)
		driver.find_element_by_css_selector("form[name='editForm']").submit()
		time.sleep(1)
		edit_buttons = driver.find_elements_by_class_name("btn-info")
		edit_buttons[0].click()
		time.sleep(1)

		click_text("Generate")
		time.sleep(1)
		tick_boxes(1, 0, 0, 0, 0)
		time.sleep(1)
		set_len(str(l))
		click_id("generate_password")
		time.sleep(1)
		password = driver.find_element_by_id("field_password").get_attribute('value')
		time.sleep(1)
		click_id("cancel_pass_gen")
		time.sleep(1)
		password_2 = driver.find_element_by_id("field_password").get_attribute('value')
		if password_2 != p:
			result = False

		driver.find_element_by_css_selector("form[name='editForm']").submit()
		time.sleep(1)
		if result:
			result = check_pass_exists(s)
		cleanup()
		time.sleep(1)
		self.assertEqual(result, True)


	def test_D1(self):
		s = "siteD1"
		u = "cats@cats.com"
		p = "stickman123"
		goto_url("/#/saturn-vault/new")
		time.sleep(1)
		input_credentials(s, u, p)
		time.sleep(1)
		driver.find_element_by_css_selector("form[name='editForm']").submit()
		time.sleep(1)
		del_buttons = driver.find_elements_by_class_name("btn-danger")
		del_buttons[0].click()
		time.sleep(1)
		click_text("Delete")
		time.sleep(1)
		del_buttons = driver.find_elements_by_class_name("btn-danger")
		time.sleep(1)
		result = check_pass_exists(s)
		time.sleep(1)
		self.assertEqual(result, False)


	def test_D2(self):
		s = "siteD2"
		u = "cats@cats.com"
		p = "stickman123"
		goto_url("/#/saturn-vault/new")
		time.sleep(1)
		input_credentials(s, u, p)
		time.sleep(1)
		driver.find_element_by_css_selector("form[name='editForm']").submit()
		time.sleep(1)
		del_buttons = driver.find_elements_by_class_name("btn-danger")
		del_buttons[0].click()
		time.sleep(1)
		click_text("Cancel")
		result = check_pass_exists(s)
		time.sleep(1)
		cleanup()
		self.assertEqual(result, True)

		
if __name__ == '__main__':
	login(account_u, account_p)
	unittest.main()
	driver.quit()

