import unittest
from aphra.translate import translate

class TestTranslate(unittest.TestCase):

    def test_translation(self):
        source_language = 'Spanish'
        target_language = 'English'
        text = 'Hola mundo'
        
        translation, = translate(source_language, target_language, text)
        self.assertIsNotNone(translation)

if __name__ == '__main__':
    unittest.main()