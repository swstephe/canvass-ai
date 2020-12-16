# -*- coding: utf8 -*-
from contextlib import closing
from datetime import datetime
from http.client import HTTPConnection
import json
import os
import unittest

from assignment import transform
from assignment.app import PORT

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
NoneType = type(None)


class TestTransform(unittest.TestCase):
    def test_transform_datetime(self):
        dt = datetime.utcnow().isoformat()
        self.assertIsInstance(transform.transform_datetime(dt), int)
        self.assertEqual(transform.transform_datetime(212), 212000)
        self.assertEqual(transform.transform_datetime(211.9), 211900)
        self.assertIsNone(transform.transform_datetime('foo'))

    def test_transform_numeric(self):
        dt = datetime.utcnow().isoformat()
        self.assertIsNone(transform.transform_numeric(dt))
        self.assertEqual(transform.transform_numeric("212"), 212)
        self.assertEqual(transform.transform_numeric("211.9"), 211.9)
        self.assertEqual(transform.transform_numeric(212), 212)
        self.assertEqual(transform.transform_numeric(211.9), 211.9)
        self.assertIsNone(transform.transform_numeric('foo'))

    def test_transform_string(self):
        dt = datetime.utcnow().isoformat()
        self.assertEqual(transform.transform_string(dt), dt)
        self.assertEqual(transform.transform_string("212"), "212")
        self.assertEqual(transform.transform_string("211.9"), "211.9")
        self.assertEqual(transform.transform_string(212), "212")
        self.assertEqual(transform.transform_string(211.9), "211.9")
        self.assertEqual(transform.transform_string("foo"), "foo")

    def test_transform_value(self):
        self.assertEqual(transform.transform_value("212"), dict(
            datetime=212000,
            numeric=212,
            string="212"
        ))
        self.assertEqual(transform.transform_value("211.9"), dict(
            datetime=211900,
            numeric=211.9,
            string="211.9"
        ))
        self.assertEqual(transform.transform_value(212), dict(
            datetime=212000,
            numeric=212,
            string="212"
        ))
        self.assertEqual(transform.transform_value(211.9), dict(
            datetime=211900,
            numeric=211.9,
            string="211.9"
        ))
        self.assertEqual(transform.transform_value("foo"), dict(
            datetime=None,
            numeric=None,
            string="foo"
        ))

    def transform_transform(self):
        dt = datetime.utcnow()
        data_in = dict(
            deviceId='transform_transform',
            timestamp=dt.isoformat(),
            readingA=dt.isoformat(),
            readingB='212',
            readingC='211.9',
            readingD=212,
            readingE=211.9,
            readingF='foo'
        )
        data_out = dict(
            source=data_in['deviceId'],
            timestamp=int(dt.timestamp()*1000),
            data=dict(
                readingA=dict(
                    datetime=int(dt.timestamp()*1000),
                    numeric=None,
                    string=dt.isoformat()
                ),
                readingB=dict(
                    datetime=212000,
                    numeric=212,
                    string='212'
                ),
                readingC=dict(
                    datetime=211900,
                    numeric=211.9,
                    string='211.9'
                ),
                readingD=dict(
                    datetime=212000,
                    numeric=212,
                    string='212'
                ),
                readingE=dict(
                    datetime=211900,
                    numeric=211.9,
                    string='211.9'
                ),
                readingF=dict(
                    datetime=None,
                    numeric=None,
                    string='foo'
                )
            )
        )
        _data = transform.transform(data_in)
        self.assertEqual(_data, data_out)


class TestApp(unittest.TestCase):
    def send_data(self, data):
        with closing(HTTPConnection(f'localhost:{PORT}')) as conn:
            if isinstance(data, str):
                data = data.encode('utf8')
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Content-Length': str(len(data))
            }
            conn.request('POST', '/', data, headers=headers)
            response = conn.getresponse()
            self.assertEqual(response.status, 200)
            return json.loads(response.read())

    def send_file(self, path):
        with open(path) as f:
            return self.send_data(f.read())

    def assert_any_sensor(self, data_in, data_out):
        self.assertIn('source', data_out)
        self.assertEqual(data_in['deviceId'], data_out['source'])
        self.assertIn('timestamp', data_out)
        self.assertEqual(transform.transform_datetime(data_in['timestamp']), data_out['timestamp'])
        for k, v in data_out['data'].items():
            self.assertIn(k, data_in)
            self.assertIn('string', v)
            self.assertIsInstance(v['string'], (str, NoneType))
            self.assertIn('numeric', v)
            self.assertIsInstance(v['numeric'], (int, float, NoneType))
            self.assertIn('datetime', v)
            self.assertIsInstance(v['datetime'], (int, NoneType))

    def test_sensor_1(self):
        path = os.path.join(DATA_DIR, 'sensor-1.json')
        with open(path) as f:
            data_in = json.load(f)
        data_out = self.send_file(path)
        self.assert_any_sensor(data_in, data_out)

    def test_sensor_2(self):
        path = os.path.join(DATA_DIR, 'sensor-2.json')
        with open(path) as f:
            data_in = json.load(f)
        data_out = self.send_file(path)
        self.assert_any_sensor(data_in, data_out)


if __name__ == '__main__':
    unittest.main()
