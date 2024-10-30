# tasks.py
from celery import shared_task
from .models import MagnetLink
from .utils import get_seeds_leechers_and_name, ensure_magnet_link
import os
import asyncio

@shared_task
def update_magnetlinks():
    print("Obtaining results")
    magnetlinks = MagnetLink.objects.all()
    for link in magnetlinks:
        
        magnetlink = ensure_magnet_link(link.magnetlink)    
        print(magnetlink)
        try:
            seeders, leechers, torrent_name = asyncio.run(get_seeds_leechers_and_name(magnetlink))
            if seeders or leechers:
                link.seeders = seeders
                link.leechers = leechers
                link.filename = torrent_name
                print(torrent_name)
                link.save()
                print(f"seeders:{seeders}, leechers:{leechers}")
        except Exception as e:
            print(f"Error actualizando link {link.id}: {e}")
    # onces the stuff is done delete all files
    print("deleting metadata")
    os.system("rm metadata/* -Rf" )
