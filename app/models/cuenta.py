from sqlalchemy import Column, Integer, String, Date, DECIMAL, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Cuenta(Base):
    __tablename__ = "cuenta"
    
    IdCuenta = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Numero = Column(String(20), nullable=False, unique=True, index=True)
    FechaApertura = Column(Date, nullable=False)
    IdTipoCuenta = Column(Integer, ForeignKey("tipocuenta.IdTipoCuenta"), nullable=False)
    IdSucursal = Column(Integer, ForeignKey("sucursal.IdSucursal"), nullable=False)
    Saldo = Column(DECIMAL(15, 2), nullable=False, default=0.00)
    Sobregiro = Column(DECIMAL(15, 2), nullable=True, default=0.00)
    GranMovimiento = Column(Boolean, nullable=True, default=False)
    SobregiroNoAutorizado = Column(Boolean, nullable=True, default=False)
    
    # Relaciones
    tipo_cuenta = relationship("TipoCuenta", back_populates="cuentas")
    sucursal = relationship("Sucursal", back_populates="cuentas")
    titulares = relationship("Titular", back_populates="cuenta", cascade="all, delete-orphan")
    movimientos = relationship("Movimiento", back_populates="cuenta", cascade="all, delete-orphan")
    prestamos = relationship("Prestamo", back_populates="cuenta", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Cuenta(id={self.IdCuenta}, numero={self.Numero}, saldo={self.Saldo})>"