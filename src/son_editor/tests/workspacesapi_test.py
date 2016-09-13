'''
Created on 26.07.2016

@author: Jonas
'''
import json
import unittest

from son_editor.app.constants import WORKSPACES
from son_editor.app.database import db_session
from son_editor.models.project import Project
from son_editor.models.user import User
from son_editor.models.workspace import Workspace
from son_editor.util.context import init_test_context


class WorkspacesTest(unittest.TestCase):
    def setUp(self):
        # Initializes test context
        self.app = init_test_context()

        # Add some dummy objects
        self.project = Project(name="Project A")
        self.user = User(name="user", email="foo@bar.com")
        self.workspace = Workspace(name="Workspace A", owner=self.user)

        # Add some relationships

        db_session.add(self.user)
        db_session.add(self.workspace)
        db_session.commit()

        # Add some session stuff ( need for finding the user's workspace )
        with self.app as c:
            with c.session_transaction() as session:
                session['userData'] = {'login': 'user'}

    def tearDown(self):
        db_session.delete(self.user)
        db_session.delete(self.workspace)
        db_session.commit()

    def testCreateWorkSpace(self):
        request_dict = {"name": "workspaceName"}
        response = self.app.post('/' + WORKSPACES + '/', data=json.dumps(request_dict), content_type='application/json')
        # Expect workspace gets created
        self.assertEqual(request_dict['name'], json.loads(response.data.decode())['name'])
        self.assertEqual(201, response.status_code)

        request_dict = {"name": "workspaceName"}
        response = self.app.post('/' + WORKSPACES + '/', data=json.dumps(request_dict), content_type='application/json')
        # Expect workspace already exists
        self.assertEqual(409, response.status_code)

    def get_wsid(self):
        response = self.app.get('/' + WORKSPACES + '/')

        # Only one workspace was created beforehand
        return int(json.loads(response.data.decode())[0]['id'])

    def testGetWorkSpaces(self):
        response = self.app.get('/' + WORKSPACES + '/')
        self.assertEqual(json.loads(response.data.decode())[0]['name'], "Workspace A")

    def testGetWorkSpace(self):
        response = self.app.get('/' + WORKSPACES + '/{}'.format(self.get_wsid()))
        self.assertEqual(json.loads(response.data.decode())['name'], "Workspace A")

        # test non existing id
        response = self.app.get('/' + WORKSPACES + '/1337')
        self.assertEqual(404, response.status_code)

    def testUpdateWorkSpace(self):
        request_dict = {"name": "workspaceToMove"}
        response = self.app.post('/' + WORKSPACES + '/',
                                 data=json.dumps(request_dict),
                                 content_type='application/json')
        id = json.loads(response.data.decode())['id']

        response = self.app.put('/' + WORKSPACES + '/{}'.format(id), data={"name": "workspaceToMove2"})
        self.assertEqual(json.loads(response.data.decode())['name'], "workspaceToMove2")

        # creating it again with the old name should work
        response = self.app.post('/' + WORKSPACES + '/',
                                 data=json.dumps(request_dict),
                                 content_type='application/json')
        id = json.loads(response.data.decode())['id']

        # renaming again to other name should create a conflict
        response = self.app.put('/' + WORKSPACES + '/{}'.format(id), data={"name": "workspaceToMove2"})
        self.assertEqual(409, response.status_code)

        # try to update non existing
        response = self.app.put('/' + WORKSPACES + '/1337', data={"name": "workspaceToMove2"})
        self.assertEqual(404, response.status_code)

    def testDeleteWorkspace(self):
        # Create at first a workspace
        request_dict = {"name": "workspaceToDelete"}
        response = self.app.post('/' + WORKSPACES + '/', data=json.dumps(request_dict), content_type='application/json',
                                 follow_redirects=True)
        id = json.loads(response.data.decode())['id']
        response = self.app.delete('/' + WORKSPACES + '/{}'.format(id))
        self.assertEqual(200, response.status_code)

        # test workspace no longer exists
        response = self.app.get('/' + WORKSPACES + '/')
        workspaces = json.loads(response.data.decode())
        for workspace in workspaces:
            self.assertNotEqual(request_dict['name'], workspace['name'])


if __name__ == '__main__':
    unittest.main()