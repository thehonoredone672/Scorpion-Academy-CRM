import random
from django.core.management.base import BaseCommand
from django.db import connection
from crm.models import Branch, Lead, Student

class Command(BaseCommand):
    help = 'Seeds the MongoDB database with explicitly mapped Django Integer IDs'

    def handle(self, *args, **kwargs):
        self.stdout.write('Wiping old data...')
        
        db = connection.cursor().db_conn
        branch_col = db[Branch._meta.db_table]
        student_col = db[Student._meta.db_table]
        lead_col = db[Lead._meta.db_table]

        student_col.delete_many({})
        lead_col.delete_many({})
        branch_col.delete_many({})

        self.stdout.write('Creating Branch...')
        # THE FIX: Explicitly add "id": 1 so Django's API can see it
        branch_col.insert_one({
            "id": 1,  # <--- Django needs this!
            "name": "Scorpion Academy", 
            "slug": "coimbatore-main", 
            "password": "dojo123", 
            "instructor": "Sensei Kumar"
        })

        self.stdout.write('Generating Fake Students...')
        first_names = ["Arjun", "Priya", "Rahul", "Neha", "Vikram", "Ananya", "Siddharth", "Kavya", "Rohan", "Meera"]
        last_initials = ["M.", "S.", "K.", "D.", "T.", "P.", "V.", "N.", "R.", "L."]
        belts = ["White", "White", "Yellow", "Yellow", "Orange", "Green", "Blue", "Brown", "Black"]
        
        students = []
        for i in range(24): 
            students.append({
                "id": i + 1,          # <--- Django needs this!
                "branch_id": 1,       # <--- Link it to Branch #1
                "name": f"{random.choice(first_names)} {random.choice(last_initials)}",
                "beltRank": random.choice(belts),
                "phone": f"98{random.randint(10000000, 99999999)}"
            })
        student_col.insert_many(students)

        self.stdout.write('Generating Fake Enquiries...')
        programs = ["Karate", "Silambam", "Yoga"]
        statuses = ["New", "New", "Contacted", "Trial Booked", "Follow Up"]
        
        leads = []
        for i in range(12): 
            leads.append({
                "id": i + 1,          # <--- Django needs this!
                "branch_id": 1,       # <--- Link it to Branch #1
                "name": f"{random.choice(first_names)} {random.choice(last_initials)}",
                "phone": f"91{random.randint(10000000, 99999999)}",
                "program": random.choice(programs),
                "status": random.choice(statuses)
            })
        lead_col.insert_many(leads)

        self.stdout.write(self.style.SUCCESS('Successfully seeded database! Added 24 Students and 12 Leads.'))