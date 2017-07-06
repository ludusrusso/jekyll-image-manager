import unittest
from jekyll_image import ImageManager

class TestDetectImagesMarkdown(unittest.TestCase):

    def setUp(self):
        print('starting')

    def tearDown(self):
        import os
        os.system('rm -rf ./imgs')

    def test_no_image(self):
        ss = '''
            #Markdown
            with no image
        '''

        img_det = ImageManager(ss)
        self.assertFalse(img_det.imgs)

    def test_one_image(self):
        ss = '''
            #Markdown
            with image
            ![lkjsd](img.png)
        '''
        img_det = ImageManager(ss)
        self.assertTrue(img_det.imgs)
        self.assertTrue('img.png' in img_det.imgs)
        self.assertEqual(len(img_det.imgs), 1)

    def test_general(self):
        for i in range(1,5):
            text, imgs = self.create_random_text_with_img(i)
            img_det = ImageManager(text)
            self.assertTrue(img_det.imgs)
            self.assertEqual(len(img_det.imgs), i)
            for img in imgs:
                self.assertTrue(img[1] in img_det.imgs)

    def test_path_replace_no(self):
        ss = '''
            #Markdown
            with no image
        '''
        img_det = ImageManager(ss)
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
        img_det = ImageManager(ss)
        self.assertEqual(ss_expected_1, img_det.replace_path_imgs('/main'))
        self.assertEqual(ss_expected_2, img_det.replace_path_imgs('main'))

    def test_path_replace_multiple(self):
        for i in range(1,5):
            text_list = self.create_random_text_list(i)
            imgs_list = self.create_random_imgs(i)
            path = '/complex_path/test/'
            imgs_list_expected = [ [img[0], path + img[1].split('/')[-1]] for img in imgs_list]
            text = self.merge_text_and_img_lists(text_list,imgs_list)
            text_expected = self.merge_text_and_img_lists(text_list,imgs_list_expected)
            img_det = ImageManager(text)
            self.assertEqual(text_expected, img_det.replace_path_imgs(path))

    def test_download_img(self):
        import os
        url = 'http://www.rokers.io/img/logo.png'
        imgs = [['logo rokers', url], ['image', 'img.png']]
        text = self.create_random_text_from_img_list(imgs)
        img_det = ImageManager(text)
        img_det.download('./imgs/')
        self.assertTrue(os.path.isdir("./imgs/"))
        self.assertTrue(os.path.exists("./imgs/logo.png"))

    def create_random_text_list(self, n_imgs):
        from faker import Factory
        import random
        import urllib.parse

        texts = []
        fake = Factory.create('it_IT')
        for _ in range(n_imgs):
            texts.append(fake.text())
        return texts

    def test_path_replace_any(self):
        import os.path
        for i in range(1,20):
            text, imgs = self.create_random_text_with_img(i)
            img_det = ImageManager(text)
            path = '/img/test/'
            img_repr = [path+img.split('/')[-1] for img in img_det.imgs]

    def create_random_text_from_img_list(self, imgs):
        texts = self.create_random_text_list(len(imgs))
        return self.merge_text_and_img_lists(texts,imgs)

    def merge_text_and_img_lists(self, text_list, imgs):
        text = ''
        for img, t in zip(imgs, text_list):
            text = text + '\n' + t
            text = text + '\n'+ '![%s](%s)'%(img[0],img[1])
        return text


    def create_random_imgs(self, n_imgs):
        from faker import Factory
        import random
        import urllib.parse
        fake = Factory.create('it_IT')
        imgs = []
        for _ in range(n_imgs):
            img_name = fake.file_path(depth=random.choice([2,3,4]), category=None, extension='png')
            if random.choice([True, False]):
                img_name = urllib.parse.urljoin(fake.uri(), img_name)
            imgs.append([fake.name(), img_name])
        return imgs



    def create_random_text_with_img(self, n_imgs):
        imgs = self.create_random_imgs(n_imgs)
        text = self.create_random_text_from_img_list(imgs)
        return text, imgs


if __name__ == '__main__':
    unittest.main()
