from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Cuentahabiente(Base):
    __tablename__ = "cuentahabiente"
    
    IdCuentahabiente = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Nombre = Column(String(100), nullable=False)
    IdTipoDocumento = Column(Integer, ForeignKey("tipodocumento.IdTipoDocumento"), nullable=False)
    Documento = Column(String(50), nullable=False, unique=True, index=True)
    Direccion = Column(String(100), nullable=True)
    Telefono = Column(String(20), nullable=True)
    IdCiudad = Column(Integer, ForeignKey("ciudad.IdCiudad"), nullable=False)
    Clave = Column(String(20), nullable=False)
    
    # Relaciones
    tipo_documento = relationship("TipoDocumento", back_populates="cuentahabientes")
    ciudad = relationship("Ciudad", back_populates="cuentahabientes")
    titulares = relationship("Titular", back_populates="cuentahabiente", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Cuentahabiente(id={self.IdCuentahabiente}, nombre={self.Nombre}, documento={self.Documento})>"