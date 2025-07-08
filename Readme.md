What is this project
This is a base for magnetlink tracking website

Why this project?
P2P is the best way of sharing, cause a few bunch of reasons, this is my own contribution to the Bittorrent Network

This is not a tracker!!! But it can give you some information about the status of the files shared in the Bittorrent Network

Why magnetlinks?
In short, magnet links are lighter, more convenient, and less dependent on central servers, making them a more robust and secure option for sharing content on P2P networks.

What it needs to run?
This is a Django project so it needs django-framework
Also it uses Celery for async tasks (Bittorrent network checks)
Database is SQLite at the moment. 

How to deploy:

<pre>
cd magnetlinks
source bin activate
python manage runserver
</pre>

You need a redis server so in the host:
<pre>
apt install redis celery
</pre>
then you can launch 
<pre>
./celery_worker.sh
</pre>
and 
<pre>
./celery_beat.sh
</pre>

Docker compose:
<pre>
docker-compose up --build 
</pre>
Contact pmartinezr@proton.me
