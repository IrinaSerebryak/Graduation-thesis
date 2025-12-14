from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure


class LoginPage(BasePage):
    """Page Object для страницы входа/регистрации"""

    # Локаторы формы входа
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='login']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    REMEMBER_ME_CHECKBOX = (By.CSS_SELECTOR, "input[name='remember']")

    # Локаторы формы регистрации
    REGISTER_LINK = (By.LINK_TEXT, "Зарегистрироваться")
    REGISTER_EMAIL = (By.CSS_SELECTOR, "input[name='email']")
    REGISTER_PASSWORD = (By.CSS_SELECTOR, "input[name='password']")
    REGISTER_CONFIRM_PASSWORD = (By.CSS_SELECTOR, "input[name='password_confirm']")
    REGISTER_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    # Сообщения об ошибках
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success-message")

    # Восстановление пароля
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Забыли пароль?")
    RECOVER_EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email']")
    RECOVER_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    @allure.step("Выполнить вход с email: '{email}'")
    def login(self, email: str, password: str, remember: bool = False):
        """Выполнить вход в систему"""
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)

        if remember and self.is_element_visible(self.REMEMBER_ME_CHECKBOX):
            self.click(self.REMEMBER_ME_CHECKBOX)

        self.click(self.LOGIN_BUTTON)

    @allure.step("Перейти на страницу регистрации")
    def go_to_register(self):
        """Перейти на страницу регистрации"""
        self.click(self.REGISTER_LINK)

    @allure.step("Зарегистрировать нового пользователя")
    def register(self, email: str, password: str, confirm_password: str = None):
        """Зарегистрировать нового пользователя"""
        self.go_to_register()

        self.type_text(self.REGISTER_EMAIL, email)
        self.type_text(self.REGISTER_PASSWORD, password)

        if confirm_password is None:
            confirm_password = password

        if self.is_element_visible(self.REGISTER_CONFIRM_PASSWORD):
            self.type_text(self.REGISTER_CONFIRM_PASSWORD, confirm_password)

        self.click(self.REGISTER_BUTTON)

    @allure.step("Восстановить пароль для email: '{email}'")
    def recover_password(self, email: str):
        """Восстановить пароль"""
        self.click(self.FORGOT_PASSWORD_LINK)

        if self.is_element_visible(self.RECOVER_EMAIL_INPUT):
            self.type_text(self.RECOVER_EMAIL_INPUT, email)
            self.click(self.RECOVER_BUTTON)

    @allure.step("Получить текст ошибки")
    def get_error_message(self) -> str:
        """Получить текст сообщения об ошибке"""
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    @allure.step("Получить текст успешного сообщения")
    def get_success_message(self) -> str:
        """Получить текст успешного сообщения"""
        if self.is_element_visible(self.SUCCESS_MESSAGE):
            return self.get_text(self.SUCCESS_MESSAGE)
        return ""

    @allure.step("Проверить успешный вход")
    def is_login_successful(self) -> bool:
        """Проверить успешность входа по URL или элементам"""
        current_url = self.driver.current_url
        return "mykp" in current_url or "profile" in current_url
