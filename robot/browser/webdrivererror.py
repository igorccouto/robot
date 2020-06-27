class WebDriverError(Exception):
    "Exception raised for errors with webdriver"
    def __init__(self, error:Exception, message:str) -> None:
        self.error_name = type(error).__name__
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'WebDriverError: ({self.error_name}) -> {self.message}'
