from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Almoxarifado(Base):
    __tablename__ = 'almoxarifado'

    id = Column(Integer, primary_key=True)
    conta = Column(String(50), nullable=False)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(255), nullable=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'conta': self.conta,
            'nome': self.nome,
            'descricao': self.descricao
        }


class Estoque(Base):
    __tablename__ = 'estoque'

    id = Column(Integer, primary_key=True)
    quantidade = Column(Integer, nullable=False)
    conta = Column(String(255), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'quantidade': self.quantidade,
            'conta': self.conta
        }


class Localizacao()
    __tablename__ = 'localizacao'

    id = Column(Integer, primary_key=True)
    corredor = Column(Integer, nullable=False)
    coluna = Column(Integer, nullable=False)
    nivel = Column(Integer, nullable=False)
    vao = Column(Integer, nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'corredor': self.corredor,
            'coluna': self.coluna,
            'nivel': self.nivel,
            'vao': self.vao
        }


class Material()
    __tablename__ = 'material'

    id = Column(Integer, primary_key=True)
    conta = Column(String(50), nullable=False)
    nome = Column(String(50), nullable=False)
    preco = Column(Float, nullable=False)
    descricao = Column(String(255), nullable=False)
    unidade = Column(Integer, nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'conta': self.conta,
            'nome': self.nome,
            'preco': self.preco,
            'descricao': self.descricao,
            'unidade': self.unidade
        }


class Usuario()
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    tipo = Column(String(15), nullable=False)
    nome = Column(String(50), nullable=False)
    senha = Column(String(50), nullable=False)
    nome_usuario = Column(String(50), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'nome': self.nome,
            'senha': self.senha,
            'nome_usuario': self.nome_usuario
        }

class Empresa()
    __tablename__ = 'empresa'

    tipo_armazenagem = Column(String(4), nullable=False)
    conta = Column(String(50), nullable=False)
    estado_conta = Column(String(10), nullable=False)
    lingua = Column(String(10), nullable=False)

    @property
    def serialize(self):
        return {
            'tipo_armazenagem': self.tipo_armazenagem,
            'conta': self.conta,
            'estado_conta': self.estado_conta,
            'lingua': self.lingua

        }

class Funcionario()
    __tablename__ = 'funcionario'

    conta = Column(String(50), nullable=False)
    acesso = Column(String(20), nullable=False)

    @property
    def serialize(self):
        return {
            'conta': self.conta,
            'acesso': self.acesso
        }