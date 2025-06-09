# scripts/backup_database.py
"""
Script to backup the database
"""
import os
import shutil
from datetime import datetime

def backup_database():
    # Create backup directory if it doesn't exist
    backup_dir = "data/backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    # Database file
    db_file = "backend/kirana_erp.db"
    
    if not os.path.exists(db_file):
        print("Database file not found!")
        return
    
    # Create backup filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"kirana_erp_{timestamp}.db")
    
    # Copy database file
    shutil.copy2(db_file, backup_file)
    
    print(f"Database backed up to: {backup_file}")
    
    # Keep only last 7 backups
    backups = sorted([f for f in os.listdir(backup_dir) if f.endswith('.db')])
    if len(backups) > 7:
        for old_backup in backups[:-7]:
            os.remove(os.path.join(backup_dir, old_backup))
            print(f"Removed old backup: {old_backup}")

if __name__ == "__main__":
    backup_database()
