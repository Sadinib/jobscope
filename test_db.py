from db.db import db

try:
    db.command("ping")
    print("✅ Conectado a MongoDB Atlas correctamente")
except Exception as e:
    print("❌ Error de conexión:", e)
