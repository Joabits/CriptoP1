from cripto_grupo_f import criptoanalisis


def test_cesar_cifra_y_descifra():
    texto = "LA CRIPTOGRAFIA"
    cifrado = criptoanalisis.cifrar_cesar(texto, 7)

    assert criptoanalisis.descifrar_cesar(cifrado, 7) == texto


def test_fuerza_bruta_incluye_clave_correcta():
    texto = "EL CANAL DE COMUNICACION"
    cifrado = criptoanalisis.cifrar_cesar(texto, 9)
    candidatos = criptoanalisis.fuerza_bruta_cesar(cifrado)

    assert any(item["clave_probada"] == 9 and item["texto_posible"] == texto for item in candidatos)
