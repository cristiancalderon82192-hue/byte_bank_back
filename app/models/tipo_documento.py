from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class TipoDocumento(Base):
    __tablename__ = "tipodocumento"
    
    IdTipoDocumento = Column(Integer, primary_key=True, index=True, autoincrement=True)
    TipoDocumento = Column(String(50), nullable=False)
    Sigla = Column(String(10), nullable=True)
    
    # Relaciones
    cuentahabientes = relationship("Cuentahabiente", back_populates="tipo_documento")
    
    def __repr__(self):
        return f"<TipoDocumento(id={self.IdTipoDocumento}, tipo={self.TipoDocumento}, sigla={self.Sigla})>"