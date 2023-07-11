from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Paciente, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS
from schemas.paciente import PacienteViewSchema

info = Info(title="Prontuário digital API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
paciente_tag = Tag(name="Paciente", description="Adição, visualização e remoção de pacientes à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um paciente cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/paciente',tags=[paciente_tag],
          responses={"200": PacienteViewSchema, "409": ErrorSchema,"400": ErrorSchema})
def add_paciente(form:PacienteSchema):
    """Adiciona um novo paciente à base de dados 

    e retorna uma representação do paciente completa.
    """
    paciente = Paciente(
        nome=form.nome,
        CPF=form.CPF,
        comorbidade=form.comorbidade)
    logger.debug(f"Adicionando paciente de nome: '{paciente.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando paciente
        session.add(paciente)
        # efetivando o comando de adição de novo paciente na tabela
        session.commit()
        logger.debug(f"Adicionado paciente de nome: '{paciente.nome}'")
        return apresenta_paciente(paciente), 200

    except IntegrityError as e:
        # Caso haja duplicidade de nome no banco de dados o IntegrityError disparara um alerta de erro
            error_msg = "Paciente de mesmo nome já salvo na base :/"
            logger.warning(f"Erro ao adicionar paciente '{paciente.nome}', {error_msg}")
            return {"mesage": error_msg}, 409

    except Exception as e:
            # caso ocorra um erro fora do previsto
            error_msg = "Não foi possível salvar novo paciente :/"
            logger.warning(f"Erro ao adicionar paciente '{paciente.nome}', {error_msg}")
            return {"mesage": error_msg}, 400  

@app.get('/pacientes', tags=[paciente_tag],
         responses={"200": ListagemPacientesSchema, "404": ErrorSchema})
def get_pacientes():
    """Faz a busca por todos os pacientes cadastrados e

    retorna uma representação da listagem de pacientes.
    """

    logger.debug(f"Coletando dados dos pacientes ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pacientes = session.query(Paciente).all()

    if not pacientes:
        # se não há pacientes cadastrados
        return {"pacientes": []}, 200
    else:
        logger.debug(f"%d pacientes econtrados" % len(pacientes))
        # retorna a representação de paciente
        print(pacientes)
        return apresenta_pacientes(pacientes), 200

@app.get('/paciente', tags=[paciente_tag],
         responses={"200": PacienteViewSchema, "404": ErrorSchema})
def get_paciente(query: PacienteBuscaSchema):
    """Faz a busca por um Paciente a partir do nome do paciente e
    retorna uma representação do paciente e comentários associados.
    """

    paciente_nome = query.nome
    logger.debug(f"Coletando dados sobre o paciente #{paciente_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    paciente = session.query(Paciente).filter(Paciente.nome == paciente_nome).first()

    if not paciente:
        # se o paciente não for encontrado
        error_msg = "Paciente não encontrado na base de dados:/"
        logger.warning(f"Erro ao buscar o paciente '{paciente_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Paciente encontrado: '{paciente.nome}'")
        # retorna a representação de paciente
        return apresenta_paciente(paciente), 200

@app.delete('/paciente', tags=[paciente_tag],
            responses={"200": PacienteDelSchema, "404": ErrorSchema})
def del_produto(query: PacienteBuscaSchema):
    """Deleta um Paciente a partir do nome informado

    Retorna uma mensagem de confirmação da remoção.
    """
    paciente_nome = unquote(unquote(query.nome))
    print(paciente_nome)
    logger.debug(f"Deletando dados sobre produto #{paciente_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Paciente).filter(Paciente.nome == paciente_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado paciente #{paciente_nome}")
        return {"mesage": "Paciente removido", "id": paciente_nome}
    else:
        # se o produto não foi encontrado
        error_msg = "Paciente não encontrado na base :/"
        logger.warning(f"Erro ao deletar paciente #'{paciente_nome}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/cometario', tags=[comentario_tag],
          responses={"200": PacienteViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adiciona de um novo comentário à um paciente cadastrado na base identificado pelo id

    Retorna uma representação dos produtos e comentários associados.
    """
    paciente_id  = form.paciente_id
    logger.debug(f"Adicionando comentários ao paciente #{paciente_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo paciente
    paciente = session.query(Paciente).filter(Paciente.id == paciente_id).first()

    if not paciente:
        # se o paciente não for encontrado
        error_msg = "Paciente não encontrado na base :/"
        logger.warning(f"Erro ao adicionar comentário ao paciente '{paciente_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # adicionando o comentário ao paciente
    paciente.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário ao paciente #{paciente_id}")

    # retorna a representação de paciente
    return apresenta_paciente(paciente), 200






    