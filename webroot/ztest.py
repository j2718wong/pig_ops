
import requests

BASE_URL = 'http://localhost:8080/'

class TestAPIAccount:
    
    def test_account_register(self):
        user_uhid   = 'WPG2P2'
        acc_name    = 'Jackson Farm'
        
        url = BASE_URL + 'account/register'
        
        data = {
            "uhid": user_uhid,
            "name": acc_name,
            "country_id": 1
        }
        
        r = requests.post(url, data = data)
        
        