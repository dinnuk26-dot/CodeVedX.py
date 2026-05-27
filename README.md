# CodeVedX.py
# Task Automation Tool

## Overview

Task Automation Tool is a Python-based automation system designed to reduce repetitive manual tasks such as:

- File organization
- Automated email sending
- Report generation
- Logging and monitoring

The project is modular, configurable, and easy to extend.

---

# Features

## File Organization
- Automatically categorizes files by extension
- Creates folders dynamically
- Handles unknown file types

## Email Automation
- Sends task completion reports
- Supports attachments

## Report Generation
- Generates CSV reports
- Tracks execution timestamps

## Logging
- Maintains execution logs
- Captures errors and task status

## Scheduling
- Runs tasks automatically at fixed intervals
//
---

# Technologies Used

- Python 3
- schedule
- smtplib
- logging
- csv
- shutil
- os

---

# Project Structure

```bash
task-automation-tool/
│
├── main.py
├── config.json
├── requirements.txt
├── README.md
│
├── logs/
├── reports/
├── organized_files/
├── sample_files/
│
└── modules/
    ├── file_organizer.py
    ├── email_sender.py
    ├── report_generator.py
    └── logger_setup.py
```
//
---

# Installation

## Clone Repository

```bash
git clone https://github.com/dinnuk26-dot/task-automation-tool.git
```

## Move into Project Directory

```bash
cd task-automation-tool
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Usage

## Add Files

Place files inside:

```bash
sample_files/
```

## Run Application

,,,bash
python main.py
---

---

# Configuration

Modify `config.json` to customize:

- Source folder
- Destination folder
- Email settings
- Scheduler interval

---

# Email Configuration

For Gmail:

1. Enable 2-Step Verification
2. Generate App Password
3. Use App Password in `config.json`

---

# Output

## Organized Files

Files will be sorted into:

- Images
- Documents
- Videos
- Music
- Archives
- Others

## Logs

Logs stored in:

```bash
logs/automation.log
```

## Reports

Reports stored in:

```bash
reports/task_report.csv
```

---

# Future Enhancements

- GUI Dashboard
- Cloud Integration
- AI File Classification
- Database Support
- Multi-threading

---

# Author

Your Name
dinnuk26-dot

# License

MIT License
