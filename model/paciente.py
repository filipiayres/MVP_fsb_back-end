from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from  model import Base, Comentario


    # Criação do banco de dados com a tabela paciente,
    # que contém nome, nome, CPF, comorbidade,
    # data de início de cadastro.

class Paciente(Base):
    __tablename__ = "paciente"

    id = Column("pk_prontuario", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    CPF = Column(String(11), unique=True)
    comorbidade = Column(String(1200), unique=True)
    data_de_inicio = Column (DateTime, default=datetime.now())
    

    # Definição do relacionamento entre o paciente e o comentário.
    # Essa relação é implicita, não está salva na tabela 'paciente',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comentarios = relationship("Comentario")

    def __init__(self, 
                 nome:str, 
                 CPF:str, 
                 comorbidade:str, 
                 data_de_inicio:Union[DateTime, None]= None): 
                 
        """
            Cadastrando um Paciente

            Arguments:
                nome: nome do paciente.
                CPF: O Cadastro Único de pessoa Física.
                comorbidade:O tipo de doença que afeta esse paciente.
                data_de_inico: data de quando o paciente foi cadastrado como.
                
        """    
        self.nome = nome
        self.CPF = CPF
        self.comorbidade = comorbidade
        self.data_de_inicio = data_de_inicio

    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário ao Paciente
        """
        self.comentarios.append(comentario)
