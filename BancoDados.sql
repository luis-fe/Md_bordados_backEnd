-- ==============================================================================
-- PROJETO: Sistema Web Controle de Ordens de Servico
-- SGBD: PostgreSQL
-- ==============================================================================

-- Habilita a extensão para geração de UUIDs (IDs não sequenciais)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ==============================================================================
-- 1. TABELAS INDEPENDENTES (Sem chaves estrangeiras)
-- ==============================================================================

CREATE TABLE IF NOT EXISTS clientes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cnpj_cpf VARCHAR(18) UNIQUE NOT NULL,
    razao_social VARCHAR(150) NOT NULL,
    descricao_cliente TEXT,
    nome_responsavel VARCHAR(100),
    email VARCHAR(100),
    contato VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS fase (
    cod_fase SERIAL PRIMARY KEY,
    descricao_fase VARCHAR(100) NOT NULL,
    fase_finalizacao BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS roteiro_padrao (
    cod_roteiro SERIAL PRIMARY KEY,
    descricao_roteiro VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS usuario (
    cod_usuario SERIAL PRIMARY KEY,
    nome_usuario VARCHAR(100) NOT NULL,
    login VARCHAR(50) UNIQUE,        
    perfil VARCHAR(30),              
    status INT DEFAULT 1,            
    contato VARCHAR(20),             
    senha VARCHAR(255),              -- CORREÇÃO: Aumentado para 255 para suportar hash Bcrypt (60 chars)
    "corTema" VARCHAR(20) DEFAULT 'Branca' CHECK ("corTema" IN ('Preto', 'Branca', 'Escura')) -- CORREÇÃO: Alinhado com a regra de negócio do backend
);

CREATE TABLE IF NOT EXISTS tamanho (
    cod_tamanho VARCHAR(10) PRIMARY KEY,
    descricao_tamanho VARCHAR(50),
    "sequenciaTamanho" INT           
);

CREATE TABLE IF NOT EXISTS autoriza_rotina (
    id_rotina SERIAL PRIMARY KEY,
    rotina TEXT UNIQUE NOT NULL
);

-- ==============================================================================
-- 2. TABELAS DE LIGAÇÃO E DEPENDENTES (Com chaves estrangeiras)
-- ==============================================================================

CREATE TABLE IF NOT EXISTS usuario_autorizado (
    cod_usuario INT NOT NULL,
    id_rotina INT NOT NULL,
    PRIMARY KEY (cod_usuario, id_rotina),
    CONSTRAINT fk_autorizado_usuario FOREIGN KEY (cod_usuario) REFERENCES usuario(cod_usuario) ON DELETE CASCADE,
    CONSTRAINT fk_autorizado_rotina FOREIGN KEY (id_rotina) REFERENCES autoriza_rotina(id_rotina) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS roteiro_padrao_fase (
    cod_roteiro INT NOT NULL,
    cod_fase INT NOT NULL,
    sequencia INT NOT NULL,
    "faseSimultanea" VARCHAR(50),    
    PRIMARY KEY (cod_roteiro, cod_fase),
    CONSTRAINT fk_roteiro FOREIGN KEY (cod_roteiro) REFERENCES roteiro_padrao(cod_roteiro) ON DELETE CASCADE,
    CONSTRAINT fk_fase FOREIGN KEY (cod_fase) REFERENCES fase(cod_fase) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS mov_usuario (
    cod_fase INT NOT NULL,
    cod_usuario INT NOT NULL,
    PRIMARY KEY (cod_fase, cod_usuario),
    CONSTRAINT fk_mov_fase FOREIGN KEY (cod_fase) REFERENCES fase(cod_fase) ON DELETE CASCADE,
    CONSTRAINT fk_mov_usuario FOREIGN KEY (cod_usuario) REFERENCES usuario(cod_usuario) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ordem_producao (
    cod_op VARCHAR(50) NOT NULL,
    cod_cliente UUID NOT NULL,
    id_op_cliente VARCHAR(100) UNIQUE,
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

CREATE TABLE IF NOT EXISTS grade_op (
    cod_op VARCHAR(50) NOT NULL,
    cod_tamanho VARCHAR(10) NOT NULL,
    cor VARCHAR(50) NOT NULL DEFAULT 'Sem Cor', 
    quantidade_qual_1 INT DEFAULT 0,
    quantidade_qual_2 INT DEFAULT 0,
    quantidade_cancelada INT DEFAULT 0,
    PRIMARY KEY (cod_op, cod_tamanho, cor),     
    CONSTRAINT fk_grade_op FOREIGN KEY (cod_op) REFERENCES ordem_producao(cod_op) ON DELETE CASCADE,
    CONSTRAINT fk_grade_tam FOREIGN KEY (cod_tamanho) REFERENCES tamanho(cod_tamanho) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS mov_fase (
    id_movimento SERIAL PRIMARY KEY,
    cod_op VARCHAR(50) NOT NULL,
    cod_fase INT NOT NULL,
    cod_usuario INT NOT NULL,
    dt_movimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_movfase_op FOREIGN KEY (cod_op) REFERENCES ordem_producao(cod_op) ON DELETE CASCADE,
    CONSTRAINT fk_movfase_fase FOREIGN KEY (cod_fase) REFERENCES fase(cod_fase) ON DELETE RESTRICT,
    CONSTRAINT fk_movfase_usuario FOREIGN KEY (cod_usuario) REFERENCES usuario(cod_usuario) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS mov_fase_tam (
    id_mov_fase_tam SERIAL PRIMARY KEY,
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

CREATE OR REPLACE FUNCTION func_gerar_id_op_cliente()
RETURNS TRIGGER AS $$
BEGIN
    NEW.id_op_cliente := NEW.cod_op || '-' || NEW.cod_cliente;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_gerar_id_op_cliente ON ordem_producao;

CREATE TRIGGER trg_gerar_id_op_cliente
BEFORE INSERT OR UPDATE ON ordem_producao
FOR EACH ROW
EXECUTE FUNCTION func_gerar_id_op_cliente();

-- ==============================================================================
-- 4. ATUALIZAÇÕES DE COLUNAS (Para tabelas que já existem)
-- ==============================================================================

ALTER TABLE tamanho ADD COLUMN IF NOT EXISTS "sequenciaTamanho" INT;

ALTER TABLE usuario ADD COLUMN IF NOT EXISTS login VARCHAR(50) UNIQUE;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS perfil VARCHAR(30);
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS status INT DEFAULT 1;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS contato VARCHAR(20);
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS senha VARCHAR(255); -- CORREÇÃO
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS "corTema" VARCHAR(20) DEFAULT 'Branca'; 

ALTER TABLE roteiro_padrao_fase ADD COLUMN IF NOT EXISTS "faseSimultanea" VARCHAR(50);

ALTER TABLE grade_op ADD COLUMN IF NOT EXISTS cor VARCHAR(50) NOT NULL DEFAULT 'Sem Cor';

-- CORREÇÃO: Garante que, se a tabela grade_op já existia e a coluna 'cor' foi adicionada via ALTER TABLE, 
-- a Chave Primária será atualizada para incluir a nova coluna.
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.table_constraints 
        WHERE table_name = 'grade_op' AND constraint_type = 'PRIMARY KEY'
    ) THEN
        ALTER TABLE grade_op DROP CONSTRAINT grade_op_pkey;
        ALTER TABLE grade_op ADD PRIMARY KEY (cod_op, cod_tamanho, cor);
    END IF;
EXCEPTION WHEN OTHERS THEN
    -- Ignora se a constraint tiver outro nome gerado dinamicamente
END $$;

-- ==============================================================================
-- 5. CARGA DE DADOS INICIAIS
-- ==============================================================================

INSERT INTO autoriza_rotina (rotina) VALUES
('cadastro de usuario (inclusao , edicao , exclusao)'),
('visualizar usuarios cadastrado'),
('cadastro clientes (inclusao , edicao , exclusao)'),
('visualizar clientes'),
('configurar tamanhos'), -- CORREÇÃO: Digitação arrumada
('configurar fases'),
('configurar roteiro'),
('visualizar relatorio producao'),
('visualizar valor financeiro nas consultas')
ON CONFLICT (rotina) DO NOTHING;