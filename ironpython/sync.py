from os import system

system('rm -r tinyimg')
system('cd .. && python setup.py sdist --formats bztar && cd ironpython')
system('cp ../dist/*.tar.bz2 .')
system('tar --strip-components=1 -xf *.tar.bz2')
system('rm *.tar.bz2')
