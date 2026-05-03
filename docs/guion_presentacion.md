# Guion sugerido de presentacion

Duracion recomendada: 10 a 15 minutos.

## 1. Introduccion

Presentar el objetivo general: una libreria educativa en Python con interfaz interactiva para estudiar seguridad, criptoanalisis y cifrado clasico.

Idea clave para decir:

```text
El proyecto separa la logica en una libreria reutilizable y la demostracion en una interfaz web.
```

En la pantalla `Inicio`, mostrar los seis modulos y explicar que cada boton del menu lateral consume funciones de la libreria `cripto_grupo_f`.

## 2. Mapeo de Debilidades

Explicar que no todos los activos tienen el mismo riesgo. Hardware, Software y Datos tienen vulnerabilidades distintas y amenazas asociadas.

Demostracion:

1. Seleccionar `Hardware`.
2. Mostrar vulnerabilidad, tipo de amenaza e impacto.
3. Cambiar a `Datos` y resaltar el cifrado como control.

## 3. Seguridad en Comunicaciones

Comparar sistema aislado contra sistema interconectado.

Mensaje clave:

```text
Cuando un sistema se conecta a una red, aparece el canal de comunicacion como nuevo punto critico.
```

Demostracion:

1. Activar y desactivar cifrado, autenticacion e integridad.
2. Mostrar como cambia el estado del canal.

## 4. Fuerza Bruta vs Criptoanalisis

Explicar que la fuerza bruta prueba claves, mientras que el criptoanalisis usa tecnica, patrones y conocimiento del idioma.

Demostracion:

1. Cambiar la clave Cesar.
2. Mostrar los candidatos de fuerza bruta.
3. Explicar que el puntaje linguistico ayuda a ordenar posibilidades.

## 5. Auditoria Academica

Presentar el caso de expedientes academicos.

Demostracion:

1. Marcar algunas preguntas P1-P4.
2. Mostrar si el estado es seguro, parcialmente seguro o inseguro.
3. Leer las recomendaciones generadas.

## 6. Analizador ESTIRANDO

Explicar monogramas y frecuencias del castellano.

Demostracion:

1. Pegar un criptograma.
2. Mostrar conteo e histograma.
3. Mostrar sustituciones sugeridas con E, A, O, S, R, N, I, D, C.
4. Ajustar una sustitucion manual y explicar que el resultado es una hipotesis de trabajo.
5. Abrir digramas y trigramas para reforzar el enfoque tecnico.

## 7. Disco de Alberti

Explicar que es un cifrador polialfabetico porque cambia el alfabeto de sustitucion durante el mensaje.

Demostracion:

1. Escribir un mensaje.
2. Elegir posicion inicial.
3. Definir cada cuantas letras rota el disco.
4. Elegir direccion y avance.
5. Cifrar y luego descifrar.
6. Mostrar la tabla paso a paso con posicion, letra indice y alfabeto interior.

## 8. Cierre

Cerrar conectando el proyecto con la rubrica:

- Implementa los seis requerimientos.
- Tiene libreria propia.
- Cifra y descifra.
- Explica procesos paso a paso.
- Incluye documentacion y pruebas.

Frase final sugerida:

```text
El sistema no solo muestra resultados, sino tambien el proceso usado para llegar a ellos.
```
