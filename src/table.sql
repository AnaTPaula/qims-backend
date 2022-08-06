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

    -- id bigint primary key,
    usuario_fk bigint not null references usuario(id) on update cascade,
    situacao_conta character varying(100) not null,
    lingua character varying(100) not null,
    tipo_armazenamento character varying(100) not null,
    aceite_termos_de_uso bit not null,
    nome_usuario character varying(100) not null,
    razao_social character varying(100) not null,
    -- cnpj character varying(18) unique not null,

);


-- FUNCIONARIO
create table funcionario(

    usuario_fk bigint not null references usuario(id) on update cascade,
    acesso character varying(100) not null,
    empresa_fk bigint not null references empresa(id) on update cascade,
    nome_usuario character varying(100) not null,

);


-- MATERIAL
create table material(

    id bigint primary key,
    nome character varying(100) not null,
    preco numeric(10,2) not null,
    descricao character varying(100) not null,
    unidade character varying(100) not null,
    empresa_fk bigint not null references empresa(id) on update cascade,

);
-- alter table material add constraint ck_preco_material check( preco >= 0);


-- ESTRUTURA MATERIAL
create table estruturaMaterial(

    material_pai_fk bigint not null references material(id) on update cascade,
    material_filho_fk bigint not null references material(id) on update cascade,

);


-- ALMOXARIFADO
create table almoxarifado(

    id bigint primary key,
    nome character varying(100) not null,
    descricao character varying(100) not null,
    empresa_fk bigint not null references empresa(id) on update cascade,

);


-- HISTORICO
create table historico(

    funcionario_fk bigint not null references funcionario(id) on update cascade,
    material_fk bigint not null references material(id) on update cascade,
    almoxarifado_fk bigint not null references almoxarifado(id) on update cascade,
    quantidade double not null,
    conta character varying(100) not null,
    operacao character varying(100) not null,
    datahora bigint not null,

);
-- alter table historico add constraint ck_quantidade_historico check( quantidade >= 0);


-- LOCALIZAÇÃO
create table localizacao(

    id bigint primary key,
    corredor character varying(100) not null,
    coluna character varying(100) not null,
    nivel character varying(100) not null,
    vao character varying(100) not null,

);


-- ESTOQUE
create table estoque(

    id bigint primary key,
    quantidade double not null,
    almoxarifado_fk bigint not null references almoxarifado(id) on update cascade,
    localizacao_fk bigint not null references localizacao(id) on update cascade,
    material_fk bigint not null references material(id) on update cascade,

);
-- alter table estoque add constraint ck_quantidade_estoque check( quantidade >= 0);

