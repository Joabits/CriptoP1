from cripto_grupo_f import comunicaciones


def test_evaluar_canal_seguro_con_tres_controles():
    resultado = comunicaciones.evaluar_canal(cifrado=True, autenticado=True, integridad=True)

    assert resultado["estado"] == "Canal seguro"
    assert resultado["riesgo"] == "Bajo"
    assert resultado["faltantes"] == []


def test_simular_transmision_sin_cifrado_expone_mensaje():
    resultado = comunicaciones.simular_transmision("EXPEDIENTE", atacante_intercepta=True, canal_cifrado=False)

    assert "EXPEDIENTE" in resultado["observacion_del_atacante"]
