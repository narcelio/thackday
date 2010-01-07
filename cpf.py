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

class Cpf(object):
    """
    Esta classe é um wrapper para ser usado com números de CPF, que além de
    oferecer um método simples de verificação, também conta com métodos para
    comparação e conversão.

    >>> a = Cpf('56068332551')
    >>> b = Cpf('560.683.325-51')
    >>> c = Cpf((1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0))
    >>> assert a.valido()
    >>> assert b.valido()
    >>> assert not c.valido()
    >>> assert a == b
    >>> assert not b == c
    >>> assert not a == c
    >>> assert eval(repr(a)) == a
    >>> assert eval(repr(b)) == b
    >>> assert eval(repr(c)) == c
    >>> assert str(a) == \"560.683.325-51\"
    >>> assert str(b) == str(a)
    >>> assert str(c) == \"123.456.789-00\"

    """


    def __init__(self, cpf):
        """Classe representando um número de CPF

        >>> a = Cpf('95524361503')
        >>> b = Cpf('955.243.615-03')
        >>> c = Cpf([9, 5, 5, 2, 4, 3, 6, 1, 5, 0, 3])

        """

        try:
            basestring
        except:
            basestring = (str, unicode)

        if isinstance(cpf, basestring):
            cpf = cpf.replace(".", "")
            cpf = cpf.replace("-", "")
            if not cpf.isdigit():
                raise ValueError("O CPF não segue a forma XXX.XXX.XXX-XX")

        if len(cpf) < 11:
            cpf = '0' * (11-len(cpf))

        self.cpf = map(int, cpf)


    def __getitem__(self, index):
        """Retorna o dígito em index como string

        >>> a = Cpf('95524361503')
        >>> a[9] == '0'
        True
        >>> a[10] == '3'
        True
        >>> a[9] == 0
        False
        >>> a[10] == 3
        False

        """
        return str(self.cpf[index])

    def __repr__(self):
        """Retorna uma representação 'real', ou seja:

        eval(repr(cpf)) == cpf

        >>> a = Cpf('95524361503')
        >>> print repr(a)
        Cpf('95524361503')
        >>> eval(repr(a)) == a
        True

        """
        return "Cpf('%s')" % ''.join([str(x) for x in self.cpf])

    def __eq__(self, other):
        """Provê teste de igualdade para números de CPF

        >>> a = Cpf('95524361503')
        >>> b = Cpf('955.243.615-03')
        >>> c = Cpf('123.456.789-00')
        >>> a == b
        True
        >>> a != c
        True
        >>> b != c
        True

        """
        if isinstance(other, Cpf):
            return self.cpf == other.cpf
        return False

    def __str__(self):
        """Retorna uma string do CPF na forma com pontos e traço

        >>> a = Cpf('95524361503')
        >>> str(a)
        '955.243.615-03'


        """
        d = ((3, "."), (7, "."), (11, "-"))
        s = map(str, self.cpf)
        for i, v in d:
            s.insert(i, v)
        r = ''.join(s)
        return r

    def valido(self):
        """Valida o número de cpf

        >>> a = Cpf('95524361503')
        >>> a.valido()
        True
        >>> b = Cpf('12345678900')
        >>> b.valido()
        False

        """
        cpf = self.cpf[:9]
        # pegamos apenas os 9 primeiros dígitos do cpf e geramos os
        # dois dígitos que faltam
        while len(cpf) < 11:

            r = sum(map(lambda(i,v):(len(cpf)+1-i)*v,enumerate(cpf))) % 11

            if r > 1:
                f = 11 - r
            else:
                f = 0
            cpf.append(f)

        # se o número com os digítos faltantes coincidir com o número
        # original, então ele é válido
        return bool(cpf == self.cpf)

    def __nonzero__(self):
        """Valida o número de cpf

        >>> a = Cpf('95524361503')
        >>> bool(a)
        True
        >>> b = Cpf('12345678900')
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
        return ''.join(map(str, self.cpf))


def doctest():
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    doctest()


# vim:tabstop=4:shiftwidth=4:expandtab:smartindent:encoding=utf-8

