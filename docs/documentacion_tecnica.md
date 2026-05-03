# Documentacion tecnica del proyecto

## Objetivo

Desarrollar una libreria educativa en Python para estudiar conceptos de criptografia clasica, criptoanalisis y seguridad de la informacion. La libreria se demuestra mediante una interfaz interactiva que permite analizar activos, comparar canales de comunicacion, estudiar fuerza bruta contra criptoanalisis, auditar expedientes academicos, analizar frecuencias y simular el Disco de Alberti.

## Modulos implementados

### 1. Mapeo de Debilidades

Clasifica activos en Hardware, Software y Datos. Para cada activo se asocian vulnerabilidades, tipo de amenaza, amenaza concreta, impacto y controles recomendados.

Ejemplo:

- Activo: expedientes academicos.
- Vulnerabilidad: datos almacenados sin cifrado.
- Tipo de amenaza: divulgacion de informacion.
- Amenaza: divulgacion de informacion confidencial.
- Control: cifrado, permisos y registro de accesos.

### 2. Seguridad en Comunicaciones

Compara sistemas aislados contra sistemas interconectados. El modulo evalua si un canal tiene cifrado, autenticacion e integridad.

Regla usada:

- 3 controles: canal seguro.
- 2 controles: canal parcialmente seguro.
- 0 o 1 control: canal inseguro.

### 3. Criptoanalisis Elegante

Usa el cifrado Cesar como ejemplo didactico. La fuerza bruta prueba todas las claves posibles. El criptoanalisis mejora la busqueda usando indicios linguisticos como palabras frecuentes del castellano.

Definicion usada en la exposicion:

- Fuerza bruta: metodo exhaustivo que intenta claves hasta encontrar una salida legible o verificable.
- Criptoanalisis: estudio tecnico del criptosistema, del idioma, de la estructura matematica y de los patrones del criptograma para reducir el espacio de busqueda.

Para la presentacion final conviene mencionar el principio de Kerckhoffs: la seguridad no debe depender de ocultar el algoritmo, sino de proteger la clave. Tambien puede mencionarse a Shannon para explicar la relacion entre confusion, difusion y seguridad moderna. No se incluyen citas textuales para evitar atribuir frases sin la fuente exacta usada por la docente.

Formula del cifrado Cesar:

```text
C = (P + k) mod 26
P = (C - k) mod 26
```

Donde `P` es la posicion de la letra plana, `C` es la posicion cifrada y `k` es el desplazamiento.

### 4. Auditoria Academica

Evalua expedientes academicos con cuatro preguntas de control:

- P1: cifrado en reposo.
- P2: acceso solo para usuarios autorizados.
- P3: registro de accesos y cambios.
- P4: copias de seguridad verificadas.

El resultado puede ser Seguro, Parcialmente seguro o Inseguro.

### 5. Analizador de Frecuencias ESTIRANDO

Cuenta monogramas en un criptograma y calcula su frecuencia relativa.

Formula:

```text
frecuencia(letra) = apariciones(letra) / total_de_letras * 100
```

Luego compara las letras mas repetidas del criptograma con las nueve letras frecuentes del castellano:

```text
E, A, O, S, R, N, I, D, C
```

Estas letras suelen concentrar una parte alta de los textos en castellano. El sistema propone sustituciones iniciales, por ejemplo `X -> E` si `X` es la letra mas frecuente del criptograma.

El modulo tambien calcula digramas y trigramas. Esto permite buscar patrones frecuentes del idioma, por ejemplo `DE`, `EN`, `ES`, `QUE`, `LOS` o `DEL`. Ademas, la interfaz permite editar sustituciones manuales con formatos como `X=E`, `Q=A` o `Z->O`.

Advertencia tecnica: la sustitucion automatica es una hipotesis inicial, no una garantia de descifrado completo. El criptoanalista debe validar las propuestas con palabras probables, digramas, trigramas y contexto.

### 6. Disco de Alberti

