from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Titular(Base):
    __tablename__ = "titular"
    
    IdCuenta = Column(Integer, ForeignKey("cuenta.IdCuenta", ondelete="CASCADE"), primary_key=True)
    IdCuentahabiente = Column(Integer, ForeignKey("cuentahabiente.IdCuentahabiente", ondelete="CASCADE"), primary_key=True)
    
    # Relaciones
    cuenta = relationship("Cuenta", back_populates="titulares")
    cuentahabiente = relationship("Cuentahabiente", back_populates="titulares")
    
    def __repr__(self):
        return f"<Titular(IdCuenta={self.IdCuenta}, IdCuentahabiente={self.IdCuentahabiente})>"