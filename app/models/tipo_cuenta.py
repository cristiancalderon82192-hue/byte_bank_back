from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.orm import relationship
from app.database import Base


class TipoCuenta(Base):
    __tablename__ = "tipocuenta"
    
    IdTipoCuenta = Column(Integer, primary_key=True, index=True, autoincrement=True)
    TipoCuenta = Column(String(50), nullable=False)
    Sobregiro = Column(DECIMAL(10, 2), nullable=True)
    
    # Relaciones
    cuentas = relationship("Cuenta", back_populates="tipo_cuenta")
    
    def __repr__(self):
        return f"<TipoCuenta(id={self.IdTipoCuenta}, tipo={self.TipoCuenta})>"