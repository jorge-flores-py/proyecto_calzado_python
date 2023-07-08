import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import numpy as np

engine = create_engine("sqlite:///ventas_calzados.db")
Session = sessionmaker(bind=engine)
Session = Session()

base = declarative_base()

class Venta(base):
    __tablename__ = "ventas"
    id = Column(Integer, primary_key=True)
    fecha = Column(String)
    producto_id = Column(Integer)
    pais = Column(String)
    genero = Column(String)
    talle = Column(String)
    precio = Column(String)

def read_db():
    ventas = Session.query(Venta).all()
    paises = []
    generos = []
    talles = []
    precios = []

    for venta in ventas:
        paises.append(venta.pais)
        generos.append(venta.genero)
        talles.append(venta.talle)
        precios.append(float(venta.precio.strip()[1:]))

    paises = np.array(paises)
    generos = np.array(generos)
    talles = np.array(talles)
    precios = np.array(precios)

    return paises, generos, talles, precios

def obtener_paises_unicos(paises):
    paises_unicos = np.unique(paises)
    return paises_unicos

def obtener_ventas_por_pais(paises_objetivo, paises, precios):
    ventas_por_pais = {}

    for pais in paises_objetivo:
        mask = paises == pais
        ventas = precios[mask]
        monto_total = np.sum(ventas)
        ventas_por_pais[pais] = monto_total
    
    return ventas_por_pais

def obtener_calzado_mas_vendido_por_pais(paises_objetivo, paises, talles):
    calzado_mas_vendido_por_pais = {}

    for pais in paises_objetivo:
        mask = paises == pais
        talles_pais = talles[mask]
        unique_talles, counts = np.unique(talles_pais, return_counts=True)
        max_count_index = np.argmax(counts)
        calzado_mas_vendido_por_pais[pais] = unique_talles[max_count_index]

    return calzado_mas_vendido_por_pais


def obtener_ventas_por_genero_pais(paises_objetivo, genero_objetivo, paises, generos):
    ventas_por_genero_pais = {}

    for pais in paises_objetivo:
        mask_pais = paises == pais
        mask_genero = generos == genero_objetivo
        ventas = np.sum(mask_pais & mask_genero)
        ventas_por_genero_pais[pais] = ventas
    return ventas_por_genero_pais 

if __name__ == "__main__":
 
    print("\n¡Aquí utilizo mis funciones!\n")
    
    paises, generos, talles, precios = read_db()

    # Prueba de las funciones
    paises_unicos = obtener_paises_unicos(paises)
    print("Países únicos:", paises_unicos)

    paises_objetivo = ["Canada", "Germany"]
    ventas_por_pais = obtener_ventas_por_pais(paises_objetivo, paises, precios)
    print("Ventas por país:", ventas_por_pais)

    genero_objetivo = "Female"
    ventas_por_genero_pais = obtener_ventas_por_genero_pais(
        paises_objetivo, genero_objetivo, paises, generos
    )
    print("Ventas por género y país:", ventas_por_genero_pais)

    calzado_mas_vendido_por_pais = obtener_calzado_mas_vendido_por_pais(
        paises_objetivo, paises, talles
    )
    print("Calzado más vendido por país:", calzado_mas_vendido_por_pais)

        
        