Welcome to sigaa-cli's documentation!
=====================================

SIGAACLI is a module for python language that enable developers to execute some
actions inside the SIGAA platform, independent of the university.

.. toctree::
   :maxdepth: 2
   
   api
   mailbox

.. warning::
    The way that the SIGAA server works is storing the state of the session in the backend 
    this makes the development a litle bit difficult.
    
    What require that we make a serie of requests to do some operations.


Instalation
###########

Execute on you system to install::

    pip install sigaa-cli

Simple Authentication Example::

    from sigaa.api import API

    api = API() # will use 'sigaa.ufpi.br' as default domain

    # return's True if the login data is correct or False if not
    api.authenticate('username', 'passwd')

Contact
#######

Author: Bruno do Nascimento Maciel

Email: brunodonascimentomaciel@gmail.com, brunodonascimentomaciel@ufpi.edu.br

Github: https://github.com/macielti