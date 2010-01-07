#!/bin/bash

# uso: trabalho_escravo_2004.sh | tee resultado-2004.csv

export PYTHONPATH=..

tr , ' ' < ministerio_publico.csv | python ../filter_valid.py | python trabalho_escravo_2004.py

