from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Ciudad(Base):
    __tablename__ = "ciudad"
    
    IdCiudad = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Ciudad = Column(String(50), nullable=False)
    
    # Relaciones
    cuentahabientes = relationship("Cuentahabiente", back_populates="ciudad")
    sucursales = relationship("Sucursal", back_populates="ciudad")
    
    def __repr__(self):
        return f"<Ciudad(id={self.IdCiudad}, nombre={self.Ciudad})>"