from pydantic import BaseModel


class ComentarioSchema(BaseModel):
    """ Define um novo comentário a ser inserido ao paciente a ser representado.
    """
    paciente_id: int = 1
    texto: str = "Este paciente finalizou o tratamento."