class Google_profile:

    """
    A class to represent a Google Chrome profile configuration for Selenium WebDriver.

    user_data_dir : str
        The file system path to the directory containing Chrome user data.
    profile_dir_name : str
        The name of the specific Chrome profile directory to use.
    """

    def __init__(self, user_data_dir: str, profile_dir_name: str) -> None:
        self.profile_path = user_data_dir
        self.profile_name = profile_dir_name