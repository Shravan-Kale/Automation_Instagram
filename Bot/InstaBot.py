import random
from time import sleep


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

from Bot import Constant
from Bot import Helper


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

    def CreateAccount(self, email: str = "", full_name: str = "", username: str = "", password: str = "", date="0/0/0",
                      gender: str = "m") -> str:
        """
        Create a New Instagram Account Using User Provided Information. If some data is missing, It will be generated
        automatically.

        data needed to create an instagram account will be randomly generated as shown below =>
        >> Email -- Taken from stored emails that are scrape from temp mail sites
        >> Full Name -- Randomly generated from stored First Name and Last Name. FirstChar_LastName + Random Digit(1000)
        >> Username (Unique) -- Randomly generated based on Full Name. FirstChar_LastName + Random Digit (0 , 1000)
        >> password (Strong) -- Randomly generated
        >> Date of Birth -- Randomly Generated with random number generator.
        >> Verification Code -- Taken from temp mail site
        
        :param: All parameters are optional and of string type
            {email} = email for the account. example -- example@gmail.com
            {full_name} = Full name for the account. format -- FirstName LastName
            {username} = username for the account.
            {password} = password for the account.
            {date} = date of birth for the account. format -- day/month/year, example -- 23/5/2001, 2/12/1995
            {gender} = gender for the account. Used for generating random names. m for male or f for female
        
        :return: returns the full details of the account.
        """

        # region Variables
        error = True
        max_error_chance = 10
        auto_generate_email = email == ""
        auto_generate_username = username == ""
        if full_name == "":
            full_name = Helper.GetRandomName(gender)
        if password == "":
            password = Helper.GetRandomPassword()
        if date == "0/0/0":
            date = Helper.GetRandomDOB()
        if auto_generate_email:
            email = Helper.GetRandomMail()
        if auto_generate_username:
            username = Helper.GetRandomUsername(full_name)
        # endregion
        # region User Details
        self.driver.get(Constant.instagram_signup_url)
        sleep(1)
        email_text_element = self.driver.find_element(By.NAME, 'emailOrPhone')
        ClearWhole(email_text_element).send_keys(email)
        sleep(random.uniform(.2, 1.5))
        name_text_element = self.driver.find_element(By.NAME, 'fullName')
        ClearWhole(name_text_element).send_keys(full_name)
        sleep(random.uniform(.2, 1.5))
        username_text_element = self.driver.find_element(By.NAME, 'username')
        ClearWhole(username_text_element).send_keys(username)
        sleep(random.uniform(.2, 1.5))
        password_text_element = self.driver.find_element(By.NAME, 'password')
        ClearWhole(password_text_element).send_keys(password)
        sleep(random.uniform(.2, 1.5))
        # Click Next
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/div/div/div/div['
                                           '1]/section/main/div/div/div[1]/div[2]/form/div[7]/div/button').click()
        # Infinite Loop Can Occur. Limit the loop iterations
        while error or max_error_chance < 0:
            max_error_chance -= 1
            sleep(1)
            try:
                error_element = self.driver.find_element(By.ID, 'ssfErrorAlert').text
            except NoSuchElementException:
                error = False
            else:
                if 'username' in error_element:
                    if auto_generate_username:
                        username = Helper.GetRandomUsername(full_name)
                    else:
                        username = input("Username Not Available. New One")
                    ClearWhole(username_text_element).send_keys(username)
                if 'email' in error_element:
                    if auto_generate_email:
                        email = Helper.GetRandomMail()
                    else:
                        email = input("Email Not Available. Enter New One")
                    ClearWhole(email_text_element).send_keys(email)
                if 'and periods.' in error_element:
                    username = input("Username Contains Unaccepted Characters. Enter New One")
                    ClearWhole(username_text_element).send_keys(username)
                self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/div/div/div/div[''1]/section/main/'
                                                   'div/div/div[1]/div[2]/form/div[7]/div/button').click()
        # endregion
        # region Date Of Birth
        day, month, year = date.split("/")
        Select(self.driver.find_element(By.XPATH, '//select[@title="Month:"]')).select_by_value(month)
        sleep(random.uniform(.2, 1.5))
        Select(self.driver.find_element(By.XPATH, '//select[@title="Day:"]')).select_by_value(day)
        sleep(random.uniform(.2, 1.5))
        Select(self.driver.find_element(By.XPATH, '//select[@title="Year:"]')).select_by_value(year)
        sleep(random.uniform(.2, 1.5))
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/div/div/div/div['
                                           '1]/section/main/div/div/div[1]/div/div[6]/button').click()
        sleep(1)
        # endregion
        # region Verification Code
        if auto_generate_email:
            verification_code = Helper.GetVerificationCodeAuto()
        else:
            verification_code = Helper.GetVerificationCodeUser()
        verification_text_element = self.driver.find_element(By.NAME, 'email_confirmation_code')
        ClearWhole(verification_text_element).send_keys(verification_code)
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/div/div/div/div['
                                           '1]/section/main/div/div/div/div[2]/form/div/div[2]/button').click()
        # endregion
        return f"User Details\n\nFull Name: {full_name}\nDate Of birth (DOB): {date}\n" \
               f"Email: {email}\nUsername: {username}\nPassword: {password}"

    def Login(self):
        """
        Log in to account using Username and Password. If cookie is stored, then login using cookie

        The account info is stored in a database. The information consist of =>
        >> Username
        >> Password
        >> Cookies
        if cookies are present, the login function tries to log in user using cookies, otherwise uses
        Username and Password
        """

        # Try logging in using cookies
        # Else use Username and Password
        pass

    def SendMessage(self, users: list[str], message: str):
        """
        Send message to intended user

        takes two arguments, sender username and message. It selects the top search result from the message search
        area and sends the message. The more exact the sender username is, the more accurate result will be
        """

        # Navigate to message page
        # Search for the user
        # Select the top user 
        # Write the message and Send
        pass

    def Like(self, url: str):
        """
        Like the given Post.
        """

        # Go to post url
        # Like the Post
        pass

    def Comment(self, url: str, comment: str):
        """
        Comment on the given Post.
        """

        # Go to post url
        # Write comment and post 
        pass

    def Share(self, url: str, users: list[str]):
        """
        Share the given Post.
        """

        # Go to post url
        # Click on Share
        # Search user from the list and select top result for every item on list
        # Click Send
        pass

    def Save(self, url: str):
        """
        Share the given Post (In default album).
        """

        # Go to post url
        # Save post 
        pass

    def Follow(self, user: list[str]):
        """
        Follow the given users profile
        """

        # Go to user url
        # Follow user 
        pass

    def UnFollow(self, users: list[str]):
        """
        Un-Follow the given users profile
        """

        # Go to user url
        # Un-Follow User
        pass

    def SearchUser(self, users: str):
        """
        Search for the given user profile and return the topmost relevant search result
        """

        # Go to Search
        # Search for user         
        pass

    def SearchPost(self, hashtag: str):
        """
        Search for the given Hashtag. Returns the top post from the topmost relevant hashtag search
        """

        # Go to Search
        # Search for hashtag 
        pass


c = InstaBot()
print(c.CreateAccount())
# email1 = "example@gmail.com"
# name1 = "random shit"
# username1 = "Shrank_23_Kale"
# password1 = "asd13mffa"
# DOB = "23/7/1995"
# c.CreateAccount(email1, name1, username1, password1, DOB)
# # input()
