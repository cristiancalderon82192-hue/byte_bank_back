from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class TipoSucursal(Base):
    __tablename__ = "tiposucursal"
    
    IdTipoSucursal = Column(Integer, primary_key=True, index=True, autoincrement=True)
    TipoSucursal = Column(String(50), nullable=False)
    
    # Relaciones
    sucursales = relationship("Sucursal", back_populates="tipo_sucursal")
    
    def __repr__(self):
        return f"<TipoSucursal(id={self.IdTipoSucursal}, tipo={self.TipoSucursal})>"