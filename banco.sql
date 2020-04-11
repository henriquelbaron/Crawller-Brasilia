create table imovel(
	id SERIAL,
	inscricao char(8) NOT NULL UNIQUE,
	PRIMARY KEY(id)
);

create table imobiliaria(
	id SERIAL,
	nome varchar(100) NOT NULL,
	cnpj char(14) NOT NULL,
	PRIMARY KEY(id)
);

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

create table consulta(
	id SERIAL,
	consultado TIMESTAMP NOT NULL,
    id_imob_imovel INTEGER,
    PRIMARY KEY(id),
	FOREIGN KEY (id_imob_imovel) REFERENCES parametro(id),
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
	PRIMARY KEY(id),
    FOREIGN KEY (id_consulta) REFERENCES consulta (id)
);


