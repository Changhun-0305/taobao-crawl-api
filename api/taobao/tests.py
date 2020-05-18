from django.test import TestCase
from django.test import Client
import json

# Create your tests here.
class TaobaoTest(TestCase):
    def setUp(self):
        client = Client()
        response = client.get('/taobao/?id=565838198470')
        self.json_data = json.loads(response.content.decode('utf-8'))

    def test_product_name(self):
        self.assertEqual(self.json_data['title'], '벨벳 야구 유니폼, 실제 보관. 지퍼 재킷')
    
    def test_product_price(self):
        self.assertEqual(self.json_data['price'], '315.00')
    
    def test_product_options(self):
        self.assertEqual(self.json_data['options'], [{'크기': ['에스', '미디엄', '엘', '특대']}, {'색상 분류': ['회색', '분홍']}])