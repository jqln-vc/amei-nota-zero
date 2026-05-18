PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS uploads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_arquivo TEXT NOT NULL,
    tipo_arquivo TEXT,
    tamanho_kb REAL,
    data_upload DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS analises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    upload_id INTEGER,
    total_avaliacoes INTEGER,
    total_positivas INTEGER,
    total_negativas INTEGER,
    total_neutras INTEGER,
    resumo TEXT,
    recomendacao TEXT,
    data_analise DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (upload_id) REFERENCES uploads(id)
);

CREATE TABLE IF NOT EXISTS logs_sistema (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nivel TEXT NOT NULL,
    modulo TEXT,
    mensagem TEXT NOT NULL,
    data_log DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS metricas_performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    funcionalidade TEXT NOT NULL,
    tempo_resposta_ms REAL,
    status_execucao TEXT,
    data_execucao DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS erros_sistema (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    modulo TEXT,
    tipo_erro TEXT,
    mensagem_erro TEXT,
    data_erro DATETIME DEFAULT CURRENT_TIMESTAMP
);