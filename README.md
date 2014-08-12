webcrawler
==========

Recorre un sitio web (haciendo breadth-first search) y escribe en la salida estándar
"CURRENT_URL","NEXT_URL"

donde CURRENT_URL es la página que se está visitando (dentro del dominio indicado en el parámetro 'domain')
y NEXT_URL es la siguiente página a ser visitada (mientras cumpla con ciertas condiciones)


Uso:
python crawl.py url depth domain > outputfile


Ejemplo:

python crawl.py http://exactas.uba.ar 1 exactas.uba.ar

Partiendo desde http://exactas.uba.ar, sigue todos los enlaces 'seguibles' de la forma http://*exactas.uba.ar/*  
que aparecen en esa página. Escribe en la salida estándar a qué páginas direcciona
Repite lo mismo con dichos enlaces, pero no los sigue, porque pertenecen a la profundidad 2.


