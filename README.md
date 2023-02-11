# Robot-Compiler-P0

## Ejecución

Se debe ejecutar el model.py, si se quiere probar con otro programa, se debe remplazar el contenido del archivo program.txt.

## Consideraciones

- Un programa para el robot debe empezar con la palabra ROBOT_R, luego una declaración de variables, de procedimientos y por último un bloque de instrucciones. Ese orden es estricto pero la aparicion de cualquiera de  los elementos es opcional a excepción de la palabra ROBOT_R. 

- Para la declaración de variables, no es necesario el punto y coma para terminar la declaración de variables, solo seguir leyendo nombres validos de variables en una misma linea que empieza con la palabra VARS, es decir, no es posible seguir declarando variables en una nueva linea que no empieza por VARS así aún no se haya puesto el ";" en la linea anterior.

- Despues de que el compilador encuentra la palabra PROCS, se asume que la declaración de procedimientos se hará de forma seguida y  sin ningún otro tipo de instrucciones de por medio como declaraciones de variables o bloques de instrucciones. Finalizará cuando posiblemente comience un bloque de instrucciones. 

- Si hay más de una instrucción en un bloque de instrucciones de un procedure, el programa falla :(