from selenium import webdriver

# Specify the path to the ChromeDriver executable
chromedriver_path = '/path/to/chromedriver'

# Specify the path to your Chrome user profile
chrome_profile_path = '/path/to/chrome/profile'

# Set Chrome options to use the existing profile
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'user-data-dir={chrome_profile_path}')

# Initialize ChromeDriver with the specified options
driver = webdriver.Chrome(chromedriver_path, options=chrome_options)

# Load WhatsApp Web
driver.get('https://web.whatsapp.com')

# Find and click on the contact or group you want to send a message to
contact_name = 'Contact or Group Name'
contact_xpath = f"//span[@title='{contact_name}']"
contact_element = driver.find_element_by_xpath(contact_xpath)
contact_element.click()

# Find the message input box
message_box = driver.find_element_by_xpath("//div[@class='_3uMse']")
message = "Hello, this is a test message."

# Type the message and send it
message_box.send_keys(message)
message_box.send_keys(Keys.ENTER)

# Close the driver
driver.quit()
