import re
import urllib.parse
import os.path
import os
import validators
import wget

class ImageManager(object):
    imgs = []

    def setUp(self):
        print 'starting'

    def tearDown(self):
        import os
        os.system('rm -rf ./imgs')


    def __init__(self, md):
        self._md = md
        self._pattern = re.compile('!\[.*\]\((.*)\)')
        self.detect_images()

    def detect_images(self):
        self.imgs = self._pattern.findall(self._md)

    def replace_path_imgs(self, path):
        def repr_alg(matchobj):
            img = matchobj.group(2).split('/')[-1]
            img = os.path.join(path, img)
            ss = '![%s](%s)'%(matchobj.group(1), img)
            return ss
        md_mod = re.sub('!\[(.*)\]\((.*)\)', repr_alg, self._md)
        return md_mod

    def download(self, path):
        if not os.path.isdir(path):
             os.makedirs(path)
        print('imgs', self.imgs)
        for img in self.imgs:
            if validators.url(img):
                wget.download(img, path)

class
