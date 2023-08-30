#!/bin/bash

sudo python3 migrate.py config.ini & wait
sudo python3 consumer.py config.ini &
sudo python3 producer.py config.ini &