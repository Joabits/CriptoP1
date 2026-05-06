from __future__ import annotations

import pytest

from cripto_grupo_f import comunicaciones


# ----------  describir_sistema() --------------
def test_describir_sistema_aislado_retorna_nombre_correcto():
    r = comunicaciones.describir_sistema("aislado")
    assert r["nombre"] == "Sistema Aislado (StandAlone)"


def test_describir_sistema_retorna_campos_completos():
    r = comunicaciones.describir_sistema("interconectado")
    for campo in ("nombre", "descripcion", "acceso", "amenaza_principal", "ejemplos", "pilares_en_riesgo"):
        assert campo in r, f"Falta el campo '{campo}' en el resultado"


def test_describir_sistema_tipo_invalido_lanza_error():
    with pytest.raises(ValueError):
        comunicaciones.describir_sistema("nube")


# -------------  calcular_superficie_ataque()
def test_calcular_superficie_aislado_puntaje_y_nivel():
    r = comunicaciones.calcular_superficie_ataque("aislado")
    assert r["puntaje_total"] == 7
    assert r["nivel"] == "Moderado"


def test_calcular_superficie_interconectado_nivel_critico():
    r = comunicaciones.calcular_superficie_ataque("interconectado")
    assert r["puntaje_total"] == 18
    assert r["nivel"] == "Critico"


def test_calcular_superficie_retorna_lista_de_vectores():
    r = comunicaciones.calcular_superficie_ataque("aislado")
    assert isinstance(r["vectores"], list)
    assert len(r["vectores"]) > 0



# --------------- filtrar_amenazas_por_tipo()

def test_filtrar_amenazas_pasivas_retorna_solo_pasivas():
    pasivas = comunicaciones.filtrar_amenazas_por_tipo("Pasivo")
    assert len(pasivas) == 1
    assert all(a["tipo_ataque"] == "Pasivo" for a in pasivas)


def test_filtrar_amenazas_activas_retorna_solo_activas():
    activas = comunicaciones.filtrar_amenazas_por_tipo("Activo")
    assert len(activas) == 2
    assert all(a["tipo_ataque"] == "Activo" for a in activas)


def test_filtrar_amenazas_tipo_invalido_lanza_error():
    with pytest.raises(ValueError):
        comunicaciones.filtrar_amenazas_por_tipo("Fisico")


# -----------  evaluar_canal()

def test_evaluar_canal_todos_activos_es_seguro():
    r = comunicaciones.evaluar_canal(cifrado=True, autenticado=True, integridad=True)
    assert r["puntaje"] == 100
    assert r["nivel"] == "Seguro"
    assert r["pilares_activos"] == ["Confidencialidad", "Autenticidad", "Integridad"]
    assert r["pilares_faltantes"] == []


def test_evaluar_canal_todos_inactivos_es_critico():
    r = comunicaciones.evaluar_canal(cifrado=False, autenticado=False, integridad=False)
    assert r["puntaje"] == 0
    assert r["nivel"] == "Critico"
    assert r["pilares_activos"] == []
    assert len(r["pilares_faltantes"]) == 3


def test_evaluar_canal_solo_cifrado_puntaje_40():
    r = comunicaciones.evaluar_canal(cifrado=True, autenticado=False, integridad=False)
    assert r["puntaje"] == 40
    assert r["nivel"] == "Inseguro"
    assert "Confidencialidad" in r["pilares_activos"]


def test_evaluar_canal_cifrado_y_autenticado_parcialmente_seguro():
    r = comunicaciones.evaluar_canal(cifrado=True, autenticado=True, integridad=False)
    assert r["puntaje"] == 75
    assert r["nivel"] == "Parcialmente Seguro"


def test_evaluar_canal_pilar_faltante_tiene_cuatro_campos():
    r = comunicaciones.evaluar_canal(cifrado=False, autenticado=True, integridad=True)
    faltante = r["pilares_faltantes"][0]
    for campo in ("pilar", "peso_perdido", "consecuencia", "amenaza_habilitada"):
        assert campo in faltante, f"Falta '{campo}' en el pilar faltante"


def test_evaluar_canal_diagnostico_es_string_no_vacio():
    r = comunicaciones.evaluar_canal(cifrado=True, autenticado=False, integridad=False)
    assert isinstance(r["diagnostico"], str)
    assert len(r["diagnostico"]) > 0



# ---------- simular_transmision()

def test_simular_transmision_canal_limpio_genera_tres_pasos():
    r = comunicaciones.simular_transmision("Nota: 9.5", canal_cifrado=False, tipo_ataque="ninguno")
    assert len(r["log"]) == 3
    assert r["mensaje_original"] == r["mensaje_recibido"]


def test_simular_transmision_pasivo_sin_cifrar_genera_cuatro_pasos():
    r = comunicaciones.simular_transmision("Nota: 9.5", canal_cifrado=False, tipo_ataque="pasivo")
    assert len(r["log"]) == 4
    etapas = [evento["etapa"] for evento in r["log"]]
    assert "Atacante" in etapas


def test_simular_transmision_pasivo_sin_cifrar_atacante_lee_mensaje():
    r = comunicaciones.simular_transmision("SECRETO", canal_cifrado=False, tipo_ataque="pasivo")
    contenido_atacante = r["log"][2]["contenido_visible"]
    assert "SECRETO" in contenido_atacante


def test_simular_transmision_pasivo_con_cifrado_atacante_no_lee():
    r = comunicaciones.simular_transmision("SECRETO", canal_cifrado=True, tipo_ataque="pasivo")
    contenido_atacante = r["log"][2]["contenido_visible"]
    assert "SECRETO" not in contenido_atacante
    assert "ilegible" in contenido_atacante


def test_simular_transmision_activo_mensaje_llega_alterado():
    r = comunicaciones.simular_transmision("Nota: 9.5", canal_cifrado=False, tipo_ataque="activo")
    assert r["mensaje_recibido"] != r["mensaje_original"]
    assert "[ALTERADO]" in r["mensaje_recibido"]


def test_simular_transmision_activo_advertencia_menciona_mitm():
    r = comunicaciones.simular_transmision("Nota: 9.5", canal_cifrado=False, tipo_ataque="activo")
    assert "MITM" in r["advertencia"]


def test_simular_transmision_log_tiene_campos_requeridos():
    r = comunicaciones.simular_transmision("Msg", canal_cifrado=False, tipo_ataque="ninguno")
    for evento in r["log"]:
        for campo in ("paso", "etapa", "evento", "contenido_visible"):
            assert campo in evento, f"Falta el campo '{campo}' en el evento del log"


def test_simular_transmision_tipo_ataque_invalido_lanza_error():
    with pytest.raises(ValueError):
        comunicaciones.simular_transmision("Msg", canal_cifrado=False, tipo_ataque="espionaje")





# def test_evaluar_canal_seguro_con_tres_controles():
#     resultado = comunicaciones.evaluar_canal(cifrado=True, autenticado=True, integridad=True)

#     assert resultado["estado"] == "Canal seguro"
#     assert resultado["riesgo"] == "Bajo"
#     assert resultado["faltantes"] == []


# def test_simular_transmision_sin_cifrado_expone_mensaje():
#     resultado = comunicaciones.simular_transmision("EXPEDIENTE", atacante_intercepta=True, canal_cifrado=False)

#     assert "EXPEDIENTE" in resultado["observacion_del_atacante"]
