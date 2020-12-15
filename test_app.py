import unittest
import requests
import os
import time


class FlaskTest(unittest.TestCase):
    def setUp(self):  # run at the beginning of the test
        os.environ['NO_PROXY'] = '0.0.0.0'

    def tearDown(self):  # runs at the end of the test
        pass

    def test_a_index(self):
        response = requests.get('http://localhost:5000')
        self.assertEqual(response.status_code, 200)

    def test_b_find_similarTweets(self):
        payload = {
            # tweet with id=200
            'search': "Poll numbers are starting to look very good. Leading in Florida @CNN Arizona and big jump in Utah. All numbers rising, national way up. Wow"
        }

        response = requests.post('http://localhost:5000', data=payload)
        self.assertEqual(response.status_code, 200)
        # vérifier que le retour au niveau du tableau de rank contient id du tweet c'est à dire 200
        # self.assertEqual(response.content,'id')

    def test_c_check_if_app_can_handle_1000request_per_minute(self):
        # verifier si l'app peut traiter 1000 requete par minute
        payload = {  # tweet with id=200
            'search': "Poll numbers are starting to look very good. Leading in Florida @CNN Arizona and big jump in Utah. All numbers rising, national way up. Wow"
        }
        a = [*range(1, 1001, 1)]
        start_time = time.time()
        for i in a:
            response = requests.post('http://localhost:5000', data=payload)
            self.assertEqual(response.status_code, 200)
            # vérifier que le retour au niveau du tableau de rank contient id du tweet c'est à dire 200
            # self.assertEqual(response.content,'id')
        self.assertTrue(time.time() - start_time <= 60)


if __name__ == '__main__':
    unittest.main()
