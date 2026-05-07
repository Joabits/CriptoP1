"""
Módulo de Mapeo de Debilidades Criptográficas
Analiza vulnerabilidades en hardware, software y datos asociadas a amenazas específicas
"""

from enum import Enum
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
import json
import hashlib
import numpy as np

class TipoActivo(Enum):
    HARDWARE = "Hardware"
    SOFTWARE = "Software"
    DATOS = "Datos"

class TipoAmenaza(Enum):
    ROBO = "Robo físico"
    INTERCEPTACION = "Interceptación de datos"
    MODIFICACION = "Modificación no autorizada"
    DENEGACION = "Denegación de servicio"
    SUPLANTACION = "Suplantación de identidad"
    CRIPTOANALISIS = "Criptoanálisis"
    LEAK_LATERAL = "Fuga por canal lateral"

class NivelRiesgo(Enum):
    CRITICO = "Crítico (9-10)"
    ALTO = "Alto (7-8)"
    MEDIO = "Medio (4-6)"
    BAJO = "Bajo (1-3)"
    INFORMATIVO = "Informativo (0)"

@dataclass
class Vulnerabilidad:
    """Representa una vulnerabilidad específica"""
    id: str
    nombre: str
    descripcion: str
    tipo_activo: TipoActivo
    amenazas_asociadas: List[TipoAmenaza]
    cvss_score: float
    cwe_id: str
    solucion: str

@dataclass
class Activo:
    """Representa un activo del sistema"""
    id: str
    nombre: str
    tipo: TipoActivo
    descripcion: str
    criticidad: int

@dataclass
class MapeoDebilidad:
    """Resultado del mapeo entre activo, vulnerabilidad y amenaza"""
    activo: Activo
    vulnerabilidad: Vulnerabilidad
    amenaza: TipoAmenaza
    probabilidad: float
    impacto: int
    riesgo_calculado: float
    recomendacion: str
    timestamp: datetime = field(default_factory=datetime.now)


