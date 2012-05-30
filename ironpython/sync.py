from os import system

system('rm -r pystacia')
system('cd .. && python setup.py sdist --formats bztar && cd ironpython')
system('cp ../dist/*.tar.bz2 .')
system('wget http://pypi.python.org/packages/source/s/six/six-1.1.0.tar.gz')
system('wget http://pypi.python.org/packages/source/d/decorator/decorator-3.3.3.tar.gz')
system('wget http://pypi.python.org/packages/source/z/zope.deprecation/zope.deprecation-3.4.0.tar.gz')
system('tar --strip-components=1 -xf *.tar.bz2')
system('tar --strip-components=1 -xf six-1.1.0.tar.gz')
system('tar --strip-components=2 -xf decorator-3.3.3.tar.gz')
system('tar --strip-components=2 -xf zope.deprecation-3.4.0.tar.gz')
system('rm *.tar.*')
