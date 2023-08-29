#!/bin/bash

python3 migrate.py config.ini & wait
python3 consumer.py config.ini &
python3 producer.py config.ini &