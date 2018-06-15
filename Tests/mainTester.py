import unittest

if __name__ == "__main__":
    # RUN THIS FILE TO TEST EVERYTHING
    all_tests = unittest.TestLoader().discover('Tests', pattern='*.py')
    unittest.TextTestRunner().run(all_tests)
