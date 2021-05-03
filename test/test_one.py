from selenium import webdriver

wd = webdriver.Chrome(r'C:\Users\yjm57\OneDrive\Documents\GitHub\News_Analyzer_APP\test\chromedriver')
wd.implicitly_wait(10)

wd.get('http://localhost:3000')

#element = wd.find_element_by_id('kw')
#elements = wd.find_elements_by_class_name('animal')
#element = wd.find_element_by_class_name('animal') #the first one
#elements = wd.find_elements_by_tag_name('a')

element = wd.find_element_by_link_text('Login')
element.click()

element = wd.find_element_by_id('login_username')
element.send_keys("jiamingy")

element = wd.find_element_by_id('login_password')
element.send_keys("123")

element = wd.find_element_by_tag_name('button')
element.click()

#wd.close()