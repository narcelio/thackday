#!/usr/bin/env python
# coding: utf8
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

'''
Lê CNPJs e CPFs na entrada padrão e escreve um CSV na saída com o resultado da
consulta da prestação de contas da campanha de 2008.
'''

import sys
from csv import writer as csv_writer

from tse.prestacao_de_contas import doador_2008

if __name__ == '__main__':
    csv = csv_writer(sys.stdout)
    csv.writerow(doador_2008.campos)

    for line in sys.stdin:
        cnpj_ou_cpf = line.strip()
        #sys.stderr.write('Pesquisando %s...\n' % cnpj_ou_cpf)
        campos = doador_2008(cnpj_ou_cpf)
        if campos:
            csv.writerow(campos)


# vim:tabstop=4:expandtab:smartindent:encoding=utf8

