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


def test_rotar_disco_alinea_clave_con_a_exterior():
    assert alberti.rotar_disco(alberti.posicion_desde_letra("f"))[0] == "F"


def test_disco_escolar_usa_alfabeto_desplazado():
    posicion_f = alberti.posicion_desde_letra("f")

    assert alberti.rotar_disco(posicion_f, tipo_disco=alberti.TIPO_DISCO_ESCOLAR).startswith("FGHIJ")


def test_alberti_escolar_cifra_y_descifra_con_misma_configuracion():
    texto = "HOLA"
    cifrado = alberti.cifrar(texto, posicion_inicial=5, rotar_cada=50, tipo_disco=alberti.TIPO_DISCO_ESCOLAR)
    descifrado = alberti.descifrar(
        cifrado["texto_salida"], posicion_inicial=5, rotar_cada=50, tipo_disco=alberti.TIPO_DISCO_ESCOLAR
    )

    assert cifrado["texto_salida"] == "MTQF"
    assert descifrado["texto_salida"] == texto
