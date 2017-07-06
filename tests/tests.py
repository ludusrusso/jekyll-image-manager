import unittest
from jekyll_image import ImageDetector

class TestDetectImagesMarkdown(unittest.TestCase):

    def test_no_image(self):
        ss = '''
            #Markdown
            with no image
        '''

        img_det = ImageDetector(ss)
        self.assertFalse(img_det.imgs)

    def test_one_image(self):
        ss = '''
            #Markdown
            with image
            ![lkjsd](img.png)
        '''
        img_det = ImageDetector(ss)
        self.assertTrue(img_det.imgs)
        self.assertTrue('img.png' in img_det.imgs)
        self.assertEqual(len(img_det.imgs), 1)

    def test_general(self):
        for i in range(1,20):
            text, imgs = self.create_random_text_with_img(i)
            img_det = ImageDetector(text)
            self.assertTrue(img_det.imgs)
            self.assertEqual(len(img_det.imgs), i)
            for img in imgs:
                self.assertTrue(img in img_det.imgs)

    def test_path_replace_no(self):
        ss = '''
            #Markdown
            with no image
        '''
        img_det = ImageDetector(ss)
        self.assertEqual(ss, img_det.replace_path_imgs('/main'))

    def test_path_replace_one(self):
        ss = '''
            #Markdown
            with image
            ![lkjsd](img.png)
        '''

        ss_expected_1 = '''
            #Markdown
            with image
            ![lkjsd](/main/img.png)
        '''

        ss_expected_2 = '''
            #Markdown
            with image
            ![lkjsd](main/img.png)
        '''
        img_det = ImageDetector(ss)
        self.assertEqual(ss_expected_1, img_det.replace_path_imgs('/main'))
        self.assertEqual(ss_expected_2, img_det.replace_path_imgs('main'))


    def create_random_text_with_img(self, n_img):
        from faker import Factory
        import random
        import urllib.parse

        text = ''
        imgs = []
        fake = Factory.create('it_IT')
        for _ in range(n_img):
            text = text + '\n' + fake.text()
            img = fake.file_path(depth=random.choice([2,3,4]), category=None, extension='png')
            if random.choice([True, False]):
                img = urllib.parse.urljoin(fake.uri(), img)
            text = text + '\n'+ '![%s](%s)'%(fake.name(),img)
            imgs.append(img)
        return text, imgs


if __name__ == '__main__':
    unittest.main()
