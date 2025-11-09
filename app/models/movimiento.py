from sqlalchemy import Column, Integer, Date, DECIMAL, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Movimiento(Base):
    __tablename__ = "movimiento"
    
    IdMovimiento = Column(Integer, primary_key=True, index=True, autoincrement=True)
    IdCuenta = Column(Integer, ForeignKey("cuenta.IdCuenta", ondelete="CASCADE"), nullable=False, index=True)
    IdSucursal = Column(Integer, ForeignKey("sucursal.IdSucursal"), nullable=False)
    Fecha = Column(Date, nullable=False, index=True)
    Valor = Column(DECIMAL(15, 2), nullable=False)
    IdTipoMovimiento = Column(Integer, ForeignKey("tipomovimiento.IdTipoMovimiento"), nullable=False)
    Descripcion = Column(String(200), nullable=True)
    
    # Relaciones
    cuenta = relationship("Cuenta", back_populates="movimientos")
    sucursal = relationship("Sucursal", back_populates="movimientos")
    tipo_movimiento = relationship("TipoMovimiento", back_populates="movimientos")
    
    def __repr__(self):
        return f"<Movimiento(id={self.IdMovimiento}, cuenta={self.IdCuenta}, valor={self.Valor})>"