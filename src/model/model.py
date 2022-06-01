from datetime import datetime

from passlib.hash import pbkdf2_sha256
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    tipo = Column(String(15), nullable=False)
    senha = Column(String(300), nullable=False)  # limitar tamanho senha em 50
    data_cadastro = Column(Integer, default=int(datetime.utcnow().timestamp()), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'dataCadastro': self.data_cadastro
        }

    def verify_password(self, senha_sem_hash: str):
        try:
            return pbkdf2_sha256.verify(senha_sem_hash, self.senha)
        except ValueError:
            return False

    def set_hash_password(self, senha: str):
        self.senha = pbkdf2_sha256.hash(senha)


class Empresa(Base):
    __tablename__ = 'empresa'

    usuario_fk = Column(Integer, ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    nome_usuario = Column(String(50), nullable=False)
    situacao_conta = Column(String(100), nullable=False)
    lingua = Column(String(10), nullable=False)
    tipo_armazenagem = Column(String(5), nullable=False)
    aceite_termos_uso = Column(Boolean, nullable=False)
    __table_args__ = (
        UniqueConstraint('nome_usuario', name='_nome_usuario_empresa_uc'),
    )

    usuario = relationship('Usuario')

    @property
    def serialize(self):
        return {
            'nomeUsuario': self.nome_usuario,
            'situacaoConta': self.situacao_conta,
            'lingua': self.lingua,
            'tipoArmazenagem': self.tipo_armazenagem,
            'aceiteTermosUso': self.aceite_termos_uso,
            **self.usuario.serialize
        }

    def set_hash_password(self, senha: str):
        self.usuario.set_hash_password(senha)

    def verify_password(self, senha_sem_hash: str):
        return self.usuario.verify_password(senha_sem_hash)


class Funcionario(Base):
    __tablename__ = 'funcionario'

    usuario_fk = Column(Integer, ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    nome_usuario = Column(String(50), nullable=False)
    acesso = Column(String(20), nullable=False)
    empresa_fk = Column(Integer, ForeignKey('empresa.usuario_fk'), nullable=False)
    __table_args__ = (
        UniqueConstraint('nome_usuario', 'empresa_fk', name='_nome_usuario_funcionario_uc'),
    )

    usuario = relationship('Usuario')

    @property
    def serialize(self):
        return {
            'nomeUsuario': self.nome_usuario,
            'acesso': self.acesso,
            'empresaId': self.empresa_fk,
            **self.usuario.serialize
        }

    def set_hash_password(self, senha: str):
        self.usuario.set_hash_password(senha)

    def verify_password(self, senha_sem_hash: str):
        return self.usuario.verify_password(senha_sem_hash)


class Administrador(Base):
    __tablename__ = 'administrador'

    usuario_fk = Column(Integer, ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    nome_usuario = Column(String(50), nullable=False)
    __table_args__ = (
        UniqueConstraint('nome_usuario', name='_nome_usuario_administrador_uc'),
    )

    usuario = relationship('Usuario')

    @property
    def serialize(self):
        return {
            'nomeUsuario': self.nome_usuario,
            **self.usuario.serialize
        }

    def set_hash_password(self, senha: str):
        self.usuario.set_hash_password(senha)

    def verify_password(self, senha_sem_hash: str):
        return self.usuario.verify_password(senha_sem_hash)


class Almoxarifado(Base):
    __tablename__ = 'almoxarifado'

    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(255), nullable=True)
    empresa_fk = Column(Integer, ForeignKey('empresa.usuario_fk', ondelete='CASCADE'), nullable=False)
    __table_args__ = (
        UniqueConstraint('nome', 'empresa_fk', name='_nome_almoxarifado_uc'),
    )

    @property
    def serialize(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'empresaId': self.empresa_fk
        }


class Material(Base):
    __tablename__ = 'material'

    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    tipo = Column(String(50), nullable=False)
    preco = Column(Float, nullable=False)
    descricao = Column(String(255), nullable=False)
    unidade = Column(String(25), nullable=False)
    empresa_fk = Column(Integer, ForeignKey('empresa.usuario_fk', ondelete='CASCADE'), nullable=False)
    __table_args__ = (
        UniqueConstraint('nome', 'empresa_fk', name='_nome_material_uc'),
    )

    @property
    def serialize(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'tipo': self.tipo,
            'preco': self.preco,
            'descricao': self.descricao,
            'unidade': self.unidade
        }


class EstruturaMaterial(Base):
    __tablename__ = 'estrutura_material'

    material_pai_fk = Column(Integer, ForeignKey('material.id', ondelete='CASCADE'), primary_key=True)
    material_filho_fk = Column(Integer, ForeignKey('material.id'), primary_key=True)

    @property
    def serialize(self):
        return {
            'material_pai_fk': self.material_pai_fk,
            'material_filho_fk': self.material_filho_fk
        }


class Localizacao(Base):
    __tablename__ = 'localizacao'

    id = Column(Integer, primary_key=True)
    corredor = Column(String(20), nullable=False)
    coluna = Column(String(20), nullable=False)
    nivel = Column(String(20), nullable=False)
    vao = Column(String(20), nullable=False)
    empresa_fk = Column(Integer, ForeignKey('empresa.usuario_fk', ondelete='CASCADE'), nullable=False)
    __table_args__ = (
        UniqueConstraint('empresa_fk', 'corredor', 'coluna', 'nivel', 'vao', name='_localizacao_localizacao_uc'),
    )

    @property
    def serialize(self):
        return {
            'id': self.id,
            'corredor': self.corredor,
            'coluna': self.coluna,
            'nivel': self.nivel,
            'vao': self.vao
        }


class Estoque(Base):
    __tablename__ = 'estoque'

    id = Column(Integer, primary_key=True)
    quantidade = Column(Float, nullable=False)
    almoxarifado_fk = Column(Integer, ForeignKey('almoxarifado.id', ondelete='CASCADE'), nullable=False)
    localizacao_fk = Column(Integer, ForeignKey('localizacao.id'), nullable=False)
    material_fk = Column(Integer, ForeignKey('material.id'), nullable=False)

    localizacao = relationship('Localizacao')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'quantidade': self.quantidade,
            'localizacao': self.localizacao.serialize,
            'materialId': self.material_fk,
            'almoxarifadoId': self.almoxarifado_fk,
        }


class Historico(Base):
    __tablename__ = 'historico'

    id = Column(Integer, primary_key=True)
    empresa_fk = Column(Integer, ForeignKey('empresa.usuario_fk', ondelete='CASCADE'), nullable=False)
    nome_funcionario = Column(String(50), nullable=False)
    quantidade = Column(Float, nullable=False)
    operacao = Column(String(50), nullable=False)
    data_hora = Column(Integer, default=datetime.utcnow().timestamp(), nullable=False)
    almoxarifado_fk = Column(Integer, ForeignKey('almoxarifado.id'), nullable=False)
    material_fk = Column(Integer, ForeignKey('material.id'), nullable=False)

    almoxarifado = relationship('Almoxarifado')
    material = relationship('Material')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'nomeFuncionario': self.nome_funcionario,
            'quantidade': self.quantidade,
            'operacao': self.operacao,
            'dataHora': self.data_hora,
            'almoxarifado': self.almoxarifado.serialize,
            'material': self.material.serialize,
        }
