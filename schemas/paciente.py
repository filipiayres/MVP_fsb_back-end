from datetime import datetime 
from pydantic import BaseModel
from typing import Optional, List
from model.paciente import Paciente

from schemas import ComentarioSchema


class PacienteSchema(BaseModel):
    """ Define como um novo paciente a ser inserido deve ser representado
    """
    nome: str = "Marcos Filipi"
    CPF: str = "12312312312"
    comorbidade: str = "Gripe"


class PacienteBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do paciente.
    """
    nome: str = "Marcos Filipi"


class ListagemPacientesSchema(BaseModel):
    """ Define como uma listagem de pacientes será retornada.
    """
    pacientes:List[PacienteSchema]


def apresenta_pacientes(pacientes: List[Paciente]):
    """ Retorna uma representação do paciente seguindo o schema definido em
        PacienteViewSchema.
    """
    result = []
    for paciente in pacientes:
        result.append({
            "nome": paciente.nome,
            "CPF": paciente.CPF,
            "comorbidade": paciente.comorbidade,
            
        })

    return {"pacientes": result}


class PacienteViewSchema(BaseModel):
    """ Define como um paciente será retornado: paciente mais os comentários.
    """
    id: int = 1
    nome: str = "Marcos Filipi"
    CPF: str = "12312312312"
    comorbidade: str = "Gripe"
    total_cometarios: int 
    comentarios:List[ComentarioSchema]
    

class PacienteDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str = "Paciente removido com sucesso"
    nome: str = "Marcos Filipi"



def apresenta_paciente(paciente: Paciente):
    """ Retorna uma representação do paciente seguindo o schema definido no
        PacienteViewSchema.
    """

    return {
        "id": paciente.id,
        "nome": paciente.nome,
        "CPF": paciente.CPF,
        "comorbidade": paciente.comorbidade,
        "total_cometarios": len(paciente.comentarios),
        "comentarios": [{"texto": c.texto} for c in paciente.comentarios]
    }




