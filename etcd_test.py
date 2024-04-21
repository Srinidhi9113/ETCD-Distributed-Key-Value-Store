import unittest
import etcd3

from etcd_client import get_all, get_value, put_kv, delete_kv

class TestEtcdClient(unittest.TestCase):
    def setUp(self):
        self.etcd_client = etcd3.client(host='localhost',port=8080)

    def test_get_all(self):
        put_kv(self.etcd_client,'key1', 'value1')
        put_kv(self.etcd_client,'key2', 'value2')
        result = get_all(self.etcd_client)
        self.assertEqual(result, {'key': ['key1', 'key2'], 'value': ['value1', 'value2']})

    def test_get_one(self):
        result = get_value(self.etcd_client,'key1')
        self.assertEqual(result, {'key': ['key1'], 'value': ['value1']})

    def test_get_none(self):
        result = get_value(self.etcd_client,'nonexistent_key')
        self.assertIsNone(result)

    def test_put_one(self):
        result = put_kv(self.etcd_client,'key', 'value')
        self.assertTrue(result)

    def test_delete_one(self):
        put_kv(self.etcd_client,'key', 'value')
        result = delete_kv(self.etcd_client,'key')
        self.assertTrue(result)

    def test_delete_none(self):
        result = delete_kv(self.etcd_client,'nonexistent_key')
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
