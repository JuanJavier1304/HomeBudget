ALTER TABLE movimiento
ADD CONSTRAINT chk_movement_type
CHECK (
    movement_type IN ('Ingreso', 'Egreso')
);

ALTER TABLE movimiento
ADD CONSTRAINT chk_variability
CHECK (
    variability IN ('Fijo', 'Variable')
);