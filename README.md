# Projeto de Treinamento e Estudo

Este repositório contém um código criado para fins de treinamento e estudo. O objetivo é fornecer uma base para desenvolvimento de aplicativos utilizando Python, banco de dados SQLite3 e o framework KivyMD.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal utilizada para o desenvolvimento do aplicativo.
- **SQLite3**: Banco de dados relacional utilizado para armazenamento local de dados.
- **KivyMD**: Framework baseado em Kivy que facilita a criação de interfaces de usuário com Material Design.

## Estrutura do Projeto
projeto/
│
├── main.py # Arquivo principal do aplicativo
├── database.db # Banco de dados SQLite3
├── requirements.txt # Dependências do projeto
└── README.md # Documentação do projeto


## Funcionalidades

- Interface de usuário moderna e responsiva utilizando KivyMD.
- Integração com banco de dados SQLite3 para persistência de dados.
- Aplicativo preparado para deploy em dispositivos Android.

## Deploy no Google Colab

Para facilitar a criação do arquivo APK, o projeto foi configurado para ser executado no Google Colab. Siga os passos abaixo para gerar o APK:

1. Acesse o [Google Colab](https://colab.research.google.com/).
2. Carregue o notebook disponibilizado no repositório (`deploy_colab.ipynb`).
3. Siga as instruções do notebook para instalar as dependências e configurar o ambiente.
4. Execute as células para compilar o aplicativo e gerar o arquivo APK.

## Como Executar o Projeto Localmente

1. Clone este repositório:
    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```
2. Crie um ambiente virtual e instale as dependências:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
3. Execute o aplicativo:
    ```bash
    python main.py
    ```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
by Arleson Pontes.
