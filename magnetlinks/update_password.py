#!/bin/python

# sorry still not working!!! need a better solution for change admin password 

import sqlite3
from django.contrib.auth.hashers import make_password
import getpass


nueva_password = getpass.getpass("Enter new password for user 'admin': ")


hash_password = make_password(nueva_password)


conn = sqlite3.connect('db.sqlite3')  # Ajusta el nombre si es necesario
cursor = conn.cursor()


cursor.execute("""
    UPDATE auth_user
    SET password = ?
    WHERE username = 'admin';
""", (hash_password,))

conn.commit()
conn.close()

print("✅ Contraseña actualizada con éxito.")
