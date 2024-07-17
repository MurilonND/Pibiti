# Wholebody MONAI Zoo

Este repositório contém um projeto de Python que utiliza a biblioteca MONAI para processamento e análise de imagens médicas. Abaixo está uma descrição dos arquivos incluídos no repositório e instruções de uso.

## Requisitos

- CUDA 12 ou superior
- Python 3.10.12

## Arquivos do Repositório

- **activate.bat** e **activate.sh**: Scripts para ativar o ambiente virtual criado pelos scripts `setup.bat` e `setup.sh`.
- **setup.bat** e **setup.sh**: Scripts para configurar o ambiente. Esses scripts fazem o download do pacote Python `virtualenv` e instalam todos os pacotes listados no arquivo `requirements.txt`.
- **requirements.txt**: Arquivo que contém a lista de pacotes necessários para o projeto.
- **wholebody_monai_zoo.py**: Arquivo executável em Python para processamento de imagens utilizando a biblioteca MONAI.
- **Wholebody_MONAI_ZOO.ipynb**: Jupyter Notebook que contém o mesmo código do arquivo `wholebody_monai_zoo.py`, mas organizado e comentado para facilitar o entendimento.

## Instruções de Uso

### Passo 1: Configurar o Ambiente

1. Clone este repositório:
    ```sh
    git clone https://github.com/seu-usuario/wholebody-monai-zoo.git
    cd wholebody-monai-zoo
    ```

2. Execute o script de configuração apropriado para o seu sistema operacional:

    No Windows:
    ```sh
    setup.bat
    ```

    No Linux/MacOS:
    ```sh
    bash setup.sh
    ```

### Passo 2: Ativar o Ambiente Virtual

1. Após a configuração, ative o ambiente virtual:

    No Windows:
    ```sh
    activate.bat
    ```

    No Linux/MacOS:
    ```sh
    source activate.sh
    ```

### Passo 3: Executar o Código

1. Com o ambiente virtual ativado, você pode executar o script Python diretamente:

    ```sh
    python wholebody_monai_zoo.py
    ```

2. Alternativamente, você pode abrir e executar o notebook Jupyter para uma versão comentada e interativa do código:

    ```sh
    jupyter notebook Wholebody_MONAI_ZOO.ipynb
    ```

## Contribuição

Sinta-se à vontade para contribuir com o projeto abrindo issues e pull requests. Certifique-se de seguir as melhores práticas de codificação e incluir testes apropriados ao enviar contribuições.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.

