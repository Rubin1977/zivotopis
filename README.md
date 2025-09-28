# Django Životopis

Webová aplikácia na prezentáciu životopisu, galérie a dokumentov. Vytvorená pomocou Django 4.2.3. Projekt slúži ako osobná prezentácia autora – obsahuje galériu, formuláre, exporty a REST API.

## 🔧 Inštalácia

```bash
git clone https://github.com/Rubin1977/zivotopis.git
cd zivotopis
python -m venv ruvenv
ruvenv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py runserver
```

📦 Závislosti
Projekt používa nasledujúce knižnice (výber z requirements.txt):

Django==4.2.3

djangorestframework==3.15.1

django-filter, django-recaptcha, django-permissionedforms

beautifulsoup4, requests, python-dotenv

openpyxl, pillow, anyascii, filetype

➡️ Kompletný zoznam nájdeš v súbore requirements.txt.

🌐 Online verzia
Galéria je dostupná na: 👉 rastislavruzbacky.eu.pythonanywhere.com/gallery
