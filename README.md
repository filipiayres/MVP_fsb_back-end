# Minha API

Este pequeno projeto faz parte do material diático da Disciplina **Desenvolvimento Full Stack Básico** .

O objetivo dessa APP é criar um programa que faça a contagem dos pacientes em tratamento para fins estatísticos da instituição. 

---
## Como executar 

Basta fazer o download dos arquivos que estão direcionádos no meu GitHub e executar no seu VisualStudio.
>https://github.com/filipiayres/MVP-Back-end



> Para a criação de um novo ambiente virtual tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

Crie o ambiente virtual direto na raíz do arquivo baixado, siga as intruções abaixo:


```
Exemplo: 
/meu_app_api$ python3 -m venv env


Ative o ambiente (env) criado.


/meu_app_api$ source env/bin/activate


Em seguida, faça a instalação dos requirements. 

(env)$ pip install -r requirements.txt


Este comando instala as dependências/bibliotecas descritas no arquivo `requirements.txt`.
```

Para executar a API, basta inserir ao terminal após o ambiente virtual ativo:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento, é recomendado executar o comando **"flask"** utilizando o parâmetro **"reload"**, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução


Lembre-se de manter o local host rodando para o funcionamento do Front-end.
