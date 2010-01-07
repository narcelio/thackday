# coding: utf-8
#
# (c) Copyright 2007 Narcélio Filho
# (c) Copyright 2006 Fabio Correa
# (c) Copyright 2005 Michel Thadeu Sabchuk
# (c) Copyright 2005 Pedro Werneck
#
# Licença: Creative Commons Attribution 2.5
# http://creativecommons.org/licenses/by/2.5/br/
#

# código original encontrado em:
# http://www.pythonbrasil.com.br/moin.cgi/VerificadorDeCpf

class Cnpj(object):
    """
    Esta classe é um wrapper para ser usado com números de CNPJ(CGC), que além
    de oferecer um método simples de verificação, também conta com métodos para
    comparação e conversão.

    >>> a = Cnpj('11222333000181')
    >>> b = Cnpj('11.222.333/0001-81')
    >>> c = Cnpj([1, 1, 2, 2, 2, 3, 3, 3, 0, 0, 0, 1, 8, 2])
    >>> assert a.valido()
    >>> assert b.valido()
    >>> assert not c.valido()
    >>> assert a == b
    >>> assert not b == c
    >>> assert not a == c
    >>> assert eval(repr(a)) == a
    >>> assert eval(repr(b)) == b
    >>> assert eval(repr(c)) == c
    >>> assert str(a) == \"11.222.333/0001-81\"
    >>> assert str(b) == str(a)
    >>> assert str(c) == \"11.222.333/0001-82\"

    """

    def __init__(self, cnpj):
        """Classe representando um número de CNPJ

        >>> a = Cnpj('11222333000181')
        >>> b = Cnpj('11.222.333/0001-81')
        >>> c = Cnpj([1, 1, 2, 2, 2, 3, 3, 3, 0, 0, 0, 1, 8, 2])

        """
        try:
            basestring
        except:
            basestring = (str, unicode)

        if isinstance(cnpj, basestring):
            if not cnpj.isdigit():
                cnpj = cnpj.replace(".", "")
                cnpj = cnpj.replace("-", "")
                cnpj = cnpj.replace("/", "")

            if not cnpj.isdigit:
                raise ValueError("O CNPJ não segue a forma XX.XXX.XXX/XXXX-XX")

        if len(cnpj) < 14:
            cnpj = '0' * (14-len(cnpj))

        self.cnpj = map(int, cnpj)


    def __getitem__(self, index):
        """Retorna o dígito em index como string

        >>> a = Cnpj('11222333000181')
        >>> a[9] == '0'
        True
        >>> a[10] == '0'
        True
        >>> a[9] == 0
        False
        >>> a[10] == 0
        False

        """
        return str(self.cnpj[index])

    def __repr__(self):
        """Retorna uma representação 'real', ou seja:

        eval(repr(cnpj)) == cnpj

        >>> a = Cnpj('11222333000181')
        >>> print repr(a)
        Cnpj('11222333000181')
        >>> eval(repr(a)) == a
        True

        """
        return "Cnpj('%s')" % ''.join([str(x) for x in self.cnpj])

    def __eq__(self, other):
        """Provê teste de igualdade para números de CNPJ

        >>> a = Cnpj('11222333000181')
        >>> b = Cnpj('11.222.333/0001-81')
        >>> c = Cnpj([1, 1, 2, 2, 2, 3, 3, 3, 0, 0, 0, 1, 8, 2])
        >>> a == b
        True
        >>> a != c
        True
        >>> b != c
        True

        """
        if isinstance(other, Cnpj):
            return self.cnpj == other.cnpj
        return False

    def __str__(self):
        """Retorna uma string do CNPJ na forma com pontos e traço

        >>> a = Cnpj('11222333000181')
        >>> str(a)
        '11.222.333/0001-81'

        """
        d = ((2, "."), (6, "."), (10, "/"), (15, "-"))
        s = map(str, self.cnpj)
        for i, v in d:
            s.insert(i, v)
        r = ''.join(s)
        return r

    def valido(self):
        """Valida o número de cnpj

        >>> a = Cnpj('11.222.333/0001-81')
        >>> a.valido()
        True
        >>> b = Cnpj('11222333000182')
        >>> b.valido()
        False

        """
        cnpj = self.cnpj[:12]
        prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        # pegamos apenas os 9 primeiros dígitos do cpf e geramos os
        # dois dígitos que faltam
        while len(cnpj) < 14:

            r = sum([x*y for (x, y) in zip(cnpj, prod)])%11

            if r > 1:
                f = 11 - r
            else:
                f = 0
            cnpj.append(f)
            prod.insert(0, 6)

        # se o número com os digítos faltantes coincidir com o número
        # original, então ele é válido
        return bool(cnpj == self.cnpj)

    def __nonzero__(self):
        """Valida o número de CNPJ

        >>> a = Cnpj('11.222.333/0001-81')
        >>> bool(a)
        True
        >>> b = Cnpj('11222333000182')
        >>> bool(b)
        False
        >>> if a:
        ...     print 'OK'
        ...
        OK

        >>> if b:
        ...     print 'OK'
        ...
        >>>
        """

        return self.valido()

    def plain(self):
        return ''.join(map(str, self.cnpj))

def doctest():
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    doctest()


# vim:tabstop=4:shiftwidth=4:expandtab:smartindent:encoding=utf-8

