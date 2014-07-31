#!/bin/bash

PYTHONPATH=. django-admin.py syncdb $@

