"""
Safe Database Connection & Portfolio Data Diagnostic Tool.
Tests current connection and prints record counts without exposing credentials.
"""
import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio.settings")

import django
django.setup()

from django.db import connection
from django.conf import settings
from website.models import (
    Profile,
    SocialLink,
    Skill,
    Experience,
    Project,
    Education,
    Certificate,
    Contact,
)
from ai_calling.models import (
    ResumeKnowledgeChunk,
    ChatInteraction,
)

def run_diagnostic():
    db_config = settings.DATABASES['default']
    engine = db_config.get('ENGINE', '')
    name = db_config.get('NAME', '')
    host = db_config.get('HOST', '')

    print("=" * 60)
    print("DJANGO DATABASE DIAGNOSTIC REPORT")
    print("=" * 60)
    print(f"Backend Engine : {engine}")
    print(f"Database Name  : {name}")
    if host:
        # Mask host if long, or show safely
        if len(host) > 12:
            masked_host = host[:4] + "..." + host[-8:]
        else:
            masked_host = host
        print(f"Host           : {masked_host}")
    else:
        print("Host           : (Local File/Default)")

    # Test connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()
        print("Connection     : [SUCCESS] Successfully connected to database!")
    except Exception as exc:
        print(f"Connection     : [FAILED] Could not connect: {exc}")
        return

    print("\n--- Portfolio Data Record Counts ---")
    models_to_check = [
        ("Profile", Profile),
        ("Social Links", SocialLink),
        ("Skills", Skill),
        ("Experiences", Experience),
        ("Projects", Project),
        ("Education", Education),
        ("Certificates", Certificate),
        ("Contacts", Contact),
        ("AI Resume Knowledge", ResumeKnowledgeChunk),
        ("AI Chat Interactions", ChatInteraction),
    ]

    total_records = 0
    for label, model in models_to_check:
        try:
            count = model.objects.count()
            total_records += count
            status = f"{count} record(s)" if count > 0 else "0 (EMPTY)"
            print(f"  {label:<22}: {status}")
        except Exception as e:
            print(f"  {label:<22}: [Error querying table: {e}]")

    print("-" * 60)
    if total_records == 0:
        print("NOTICE: Database connected, but tables are currently empty.")
        print("Run `python manage.py migrate` and `python manage.py seed_data` to populate.")
    else:
        print(f"STATUS: Found {total_records} total portfolio records in this database.")
    print("=" * 60)

if __name__ == "__main__":
    run_diagnostic()
