import os
import flaskr
import unittest
import tempfile

class FlaskrTest(unittest.TestCase):

    def set_up(self):
        self.datab_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        flaskr.init_datab()

    def tear_down(self):
        os.close(self.datab_fb)
        os.unlink(flaskr.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()
