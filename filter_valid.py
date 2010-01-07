#!/usr/bin/env python
# coding: utf8
#
# extract_cnpjs.py
#
# Filtra só CNPJs ou CPFs válidos na entrada padrão
#
# (c) Copyright 2009 by Narcelio Filho <narcelio@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys

from cnpj import Cnpj
from cpf import Cpf

if __name__ == '__main__':
    for line in sys.stdin.readlines():
        for part in line.split():
            cnpj_ou_cpf = Cnpj(line.strip())
            if not cnpj_ou_cpf.valido():
                cnpj_ou_cpf = Cpf(line.strip())
                if not cnpj_ou_cpf.valido():
                    continue

            print cnpj_ou_cpf


# vim:tabstop=4:expandtab:smartindent:encoding=utf8