Simula un cifrador polialfabetico. Se usa un alfabeto exterior fijo y un disco interior desordenado. Cada cierto numero de letras, el disco interior rota. La interfaz permite configurar posicion inicial, intervalo de rotacion, direccion y avance.

Alfabetos usados:

```text
Exterior: ABCDEFGHIJKLMNOPQRSTUVWXYZ
Interior: PHQGIUMEAYLNOFDXJKRCVSTZWB
```

Proceso de cifrado:

1. Se normaliza el texto a mayusculas sin acentos.
2. Se ubica cada letra en el alfabeto exterior.
3. Se toma la letra correspondiente en el disco interior rotado.
4. Cada `N` letras procesadas, el disco interior rota segun la direccion y avance configurados.

Proceso de descifrado:

1. Se usa la misma posicion inicial y el mismo intervalo de rotacion.
2. Se ubica la letra cifrada en el disco interior actual.
3. Se recupera la letra correspondiente del alfabeto exterior.

## Ejemplo Alberti

Entrada:

```text
Texto: LA SEGURIDAD
Posicion inicial: 3
Rotar cada: 5 letras
```

El programa genera un criptograma y una tabla paso a paso con la posicion del disco, la letra indice, el alfabeto interior usado y la letra resultante.

## Manual de uso

1. Instalar dependencias con `pip install -r requirements.txt`.
2. Ejecutar `streamlit run app.py`.
3. Elegir un modulo en el menu lateral.
4. Ingresar datos de prueba.
5. Revisar tablas, graficos y resultados.

## Pruebas y validacion

El proyecto incluye pruebas con `pytest` para verificar:

- Cifrado y descifrado correcto del Disco de Alberti.
- Rotacion hacia derecha e izquierda en Alberti.
- Conteo y sugerencia de frecuencias.
- Conteo de digramas y parseo de sustituciones manuales.
- Evaluacion de auditoria academica.
- Evaluacion de canales de comunicacion.
- Mapeo de debilidades con tipo de amenaza.
- Fuerza bruta sobre Cesar.

## Cobertura frente a la rubrica

| Criterio | Evidencia en el proyecto |
|---|---|
| Implementacion funcional | Seis secciones disponibles en la interfaz Streamlit. |
| Correctitud criptografica | Cesar, analisis de frecuencias y Alberti tienen funciones separadas y pruebas. |
| Diseno modular | La logica esta en `cripto_grupo_f/`; la interfaz solo consume la libreria. |
| Interfaz | Menu lateral, formularios, tablas, metricas, graficos y simulaciones. |
| Visualizacion | Diagramas de comunicacion, histograma de frecuencias y tablas paso a paso. |
| Documentacion | Este documento cubre objetivo, algoritmo, matematica, ejemplo y manual. |
| Pruebas | Carpeta `tests/` con validaciones automaticas para modulos criptograficos y de seguridad. |
| Innovacion | Enfoque didactico con comparativas y escenarios interactivos. |
| Presentacion | Se puede repartir un modulo por integrante y cerrar con Alberti/frecuencias. |

## Referencias bibliograficas sugeridas

- Kerckhoffs, A. (1883). La cryptographie militaire. Journal des sciences militaires.
- Shannon, C. E. (1949). Communication Theory of Secrecy Systems. Bell System Technical Journal.
- Menezes, A. J., van Oorschot, P. C., & Vanstone, S. A. (1996). Handbook of Applied Cryptography. CRC Press.
- Stallings, W. (2017). Cryptography and Network Security: Principles and Practice. Pearson.
- Paar, C., & Pelzl, J. (2010). Understanding Cryptography. Springer.

Estas referencias sirven como respaldo teorico general. Si la docente proporciono autores especificos en clase, deben agregarse tambien para alinear el documento con la bibliografia oficial.

## Mejoras futuras recomendadas

- Exportar reportes de auditoria en PDF o CSV.
- Agregar capturas de pantalla al documento final.
- Agregar una seccion de bibliografia oficial si la docente exige autores especificos.
