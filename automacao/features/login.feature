# language: pt
Funcionalidade: Login no BarrigaRest
  Como usuário
  Quero autenticar-me no sistema
  Para acessar a área restrita e gerenciar minhas informações

  Cenário Outline: Login bem-sucedido
    Dado que eu acesso a página de login em "https://barrigarest.wcaquino.me/"
    E que existe um usuário com email "<email>" e senha "<senha>"
    Quando eu preencho o campo "Email" com "<email>"
    E eu preencho o campo "Senha" com "<senha>"
    E eu clico no botão "Entrar"
    Então eu devo ser redirecionado para a página inicial
    E devo ver um elemento indicando que estou autenticado (por exemplo: "Sair", "Perfil" ou "Bem-vindo")

  Exemplos:
    | email | senha |
    | a@a   | a     |
