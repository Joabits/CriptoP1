from cripto_grupo_f import alberti


def test_alberti_cifra_y_descifra_con_misma_configuracion():
    texto = "LA SEGURIDAD DEL CANAL ES IMPORTANTE"
    cifrado = alberti.cifrar(texto, posicion_inicial=4, rotar_cada=3)
    descifrado = alberti.descifrar(cifrado["texto_salida"], posicion_inicial=4, rotar_cada=3)

    assert descifrado["texto_salida"] == texto


def test_alberti_rechaza_rotacion_invalida():
    try:
        alberti.cifrar("ABC", posicion_inicial=0, rotar_cada=0)
    except ValueError as exc:
        assert "rotar_cada" in str(exc)
    else:
        raise AssertionError("Se esperaba ValueError")


def test_alberti_cifra_y_descifra_con_rotacion_izquierda():
    texto = "MENSAJE CON ROTACION INVERSA"
    cifrado = alberti.cifrar(texto, posicion_inicial=10, rotar_cada=4, direccion="izquierda", avance=2)
    descifrado = alberti.descifrar(
        cifrado["texto_salida"], posicion_inicial=10, rotar_cada=4, direccion="izquierda", avance=2
    )

    assert descifrado["texto_salida"] == texto
    assert cifrado["letra_inicial"] == "K"


def test_posicion_desde_letra_normaliza_entrada():
    assert alberti.posicion_desde_letra("d") == 3
