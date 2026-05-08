CREATE TABLE usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT,
    senha TEXT
);

CREATE TABLE tarefa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    descricao TEXT,
    usuario_id INTEGER,
    FOREIGN KEY(usuario_id) REFERENCES usuario(id)
);