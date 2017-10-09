import flask_rest_api
from flask_rest_api import db
from flask_rest_api.application import create_app
import unittest
import json

from flask_rest_api.problems.models import Problem

class TestView(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def get_ids(self,problems):
        ids=[]
        for i in problems:
            ids.append(i['id'])
        return ids

    def test_post_get_delete(self):
        data={'answer': '-2182',
              'distraction1': '3176',
              'distraction2': ' 6529',
              'distraction3': ' 6903',
              'distraction4': '',
              'distraction5': '',
              'question': 'What is 1754 - 3936?'}

        expected_resp = data

        response = self.client.post('/v1/problems', data=json.dumps(data), content_type='application/json')
        problem = json.loads(response.get_data(as_text=True))

        assert response.status_code == 200

        response = self.client.get('/v1/problems/' + str(problem.get('id')))
        expected_resp['id'] = problem.get('id')

        assert response.status_code == 200

        problem = json.loads(response.get_data(as_text=True))

        assert problem == expected_resp

        response = self.client.delete('/v1/problems/' + str(problem.get('id')))
        assert response.status_code == 204

        response = self.client.get('/v1/problems/' + str(problem.get('id')))
        assert response.status_code == 404
        
    def test_sort(self):

        data={'limit':4,'sort':''}
        response = self.client.post('/v1/problems/filter', data=json.dumps(data), content_type='application/json')
        problems = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200

        assert self.get_ids(problems)==[3, 5, 4, 10]

        data={'limit':4,'sort':'asc'}
        response = self.client.post('/v1/problems/filter', data=json.dumps(data), content_type='application/json')
        problems = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200

        assert self.get_ids(problems)==[7, 8, 1, 9]

    def test_limit_page(self):

        data={'limit':10}
        response = self.client.post('/v1/problems/filter', data=json.dumps(data), content_type='application/json')
        problems = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200

        ids_all = self.get_ids(problems)
        assert len(ids_all)==10

        data={'limit':2,'page_start':2}
        response = self.client.post('/v1/problems/filter', data=json.dumps(data), content_type='application/json')
        problems = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200

        ids_page = self.get_ids(problems)
        assert ids_page==ids_all[2:4]

        data={'limit':2,'page_start':4}
        response = self.client.post('/v1/problems/filter', data=json.dumps(data), content_type='application/json')
        problems = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200

        ids_page = self.get_ids(problems)
        assert ids_page==ids_all[4:6]

    def test_filter_search(self):

        data={'search': '1754'}
        response = self.client.post('/v1/problems/filter', data=json.dumps(data), content_type='application/json')

        assert response.status_code == 200

        problem = json.loads(response.get_data(as_text=True))

        assert '1754' in problem[0]['question']

    def test_get_filter_sort_page_search(self):
        data={'search': ' - ','limit':2,'page_start':2, 'sort':'desc'}
        response = self.client.post('/v1/problems/filter', data=json.dumps(data), content_type='application/json')
        problems = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200

        ids_page = self.get_ids(problems)
        assert ids_page==[9,1]

    def test_put(self):
        data={'answer': '-2182',
              'distraction1': '3176',
              'distraction2': ' 6529',
              'distraction3': ' 6903',
              'distraction4': '',
              'distraction5': '',
              'question': 'What is 1754 - 3936?'}

        data_put={'answer': '0',
              'distraction1': '1',
              'distraction2': '2',
              'distraction3': '3',
              'distraction4': '4',
              'distraction5': '5',
              'question': 'What is 0?'}

        expected_resp = data

        response = self.client.post('/v1/problems', data=json.dumps(data), content_type='application/json')
        problem = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200

        response = self.client.get('/v1/problems/' + str(problem.get('id')))
        expected_resp['id'] = problem.get('id')
        assert response.status_code == 200

        problem = json.loads(response.get_data(as_text=True))
        assert problem == expected_resp

        response = self.client.put('/v1/problems/'+ str(problem.get('id')), data=json.dumps(data_put), content_type='application/json')
        assert response.status_code == 200

        response = self.client.get('/v1/problems/' + str(problem.get('id')))
        expected_resp['id'] = problem.get('id')
        assert response.status_code == 200

        assert problem == expected_resp

    def test_solve(self):

        response = self.client.get('/v1/problems/1/solve/-2182')
        result = json.loads(response.get_data(as_text=True))

        assert response.status_code == 200
        assert result['result']=='correct'

        response = self.client.get('/v1/problems/1/solve/1234')
        result = json.loads(response.get_data(as_text=True))

        assert response.status_code == 200
        assert result['result']=='wrong'

if __name__ == '__main__':
    unittest.main()