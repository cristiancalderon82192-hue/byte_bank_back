from sqlalchemy.orm import Session
from app.models.prestamo import Prestamo
from app.schemas.prestamo import PrestamoCreate, PrestamoUpdate, CalculoCuota
from typing import List, Optional
from decimal import Decimal
import math


def get_prestamo(db: Session, prestamo_id: int) -> Optional[Prestamo]:
    return db.query(Prestamo).filter(Prestamo.IdPrestamo == prestamo_id).first()


def get_prestamo_by_numero(db: Session, numero: str) -> Optional[Prestamo]:
    return db.query(Prestamo).filter(Prestamo.Numero == numero).first()


def get_prestamos(db: Session, skip: int = 0, limit: int = 100) -> List[Prestamo]:
    return db.query(Prestamo).offset(skip).limit(limit).all()


def get_prestamos_by_cuenta(db: Session, cuenta_id: int) -> List[Prestamo]:
    return db.query(Prestamo).filter(Prestamo.IdCuenta == cuenta_id).all()


def calcular_cuota(datos: CalculoCuota) -> dict:
    """
    Calcular la cuota mensual de un préstamo usando la fórmula de amortización francesa.
    
    Fórmula: Cuota = P * (i * (1 + i)^n) / ((1 + i)^n - 1)
    Donde:
    - P = Monto del préstamo
    - i = Tasa de interés mensual (tasa anual / 12 / 100)
    - n = Número de cuotas (plazo en meses)
    """
    P = float(datos.Valor)
    tasa_anual = float(datos.Interes)
    n = datos.Plazo
    seguro = float(datos.Seguro or Decimal("0"))
    
    # Si la tasa es 0, la cuota es simplemente el capital dividido por el plazo
    if tasa_anual == 0:
        cuota_capital = P / n
        cuota_mensual = cuota_capital + seguro
    else:
        # Tasa mensual
        i = tasa_anual / 12 / 100
        
        # Calcular cuota usando fórmula de amortización
        factor = (i * math.pow(1 + i, n)) / (math.pow(1 + i, n) - 1)
        cuota_capital = P * factor
        cuota_mensual = cuota_capital + seguro
    
    total_a_pagar = cuota_mensual * n
    total_intereses = total_a_pagar - P
    
    return {
        "CuotaMensual": round(Decimal(cuota_mensual), 2),
        "TotalAPagar": round(Decimal(total_a_pagar), 2),
        "TotalIntereses": round(Decimal(total_intereses), 2)
    }


def create_prestamo(db: Session, prestamo: PrestamoCreate) -> Prestamo:
    # Si no se proporciona la cuota, calcularla
    if prestamo.Cuota is None:
        calculo = calcular_cuota(CalculoCuota(
            Valor=prestamo.Valor,
            Interes=prestamo.Interes,
            Plazo=prestamo.Plazo,
            Seguro=prestamo.Seguro
        ))
        prestamo.Cuota = calculo["CuotaMensual"]
    
    db_prestamo = Prestamo(**prestamo.dict())
    db.add(db_prestamo)
    db.commit()
    db.refresh(db_prestamo)
    return db_prestamo


def update_prestamo(db: Session, prestamo_id: int, prestamo: PrestamoUpdate) -> Optional[Prestamo]:
    db_prestamo = get_prestamo(db, prestamo_id)
    if db_prestamo:
        update_data = prestamo.dict(exclude_unset=True)
        
        # Si se actualizan parámetros del préstamo, recalcular la cuota
        if any(k in update_data for k in ['Interes', 'Plazo', 'Seguro']) and 'Cuota' not in update_data:
            calculo = calcular_cuota(CalculoCuota(
                Valor=db_prestamo.Valor,
                Interes=update_data.get('Interes', db_prestamo.Interes),
                Plazo=update_data.get('Plazo', db_prestamo.Plazo),
                Seguro=update_data.get('Seguro', db_prestamo.Seguro)
            ))
            update_data['Cuota'] = calculo["CuotaMensual"]
        
        for key, value in update_data.items():
            setattr(db_prestamo, key, value)
        db.commit()
        db.refresh(db_prestamo)
    return db_prestamo


def delete_prestamo(db: Session, prestamo_id: int) -> bool:
    db_prestamo = get_prestamo(db, prestamo_id)
    if db_prestamo:
        db.delete(db_prestamo)
        db.commit()
        return True
    return False