from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Sucursal(Base):
    __tablename__ = "sucursal"
    
    IdSucursal = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Sucursal = Column(String(50), nullable=False)
    IdCiudad = Column(Integer, ForeignKey("ciudad.IdCiudad"), nullable=False)
    IdTipoSucursal = Column(Integer, ForeignKey("tiposucursal.IdTipoSucursal"), nullable=False)
    Direccion = Column(String(100), nullable=True)
    Telefono = Column(String(20), nullable=True)
    Horario = Column(String(50), nullable=True)
    
    # Relaciones
    ciudad = relationship("Ciudad", back_populates="sucursales")
    tipo_sucursal = relationship("TipoSucursal", back_populates="sucursales")
    cuentas = relationship("Cuenta", back_populates="sucursal")
    movimientos = relationship("Movimiento", back_populates="sucursal")
    
    def __repr__(self):
        return f"<Sucursal(id={self.IdSucursal}, nombre={self.Sucursal})>"