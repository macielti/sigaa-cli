Welcome to sigaa-cli's documentation!
=====================================

SIGAACLI is a module for python language that enable developers to execute some
actions inside the SIGAA platform, independent of the university.

.. toctree::
   :maxdepth: 2
   
   code

Instalation
###########

Execute on you system to install::

    pip install sigaa-cli

Simple Authentication Example::

    from sigaa import API

    api = API() # will use 'sigaa.ufpi.br' as default domain

    # return's True if the login data is correct or False if not
    api.authenticate('username', 'passwd') 



Contact
#######

Author: Bruno do Nascimento Maciel

Email: brunodonascimentomaciel@gmail.com, brunodonascimentomaciel@ufpi.edu.br

Github: https://github.com/macielti