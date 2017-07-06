import unittest
from jekyll_image import ImageDetector

class TestDetectImagesMarkdown(unittest.TestCase):

    def setUp(self):
        print('starting test')

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
        pass

    def create_random_text_with_img(self, n_img):
        from faker import Factory
        text = ''
        imgs = []
        fake = Factory.create('it_IT')
        for _ in range(n_img):
            '\n'.join([text, fake.text()])
            img = faker.file_name(category=None, extension='png')


if __name__ == '__main__':
    unittest.main()
