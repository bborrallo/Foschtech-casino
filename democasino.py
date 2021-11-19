'''
Created on 18 nov 2021

@author: Borja Borrallo
'''
#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pytesseract
from selenium.webdriver.android.webdriver import WebDriver


class CasinoTest(unittest.TestCase):
    #############################
    #    PRECONDITIONS
    #############################
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path="C:/Users/Borja Borrallo/Downloads/chromedriver.exe")                # Se selecciona el driver de chrome
        pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'                             # Se anade pytesseract al path de variables de entorno
        self.success = False                                                                                                # Variable para saber si se ha producido el registro correctamente
        
    #############################
    #    TEST CASE
    #############################    
    def test(self):    
        self.driver.get('https://demo.casino')                                                                              # Ir al dominio web
        assert self.driver.title == "Lets bet"                                                                              # Comprobar el titulo de la web
        self.driver.find_element_by_xpath('//a[@href="/user/registration"]').click()                                        # Click sobre el boton "Registration"
        username = self.driver.find_element_by_id("core__protected_modules_user_yiiForm_RegistrationForm_email")            # Selecciona espacio de email
        username.send_keys("test20@test.us")                                                                                 # Escribe la direccion mail
        password = self.driver.find_element_by_id("core__protected_modules_user_yiiForm_RegistrationForm_password")         # Selecciona espacio para password
        pswd = "Test1234"                                                                                                   # Variable local para el hacer mas parametizable el password
        password.send_keys(pswd)                                                                                            # Escribe password
        passwordConfirmation = self.driver.find_element_by_id("core__protected_modules_user_yiiForm_RegistrationForm_password_confirmation")        # Selecciona y escribe confimacion pass
        passwordConfirmation.send_keys(pswd)                    
        self.driver.find_element_by_css_selector("label[for='core__protected_modules_user_yiiForm_RegistrationForm_terms_and_conditions']").click() # Se aceptan los terminos y condiciones
        currentUrl = self.driver.current_url
        try:
            while(self.success == False):                                                                                       # Se genera un bucle para checkear el captcha y repetir estos pasos en caso de ser un captcha erroneo
                self.driver.find_element_by_id('yw1').screenshot('captcha.png')                                                 # Se realiza una captura del captcha para poder extraer el texto de la imagen
                captchaText = pytesseract.image_to_string('captcha.png')                                                        # Se extrae el texto de la imagen con ayuda de pytesseract
                captchaCode = self.driver.find_element_by_id("core__protected_modules_user_yiiForm_RegistrationForm_captcha")       # Se selecciona el espacio de captcha     
                captchaCode.send_keys(captchaText)                                                                                  # Se escribe el captcha
                if (currentUrl == self.driver.current_url):                                                                         # Si no ha cambiado la url es debido a un error en el registro (en este caso solo se comprueba el captcha)       
                    if(self.driver.find_element_by_xpath("//div[@class='form__input form__input--captcha captcha--v1 error']//div[@class='form__notification form__notification--error form__error-message']").is_displayed()): # Se comprueba si aparece una notificacion de error de captcha
                        self.driver.find_element_by_id('yw1_button').click()                                                        # Se hace click en generar otro captcha
                        self.driver.find_element_by_id("core__protected_modules_user_yiiForm_RegistrationForm_captcha").clear()     # Se elimina el captcha anterior para poder escribir el nuevo
                        sleep(2)
                else:                                                                                                               # En caso de no aparecer dicha notificacion de error, se da por exitoso el registro
                    self.success = True                                                                                             # En este test, ya que no se indica, se da por hecho que tanto el mail como el pass son correctos, puesto que se definen por el programador en el propio test          
        except:
            AssertionError ("Ha ocurrido un error en el registro")
        assert self.driver.current_url == "https://demo.casino/registrationSuccess"                                                 # Se comprueba que se ha llegado a la url de registro completado
        
        # Tras el registro se continua con la feature
        self.driver.find_element_by_xpath("//i[@class='icon-mobile-menu']").click()                                                                                                                         # Se abre el desplegable
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//li[@class="quick-links-menu__item"]//a[@href="/gameList"]'))).click()                                                 # Se clica en GAMES                                                
        self.driver.find_element_by_xpath('//a[@href="/gameGroup/slots"]').click()                                                                                                                          # Se selecciona Slots
        game = self.driver.find_element_by_xpath('//div[@class="games__item__img"]//img[@src="/uploads/images/games/gis_Booongo_642029bae18a237383f07b54d69be64a552fdcf3.png?last-update=1627792644"]')
        action = ActionChains(self.driver)                                              
        action.move_to_element(game)
        action.perform()                                                                                                                                                                                    # Se mueve el cursor encima de un juego para que aparezca el boton
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="games__item--buttons"]//span[@class="button button--s2 button--t1 button--play"]'))).click()              # Se clica sobre el juego
        assert self.driver.current_url == "https://demo.casino/game/realGame/12126"                                                                                                                         # Se comprueba que el juego seleccionado se abre
        
        
    #############################
    #    POSTCONDITIONS
    #############################    
    def tearDown(self):
        self.driver.quit()                                                                                                   # Cierra el browser
        
        
if __name__ == "__main__":
    unittest.main()