from cripto_grupo_f import debilidades


def test_obtener_debilidades_incluye_tipo_amenaza():
    datos = debilidades.obtener_debilidades("Datos")

    assert datos
    assert all("tipo_amenaza" in item for item in datos)


def test_resumen_por_tipo_cubre_tres_clases():
    tipos = {item["tipo"] for item in debilidades.resumen_por_tipo()}

    assert tipos == {"Hardware", "Software", "Datos"}