#!/bin/bash

# uso: trabalho_escravo_2008.sh | tee resultado_2008.csv

export PYTHONPATH=..

tr , ' ' < ministerio_publico.csv | python ../filter_valid.py | python trabalho_escravo_2008.py

