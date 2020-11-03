[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
# Agenda de alumnos de Intercambio
El objetivo del proyecto es coordinar los correos de los alumnos de intercambio de la Universidad de Granada

## Problema a resolver

Actualmente la coordinación de alumnos de intercambio se realiza mediante archivos de Excel, que deben ser procesadas varias veces y que resultan difíciles de manejar y editar a diario. Además se deben organizar los correos que se envían a los alumnos y elegir subconjuntos de los mismos de acorde a las necesidades del itercambio.

Es una tarea complicada y requiere de mucha precisión ya que se entablan relaciones con muchos destinos, tanto para alumnos que salen se la Universidad, como los que entran.

Es por ello que se trata de una herramienta crítica que debe funcionar a la perfección y garantizar resultados correctos en cada una de sus acciones.

## Arquitectura

La arquitectura elegida es orientada a eventos. Esto se debe a varios procesos que toman bastante tiempo: trabajar con los ficheros de Excel, alrededor de dos segundos; y enviar correos, que dependiendo de la lista pueden llevar varios minutos.

Además, la arquitectura orientada a eventos con las herramientas Celery y RabbitMQ permiten detectar errores en las tareas fácilmente, evitando pérdidas de información como correos no enviados, así como correos que no deberían ser enviados de nuevo.

Se utilizará Django por su facilidad a la hora de generar una App Web completa, aunque en principio se desarrollará sólo el backend. Otra de las ventajas es que se integra bastante bien con Celery.

## Historias de usuario

Ana y Beatriz trabajan en la Universidad de Granada. Ana se encarga de enviar correos a los alumnos para orientarles en sus trámites de intercambio. Beatriz se encarga de manejar las listas de los correos de los alumnos para que estén en orden.

> [Beatriz quiere crear/borrar una lista de correos, para introducir en ella los datos de los alumnos.](https://github.com/GabCas28/Agenda-Alumnos-Intercambio/issues/1)

> [Beatriz quiere añadir/modificar/borrar un alumno concreto de una lista manualmente, para mantener los datos actualizados.](https://github.com/GabCas28/Agenda-Alumnos-Intercambio/issues/2)

> [Beatriz quiere volcar una hoja de Excel con los datos de los alumnos en una lista de correos, para no tener que añadirlos uno a uno.](https://github.com/GabCas28/Agenda-Alumnos-Intercambio/issues/5)

> [Beatriz quiere agrupar las listas de correos por categorías, para mantenerlas ordenadas.](https://github.com/GabCas28/Agenda-Alumnos-Intercambio/issues/6)

> [Ana quiere añadir/modificar/borrar una plantilla de correo, que utilizará para enviar correos a los alumnos.](https://github.com/GabCas28/Agenda-Alumnos-Intercambio/issues/3)

> [Ana quiere enviar un correo utilizando una plantilla, a una lista de correos, evitando así enviarlos uno a uno.](https://github.com/GabCas28/Agenda-Alumnos-Intercambio/issues/4)

> [Ana quiere hacer cambios temporales en la plantilla y en la lista justo antes de enviar el correo, para ajustarse mejor a las necesidades del momento.](https://github.com/GabCas28/Agenda-Alumnos-Intercambio/issues/7)

## Hitos e Issues

1. [Crear y Exportar listas de correos.](https://github.com/GabCas28/Agenda-Alumnos-Intercambio/milestone/1)
    - [Beatriz quiere crear/borrar una lista de correos, para introducir en ella los datos de los alumnos.](https://github.com/GabCas28/Agenda-Alumnos-Intercambio/issues/1)
      * Crear una nueva lista
      * Borrar lista
    - [Beatriz quiere volcar una hoja de Excel con los datos de los alumnos en una lista de correos, para no tener que añadirlos uno a uno.](https://github.com/GabCas28/Agenda-Alumnos-Intercambio/issues/5)
      * Añadir correos a una lista a partir de Excel
      * Exportar listas en formato Excel
    - [Beatriz quiere agrupar las listas de correos por categorías, para mantenerlas ordenadas.](https://github.com/GabCas28/Agenda-Alumnos-Intercambio/issues/6)
      * Establecer categorías para las listas
  
2. [Manejar datos de los alumnos.](https://github.com/GabCas28/Agenda-Alumnos-Intercambio/milestone/2)
    - [Beatriz quiere añadir/modificar/borrar un alumno concreto de una lista manualmente, para mantener los datos actualizados.](https://github.com/GabCas28/Agenda-Alumnos-Intercambio/issues/2)
      * Añadir datos de alumno
      * Editar datos de alumno
      * Borrar datos de alumno
  
3. [Añadir plantillas y editarlas](https://github.com/GabCas28/Agenda-Alumnos-Intercambio/milestone/3)
    - [Ana quiere añadir/modificar/borrar una plantilla de correo, que utilizará para enviar correos a los alumnos.](https://github.com/GabCas28/Agenda-Alumnos-Intercambio/issues/3)
      * Crear Plantilla
      * Mostrar Plantilla
      * Editar Plantilla
      * Borrar Plantilla
  
4. [Enviar correos](https://github.com/GabCas28/Agenda-Alumnos-Intercambio/milestone/4)
    - [Ana quiere enviar un correo utilizando una plantilla, a una lista de correos, evitando así enviarlos uno a uno.](https://github.com/GabCas28/Agenda-Alumnos-Intercambio/issues/4)
      * Enviar correo a una lista, utilizando una plantilla
    - [Ana quiere hacer cambios temporales en la plantilla y en la lista justo antes de enviar el correo, para ajustarse mejor a las necesidades del momento.](https://github.com/GabCas28/Agenda-Alumnos-Intercambio/issues/7)
      * Permitir modificaciones en lista y plantilla antes de enviar
  
## Planificación

Para poder enviar correos lo más rápido posible, se intentará crear un prototipo lo más rápido posible, con las funcionalidades mas básicas del proyecto. Desde introducir los datos de un alumno hasta enviarle un correo utilizando una plantilla. Entonces se procederá a añadir todos los requisitos restantes.

El orden de creación para el prototipo básico es el siguiente:

1. Crear una lista
2. Añadir datos de alumno
3. Crear una plantilla
4. Enviar un correo a la lista (de un solo alumno) usando la única plantilla disponible.
  
Una vez el prototipo esté funcionando, se empezarán a completar uno a uno (empezando por el 1 hasta el 4), los diferentes hitos del proyecto.

## Entidad

Para comenzar el proyecto se crea la clase ListaAlumnos, que es el primer objeto a crear dentro de la planificación propuesta:

* [ListaAlumnos](./src/ListaAlumnos.py)

La clase Alumno se creará más adelante pues se requiere más información.

## Licencia

Este proyecto está bajo la licencia: [GPL-3.0 License](LICENSE.md).
