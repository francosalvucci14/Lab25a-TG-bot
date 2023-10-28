import os
from datetime import datetime
import json

LOG_DIR = 'log/'

def log_file(
    document: dict,
    log_dir: str = LOG_DIR,
    is_error: bool = False
):


    if document is None:
        return

    # verifica se esiste la cartella di log
    if not os.path.exists(log_dir):
        # crea una cartella di log
        os.mkdir(log_dir)

    today = datetime.today().strftime('%Y-%m-%d')
    if not is_error:
        file_name = f'{today}.json'
    else:
        file_name = f'{today}.error.json'

    file_path = os.path.join(log_dir, file_name)

    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump([], f)

    data = []
    with open(file_path, 'r') as f:
        data = json.load(f)

    document['date'] = datetime.now().isoformat()
    data.append(document)

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def log_file_cand(
    document: dict,
    log_dir: str = LOG_DIR
):


    if document is None:
        return

    # verifica se esiste la cartella di log
    if not os.path.exists(log_dir):
        # crea una cartella di log
        os.mkdir(log_dir)

    #today = datetime.today().strftime('%Y-%m-%d')
    file_name = f'cand.json'

    file_path = os.path.join(log_dir, file_name)

    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump([], f)

    data = []
    with open(file_path, 'r') as f:
        data = json.load(f)

    document['date'] = datetime.now().isoformat()
    data.append(document)

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)