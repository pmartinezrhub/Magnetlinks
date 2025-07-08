import sqlite3
from django.contrib.auth.hashers import make_password
import getpass

# Pedir contraseña de forma segura
nueva_password = getpass.getpass("Introduce la nueva contraseña para el usuario 'admin': ")

# Generar el hash
hash_password = make_password(nueva_password)

# Conectar a SQLite
conn = sqlite3.connect('db.sqlite3')  # Ajusta el nombre si es necesario
cursor = conn.cursor()

# Actualizar contraseña
cursor.execute("""
    UPDATE auth_user
    SET password = ?
    WHERE username = 'admin';
""", (hash_password,))

conn.commit()
conn.close()

print("✅ Contraseña actualizada con éxito.")
