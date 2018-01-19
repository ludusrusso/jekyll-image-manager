#!/usr/bin/env python

import re
import urllib.parse
import os.path
import os
import validators
import wget

class ImageManager(object):
    imgs = []
    def __init__(self, md):
        self._md = md
        self._patterns = [re.compile('^image: (.+[png|jpeg|jpg])', flags=re.MULTILINE), re.compile('!\[[^\]]*\]\(([^\)]*)\)')]
        self.detect_images()

    def detect_images(self):
        imgs = []
        for patter in self._patterns:
            imgs += patter.findall(self._md)
            print('   ----------- ', imgs)
        self.imgs = imgs

    def replace_path_imgs(self, path):
        def repr_alg(matchobj):
            img = matchobj.group(2).split('/')[-1]
            img = os.path.join(path, img)
            ss = '![%s](%s)'%(matchobj.group(1), img)
            return ss

        def repr_alg_2(matchobj):
            img = matchobj.group(1)
            if validators.url(img):
                img = os.path.join(path, img.split('/')[-1])
            ss = 'image: %s'%(img)
            return ss

        md_mod = re.sub('!\[([^\]]*)\]\(([^\)]*)\)', repr_alg, self._md)
        md_mod = re.sub('^image: (.+[png|jpeg|jpg])$', repr_alg_2, md_mod, flags=re.MULTILINE)
        return md_mod

    def download(self, path):
        if not os.path.isdir(path):
             os.makedirs(path)
        for img in self.imgs:
            if validators.url(img):
                if not img.split('/')[-1].split('?')[0] in os.listdir(path):
                    try:
                        wget.download(img, path)
                    except:
                        print('unable to downlaod %s', img)
                else:
                    print("Image already in folder!")

def main(jk_folder):
    import os
    path = os.path.join(jk_folder, '_posts/')
    text_files = [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.md') or f.endswith('.markdown')]
    for f in text_files:
        print('working on: ', f.split('/')[-1])
        content = ''
        with open(f, 'r') as content_file:
            content = content_file.read()
        im = ImageManager(content)
        img_path = 'assets/imgs/' + f.split('/')[-1]
        im.download(os.path.join(jk_folder, img_path))
        with open(f, 'w') as content_file:
            content = content_file.write(im.replace_path_imgs('/'+img_path))

if __name__ == '__main__':
    import sys
    print (sys.argv)
    main(sys.argv[1])
