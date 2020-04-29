create table imovel(
	id SERIAL,
	inscricao char(8) NOT NULL UNIQUE,
	PRIMARY KEY(id)
);

CREATE INDEX index_imovel
ON imovel (inscricao);

create table imobiliaria(
	id SERIAL,
	nome varchar(100) NOT NULL,
	cnpj char(14) NOT NULL UNIQUE,
	PRIMARY KEY(id)
);

CREATE INDEX index_cnpj
ON imobiliaria (cnpj);

create table parametro(
    id SERIAL,
    codigoImovel varchar(255),
	numeroContrato varchar(255),
	id_imovel INTEGER,
	id_imobiliaria INTEGER,
	PRIMARY KEY(id),
	FOREIGN KEY (id_imovel) REFERENCES imovel (id),
    FOREIGN KEY (id_imobiliaria) REFERENCES imobiliaria (id)
);
CREATE TYPE estado AS ENUM ('PROCESSADO', 'REPROCESSAR', 'PROCESSANDO');
create table consulta(
	id SERIAL,
	consultado TIMESTAMP NOT NULL,
	estado estado,
    parametro INTEGER,
    PRIMARY KEY(id),
	FOREIGN KEY (parametro) REFERENCES parametro(id)
);

create table fatura(
	id SERIAL,
	id_consulta integer,
	pdf varchar(150),
	nome varchar(100),
	cpfCnpj varchar(18),
	endereco varchar(100),
	codReceita varchar(20),
	referencia varchar(10),
	vencimento DATE,
	exercicio varchar(10),
	codBarras varchar(60),
	valor numeric(10,2),
	juros numeric(10,2),
	multas numeric(10,2),
	desconto numeric(10,2),
	outros numeric(10,2),
	valorCobrado numeric(10,2),
	numeroDocumento varchar(30),
	numeroDam varchar(20),
	agencia varchar(10),
	nossoNumero varchar(30),
	codigoBeneficiario varchar(10),

	PRIMARY KEY(id),
    FOREIGN KEY (id_consulta) REFERENCES consulta (id)
);


INSERT INTO imobiliaria (nome,cnpj) values ('Projeta','00000000000000');