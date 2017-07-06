import re

class ImageDetector(object):
    imgs = []

    def __init__(self, md):
        self._md = md
        self._pattern = re.compile('!\[.*\]\((.*)\)')
        self.detect_images()

    def detect_images(self):
        self.imgs = self._pattern.findall(self._md)
