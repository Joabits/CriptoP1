from cripto_grupo_f import criptoanalisis


def test_cesar_cifra_y_descifra():
    texto = "LA CRIPTOGRAFIA"
    cifrado = criptoanalisis.cifrar_cesar(texto, 7)

    assert criptoanalisis.descifrar_cesar(cifrado, 7) == texto


def test_cesar_alfabeto_espanol_conserva_enie():
    texto = "NIÑO"
    cifrado = criptoanalisis.cifrar_cesar(texto, 1, criptoanalisis.ALFABETO_ESPANOL)

    assert cifrado == "ÑJOP"
    assert criptoanalisis.descifrar_cesar(cifrado, 1, criptoanalisis.ALFABETO_ESPANOL) == texto


def test_fuerza_bruta_incluye_clave_correcta():
    texto = "EL CANAL DE COMUNICACION"
    cifrado = criptoanalisis.cifrar_cesar(texto, 9)
    candidatos = criptoanalisis.fuerza_bruta_cesar(cifrado)

    assert any(item["clave_probada"] == 9 and item["texto_posible"] == texto for item in candidatos)


def test_definiciones_autores_incluyen_respaldo_teorico():
    definiciones = criptoanalisis.definiciones_autores()

    assert any(item["autor"] == "Kerckhoffs" for item in definiciones)
    assert any("busqueda exhaustiva" in item["idea"] for item in definiciones)


def test_analisis_criptoanalitico_sugiere_clave_por_frecuencia():
    texto = "ESTE TEXTO REPITE E PARA CREAR UNA PISTA TECNICA"
    cifrado = criptoanalisis.cifrar_cesar(texto, 4)
    analisis = criptoanalisis.analisis_criptoanalitico_cesar(cifrado)

    assert analisis[0]["clave_sugerida"] == 4


def test_fuerza_bruta_usa_alfabeto_espanol():
    texto = "HOLA NIÑO"
    cifrado = criptoanalisis.cifrar_cesar(texto, 3, criptoanalisis.ALFABETO_ESPANOL)
    candidatos = criptoanalisis.fuerza_bruta_cesar(cifrado, criptoanalisis.ALFABETO_ESPANOL)

    assert any(item["clave_probada"] == 3 and item["texto_posible"] == texto for item in candidatos)
