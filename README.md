# Desarrollo Prueba R5 _ Jorge Poveda 


## Tecnologias

Lista de tecnologias usadas en repositorio:

- [Flask]
- [Python]
- [mongoDB]
- [Docker]
- [asyncio]

## Endpoints

A continuacion se encontrara la informacion de los endpoints desarrollados en la prueba asignada.

| Path | Description | Example | Method |
| ------ | ------ |  ------ | ------ |
| /register | Obtencion de session que permite el consumo de los demas endpoints | [pruebar5jorgepoveda.ml/register][PlDb] |GET|
| /books | Trae todos los libros registrados en la db interna| [pruebar5jorgepoveda.ml/books][PlGh] |GET|
| /books/`{filter}`/`{value}` | Realiza busqueda filtrada segun los parametros enviados| [pruebar5jorgepoveda.ml/books/title/la+tregua][PlGd] |GET|
| /books/`{isbn}` | Elimina libros en la base de datos interna por identificador unico para libros| [pruebar5jorgepoveda.ml/books/9588912490][PlOd] |DELETE|

## Filters enabled

Lista de filtros disponibles no aplica case sensitive, solo en el envio del value.

| Filter | Description |
| ------ | ------ |
| isbn | Se realiza la busqueda por identificador unico para libros
| title | Se realiza la busqueda por titulo
| authors | Se realiza la busqueda por autor
| category | Se realiza la busqueda por categoria
| editor | Se realiza la busqueda por editorial

# Execute

El proyecto fue realizado con Flask, como base de datos se utiliza mongoDB, interconectado y dockerizado para una rapida inicializacion 

construccion de imagen:

```sh
docker-compose build
```

ejecucion de proyecto:

```sh
docker-compose run 
```
`or`
```sh
docker-compose run -d
```


**Desarrollado por: Jorge Poveda**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [mongoDB]: <https://docs.mongodb.com/manual/tutorial/getting-started/>
   [Docker]: <https://www.docker.com/>
   [Python]: <https://www.python.org/>
   [asyncio]: <https://docs.python.org/3.6/library/asyncio.html>
   [Flask]: <http://angularjs.org>

   [PlDb]: <https://pruebar5jorgepoveda.ml/register>
   [PlGh]: <https://pruebar5jorgepoveda.ml/books>
   [PlGd]: <https://pruebar5jorgepoveda.ml/books/title/la+tregua>
   [PlOd]: <https://pruebar5jorgepoveda.ml/books/9588912490>
