# region Imports
# region Inbuilt imports
import random
from time import sleep
# endregion
# region Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
# endregion
# region Helper imports
from Bot import Constant
from Bot import Helper
from Bot import Elements_Search_Path
# endregion
# endregion


def ClearWhole(element: WebElement) -> WebElement:
    element.send_keys(Keys.CONTROL + "a")
    element.send_keys(Keys.DELETE)
    return element


def ClearBackspace(element: WebElement, times: int) -> WebElement:
    for i in range(times):
        element.send_keys(Keys.BACK_SPACE)
    return element


class InstaBot:
    def __init__(self, options: Options = Options(), service: Service = Service(), keep_alive: bool = True) -> None:
        self.options = options
        self.service = service
        self.keep_alive = keep_alive
        self.driver = webdriver.Chrome(self.options, self.service, self.keep_alive)
        self.driver.implicitly_wait(30)

    def CreateAccount(self, email: str = None, full_name: str = None, username: str = None, password: str = None,
                      date: str = None, gender: str = "m") -> str:
        """
        Create a New Instagram Account Using User Provided Information.
        If some data is missing, It will be generated automatically.

        Data needed to create an instagram account will be randomly generated as shown below =>
        >> Email -- Taken from stored emails that are scrape from temp mail sites
        >> Full Name -- Randomly generated from stored First Name and Last Name. FirstChar_LastName + Random Digit(1000)
        >> Username (Unique) -- Randomly generated based on Full Name. FirstChar_LastName + Random Digit (0 , 1000)
        >> password (Strong) -- Randomly generated
        >> Date of Birth -- Randomly Generated with random number generator.
        >> Verification Code -- Taken from temp mail site
        
        :param: All parameters are optional and of string type
            {email} = email for the account. example -- example@gmail.com
            {full_name} = Full name for the account. format -- FirstName LastName
            {username} = username for the account. Only letters numbers underscore and period. Not end with period
            {password} = password for the account.
            {Date} = date of birth for the account. format -- day/month/year, example -- 23/5/2001, 2/12/1995
            {gender} = gender for the account. Used for generating random names. M for male or f for female
        
        :return: Return the full details of the account.
        """

        # region Variables
        error = True
        max_error_chance = 10
        auto_generate_email = False
        auto_generate_username = False
        if full_name is None:
            full_name = Helper.GetRandomName(gender)
        if password is None:
            password = Helper.GetRandomPassword()
        if date is None:
            date = Helper.GetRandomDOB()
        if email is None:
            auto_generate_email = True
            email = Helper.GetRandomMail()
        if username is None:
            auto_generate_username = True
            email = Helper.GetRandomUsername(full_name)
        # endregion
        # region User Details
        self.driver.get(Constant.instagram_signup_url)
        sleep(1)
        try:
            email_text_element = self.driver.find_element(By.NAME, Elements_Search_Path.email_text_area)
            ClearWhole(email_text_element).send_keys(email)
            sleep(random.uniform(.2, 1.5))
            name_text_element = self.driver.find_element(By.NAME, Elements_Search_Path.name_text_area)
            ClearWhole(name_text_element).send_keys(full_name)
            sleep(random.uniform(.2, 1.5))
            username_text_element = self.driver.find_element(By.NAME, Elements_Search_Path.username_text_area)
            ClearWhole(username_text_element).send_keys(username)
            sleep(random.uniform(.2, 1.5))
            password_text_element = self.driver.find_element(By.NAME, Elements_Search_Path.password_text_area)
            ClearWhole(password_text_element).send_keys(password)
            sleep(random.uniform(.2, 1.5))
        except NoSuchElementException:
            print("Error occurred while finding text area fro details. Please Try Again")
            return "No Element Found"
        # Infinite Loop Can Occur. Limit the loop iterations
        self.driver.implicitly_wait(0)
        while error or max_error_chance < 0:
            try:
                self.driver.find_element(By.XPATH, Elements_Search_Path.details_next_button).click()
            except NoSuchElementException:
                print("Error occurred while clicking on next button (Account details). Please Try Again")
                return "No Element Found"
            max_error_chance -= 1
            sleep(1)
            try:
                error_element = self.driver.find_element(By.XPATH, Elements_Search_Path.details_error_div).text
            except NoSuchElementException:
                error = False
            else:
                if 'username' in error_element:
                    if auto_generate_username:
                        username = Helper.GetRandomUsername(full_name)
                    else:
                        username = input("Username Not Available. Enter New One")
                    ClearWhole(username_text_element).send_keys(username)
                elif 'password' in error_element:
                    password = input("Password Not Strong. Enter New One")
                    ClearWhole(password_text_element).send_keys(password)
                elif 'email' in error_element:
                    if auto_generate_email:
                        email = Helper.GetRandomMail()
                    else:
                        email = input("Email Not Available. Enter New One")
                    ClearWhole(email_text_element).send_keys(email)
                else:
                    print(f"Error occurred while creating account. Error:- {error_element}. Please Try Again")
                    return f"Error:- {error_element}"

        self.driver.implicitly_wait(30)
        # endregion
        # region Date Of Birth
        day, month, year = date.split("/")
        try:
            Select(self.driver.find_element(By.XPATH, Elements_Search_Path.month_selection)).select_by_value(month)
            sleep(random.uniform(.2, 1.5))
            Select(self.driver.find_element(By.XPATH, Elements_Search_Path.day_selection)).select_by_value(day)
            sleep(random.uniform(.2, 1.5))
            Select(self.driver.find_element(By.XPATH, Elements_Search_Path.year_selection)).select_by_value(year)
            sleep(random.uniform(.2, 1.5))
            self.driver.find_element(By.XPATH, Elements_Search_Path.dob_next_button).click()
        except NoSuchElementException:
            print("Error occurred while selecting date of birth. Please Try Again")
            return "No Element Found"
        sleep(1)
        # endregion
        # region Verification Code
        if auto_generate_email:
            verification_code = Helper.GetVerificationCodeAuto()
        else:
            verification_code = input("Enter Verification Code")
        try:
            verification_text_element = self.driver.find_element(By.NAME, Elements_Search_Path.verification_text_area)
            ClearWhole(verification_text_element).send_keys(verification_code)
            self.driver.find_element(By.XPATH, Elements_Search_Path.verification_next_button).click()
        except NoSuchElementException:
            print("Error occurred while doing verification. Please Try Again")
            return "No Element Found"
        # endregion
        return f"User Details\n\nFull Name: {full_name}\nDate Of birth (DOB): {date}\n" \
               f"Email: {email}\nUsername: {username}\nPassword: {password}"

    def Login(self, username: str, password: str):
        """
        Log in to account using Username and Password.
        If a cookie is stored, then login using cookie

        The account info is stored in a database. The information consist of =>
        >> Username
        >> Password
        >> Cookies
        if cookies are present, the login function tries to log in user using cookies, otherwise uses
        Username and Password
        """

        error = True
        max_error_chance = 10
        self.driver.get(Constant.instagram_login_url)
        sleep(1)
        try:
            self.driver.implicitly_wait(2)
            if len(Constant.cookie) > 0:
                for c in Constant.cookie:
                    self.driver.add_cookie(c)
                self.driver.refresh()
                sleep(1)
            username_text_element = self.driver.find_element(By.NAME, Elements_Search_Path.username_login_text_area)
        except NoSuchElementException:
            pass
        else:
            self.driver.implicitly_wait(30)
            password_text_element = self.driver.find_element(By.NAME, Elements_Search_Path.password_login_text_area)
            ClearWhole(username_text_element).send_keys(username)
            ClearWhole(password_text_element).send_keys(password)
            submit_button_element = self.driver.find_element(By.XPATH, Elements_Search_Path.login_submit_button)
            submit_button_element.click()
            sleep(1)
            # Infinite Loop Can Occur. Limit the loop iterations
            while error or max_error_chance < 0:
                self.driver.implicitly_wait(0)
                max_error_chance -= 1
                sleep(10)
                try:
                    error_text = self.driver.find_element(By.XPATH, Elements_Search_Path.login_error_div).text
                except NoSuchElementException:
                    error = False
                else:
                    if 'password' in error_text:
                        password = input("Password Incorrect. Enter New One")
                        ClearWhole(password_text_element).send_keys(password)
                    submit_button_element.click()
                self.driver.implicitly_wait(30)
        try:
            self.driver.find_element(By.XPATH, Elements_Search_Path.not_now_button).click()
        except NoSuchElementException:
            pass

    def SendMessage(self, users: list[str], message: str):
        """
        Send a message to the intended user

        Takes two arguments, sender username and message.
        It selects the top search result from the message search
        area and sends the message. The more exact the sender username is, the more accurate result will be
        """

        self.driver.get(Constant.instagram_direct_message_url)
        sleep(1)
        try:
            self.driver.find_element(By.XPATH, Elements_Search_Path.message_button).click()
            search_element = self.driver.find_element(By.XPATH, Elements_Search_Path.message_search_text_area)
        except NoSuchElementException:
            print("Error occurred while initiating send message. Please Try Again")
            return "No Element Found"

        try:
            for user in users:
                search_element.send_keys(user)
                sleep(1)
                self.driver.find_element(By.XPATH, Elements_Search_Path.message_top_user).click()
            sleep(1)
            self.driver.find_element(By.XPATH, Elements_Search_Path.message_next_button).click()
        except NoSuchElementException:
            print("Error occurred while selecting user. Please Try Again")
            return "No Element Found"
        try:
            message_box_element = self.driver.find_element(By.XPATH, Elements_Search_Path.message_text_area)
            ClearWhole(message_box_element).send_keys(message)
            sleep(.5)
            self.driver.find_element(By.XPATH, Elements_Search_Path.message_send_button).click()
        except NoSuchElementException:
            print("Error occurred while sending message. Please Try Again")
            return "No Element Found"

    def Like(self, url: str):
        """
        Like the given Post.
        """

        self.driver.get(url)
        try:
            self.driver.find_element(By.XPATH, Elements_Search_Path.like_button).click()
        except NoSuchElementException:
            print("Error occurred while liking post. Please Try Again")
            return "No Element Found"

    def Comment(self, url: str, comment: str):
        """
        Comment on the given Post.
        """

        self.driver.get(url)
        try:
            self.driver.find_element(By.XPATH, Elements_Search_Path.comment_button).click()
            comment_element = self.driver.find_element(By.XPATH, Elements_Search_Path.comment_text_area)
            ClearWhole(comment_element).send_keys(comment)
            self.driver.find_element(By.XPATH, Elements_Search_Path.comment_post_button).click()
        except NoSuchElementException:
            print("Error occurred while commenting. Please Try Again")
            return "No Element Found"

    def Share(self, url: str, users: list[str], msg: str = None):
        """
        Share the given Post.
        """

        self.driver.get(url)
        try:
            self.driver.find_element(By.XPATH, Elements_Search_Path.share_button).click()
            search_element = self.driver.find_element(By.XPATH, Elements_Search_Path.share_search_text_area)
        except NoSuchElementException:
            print("Error occurred while initiating share. Please Try Again")
            return "No Element Found"
        try:
            for user in users:
                search_element.click()
                search_element.send_keys(user)
                sleep(1)
                self.driver.find_element(By.XPATH, Elements_Search_Path.share_top_user).click()
        except NoSuchElementException:
            print("Error occurred while selecting user. Please Try Again")
            return "No Element Found"
        try:
            if msg is not None:
                self.driver.find_element(By.XPATH, Elements_Search_Path.share_message_text_area).send_keys(msg)
                sleep(1)
            self.driver.find_element(By.XPATH, Elements_Search_Path.share_send_button).click()
        except NoSuchElementException:
            print("Error occurred while sharing post. Please Try Again")
            return "No Element Found"

    def Save(self, url: str):
        """
        Share the given Post (In default album).
        """

        self.driver.get(url)
        try:
            self.driver.find_element(By.XPATH, Elements_Search_Path.save_button).click()
        except NoSuchElementException:
            print("Error occurred while saving post. Please Try Again")
            return "No Element Found"

    def Follow(self, users: list[str] = None, users_url: list[str] = None):
        """
        Follow the given users profile
        """

        try:
            if users is not None:
                for user in users:
                    url = self.SearchUser(user)
                    self.driver.get(url)
                    self.driver.find_element(By.XPATH, Elements_Search_Path.follow_button).click()
            if users_url is not None:
                for url in users_url:
                    self.driver.get(url)
                    self.driver.find_element(By.XPATH, Elements_Search_Path.follow_button).click()
        except NoSuchElementException:
            print("Error occurred while following user. Please Try Again")
            return "No Element Found"

    def UnFollow(self, users: list[str] = None, users_url: list[str] = None):
        """
        Un-Follow the given users profile
        """

        try:
            if users is not None:
                for user in users:
                    url = self.SearchUser(user)
                    self.driver.get(url)
                    self.driver.find_element(By.XPATH, Elements_Search_Path.follow_dropdown).click()
                    self.driver.find_element(By.XPATH, Elements_Search_Path.unfollow_button).click()
            if users_url is not None:
                for url in users_url:
                    self.driver.get(url)
                    self.driver.find_element(By.XPATH, Elements_Search_Path.follow_dropdown).click()
                    self.driver.find_element(By.XPATH, Elements_Search_Path.unfollow_button).click()
        except NoSuchElementException:
            print("Error occurred while un-following user. Please Try Again")
            return "No Element Found"

    def SearchUser(self, user: str) -> str:
        """
        Search for the given user profile and return the topmost relevant search result

        :return: Return the url of the top account.
        """

        try:
            self.driver.get(Constant.inatagram_base_url)
            self.driver.find_element(By.XPATH, Elements_Search_Path.search_button).click()
            self.driver.find_element(By.XPATH, Elements_Search_Path.search_text_area).send_keys(user)
            user_url = self.driver.find_element(By.XPATH, Elements_Search_Path.search_user_a).get_attribute('href')
        except NoSuchElementException:
            print("Error occurred while searching user. Please Try Again")
            return "No Element Found"
        return user_url

    def SearchHashtag(self, hashtag: str, hashtag_number: int = 1) -> str:
        """
        Search for the given Hashtag. Returns the top post from the topmost relevant hashtag search

        :return: Return the url of the top hashtag.
        """

        self.driver.get(Constant.inatagram_base_url)
        if hashtag[0] != '#':
            hashtag = '#' + hashtag
        try:
            self.driver.find_element(By.XPATH, Elements_Search_Path.search_button).click()
            self.driver.find_element(By.XPATH, Elements_Search_Path.search_text_area).send_keys(hashtag)
            top_hashtag_url = self.driver.find_element(By.XPATH, Elements_Search_Path.hashtag_element +
                                                       str(min([hashtag_number, 55])) + ']/a').get_attribute('href')
        except NoSuchElementException:
            print("Error occurred while searching hashtag. Please Try Again")
            return "No Element Found"
        return top_hashtag_url

    def GetPostUsersFromHashtagNumber(self, hashtag: str, hashtag_number: int = 1, number_of_posts: int = 9) \
            -> list[str]:
        """
        Search for the given Hashtag and return the users of the top posts

        :return: Return the list of users having top posts.
        """

        top_hashtag_url = self.SearchHashtag(hashtag, min([hashtag_number, 55]))
        users = []
        number_of_posts -= 1
        rows = (min([number_of_posts - 1, 8]) // 3)
        cols = (min([number_of_posts - 1, 8]) % 3)
        self.driver.get(top_hashtag_url)
        for row in range(1, rows + 2):
            for col in range(1, cols + 2):
                try:
                    post_link = self.driver.find_element(By.XPATH, Elements_Search_Path.hashtag_post_element
                                                         + str(row) + ']/div[' + str(col) + ']/a').get_attribute('href')
                    self.driver.execute_script(f"window.open('{Constant.inatagram_base_url + post_link}');")
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    user = self.driver.find_element(By.XPATH,
                                                    Elements_Search_Path.hashtag_post_user_a).get_attribute('href')
                    users.append(user)
                except NoSuchElementException:
                    pass
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
        return users
