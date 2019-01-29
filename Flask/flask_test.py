from selenium import webdriver

# driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')

driver = webdriver.Firefox()

driver.implicitly_wait(30)

driver.maximize_window()

driver.quit()

