from cripto_grupo_f import auditoria


def test_auditoria_segura_con_cuatro_controles():
    resultado = auditoria.evaluar_auditoria({"P1": True, "P2": True, "P3": True, "P4": True})

    assert resultado["estado"] == "Seguro"
    assert resultado["puntaje"] == 4


def test_auditoria_insegura_con_un_control():
    resultado = auditoria.evaluar_auditoria({"P1": True, "P2": False, "P3": False, "P4": False})

    assert resultado["estado"] == "Inseguro"
    assert len(resultado["recomendaciones"]) == 3
