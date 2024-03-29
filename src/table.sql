-- USUARIO
create table IF NOT EXISTS usuario(
    id serial primary key,
    tipo character varying(15) not null,
    senha character varying(300) not null,
    data_cadastro bigint not null default extract(epoch from now())
);


-- ADMINISTRADOR
create table IF NOT EXISTS administrador(
    usuario_fk bigint primary key references usuario(id) on update cascade on delete cascade,
    nome_usuario character varying(50) not null,
    constraint _nome_usuario_administrador_uc unique(nome_usuario)
);


-- EMPRESA
create table IF NOT EXISTS empresa(
    usuario_fk bigint primary key references usuario(id) on update cascade on delete cascade,
    situacao_conta character varying(100) not null,
    tipo_armazenagem character varying(100) not null,
    aceite_termos_de_uso boolean not null default false,
    nome_usuario character varying(100) not null,
    razao_social character varying(100) not null,
    constraint _nome_usuario_empresa_uc unique(nome_usuario)
);


-- OPERADOR
create table IF NOT EXISTS operador(
    usuario_fk bigint primary key references usuario(id) on update cascade on delete cascade,
    tipo_acesso character varying(20) not null,
    empresa_fk bigint not null references empresa(usuario_fk),
    nome_usuario character varying(100) not null,
    constraint _nome_usuario_funcionario_uc unique(nome_usuario, empresa_fk)
);


-- PRODUTO
create table IF NOT EXISTS produto(
    id serial primary key,
    nome character varying(100) not null,
    preco float not null,
    descricao character varying(200),
    unidade character varying(25) not null,
    estoque_minimo float,
    estoque_maximo float,
    ponto_reposicao float,
    empresa_fk bigint not null references empresa(usuario_fk) on update cascade on delete cascade,
    constraint _nome_produto_uc unique(nome, empresa_fk)
);


-- ESTOQUE
create table IF NOT EXISTS estoque(
    id serial primary key,
    nome character varying(100) not null,
    descricao character varying(200),
    empresa_fk bigint not null references empresa(usuario_fk) on update cascade on delete cascade,
    constraint _nome_estoque_uc unique(nome, empresa_fk)
);

-- PRODUTO ESTOQUE
create table IF NOT EXISTS produto_estoque(
    id serial primary key,
    quantidade float not null,
    localizacao character varying(100),
    produto_fk bigint not null references produto(id) on update cascade,
    estoque_fk bigint not null references estoque(id) on update cascade,
    empresa_fk bigint not null references empresa(usuario_fk) on update cascade on delete cascade,
    constraint _produto_estoque_uc unique(produto_fk, estoque_fk, empresa_fk)
);


-- HISTORICO
create table IF NOT EXISTS historico(
    id serial primary key,
    registro_operador bigint not null,
    nome_operador character varying(100) not null,
    nome_estoque character varying(100) not null,
    estoque_id bigint not null,
    nome_estoque_destino character varying(100),
    estoque_id_destino bigint,
    quantidade float not null,
    data_hora bigint not null default extract(epoch from now()),
    operacao character varying(100) not null,
    nome_produto character varying(100) not null,
    produto_fk bigint not null references produto(id) on update cascade,
    empresa_fk bigint not null references empresa(usuario_fk) on update cascade on delete cascade
);


-- LOTE
create table IF NOT EXISTS lote(
    id serial primary key,
    codigo_lote character varying(100) not null,
    data_entrada bigint not null,
    data_validade bigint,
    quantidade float not null,
    empresa_fk bigint not null references empresa(usuario_fk) on update cascade on delete cascade
);


-- ESTOQUE LOTE
create table IF NOT EXISTS estoque_lote(
    produto_estoque_fk bigint not null references produto_estoque(id) on update cascade,
    lote_fk bigint not null references lote(id) on update cascade,
    empresa_fk bigint not null references empresa(usuario_fk) on update cascade on delete cascade,
    constraint _produto_estoque_lote_uc unique(produto_estoque_fk, lote_fk, empresa_fk)
);
