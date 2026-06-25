#!/usr/bin/env python
# manage.py — Django's CLI utility. Use this to run the server, create
# migrations, open the shell, and run any management commands.

import os, sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coursemanager.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Django not found. Activate your virtual environment.") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
