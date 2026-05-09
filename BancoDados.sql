-- ==============================================================================
-- PROJETO: Sistema Web Controle de Ordens de Servico
-- SGBD: PostgreSQL
-- ==============================================================================

-- Habilita a extensão para geração de UUIDs (IDs não sequenciais)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ==============================================================================
-- 1. TABELAS INDEPENDENTES (Sem chaves estrangeiras)
-- ==============================================================================

CREATE TABLE clientes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- ID não sequencial
    cnpj_cpf VARCHAR(18) UNIQUE NOT NULL,
    razao_social VARCHAR(150) NOT NULL,
    descricao_cliente TEXT,
    nome_responsavel VARCHAR(100),
    email VARCHAR(100),
    contato VARCHAR(50)
);

CREATE TABLE fase (
    cod_fase SERIAL PRIMARY KEY,
    descricao_fase VARCHAR(100) NOT NULL,
    fase_finalizacao BOOLEAN DEFAULT FALSE
);

CREATE TABLE roteiro_padrao (
    cod_roteiro SERIAL PRIMARY KEY,
    descricao_roteiro VARCHAR(100) NOT NULL
);

CREATE TABLE usuario (
    cod_usuario SERIAL PRIMARY KEY,
    nome_usuario VARCHAR(100) NOT NULL
);

CREATE TABLE tamanho (
    cod_tamanho VARCHAR(10) PRIMARY KEY, -- Ex: P, M, G, 38, 40
    descricao_tamanho VARCHAR(50)
);


-- ==============================================================================
-- 2. TABELAS DE LIGAÇÃO E DEPENDENTES (Com chaves estrangeiras)
-- ==============================================================================

CREATE TABLE roteiro_padrao_fase (
    cod_roteiro INT NOT NULL,
    cod_fase INT NOT NULL,
    sequencia INT NOT NULL,
    PRIMARY KEY (cod_roteiro, cod_fase),
    CONSTRAINT fk_roteiro FOREIGN KEY (cod_roteiro) REFERENCES roteiro_padrao(cod_roteiro) ON DELETE CASCADE,
    CONSTRAINT fk_fase FOREIGN KEY (cod_fase) REFERENCES fase(cod_fase) ON DELETE RESTRICT
);

CREATE TABLE mov_usuario (
    cod_fase INT NOT NULL,
    cod_usuario INT NOT NULL,
    PRIMARY KEY (cod_fase, cod_usuario),
    CONSTRAINT fk_mov_fase FOREIGN KEY (cod_fase) REFERENCES fase(cod_fase) ON DELETE CASCADE,
    CONSTRAINT fk_mov_usuario FOREIGN KEY (cod_usuario) REFERENCES usuario(cod_usuario) ON DELETE CASCADE
);

CREATE TABLE ordem_producao (
    cod_op VARCHAR(50) NOT NULL, -- Digitado pelo usuário
    cod_cliente UUID NOT NULL,
    id_op_cliente VARCHAR(100) UNIQUE, -- Concatenado via Trigger
    descricao_op TEXT,
    cod_roteiro INT NOT NULL,
    valor_unitario NUMERIC(10, 2) DEFAULT 0.00,
    data_previsao DATE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_geracao INT NOT NULL,
    status_op VARCHAR(30) DEFAULT 'Criada',
    PRIMARY KEY (cod_op),
    CONSTRAINT fk_op_cliente FOREIGN KEY (cod_cliente) REFERENCES clientes(id) ON DELETE RESTRICT,
    CONSTRAINT fk_op_roteiro FOREIGN KEY (cod_roteiro) REFERENCES roteiro_padrao(cod_roteiro) ON DELETE RESTRICT,
    CONSTRAINT fk_op_usuario FOREIGN KEY (usuario_geracao) REFERENCES usuario(cod_usuario) ON DELETE RESTRICT
);

CREATE TABLE grade_op (
    cod_op VARCHAR(50) NOT NULL,
    cod_tamanho VARCHAR(10) NOT NULL,
    quantidade_qual_1 INT DEFAULT 0,
    quantidade_qual_2 INT DEFAULT 0,
    quantidade_cancelada INT DEFAULT 0,
    PRIMARY KEY (cod_op, cod_tamanho),
    CONSTRAINT fk_grade_op FOREIGN KEY (cod_op) REFERENCES ordem_producao(cod_op) ON DELETE CASCADE,
    CONSTRAINT fk_grade_tam FOREIGN KEY (cod_tamanho) REFERENCES tamanho(cod_tamanho) ON DELETE RESTRICT
);

CREATE TABLE mov_fase (
    id_movimento SERIAL PRIMARY KEY, -- Adicionada PK auxiliar para o histórico
    cod_op VARCHAR(50) NOT NULL,
    cod_fase INT NOT NULL,
    cod_usuario INT NOT NULL,
    dt_movimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_movfase_op FOREIGN KEY (cod_op) REFERENCES ordem_producao(cod_op) ON DELETE CASCADE,
    CONSTRAINT fk_movfase_fase FOREIGN KEY (cod_fase) REFERENCES fase(cod_fase) ON DELETE RESTRICT,
    CONSTRAINT fk_movfase_usuario FOREIGN KEY (cod_usuario) REFERENCES usuario(cod_usuario) ON DELETE RESTRICT
);

CREATE TABLE mov_fase_tam (
    id_mov_fase_tam SERIAL PRIMARY KEY, -- Adicionada PK auxiliar
    cod_op VARCHAR(50) NOT NULL,
    cod_fase INT NOT NULL,
    cod_tamanho VARCHAR(10) NOT NULL,
    quantidade_qual_1 INT DEFAULT 0,
    quantidade_qual_2 INT DEFAULT 0,
    quantidade_cancelada INT DEFAULT 0,
    CONSTRAINT fk_movfasetam_op FOREIGN KEY (cod_op) REFERENCES ordem_producao(cod_op) ON DELETE CASCADE,
    CONSTRAINT fk_movfasetam_fase FOREIGN KEY (cod_fase) REFERENCES fase(cod_fase) ON DELETE RESTRICT,
    CONSTRAINT fk_movfasetam_tam FOREIGN KEY (cod_tamanho) REFERENCES tamanho(cod_tamanho) ON DELETE RESTRICT
);

-- ==============================================================================
-- 3. TRIGGERS E FUNÇÕES
-- ==============================================================================

-- Função para concatenar op + cliente
CREATE OR REPLACE FUNCTION func_gerar_id_op_cliente()
RETURNS TRIGGER AS $$
BEGIN
    -- Concatena o cod_op (digitado) com o cod_cliente (UUID).
    -- Exemplo de saída: 'OP123-550e8400-e29b-41d4-a716-446655440000'
    NEW.id_op_cliente := NEW.cod_op || '-' || NEW.cod_cliente;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger disparada ANTES de inserir ou atualizar na tabela OrdemProducao
CREATE TRIGGER trg_gerar_id_op_cliente
BEFORE INSERT OR UPDATE ON ordem_producao
FOR EACH ROW
EXECUTE FUNCTION func_gerar_id_op_cliente();