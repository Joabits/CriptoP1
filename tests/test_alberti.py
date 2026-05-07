from cripto_grupo_f import alberti
from cripto_grupo_f.alberti import ALFABETO_EXTERIOR, ALFABETO_INTERIOR


def test_alberti_cifra_y_descifra_con_misma_configuracion():
    # Solo letras del alfabeto exterior historico (sin H, J, K, U, W, Y)
    texto = "EL SECRETO"
    cifrado = alberti.cifrar(texto, posicion_inicial=4, rotar_cada=3)
    descifrado = alberti.descifrar(cifrado["texto_salida"], posicion_inicial=4, rotar_cada=3)

    assert descifrado["texto_salida"] == cifrado["texto_entrada"]


def test_alberti_rechaza_rotacion_invalida():
    try:
        alberti.cifrar("ABC", posicion_inicial=0, rotar_cada=0)
    except ValueError as exc:
        assert "rotar_cada" in str(exc)
    else:
        raise AssertionError("Se esperaba ValueError")


def test_alberti_cifra_y_descifra_con_rotacion_izquierda():
    texto = "CANAL SEGURO"
    cifrado = alberti.cifrar(texto, posicion_inicial=10, rotar_cada=4, direccion="izquierda", avance=2)
    descifrado = alberti.descifrar(
        cifrado["texto_salida"], posicion_inicial=10, rotar_cada=4, direccion="izquierda", avance=2
    )

    assert descifrado["texto_salida"] == cifrado["texto_entrada"]
    # El simbolo inicial en posicion 10 del alfabeto interior
    assert cifrado["simbolo_inicial"] == ALFABETO_INTERIOR[10]


def test_posicion_desde_letra_funciona():
    # '&' esta en posicion 0 del alfabeto interior
    assert alberti.posicion_desde_letra("&") == 0
    # 'a' esta en posicion 4
    assert alberti.posicion_desde_letra("a") == 4


def test_rotar_disco_alinea_primer_simbolo():
    # Rotando a posicion 0, el primer simbolo interior queda alineado con el primer exterior
    disco = alberti.rotar_disco(0)
    assert disco[0] == ALFABETO_INTERIOR[0]


def test_rotar_disco_desplaza_correctamente():
    disco = alberti.rotar_disco(3)
    # El simbolo en posicion 3 del interior original debe quedar primero
    assert disco[0] == ALFABETO_INTERIOR[3]


def test_disco_escolar_desplaza_igual():
    disco_escolar = alberti.rotar_disco(5, tipo_disco=alberti.TIPO_DISCO_ESCOLAR)
    assert disco_escolar[0] == ALFABETO_INTERIOR[5]


def test_alberti_escolar_cifra_y_descifra():
    texto = "ABCDE"
    cifrado = alberti.cifrar(texto, posicion_inicial=2, rotar_cada=50, tipo_disco=alberti.TIPO_DISCO_ESCOLAR)
    descifrado = alberti.descifrar(
        cifrado["texto_salida"], posicion_inicial=2, rotar_cada=50, tipo_disco=alberti.TIPO_DISCO_ESCOLAR
    )

    assert descifrado["texto_salida"] == cifrado["texto_entrada"]


def test_alfabetos_tienen_mismo_tamano():
    assert len(ALFABETO_EXTERIOR) == len(ALFABETO_INTERIOR)


def test_alfabeto_exterior_no_tiene_letras_prohibidas():
    letras_prohibidas = set("HJKUWY")
    for letra in ALFABETO_EXTERIOR:
        assert letra not in letras_prohibidas, f"'{letra}' no deberia estar en el alfabeto exterior"


def test_ejemplo_historico_el_secreto():
    # Verifica que cifrar y descifrar "EL SECRETO" (el ejemplo de la diapositiva) funciona
    texto = "EL SECRETO"
    cifrado = alberti.cifrar(texto, posicion_inicial=0, rotar_cada=5)
    descifrado = alberti.descifrar(cifrado["texto_salida"], posicion_inicial=0, rotar_cada=5)
    assert descifrado["texto_salida"] == cifrado["texto_entrada"]