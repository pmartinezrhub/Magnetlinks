# utils.py

import libtorrent as lt
import time
from asgiref.sync import sync_to_async
import re

@sync_to_async
def get_seeds_leechers_and_name(magnet_link):
    session = lt.session()
    session.listen_on(6881, 6891)

    params = {
        'save_path': 'metadata',
    }
    handle = lt.add_magnet_uri(session, magnet_link, params)

    max_attempts = 5  # Número máximo de intentos
    attempts = 0

    while not handle.has_metadata():
        if attempts >= max_attempts:
            print(f"Max attempts reached for {magnet_link}. Metadata not found.")
            return None, None, None  # Salida si no se encuentran metadatos
        
        print(f"Waiting for metadata to be downloaded for {magnet_link}... Attempt {attempts + 1}/{max_attempts}")
        time.sleep(5)  # Espera antes de volver a verificar
        attempts += 1

    # Si llegamos aquí, se han encontrado los metadatos
    torrent_info = handle.get_torrent_info()
    torrent_name = torrent_info.name()  
    status = handle.status()
    num_seeders = status.num_seeds
    num_leechers = status.num_peers - status.num_seeds
    total_size = torrent_info.total_size()  
    
    return torrent_name, num_seeders, num_leechers, total_size

def ensure_magnet_link(magnet_link):
    hash_match = re.search(r'btih:([A-Fa-f0-9]{40})', magnet_link)

    if hash_match:
        hash_value = hash_match.group(1)  
    else:
        hash_value = magnet_link if re.match(r'^[A-Fa-f0-9]{40}$', magnet_link) else None
    
    if hash_value:
        magnetlink = f"magnet:?xt=urn:btih:{hash_value}"
    else:
        magnetlink = magnet_link  
        
    return magnetlink