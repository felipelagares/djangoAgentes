# Estudo de caso: Django framework, algoritmo recomendador de filmes
## Grupo:
- Felipe Galvão Lagares
- Hailton David Lemos
- Raphael Abenom dos Santos

### Video
[link para o video no youtube](https://youtu.be/HDANciib2Ws?feature=shared) com uma explicação básica do projeto rodando.

## Recomendações pessoais
### github
O github é no mínimo uma excelente ferramenta de versionamento de código mas para quem está iniciando é dificil decorar
a grande quantidade de comandos e funcionalidades. Baixe o [Github Desktop](https://desktop.github.com/download/) tente 
copiar este repositório com ele em code -> abrir com github desktop.

## Rodando a aplicação localmente 🤞

O csv com os dados está disponivel [aqui](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset/data)

### Python
Instalar o python, se ja não o tiver, baixando o instalador no final da pagina deste do site oficial do python: [link](https://www.python.org/downloads/release/python-3126/).
Esse link leva para a versão 3.12.6 que é a que estou usando, é possivel que haja conflitos das bibliotecas com outras
versões do python mas pode ser que rode sem nenhum problema também. Nessa versão eu sei que funciona.

### criando o ambiente virtual
- `python -m venv venv` cria uma ambiente virtual chamado venv 
- `venv/Scripts/activate` ativa o ambiente virtual. Se houver falhas de permissão consulte a
[documentação de venv do python](https://docs.python.org/pt-br/dev/library/venv.html) e a 
[pagina de informações de politicas de execução da microsoft](https://learn.microsoft.com/pt-br/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.5)

### instalando os requisitos do projeto
- `pip install -r requirements.txt` faz o pip instalar o que estiver listado no arquivo requirements.txt. 
(-r informa um arquivo de requisitos)


### Fazendo as migrações
Se estiver utilizando esse projeto após baixá-lo é possivel que não seja necessário fazer novamente as migrações mas
rodar os comandos não alterará os dados que ja estão no banco de dados. Caso esteja com um banco de dados vazio será 
necessário populá-lo, olhe então os comentários dentro da main de genericApp/src/recomendation.py. 
- `python manage.py makemigrations` cria os arquivos de migração para o seu bdd automaticamente com base nos seus models
- `python manage.py migrate` realiza as alterações no seu banco de dados.

### Rodar o app
- `python manage.py runserver` roda o servidor. O link deve ser exibido no seu terminal quando estiver rodando, o que 
demorará alguns instantes pois o cálculo dos embeddings é feito antes do serviço ir ao ar (embeddings são a 
vetorização das descrições de filmes pré-processadas. Ler o resto dessa documentação e recomendation.py).


## Diretórios e arquivos do projeto
### Django agentes
### genericApp
#### migrations
- Diretório onde ficam as migrações do banco de dados, os arquivos são criados automaticamente com o comando 
`python manage.py makemigrations` baseado nos models definidos em seu arquivo models e representam
os comandos de bancos de dados usados para criar as tabelas necessárias para acomodar seus models. Por si só os comandos
não são aplicados, deve ser utilizado `python manage.py migrate` para que os comandos sejam de fato aplicados ao BDD

#### src
- Diretório criado manualmente para acomodar arquivos de código com funções específicas
##### ploting.py
- Arquivo python onde eu defino as funções de  plotagem de gráfico baseado nas avaliações dos filmes

##### populate.py
- Arquivo python onde eu crio a funçao que popula meu banco de dados, ela recebe um arquivo e espera que certas
colunas estejam presentes nele (as mesmas definidas no models).

##### recomendation.py
- Arquivo python com as definições de funções de busca de filmes por nome. O modelo é pré-treinado para comparar vetores
que eu gero como embeddings sempre que o app é iniciado com `python manage.py runserver` por isso o app demora alguns 
instantes para iniciar, já que os cálculos são feitos na hora (atenção a explicação da \_\_main__)

#### static
- Diretóro com os estilos css e imagens utilizadas no frontend do app respectivamente nas pastas css e images.

#### templates
- Diretório com os arquivos .html que formam a estrutura da minha página e ditam as interações do usuário com o app.

#### admin
- Arquivo python de registro dos models do Django admin. Configura o Django admin.

#### models
- Arquivo python que define as tabelas no meu bando de dados. A partir dele as migrations serão geradas.

#### serializers
- Arquivo python que define a "transmissão" do meu objeto. ele transforma os models em json.

#### tests
- Arquivo python onde seriam definidos os testes se houvesse algum. gerado automaticamente pelo Django.

#### urls
- Arquivo python com a definição das urls internas do app. Definidos pelo usuário cada linha possui:
  - A string que é usada como url.
  - A view que interpreta as interações feitas no link.
  - O atributo *__name__* que será utilizado dentro dos htmls pelo Django para direcionar as requisições para as views.

#### views
- Arquivo python com as views, parte central do projeto. Quando o usuário interage com a página, as views são acionadas
para tratar a requisição feita, chamar as funções, processar e retornar ou redirecionar dados para a tela.

### project_root
#### asgi
- O arquivo asgi.py no Django serve como a interface de gateway de servidor assíncrono (ASGI, Asynchronous Server 
Gateway Interface). Ele é o ponto de entrada para que servidores web compatíveis com ASGI se conectem à aplicação 
Django. É essencial para lidar com comunicações assíncronas e em tempo real, como WebSockets ou long-polling, além de 
ser compatível com as tradicionais requisições HTTP síncronas.
<br>
*__texto gerado por IA__*

#### settings
- Arquivo de configuração gerado pelo Django. Ao gerar o app voce deve adicioná-lo a lista de INSTALLED_APPS.

#### urls
- Arquivo python com as urls do seu projeto todo. Se voce tiver varios app as urls para eles devem ser adicionadas.
Aqui é o geral e dentro do app são os específicos.

#### wsgi
- O arquivo wsgi.py no Django é usado como ponto de entrada para o WSGI (Web Server Gateway Interface), que é a 
interface padrão para comunicação entre servidores web e aplicações web baseadas em Python. Ele é utilizado em 
configurações de produção para lidar com requisições HTTP de maneira síncrona.
<br>
*__texto gerado por IA__*

#### .gitignore
- Arquivo para informar ao git o que ele deve ignorar. No meu caso uma pasta media que é onde fica guardado os arquivos
upados, as configs da minha IDE que sempre ficam mudando sem eu entender e meu ambiente virtual que possui o 
interpretador python do projeto com as bibliotecas instaladas.

#### db.sqlite3
- Banco de dados padrão do Django quando o projeto é gerado.

#### manage.py
- Arquivo principal do framework que gerencia tudo. ele é chamado sempre para fazer alteração no baco ou iniciar o 
serviço.

#### README.md
- Este arquivo de texto que está descrevendo o projeto e dando instruções.

#### requirements.txt
- Arquivo de texto com os requisitos do projeto.
