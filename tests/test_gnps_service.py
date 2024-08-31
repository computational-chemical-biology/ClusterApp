import unittest

import pandas

from api.src.service.gnps import Proteosafe


class TestGnpsService(unittest.TestCase):



    def test_FBMN_get_gnps_request(self):
        workflow = 'FBMN'
        task_id = 'your-task-id'
        gnps = Proteosafe(workflow=workflow, taskid=task_id)
        gnps.get_gnps()
        meta = gnps.meta
        feat = gnps.feat

        self.assertIsNotNone(meta)
        self.assertIsNotNone(feat)
        self.assertIsInstance(meta, pandas.core.frame.DataFrame)
        self.assertIsInstance(feat, pandas.core.frame.DataFrame)

            
    def test_fbmn_get_gnps_request_exception(self):
        workflow = 'FBMN'
        task_id = 'task_id'
        gnps = Proteosafe(workflow=workflow, taskid=task_id)
        with self.assertRaises(Exception) as context:
            gnps.get_gnps()

    def test_V2_get_gnps_request_exception(self):
        workflow = 'V2'
        task_id = 'task_id'
        gnps = Proteosafe(workflow=workflow, taskid=task_id)
        with self.assertRaises(Exception) as context:
            gnps.get_gnps()

            

    def test_FBMN_gnps2_get_gnps_request_exception(self):
        workflow = 'FBMN-gnps2'
        task_id = 'task_id'
        gnps = Proteosafe(workflow=workflow, taskid=task_id)
        with self.assertRaises(Exception) as context:
            gnps.get_gnps()