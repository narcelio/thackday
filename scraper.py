#!/usr/bin/env python
# coding: utf8
#
# scraper.py
#
# Web scraper
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

import logging
import mechanize

from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup


class Scraper(object):
    '''
    Cria um objeto que interage com páginas na Web. Exemplo:

    >>> scraper = Scraper()
    >>> scraper.open('http://www.tse.gov.br/sadSPCE06F3/faces/careceitaByDoador.jsp')
    >>> scraper.browser.form['frmByDoador:cdCpfCgc'] = '05323733000180'
    >>> scraper.submit(name='frmByDoador:_id4')
    >>> len(str(scraper.html))
    7901
    >>> print str(scraper.html)[1:63]
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
    '''

    def __init__(self):
        logging.info('Creating browser')
        self.browser = self._create_browser()


    def _create_browser(self):
        browser = mechanize.Browser()

        browser.addheaders = [
            ('Accept', 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5'),
            ('Accept-Language', 'en-us,en;q=0.7,pt-br;q=0.3'),
            ('Accept-Encoding', 'gzip,deflate'),
            ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'),
        ]
        browser.set_handle_robots(False)
        browser.set_handle_gzip(True)
        browser.set_handle_referer(True)

        # FIXME
        logger = logging.getLogger('mechanize')
        logger.setLevel(logging.INFO)

        return browser


    def open(self, url):
        '''Abre a url do parâmetro, seleciona o primeiro form caso haja algum e
        cria o atributo self.html com o BeautifulSoup()'''

        logging.info('Opening URL ' + url)
        self.browser.open(url)
        try:
            self.browser.select_form(nr=0)
        except mechanize._mechanize.FormNotFoundError:
            pass
        self.html = BeautifulSoup(self.browser.response().read())
        self.browser.response().seek(0)


    def submit(self, **kw):
        '''Faz o submit no form selecionado'''
        logging.info('Submitting form')
        self.browser.submit(**kw)
        try:
            self.browser.select_form(nr=0)
        except mechanize._mechanize.FormNotFoundError:
            pass
        self.html = BeautifulSoup(self.browser.response().read())
        self.browser.response().seek(0)


def html2unicode(s):
    '''Converte uma string com entidades HTML para unicode'''
    n = BeautifulStoneSoup(s, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    return unicode(n)


if __name__ == "__main__":
    import doctest
    doctest.testmod()


# vim:tabstop=4:expandtab:smartindent:encoding=utf8

