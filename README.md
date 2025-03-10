# Backup Monitor Script

This Python script monitors backup directories for outdated or missing backups and sends alerts to RocketChat. It's designed to work with a Nextcloud backup solution and supports nested folder structures for multiple databases per client.

## Features

- Monitors backup folders for outdated or missing backups
- Supports nested folder structure (one level deep)
- Configurable backup frequency per folder using count.txt files
- Sends formatted alerts to RocketChat
- Console output for monitoring and debugging

## Requirements

- Python 3.x
- `requests` library (install using `pip install requests`)

## Installation

1. Clone the repository or download the script
2. Install required dependencies:

```bash
pip install requests
```

## Configuration

### Script Variables

In `backup_monitor.py`, configure these variables:

```python
BACKUP_FOLDER = '/path/to/your/backups/' # Root path to backup directories
ROCKETCHAT_WEBHOOK = 'your_webhook_url' # RocketChat webhook URL
```

### Backup Folder Structure

The script supports the following folder structures:

```
Backups/
├── Client1/
│ ├── Database1/
│ │ ├── backup.zip
│ │ └── count.txt
│ └── Database2/
│ ├── backup.zip
│ └── count.txt
└── Client2/
├── backup.zip
└── count.txt
```

### count.txt Format

Each backup folder can contain a `count.txt` file to specify the maximum allowed age of backups:

```
days=3
```

If `count.txt` is missing or invalid, the default value is 3 days.

## Usage

Run the script:

```bash
python3 backup_monitor.py
```

## Alert Format

The script sends alerts to RocketChat in the following format:

```bash
🚨 Outdated Backup Alert
⚠️ ClientName/DatabaseName
Last backup: YYYY-MM-DD HH:MM:SS
Days since last backup: X
Expected backup frequency: Y days
⚠️ ClientName: No backup files found!
```

## Error Handling

- The script skips the 'Archives' folder and hidden folders (starting with '.')
- Invalid count.txt files default to 3 days
- Failed RocketChat notifications are logged to console
- Missing backup folders are reported as "No backup files found"

## Console Output

The script provides console output for monitoring:
- Confirmation when no outdated backups are found
- Preview of the message being sent to RocketChat
- Success/failure status of RocketChat notification

## Author

[Michael Vaynagiy]
