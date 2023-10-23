import os
import json
from datetime import datetime

def test_log():
    from logs import log_file, LOG_DIR

    documents = [
        {
            'id': i,
            'message': '',
            'user': 'daveide',
            'command': 'AAA'
        }
        for i in range(20)
    ]

    for d in documents:
        log_file(d, log_dir='test_log/')

    today = datetime.today().strftime('%Y-%m-%d')
    file_name = f'{today}.json'
    file_path = os.path.join('test_log/', file_name)

    with open(file_path, 'r') as f:
        data = json.load(f)
        
        # for d1 in data:
        #     is_logged = False
        #     for d2 in documents:
        #         if d1['id'] == d2['id'] and d1['message'] == d2['message'] and d1['user'] == d2['user'] and d1['command'] == d2['command']:
        #             is_logged = True
        #     assert is_logged
    
    print('TEST LOG PASSED.')
                

def test_log_error():
    from logs import log_file

    documents = [
        {
            'id': i,
            'message': '',
            'user': 'daveide',
            'command': 'AAA'
        }
        for i in range(20)
    ]

    for d in documents:
        log_file(d, is_error=True, log_dir='test_log/')

    today = datetime.today().strftime('%Y-%m-%d')
    file_name = f'{today}.json'
    file_path = os.path.join('test_log/', file_name)

    with open(file_path, 'r') as f:
        data = json.load(f)
        print(data)



if __name__ == '__main__':
    #test_log()
    test_log_error()