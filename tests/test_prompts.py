import unittest
from aphra.prompts import get_prompt

class TestPrompts(unittest.TestCase):
    """
    Test cases for the prompt functions in the aphra module.
    """

    def test_get_prompt(self):
        """
        Test getting a prompt and formatting it correctly.
        """
        file_name = 'step1_system.txt'
        prompt = get_prompt(file_name, source_language='Spanish', target_language='English')
        self.assertIn('Spanish', prompt)

if __name__ == '__main__':
    unittest.main()
