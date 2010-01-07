#!/bin/bash

# uso: trabalho_escravo_2006.sh > resultado-2006.csv

export PYTHONPATH=..

tr , ' ' < ministerio_publico.csv | python ../filter_valid.py | python trabalho_escravo_2006.py

