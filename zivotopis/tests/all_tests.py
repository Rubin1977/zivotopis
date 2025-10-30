import os
import sys
import django
import unittest

# --- Inicializácia Django prostredia ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zivotopis.settings')
django.setup()

# --- Vytvorenie testového loadera a suite ---
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# --- Základný adresár testov ---
base_dir = os.path.dirname(__file__)

# --- Automatické objavenie testov vo všetkých podpriečinkoch ---
for subfolder in ['test_db', 'test_save']:
    path = os.path.join(base_dir, subfolder)
    suite.addTests(loader.discover(start_dir=path, pattern='test_*.py'))

# --- Spustenie testov ---
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

# --- Ukončenie procesu, aby Django nespúšťal testy druhýkrát ---
# (ak testy prebehli úspešne, návratový kód bude 0)
sys.exit(0 if result.wasSuccessful() else 1)
