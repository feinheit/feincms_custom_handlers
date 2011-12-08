""" This is for FeinCMS >= 1.5. For older versions use the legacy module.
"""

class NotMyJob(Exception):
    def __init__(self, author):
        self.author = author

    def __str__(self):
        return repr(self.author)
