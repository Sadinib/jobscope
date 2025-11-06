# test_celery.py
import sys
import os
import time
sys.path.append('.')

from tasks.scraping_tasks import manual_scrape

print("🚀 ENVIANDO TAREA A CELERY...")
result = manual_scrape.delay("python", "Medellín")
print(f"📨 Tarea ID: {result.id}")

print("⏳ El scraping está corriendo en segundo plano...")
print("💡 Puedes seguir usando esta terminal mientras Celery trabaja")

# Opción 1: Esperar resultado (recomendado para primera prueba)
try:
    print("🕒 Esperando resultado 10 minutos...")
    output = result.get(timeout=600)  # 5 minutos timeout
    print("\n✅ RESULTADO OBTENIDO:")
    print(f"   Status: {output['status']}")
    print(f"   Total trabajos: {output['total_jobs']}")
    print(f"   Búsqueda: {output['query']} en {output['location']}")
except Exception as e:
    print(f"❌ Error: {e}")