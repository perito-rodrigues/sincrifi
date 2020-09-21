CREATE TABLE [AGENCIAS] (
	NUMERO_BANCO decimal(3) NULL DEFAULT '0',
	NUMERO_AGENCIA decimal(4) NULL DEFAULT '0',
	NOME_AGENCIA varchar(50) NULL,
	ENDERECO_LOGRADOURO varchar(80) NULL,
	ENDERECO_CIDADE varchar(40) NULL,
	ENDERECO_UF varchar(2) NULL,
	ENDERECO_PAIS varchar(40) NULL,
	ENDERECO_CEP varchar(8) NULL,
	TELEFONE_AGENCIA varchar(20) NULL,
	DATA_ABERTURA_AGENCIA datetime NULL,
	DATA_FECHAMENTO_AGENCIA datetime NULL
)
GO
CREATE TABLE [CONTAS] (
	NUMERO_BANCO decimal(3) NULL,
	NUMERO_AGENCIA decimal(4) NULL,
	NUMERO_CONTA varchar(20) NULL,
	TIPO_CONTA decimal(1) NULL,
	DATA_ABERTURA_CONTA datetime NULL,
	DATA_ENCERRAMENTO_CONTA datetime NULL,
	MOVIMENTACAO_CONTA decimal(1) NULL
)
GO
CREATE TABLE [TIPO_CONTA] (
	ID decimal NULL UNIQUE,
	NOME varchar(30) NULL UNIQUE
)
GO
CREATE TABLE [TIPO_MOVIMENTACAO] (
	DESCRICAO text NULL,
	ID decimal NULL
)
GO
CREATE TABLE [TITULARES] (
	NUMERO_BANCO decimal(3) NULL,
	NUMERO_AGENCIA decimal(4) NULL,
	NUMERO_CONTA varchar(20) NULL,
	TIPO_CONTA decimal(1) NULL,
	TIPO_TITULAR varchar(1) NULL,
	PESSOA_INVESTIGADA decimal(1) NULL,
	TIPO_PESSOA_TITULAR decimal(1) NULL,
	CPF_CNPJ_TITULAR decimal(14) NULL,
	NOME_TITULAR varchar(80) NULL,
	NOME_DOC_IDENTIFICACAO varchar(50) NULL,
	NUMER_DOC_IDENTIFICACAO varchar(20) NULL,
	EDNDERECO_LOGRADOURO varchar(80) NULL,
	ENDERECO_CIDADE varchar(40) NULL,
	ENDERECO_UF varchar(2) NULL,
	ENDERECO_PAIS varchar(40) NULL,
	ENDERECO_CEP varchar(8) NULL,
	TELEFONE_PESSOA varchar(20) NULL,
	VALOR_RENDA decimal(14) NULL,
	DATA_ATUALIZACAO_RENDA datetime NULL,
	DATA_INICIO_RELACIONAMENTO datetime NULL,
	DATA_FIM_RELACIONAMENTO datetime NULL
)
GO
CREATE TABLE [TIPO_TITULAR] (
	CODIG varchar(1) NOT NULL,
	DESCRICAO varchar(255) NULL,

  CONSTRAINT [PK_TIPO_TITULAR] PRIMARY KEY CLUSTERED
  (
  [CODIG] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO
CREATE TABLE [EXTRATO] (
	CODIGO_CHAVE_EXTRATO decimal(18) NOT NULL,
	NUMERO_BANCO decimal(3) NULL,
	NUMERO_AGENCIA decimal(4) NULL,
	NUMERO_CONTA varchar(20) NULL,
	TIPO_CONTA decimal(1) NULL,
	DATA_LANCAMENTO datetime NULL,
	NUMERO_DOCUMENTO varchar(20) NULL,
	DESCRICAO_LANCAMENTO varchar(50),
	TIPO_LANCAMENTO decimal(3) NULL,
	VALOR_LANCAMENTO decimal NULL,
	NATUREZA_LANCAMENTO varchar(1) NULL,
	VALOR_SALDO decimal NULL,
	NATUREZA_SALDO varchar(1) NULL,
	LOCAL_TRANSACAO varchar(80) NULL,
	
  CONSTRAINT [PK_EXTRATO] PRIMARY KEY CLUSTERED
  (
  [CODIGO_CHAVE_EXTRATO] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO
CREATE TABLE [TIPO_LANCAMENTO] (
	CODIGO decimal(3) NOT NULL,
	DESCRICAO varchar(80) NULL,
	
  CONSTRAINT [PK_TIPO_LANCAMENTO] PRIMARY KEY CLUSTERED
  (
  [CODIGO] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO
CREATE TABLE [ORIGEM_DESTINO] (
	CODIGO_CHAVE_OD decimal(18) NOT NULL,
	CODIGO_CHAVE_EXTRATO decimal(18) NULL,
	VALOR_TRANSACAO decimal NULL,
	NUMERO_DOCUMENTO_TRANSACAO varchar(20) NULL,
	NUMERO_BANCO_OD decimal(3) NULL,
	NUMERO_AGENCIA_OD decimal(4) NULL,
	NUMERO_CONTA_OD varchar(20) NULL,
	TIPO_CONTA_OD decimal(1) NULL,
	TIPO_PESSOA_OD decimal(1) NULL,
	CPF_CNPJ_OD decimal(14) NULL,
	NOME_PESSOA_OD varchar(80) NULL,
	NOME_DOC_IDENTIFICACAO_OD varchar(50) NULL,
	NUMERO_DOC_IDENTIFICACAO_OD varchar(20) NULL,
	CODIGO_DE_BARRAS varchar(100) NULL,
	NOME_ENDOSSANTE_CHEQUE varchar(80) NULL,
	DOC_ENDOSSANTE_CHEQUE varchar(50) NULL,
	SITUACAO_IDENTIFICACAO decimal(1) NULL,
	OBSERVACAO varchar(250) NULL,
	
  CONSTRAINT [PK_ORIGEM_DESTINO] PRIMARY KEY CLUSTERED
  (
  [CODIGO_CHAVE_OD] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO