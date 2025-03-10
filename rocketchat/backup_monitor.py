#!/usr/bin/env python3

import os
import glob
from datetime import datetime
import requests
import json

class BackupMonitor:
    def __init__(self, backup_folder, rocket_chat_webhook):
        self.backup_folder = backup_folder
        self.rocket_chat_webhook = rocket_chat_webhook
        self.outdated_backups = []

    def scan_backups(self):
        """Scan backup folders and check for outdated backups"""
        for client_dir in os.scandir(self.backup_folder):
            if not client_dir.is_dir() or client_dir.name == 'Archives' or client_dir.name.startswith('.'):
                continue

            # Check if client has nested folders
            subdirs = [d for d in os.scandir(client_dir.path) if d.is_dir() and not d.name.startswith('.')]
            
            if subdirs:  # Process nested folders
                for subdir in subdirs:
                    self._process_backup_folder(subdir.path, f"{client_dir.name}/{subdir.name}")
            else:  # Process client folder directly
                self._process_backup_folder(client_dir.path, client_dir.name)

    def _process_backup_folder(self, folder_path, display_name):
        """Process a single backup folder"""
        # Get latest zip file
        zip_files = glob.glob(os.path.join(folder_path, '*.zip'))
        if not zip_files:
            self.outdated_backups.append({
                'client': display_name,
                'status': 'No backups found',
                'days_old': 'N/A',
                'expected_frequency': 'N/A'
            })
            return

        latest_backup = max(zip_files, key=os.path.getctime)
        backup_time = datetime.fromtimestamp(os.path.getctime(latest_backup))
        days_old = (datetime.now() - backup_time).days

        # Get expected backup frequency from count.txt
        count_file = os.path.join(folder_path, 'count.txt')
        try:
            with open(count_file, 'r') as f:
                line = f.readline().strip()
                expected_days = int(line.split('=')[1])
        except:
            expected_days = 3

        if days_old > expected_days:
            self.outdated_backups.append({
                'client': display_name,
                'status': 'Outdated backup',
                'days_old': days_old,
                'expected_frequency': expected_days,
                'last_backup': backup_time.strftime('%Y-%m-%d %H:%M:%S')
            })

    def send_alert(self):
        """Send alert to RocketChat if there are outdated backups"""
        if not self.outdated_backups:
            print("No outdated backups found.")
            return

        message = "🚨 *Outdated Backup Alert*\n\n"
        for backup in self.outdated_backups:
            if backup['status'] == 'No backups found':
                message += f"⚠️ *{backup['client']}*: No backup files found!\n\n"
            else:
                message += (f"⚠️ *{backup['client']}*\n"
                          f"- Last backup: {backup['last_backup']}\n"
                          f"- Days since last backup: {backup['days_old']}\n"
                          f"- Expected backup frequency: {backup['expected_frequency']} days\n\n")

        # Print message to console
        print("\nPreparing to send the following message to RocketChat:")
        print("-" * 50)
        print(message)
        print("-" * 50)

        payload = {
            "text": message,
            "alias": "Backup Monitor"
        }

        try:
            response = requests.post(
                self.rocket_chat_webhook,
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            print("✅ Message successfully sent to RocketChat")
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to send alert to RocketChat: {e}")

def main():
    # Configure these variables
    BACKUP_FOLDER = 'Projects/nextcloud-backup-analyzer/Backups/'
    ROCKETCHAT_WEBHOOK = 'https://rocketdomain.com/hooks/X'

    monitor = BackupMonitor(BACKUP_FOLDER, ROCKETCHAT_WEBHOOK)
    monitor.scan_backups()
    monitor.send_alert()

if __name__ == "__main__":
    main() 