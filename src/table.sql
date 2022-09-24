-- USUARIO
create table usuario(
    id serial primary key,
    tipo character varying(15) not null,
    senha character varying(300) not null,
    data_cadastro bigint not null default cast(to_char((current_timestamp)::TIMESTAMP,'yyyymmddhhmiss') as BigInt)
);


-- ADMINISTRADOR
create table administrador(
    usuario_fk bigint primary key references usuario(id) on update cascade on delete cascade,
    nome_usuario character varying(50) not null,
    constraint _nome_usuario_administrador_uc unique(nome_usuario)
);


-- EMPRESA
create table empresa(
    usuario_fk bigint primary key references usuario(id) on update cascade on delete cascade,
    situacao_conta character varying(100) not null,
    tipo_armazenagem character varying(100) not null,
    aceite_termos_de_uso boolean not null default false,
    nome_usuario character varying(100) not null,
    razao_social character varying(100) not null,
    constraint _nome_usuario_empresa_uc unique(nome_usuario)
);


-- OPERADOR
create table operador(
    usuario_fk bigint primary key references usuario(id) on update cascade on delete cascade,
    tipo_acesso character varying(20) not null,
    empresa_fk bigint not null references empresa(usuario_fk),
    nome_usuario character varying(100) not null,
    constraint _nome_usuario_funcionario_uc unique(nome_usuario, empresa_fk)
);


-- PRODUTO
create table produto(
    id serial primary key,
    nome character varying(100) not null,
    preco float not null,
    descricao character varying(200),
    unidade character varying(25) not null,
    estoque_minimo float not null,
    estoque_maximo float not null,
    ponto_reposicao float not null,
    empresa_fk bigint not null references empresa(usuario_fk) on update cascade on delete cascade,
    constraint _nome_produto_uc unique(nome, empresa_fk)
);


-- ESTOQUE
create table estoque(
    id serial primary key,
    nome character varying(100) not null,
    quantidade float not null,
    descricao character varying(200),
    localizacao character varying(100) not null,
    produto_fk bigint not null references produto(id) on update cascade,
    empresa_fk bigint not null references empresa(usuario_fk) on update cascade on delete cascade
);


-- HISTORICO
create table historico(
    operador_fk bigint not null references operador(usuario_fk) on update cascade,
    produto_fk bigint not null references produto(id) on update cascade,
    estoque_fk bigint not null references estoque(id) on update cascade,
    quantidade float not null,
    empresa_fk bigint not null references empresa(usuario_fk) on update cascade on delete cascade,
    operacao character varying(100) not null,
    datahora bigint not null default cast(to_char((current_timestamp)::TIMESTAMP,'yyyymmddhhmiss') as BigInt)
);


-- LOTE
create table lote(
    id serial primary key,
    codigo_lote character varying(100) not null,
    data_entrada bigint not null,
    data_validade bigint not null,
    quantidade float not null,
    empresa_fk bigint not null references empresa(usuario_fk) on update cascade on delete cascade
);


-- ESTOQUE LOTE
create table estoque_lote(
    estoque_fk bigint not null references estoque(id) on update cascade,
    lote_fk bigint not null references lote(id) on update cascade,
    empresa_fk bigint not null references empresa(usuario_fk) on update cascade on delete cascade
);
