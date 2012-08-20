#!/bin/bash
python src/webui/manage.py loaddata basedata
python src/webui/manage.py loaddata widget
