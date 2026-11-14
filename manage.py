#!/usr/bin/env python
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockz.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            'No se pudo importar Django. Asegurate de instalar las dependencias del proyecto.'
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
