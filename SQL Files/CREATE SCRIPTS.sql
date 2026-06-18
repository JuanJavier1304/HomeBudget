-- ==========================
-- TABLA USUARIO
-- ==========================
CREATE TABLE usuario (
    pk1 SERIAL PRIMARY KEY,
    dni VARCHAR(8) NOT NULL UNIQUE,
    firstname VARCHAR(20) NOT NULL,
    lastname VARCHAR(20) NOT NULL,
    date_create TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_enable CHAR(1) NOT NULL DEFAULT '1'
);

-- ==========================
-- TABLA CATEGORIA
-- ==========================
CREATE TABLE categoria (
    pk1 SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL UNIQUE
);

-- ==========================
-- TABLA SUBCATEGORIA
-- ==========================
CREATE TABLE subcategoria (
    pk1 SERIAL PRIMARY KEY,
    category_pk1 INTEGER NOT NULL,
    name VARCHAR(30) NOT NULL,

    CONSTRAINT fk_subcategoria_categoria
        FOREIGN KEY (category_pk1)
        REFERENCES categoria(pk1)
);


-- ==========================
-- TABLA METODO DE PAGO
-- ==========================
CREATE TABLE metodo_pago(
    pk1 SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL UNIQUE
);

-- ==========================
-- TABLA MOVIMIENTO
-- ==========================
CREATE TABLE movimiento (
    pk1 SERIAL PRIMARY KEY,
    user_pk1 INTEGER NOT NULL,
    date_create TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    movement_date TIMESTAMP NOT NULL,
    movement_type VARCHAR(30) NOT NULL,
    description VARCHAR(100) NOT NULL,
    category_pk1 INTEGER NOT NULL,
    subcategory_pk1 INTEGER,
    amount NUMERIC(12,2) NOT NULL,
    payment_method_pk1 INTEGER NOT NULL,
    variability VARCHAR(30),
    comment VARCHAR(150),
    CONSTRAINT fk_movimiento_usuario
        FOREIGN KEY (user_pk1)
        REFERENCES usuario(pk1),
    CONSTRAINT fk_movimiento_categoria
        FOREIGN KEY (category_pk1)
        REFERENCES categoria(pk1),
    CONSTRAINT fk_movimiento_subcategoria
        FOREIGN KEY (subcategory_pk1)
        REFERENCES subcategoria(pk1),
    CONSTRAINT fk_movimiento_payment_method
        FOREIGN KEY (payment_method_pk1)
        REFERENCES metodo_pago(pk1)
);