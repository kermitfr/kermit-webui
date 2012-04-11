#!/bin/bash

python src/webui/manage.py dumpdata --indent=4 > $1
