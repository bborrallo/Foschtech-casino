'''
Created on 18 nov 2021

@author: Borja Borrallo
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import pytesseract


class CasinoTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path="C:/Users/Borja Borrallo/Downloads/chromedriver.exe")
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        self.success = False
        
        
    def test(self):    
        self.driver.get('https://demo.casino')
        assert self.driver.title == "Lets bet"
        self.driver.find_element_by_xpath('//a[@href="/user/registration"]').click()
        username = self.driver.find_element_by_id("core__protected_modules_user_yiiForm_RegistrationForm_email")
        username.send_keys("test2566452@test.us")
        password = self.driver.find_element_by_id("core__protected_modules_user_yiiForm_RegistrationForm_password")
        pswd = "Test1234"
        password.send_keys(pswd)
        passwordConfirmation = self.driver.find_element_by_id("core__protected_modules_user_yiiForm_RegistrationForm_password_confirmation")
        passwordConfirmation.send_keys(pswd)
        self.driver.find_element_by_css_selector("label[for='core__protected_modules_user_yiiForm_RegistrationForm_terms_and_conditions']").click()
        captchaCode = self.driver.find_element_by_id("core__protected_modules_user_yiiForm_RegistrationForm_captcha")
        while(self.success == False):
            self.driver.find_element_by_id('yw1').screenshot('captcha.png')
            captchaText = pytesseract.image_to_string('captcha.png')  
            captchaCode.send_keys(captchaText)
            try:
                if(self.driver.find_element_by_xpath("//div[@class='form__input form__input--captcha captcha--v1 error']//div[@class='form__notification form__notification--error form__error-message']").is_displayed()):
                    self.driver.find_element_by_id('yw1_button').click()
                    self.driver.find_element_by_id("core__protected_modules_user_yiiForm_RegistrationForm_captcha").clear()
                else:
                    self.success = True
            except:
                self.success = True
                
            #self.driver.find_element_by_xpath("//div[@class='form__wrapper']//fieldset[@class='form__section form__section--submit']//button").click()
        #self.driver.execute_script("window.scrollTo(0, 500)")
        sleep(15)
        
        
    def tearDown(self):
        self.driver.quit()
        
        
if __name__ == "__main__":
    unittest.main()