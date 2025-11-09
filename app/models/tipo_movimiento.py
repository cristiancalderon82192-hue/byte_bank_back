from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class TipoMovimiento(Base):
    __tablename__ = "tipomovimiento"
    
    IdTipoMovimiento = Column(Integer, primary_key=True, index=True, autoincrement=True)
    TipoMovimiento = Column(String(50), nullable=False)
    
    # Relaciones
    movimientos = relationship("Movimiento", back_populates="tipo_movimiento")
    
    def __repr__(self):
        return f"<TipoMovimiento(id={self.IdTipoMovimiento}, tipo={self.TipoMovimiento})>"