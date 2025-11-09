from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Prestamo(Base):
    __tablename__ = "prestamo"
    
    IdPrestamo = Column(Integer, primary_key=True, index=True, autoincrement=True)
    IdCuenta = Column(Integer, ForeignKey("cuenta.IdCuenta", ondelete="CASCADE"), nullable=False, index=True)
    Numero = Column(String(20), nullable=False, unique=True, index=True)
    Fecha = Column(Date, nullable=False)
    Valor = Column(DECIMAL(15, 2), nullable=False)
    Interes = Column(DECIMAL(5, 2), nullable=False)
    Plazo = Column(Integer, nullable=False)  # En meses
    Seguro = Column(DECIMAL(10, 2), nullable=True, default=0.00)
    Cuota = Column(DECIMAL(15, 2), nullable=False)
    
    # Relaciones
    cuenta = relationship("Cuenta", back_populates="prestamos")
    
    def __repr__(self):
        return f"<Prestamo(id={self.IdPrestamo}, numero={self.Numero}, valor={self.Valor})>"