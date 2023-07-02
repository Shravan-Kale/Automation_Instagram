from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

class InstaBot(webdriver.Chrome):
    def __init__(self, options: Options = Options(), service: Service = Service(), keep_alive: bool = True) -> None:
        self.options = options
        self.service = service
        self.keep_alive = keep_alive
        super().__init__(self.options, self.service, self.keep_alive)
        

    def CreateAccount(self, email: str = "", full_name: str = "", username: str = "", password: str = "", date = "0 0 0"):
        """
        Create a New Instagram Account Using User Provided Information. If some data is missing, It will be generated automatically. 

        data needed to create a instagram account will be randomly generated as shown below =>
        >> Email -- Taken from temp mail sites
        >> Full Name -- Randomly generated from stored First Name and Last Name
        >> USername (Unique) -- Randomly generated based on Full Name
        >> password (Strong) -- Randomly generated
        >> Date of Birth -- Randomly Generated with random number generator. D-random(0, 30) M-random(0, 12) Y-random(1950, 2000)
        >> Verification Code -- Taken from temp mail site
        """

        # Fill the details
        # Click Next
        # Fill DOB -- DOB format, Space seperated DD MM YYYY. ex 26 07 2023
        # Click Next
        # Fill Verification Code
        # Click Done
        # Click Not Now Notification
        pass


    def Login(self):
        """
        Log in to account using Username and Password. If cookie is stored, then login using cookie

        The account info is stored in a database. The information consist of =>
        >> Username
        >> Password
        >> Cookies
        if cookies are present, the login function tryes to login user using cookies, otherwise uses Username and Password
        """

        # Try looging in using cookies
        # Else use Username and Password
        pass


    def SendMessage(self, users: list[str], message: str):
        """
        Send message to intended user

        takes two arguments, sender username and message. It selects the top search result from the message search area and sends the message. The more exact the sender username is, the more accurate result will be
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
        # Un-FOllow User 
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
        Search for the given Hashtag. Returns the top post from the topmost relevant hastag search
        """

        # Go to Search
        # Search for hashtag 
        pass