class MapeoDebilidadesCripto:
    """Motor principal de mapeo de debilidades criptográficas"""
    
    def __init__(self):
        self.vulnerabilidades_db = self._inicializar_vulnerabilidades()
        self.activos_db = self._inicializar_activos_ejemplo()
        self.mapeos_realizados: List[MapeoDebilidad] = []
        
    def _inicializar_vulnerabilidades(self) -> Dict[str, Vulnerabilidad]:
        """Base de conocimiento de vulnerabilidades criptográficas"""
        return {
            "CWE-311": Vulnerabilidad(
                id="CWE-311",
                nombre="Falta de cifrado en datos sensibles",
                descripcion="Los datos sensibles se transmiten o almacenan sin cifrado adecuado",
                tipo_activo=TipoActivo.DATOS,
                amenazas_asociadas=[TipoAmenaza.INTERCEPTACION, TipoAmenaza.MODIFICACION],
                cvss_score=7.5,
                cwe_id="CWE-311",
                solucion="Implementar TLS 1.3 para transporte y AES-256-GCM para almacenamiento"
            ),
            "CWE-326": Vulnerabilidad(
                id="CWE-326",
                nombre="Clave criptográfica débil",
                descripcion="Uso de claves con longitud insuficiente o débiles",
                tipo_activo=TipoActivo.SOFTWARE,
                amenazas_asociadas=[TipoAmenaza.CRIPTOANALISIS],
                cvss_score=8.0,
                cwe_id="CWE-326",
                solucion="Usar claves RSA 2048+ o ECC 256+ bits"
            ),
            "CWE-327": Vulnerabilidad(
                id="CWE-327",
                nombre="Algoritmo criptográfico roto o inseguro",
                descripcion="Uso de algoritmos como MD5, SHA1, DES, RC4",
                tipo_activo=TipoActivo.SOFTWARE,
                amenazas_asociadas=[TipoAmenaza.CRIPTOANALISIS, TipoAmenaza.MODIFICACION],
                cvss_score=9.0,
                cwe_id="CWE-327",
                solucion="Migrar a SHA-256, AES-256, ChaCha20-Poly1305"
            ),
            "CWE-329": Vulnerabilidad(
                id="CWE-329",
                nombre="No usar vector de inicialización (IV)",
                descripcion="Modos ECB o uso incorrecto de IV en cifrado",
                tipo_activo=TipoActivo.SOFTWARE,
                amenazas_asociadas=[TipoAmenaza.CRIPTOANALISIS],
                cvss_score=6.5,
                cwe_id="CWE-329",
                solucion="Usar modo GCM o CBC con IV aleatorio por operación"
            ),
            "CWE-200": Vulnerabilidad(
                id="CWE-200",
                nombre="Exposición de información sensible",
                descripcion="Logs, errores o respuestas que filtran datos",
                tipo_activo=TipoActivo.DATOS,
                amenazas_asociadas=[TipoAmenaza.INTERCEPTACION],
                cvss_score=6.0,
                cwe_id="CWE-200",
                solucion="Sanitizar outputs, logs y mensajes de error"
            ),
            "HW-001": Vulnerabilidad(
                id="HW-001",
                nombre="Sin protección física contra extracción",
                descripcion="Hardware accesible sin controles físicos",
                tipo_activo=TipoActivo.HARDWARE,
                amenazas_asociadas=[TipoAmenaza.ROBO, TipoAmenaza.LEAK_LATERAL],
                cvss_score=7.0,
                cwe_id="CWE-693",
                solucion="Instalar cerraduras, vigilancia, HSM, TPM"
            ),
            "HW-002": Vulnerabilidad(
                id="HW-002",
                nombre="Canales laterales electromagnéticos",
                descripcion="Emisiones EM que pueden filtrar claves",
                tipo_activo=TipoActivo.HARDWARE,
                amenazas_asociadas=[TipoAmenaza.LEAK_LATERAL, TipoAmenaza.CRIPTOANALISIS],
                cvss_score=8.5,
                cwe_id="CWE-1300",
                solucion="Blindaje EM, mitigaciones a nivel de diseño"
            ),
            "SW-001": Vulnerabilidad(
                id="SW-001",
                nombre="Generación débil de números aleatorios",
                descripcion="Uso de PRNG predecible o mal seed",
                tipo_activo=TipoActivo.SOFTWARE,
                amenazas_asociadas=[TipoAmenaza.CRIPTOANALISIS, TipoAmenaza.SUPLANTACION],
                cvss_score=9.5,
                cwe_id="CWE-338",
                solucion="Usar CSPRNG como secrets, os.urandom, o /dev/urandom"
            ),
            "DT-001": Vulnerabilidad(
                id="DT-001",
                nombre="Almacenamiento de contraseñas sin hash",
                descripcion="Contraseñas en texto plano o hash sin salt",
                tipo_activo=TipoActivo.DATOS,
                amenazas_asociadas=[TipoAmenaza.INTERCEPTACION, TipoAmenaza.MODIFICACION],
                cvss_score=9.0,
                cwe_id="CWE-522",
                solucion="Usar bcrypt, Argon2 o PBKDF2 con salt"
            )
        }
    
    def _inicializar_activos_ejemplo(self) -> Dict[str, Activo]:
        """Activos de ejemplo para demostración"""
        return {
            "HW_SERVER": Activo("HW_SERVER", "Servidor Principal", TipoActivo.HARDWARE, 
                               "Servidor con datos críticos", 5),
            "SW_APP": Activo("SW_APP", "Aplicación Web", TipoActivo.SOFTWARE,
                            "Frontend y backend de la app", 4),
            "DB_CLIENTES": Activo("DB_CLIENTES", "Base de Clientes", TipoActivo.DATOS,
                                 "Información personal de clientes", 5),
            "HW_LAPTOP": Activo("HW_LAPTOP", "Laptop Administrador", TipoActivo.HARDWARE,
                               "Equipo con acceso privilegiado", 4),
            "SW_CRYPTO": Activo("SW_CRYPTO", "Módulo Criptográfico", TipoActivo.SOFTWARE,
                               "Librerías de cifrado", 5),
            "DB_KEYS": Activo("DB_KEYS", "Almacén de Claves", TipoActivo.DATOS,
                             "Claves criptográficas", 5)
        }
    
    def calcular_matching(self, activo: Activo, vulnerabilidad: Vulnerabilidad) -> Tuple[float, int, List[str]]:
        """
        Algoritmo de matching con ponderación matemática
        Retorna: (probabilidad, impacto, razones)
        
        Fórmula matemática:
        P = w1 * match_tipo + w2 * relevancia_directa + w3 * criticidad_activo
        donde w = [0.4, 0.4, 0.2] y cada factor normalizado [0-1]
        """
        razones = []
        
        # Factor 1: Coincidencia de tipo de activo (40% peso)
        match_tipo = 1.0 if activo.tipo == vulnerabilidad.tipo_activo else 0.0
        if match_tipo:
            razones.append(f"✓ El activo '{activo.nombre}' es de tipo {activo.tipo.value} y la vulnerabilidad {vulnerabilidad.id} aplica a este tipo")
        else:
            razones.append(f"✗ El activo es {activo.tipo.value} pero la vulnerabilidad aplica a {vulnerabilidad.tipo_activo.value}")
        
        # Factor 2: Relevancia directa
        relevancia = match_tipo
        
        # Factor 3: Criticidad del activo
        criticidad_normalizada = activo.criticidad / 5.0
        
        # Cálculo final de probabilidad
        pesos = [0.4, 0.4, 0.2]
        probabilidad = (pesos[0] * match_tipo + 
                       pesos[1] * relevancia + 
                       pesos[2] * criticidad_normalizada)
        
        # Ajuste por CVSS
        if vulnerabilidad.cvss_score >= 8.0:
            probabilidad = min(1.0, probabilidad * 1.2)
            razones.append(f"⚠ Vulnerabilidad con CVSS alto ({vulnerabilidad.cvss_score}) → +20% probabilidad")
        
        # Impacto
        impacto = int((activo.criticidad + (vulnerabilidad.cvss_score / 2)) / 2)
        impacto = max(1, min(5, round(impacto)))
        
        return round(probabilidad, 3), impacto, razones
    
    def mapear_activo_con_vulnerabilidades(self, activo_id: str) -> List[MapeoDebilidad]:
        """Mapea un activo contra todas las vulnerabilidades relevantes"""
        if activo_id not in self.activos_db:
            raise ValueError(f"Activo {activo_id} no encontrado")
        
        activo = self.activos_db[activo_id]
        resultados = []
        
        for vuln in self.vulnerabilidades_db.values():
            if activo.tipo != vuln.tipo_activo:
                continue
                
            probabilidad, impacto, razones = self.calcular_matching(activo, vuln)
            
            riesgo = probabilidad * impacto * 2
            
            recomendacion = f"Para '{activo.nombre}' con vulnerabilidad {vuln.nombre}: {vuln.solucion}"
            
            amenaza_principal = vuln.amenazas_asociadas[0] if vuln.amenazas_asociadas else TipoAmenaza.INTERCEPTACION
            
            mapeo = MapeoDebilidad(
                activo=activo,
                vulnerabilidad=vuln,
                amenaza=amenaza_principal,
                probabilidad=probabilidad,
                impacto=impacto,
                riesgo_calculado=round(riesgo, 2),
                recomendacion=recomendacion
            )
            resultados.append(mapeo)
        
        resultados.sort(key=lambda x: x.riesgo_calculado, reverse=True)
        self.mapeos_realizados.extend(resultados)
        return resultados
    
    def obtener_matriz_riesgos(self) -> np.ndarray:
        """Genera matriz matemática de riesgos"""
        amenazas = list(TipoAmenaza)
        activos = list(self.activos_db.values())
        
        matriz = np.zeros((len(activos), len(amenazas)))
        
        for i, activo in enumerate(activos):
            mapeos = self.mapear_activo_con_vulnerabilidades(activo.id)
            for mapeo in mapeos:
                j = amenazas.index(mapeo.amenaza)
                matriz[i, j] = max(matriz[i, j], mapeo.riesgo_calculado)
        
        return matriz
    
    def generar_informe_critico(self, umbral_riesgo: float = 6.0) -> List[Dict]:
        """Genera informe de vulnerabilidades críticas"""
        criticas = []
        for mapeo in self.mapeos_realizados:
            if mapeo.riesgo_calculado >= umbral_riesgo:
                criticas.append({
                    "activo": mapeo.activo.nombre,
                    "vulnerabilidad": mapeo.vulnerabilidad.nombre,
                    "cwe_id": mapeo.vulnerabilidad.cwe_id,
                    "amenaza": mapeo.amenaza.value,
                    "riesgo": mapeo.riesgo_calculado,
                    "probabilidad": f"{mapeo.probabilidad*100:.1f}%",
                    "recomendacion": mapeo.recomendacion
                })
        return criticas
    
    def estadisticas_generales(self) -> Dict:
        """Estadísticas del análisis"""
        if not self.mapeos_realizados:
            return {"error": "No hay mapeos realizados"}
        
        riesgos = [m.riesgo_calculado for m in self.mapeos_realizados]
        return {
            "total_mapeos": len(self.mapeos_realizados),
            "riesgo_promedio": round(np.mean(riesgos), 2),
            "riesgo_maximo": round(np.max(riesgos), 2),
            "riesgo_minimo": round(np.min(riesgos), 2),
            "activos_analizados": len(set(m.activo.id for m in self.mapeos_realizados)),
            "vulnerabilidades_encontradas": len(set(m.vulnerabilidad.id for m in self.mapeos_realizados))
        }