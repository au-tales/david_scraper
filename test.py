from selenium import webdriver
from selenium.webdriver.common.proxy import ProxyType, Proxy #proxy module
import time
from webdriver_manager.chrome import ChromeDriverManager

proxy_ip = '207.180.216.144:19006' #get a free proxy from the websites in the description

#setting up proxy
proxy =Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = proxy_ip
proxy.ssl_proxy = proxy_ip

#linking proxy and setting up driver
capabilities = webdriver.DesiredCapabilities.CHROME
proxy.add_to_capabilities(capabilities)
driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=capabilities) # replace the chromedriver path
time.sleep(6)
#loading test page
driver.get('https://www.amazon.com/Belli-Acne-Control-Spot-Treatment/dp/B00I9MZZTC')

driver.quit()