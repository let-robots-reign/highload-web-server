import logging
from urllib import parse


class Request:
    """
    Класс HTTP-запроса
    """
    def __init__(self, unparsed_message):
        self.method = self.url = self.protocol = ''
        self.is_valid = False

        lines = unparsed_message.splitlines()

        try:
            self.method, dirty_url, self.protocol = lines[0].split()
            self.url = parse.unquote(dirty_url)
            if '?' in self.url:
                self.url = self.url[:self.url.find('?')]

            self.is_valid = True

        except Exception as e:
            logging.error(e)
            self.is_valid = False
