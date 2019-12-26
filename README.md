# sigaa-cli [![Build Status](https://travis-ci.com/macielti/sigaa-cli.svg?branch=master)](https://travis-ci.com/macielti/sigaa-cli) ![Python 2.7, 3.5, 3.6, 3.7](https://img.shields.io/badge/python-2.7%2C%203.5%2C%203.6%2C%203.7-blue.svg) ![Build Docs Status](https://readthedocs.org/projects/sigaa-cli/badge/?version=latest)

Módulo Python (não oficial) para servir como base para o desenvolvimento de um Command Line Interface para a plataforma SIGAA.

Com o desenvolvimento de uma interface de linha de comando ou até mesmo uma aplicação com interface gráfica poderemos assim utilizar o SIGAA com redução, em um certo grau, dos problemas gerados por uma internet de baixa qualidade ou de inconsistências na compatibilidade com navegadores.

## Documentation

The documentation is [here](https://sigaa-cli.readthedocs.io)

## Installation

Run the following to install:

```python
pip install sigaa-cli
```

Funcionalidades Previstas:

**Observação**: Novas funcionalidades podem ser solicitadas através da abertura de uma *nova issue* ou de um *pull request*.

-  [x] Autenticação com a plataforma online

	- [x] Gerar um id de sessão não autencicado;

	- [x] Autenticar o id de sessão gerado anteriormente;

	- [x] Acessar Cookies da sessão;
	
	- [x] Verificar status da authenticação do sistema;

- [ ] Listar Turmas ativas.

	- [ ] Listar turmas ativas do estudante;

- [ ] Listar Tarefas

	- [ ] A partir do código de uma turma ativa do estudante, poder gerar uma lista de tarefas daquela determinada turma, extraindo informações referente a prazos.

**Mais funcionalidades serão adicionadas a medida que as já propostas forem entregues.**