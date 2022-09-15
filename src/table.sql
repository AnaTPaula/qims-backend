-- USUARIO
create table usuario(
    id bigint primary key,
    tipo character varying(100) not null,
    senha character varying(100) not null,
    data_cadastro bigint not null,
);


-- ADMINISTRADOR
create table administrador(
    usuario_fk bigint not null references usuario(id) on update cascade,
    nome_usuario character varying(100) not null,
);


-- EMPRESA
create table empresa(
    usuario_fk bigint not null references usuario(id) on update cascade,
    situacao_conta character varying(100) not null,
    tipo_armazenagem character varying(100) not null,
    aceite_termos_de_uso bit not null,
    nome_usuario character varying(100) not null,
    razao_social character varying(100) not null,
);


-- OPERADOR
create table operador(
    usuario_fk bigint not null references usuario(id) on update cascade,
    tipo_acesso character varying(100) not null,
    empresa_fk bigint not null references empresa(id) on update cascade,
    nome_usuario character varying(100) not null,
);


-- PRODUTO
create table produto(
    id bigint primary key,
    nome character varying(100) not null,
    preco numeric(10,2) not null,
    descricao character varying(100) not null,
    unidade character varying(100) not null,
    estoque_minimo integer not null,
    estoque_maximo integer not null,
    ponto_reposicao integer not null,
    empresa_fk bigint not null references empresa(id) on update cascade,
);


-- ESTOQUE
create table estoque(
    id bigint primary key,
    nome character varying(100) not null,
    quantidade double not null,
    descricao character varying(100) not null,
    localizacao character varying(100) not null,
    produto_fk bigint not null references produto(id) on update cascade,
);


-- HISTORICO
create table historico(
    operador_fk bigint not null references operador(id) on update cascade,
    produto_fk bigint not null references produto(id) on update cascade,
    estoque_fk bigint not null references estoque(id) on update cascade,
    quantidade double not null,
    empresa_id bigint not null,
    operacao character varying(100) not null,
    datahora bigint not null,
);


-- LOTE
create table lote(
    id bigint primary key,
    codigo_lote integer not null,
    data_entrada bigint not null,
    data_validade bigint not null,
    quantidade double not null,
);


-- ESTOQUE LOTE
create table estoque_lote(
    estoque_fk bigint not null references estoque(id) on update cascade,
    lote_fk bigint not null references lote(id) on update cascade,
);
