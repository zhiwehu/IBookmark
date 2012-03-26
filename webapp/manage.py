#!/usr/bin/env python
from django.core.management import execute_from_command_line

import environment

environment.setup_environ(__file__)

if __name__ == "__main__":
    execute_from_command_line()
