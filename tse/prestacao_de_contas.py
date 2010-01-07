#!/usr/bin/env python
# coding: utf8
#
# Funções para consulta de doadores na base de dados de
# prestação de contas do TSE
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

from re import compile as regexp

from scraper import Scraper
from scraper import html2unicode
from cnpj import Cnpj
from cpf import Cpf


scraper = None

def pessoa_or_valueerror(cnpj_ou_cpf):
    pessoa = Cnpj(cnpj_ou_cpf)
    if not pessoa.valido():
        pessoa = Cpf(cnpj_ou_cpf)
        def unico_algarismo_repetido(s):
            return s == (s[0] * len(s))
        if not pessoa.valido() or unico_algarismo_repetido(pessoa.plain()):
            raise ValueError('CNPJ/CPF inválido')
    return pessoa


def doador_2004(cnpj_ou_cpf):
    u'''
    Retorna uma tabela com as doações desta pessoa (cnpj_ou_cpf). A tabela
    é uma lista de listas, cada uma contendo os campos em "doador_2004.campos".

    >>> tabela = doador_2004('85.907.012/0001-57')
    >>> tabela is not None
    True
    >>> len(tabela)
    16
    >>> len(tabela[0]) == len(doador_2004.campos)
    True

    URL: http://www.tse.gov.br/internet/eleicoes/2004/prest_blank.htm
    '''

    pessoa = pessoa_or_valueerror(cnpj_ou_cpf)
    scraper = Scraper()

    url = 'http://www.tse.gov.br/sadEleicao2004Prestacao/spce/index.jsp'
    scraper.open(url)

    scraper.browser.select_form(name='formDoador')
    scraper.browser.form.find_control(name='nome').readonly = False
    scraper.browser.form.find_control(name='numero').readonly = False
    scraper.browser.form['numero'] = pessoa.plain()
    scraper.browser.form['nome'] = '%'

    try:
        scraper.submit()
    except:
        return None

    if not scraper.html.find(text=regexp('Valor Total de Fornecimento')):
        return None

    table = scraper.html.findAll('table')[-1]

    lines = []
    for tr in table.findAll('tr')[1:-1]:
        columns = []
        for td in tr.findAll('td'):
            try:
                contents = td.b.contents
            except:
                contents = td.contents
            content = ' '.join(contents).strip()
            text = html2unicode(content)
            columns.append(text)
        lines.append(columns)

    return lines

doador_2004.campos = ['UF', 'Município', 'Partido', 'Nome', 'Número', 'Candidatura', 'Valor']


def doador_2006(cnpj_ou_cpf):
    u'''
    Retorna uma tabela com as doações desta pessoa (cnpj_ou_cpf). A tabela é
    uma lista de listas, cada uma contendo os campos em "doador_2006.campos".

    >>> tabela = doador_2006('181.929.206-15')
    >>> tabela is not None
    True
    >>> len(tabela)
    1
    >>> len(tabela[0]) == len(doador_2006.campos)
    True

    URL: http://www.tse.gov.br/internet/eleicoes/2006/prest_contas_blank.htm
    '''

    pessoa = pessoa_or_valueerror(cnpj_ou_cpf)
    scraper = Scraper()

    url = 'http://www.tse.gov.br/sadSPCE06F3/faces/careceitaByDoador.jsp'
    scraper.open(url)

    scraper.browser.form['frmByDoador:cdCpfCgc'] = pessoa.plain()
    scraper.submit(name='frmByDoador:_id4')

    strong = scraper.html.find('strong', text=regexp('.*prestadas pelo doador.*'))

    if strong is None:
        return None

    table = strong.parent.parent.parent.parent
    table = table.nextSibling.nextSibling.nextSibling.nextSibling

    lines = []
    for tr in table.tbody.findAll('tr'):
        columns = []
        for td in tr.findAll('td'):
            content = td.contents[0].strip()
            text = html2unicode(content)
            columns.append(text)
        lines.append(columns)

    return lines

doador_2006.campos = ['Candidato', 'Partido - UF', 'Data', 'Valor', 'Tipo']


def doador_2008(cnpj_ou_cpf):
    u'''
    Consulta o CNPJ ou CPF informado na página de doadores da campanha de 2008
    e retorna uma lista contendo os campos em "doador_2008.campos".

    Exemplo:

    >>> campos = doador_2008('00000000000191')
    >>> campos is not None
    True
    >>> len(campos) == len(doador_2008.campos)
    True
    '''

    pessoa = pessoa_or_valueerror(cnpj_ou_cpf)
    scraper = Scraper()

    # primeiro verifica se a pessoa foi doadora
    url = 'http://www.tse.jus.br/spce2008ConsultaFinanciamento/lovPesquisaDoador.jsp'
    scraper.open(url)

    scraper.browser.form['cdCpfCnpjDoador'] = pessoa.plain()
    scraper.browser.form.find_control(name='acao').readonly = False
    scraper.browser.form['acao'] = 'pesquisar'
    scraper.submit()

    if scraper.html.find('font', text=regexp('A pesquisa n.o retornou resultado.')):
        return None

    # e pega a lista de quem recebeu
    url = 'http://www.tse.jus.br/spce2008ConsultaFinanciamento/inicioServlet.do?acao=candidato'
    scraper.open(url)
    scraper.browser.form.find_control(name='cdCpfCnpjDoador').readonly = False
    scraper.browser.form['cdCpfCnpjDoador'] = pessoa.plain()
    scraper.browser.form.find_control(name='acao').readonly = False
    scraper.browser.form['acao'] = 'resumo'
    scraper.submit()

    url = 'http://www.tse.jus.br/spce2008ConsultaFinanciamento/listaReceitaCand.jsp'
    scraper.open(url)
    td = scraper.html.find('td', attrs={'class':'Left'})

    fields = []
    while True:
        try:
            # vai percorrendo os campos <td> e pegando o conteúdo
            items = [c for c in td.contents if isinstance(c, basestring)]
            s = ''.join(items)
            s = s.strip()
            fields.append(s.encode('utf8'))
            td = td.nextSibling.nextSibling
        except AttributeError:
            break

    return fields


doador_2008.campos = [
    'Doador',
    'CPF/CNPJ',
    'Data',
    'Valor R$',
    'Tipo do Recurso',
    'Espécie do Recurso',
    'Nome do Candidato',
    'Número',
    'Partido',
    'Candidatura',
    'Município-UF'
]



if __name__ == '__main__':
    import doctest
    doctest.testmod()


# vim:tabstop=4:expandtab:smartindent:encoding=utf8

