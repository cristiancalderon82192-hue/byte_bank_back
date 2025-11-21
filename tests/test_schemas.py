"""
Script de prueba para validar los schemas Pydantic.
Ejecutar desde la raíz del proyecto: python test_schemas.py

Este script NO es una prueba unitaria (pytest), sino una validación
rápida para verificar que los schemas funcionan correctamente.
"""

from datetime import date
from decimal import Decimal

print("Probando Schemas Pydantic")
print("=" * 50)

# ============================================
# 1. Probar Schema de Ciudad
# ============================================
print("\n1.Probando CiudadCreate...")
try:
    from app.schemas.ciudad import CiudadCreate, CiudadResponse
    
    ciudad = CiudadCreate(Ciudad="Bogotá")
    print(f"CiudadCreate: {ciudad.model_dump()}")
    
    # Simular response
    ciudad_response = CiudadResponse(IdCiudad=1, Ciudad="Bogotá")
    print(f"CiudadResponse: {ciudad_response.model_dump()}")
except Exception as e:
    print(f"Error: {e}")

# ============================================
# 2. Probar Schema de Cuentahabiente
# ============================================
print("\n2. Probando CuentahabienteCreate...")
try:
    from app.schemas.cuentahabiente import CuentahabienteCreate
    
    cuentahabiente = CuentahabienteCreate(
        Nombre="Juan Pérez",
        IdTipoDocumento=1,
        Documento="1234567890",
        Direccion="Calle 123",
        Telefono="3001234567",
        IdCiudad=1,
        Clave="clave123"
    )
    print(f"CuentahabienteCreate: {cuentahabiente.model_dump()}")
except Exception as e:
    print(f"Error: {e}")

# ============================================
# 3. Probar Schema de Cuenta
# ============================================
print("\n3. Probando CuentaCreate...")
try:
    from app.schemas.cuenta import CuentaCreate
    
    cuenta = CuentaCreate(
        Numero="1234567890",
        FechaApertura=date.today(),
        IdTipoCuenta=1,
        IdSucursal=1,
        Saldo=Decimal("1000000.00")
    )
    print(f"CuentaCreate: {cuenta.model_dump()}")
except Exception as e:
    print(f"Error: {e}")

# ============================================
# 4. Probar Schema de Depósito
# ============================================
print("\n4. Probando DepositoCreate...")
try:
    from app.schemas.movimiento import DepositoCreate
    
    deposito = DepositoCreate(
        IdCuenta=1,
        IdSucursal=1,
        Valor=Decimal("500000.00"),
        Descripcion="Depósito de prueba"
    )
    print(f"DepositoCreate: {deposito.model_dump()}")
except Exception as e:
    print(f"Error: {e}")

# ============================================
# 5. Probar Schema de Transferencia
# ============================================
    print("\n5. Probando TransferenciaCreate...")
try:
    from app.schemas.movimiento import TransferenciaCreate
    
    transferencia = TransferenciaCreate(
        IdCuentaOrigen=1,
        IdCuentaDestino=2,
        IdSucursal=1,
        Valor=Decimal("100000.00"),
        Descripcion="Transferencia de prueba"
    )
    print(f"TransferenciaCreate: {transferencia.model_dump()}")
except Exception as e:
    print(f"Error: {e}")

# ============================================
# 6. Probar Schema de Préstamo
# ============================================
print("\n6. Probando PrestamoCreate...")
try:
    from app.schemas.prestamo import PrestamoCreate
    
    prestamo = PrestamoCreate(
        IdCuenta=1,
        Numero="PRE-20240001",
        Fecha=date.today(),
        Valor=Decimal("10000000.00"),
        Interes=Decimal("12.50"),
        Plazo=36,
        Seguro=Decimal("50000.00")
    )
    print(f"PrestamoCreate: {prestamo.model_dump()}")
except Exception as e:
    print(f"Error: {e}")

# ============================================
# 7. Probar Cálculo de Cuota
# ============================================
print("\n7. Probando CalculoCuota...")
try:
    from app.schemas.prestamo import CalculoCuota
    from app.crud.prestamo import calcular_cuota
    
    calculo = CalculoCuota(
        Valor=Decimal("10000000.00"),
        Interes=Decimal("12.50"),
        Plazo=36,
        Seguro=Decimal("50000.00")
    )
    resultado = calcular_cuota(calculo)
    print(f"Cuota Mensual: ${resultado['CuotaMensual']:,.2f}")
    print(f"Total a Pagar: ${resultado['TotalAPagar']:,.2f}")
    print(f"Total Intereses: ${resultado['TotalIntereses']:,.2f}")
except Exception as e:
    print(f"Error: {e}")

# ============================================
# 8. Probar Validaciones
# ============================================
print("\n8. Probando Validaciones...")
try:
    from app.schemas.cuenta import CuentaCreate
    from pydantic import ValidationError
    
    # Intentar crear cuenta con número inválido (debe fallar)
    try:
        cuenta_invalida = CuentaCreate(
            Numero="ABC123",  # Solo acepta dígitos
            FechaApertura=date.today(),
            IdTipoCuenta=1,
            IdSucursal=1
        )
        print("Error: Validación falló - debería rechazar números con letras")
    except ValidationError as ve:
        print("Error: Validación funcionó correctamente - rechazó número inválido")
except Exception as e:
    print(f"Error: Error inesperado: {e}")

print("\n" + "=" * 50)
print("Error: Pruebas de schemas completadas")
print("\nPara pruebas más completas, usa pytest en la carpeta tests/")