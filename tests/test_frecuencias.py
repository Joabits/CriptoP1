from cripto_grupo_f import frecuencias


def test_contar_monogramas_normaliza_acentos_y_espacios():
    conteo = frecuencias.contar_monogramas("A a, E! ñ")

    assert conteo["A"] == 2
    assert conteo["E"] == 1
    assert conteo["N"] == 1


def test_sugerir_sustituciones_usa_orden_de_frecuencia():
    sugerencias = frecuencias.sugerir_sustituciones("XXX YY Z", limite=3)

    assert sugerencias[0]["letra_cifrada"] == "X"
    assert sugerencias[0]["sugerencia_texto_plano"] == "E"
    assert sugerencias[1]["sugerencia_texto_plano"] == "A"


def test_contar_ngramas_calcula_digramas():
    digramas = frecuencias.contar_ngramas("ABABA", longitud=2)

    assert digramas[0]["ngrama"] == "AB"
    assert digramas[0]["conteo"] == 2


def test_parsear_sustituciones_acepta_varios_formatos():
    mapa = frecuencias.parsear_sustituciones("X=E, Q->A; Z:R")

    assert mapa == {"X": "E", "Q": "A", "Z": "R"}
