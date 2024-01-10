# Desafio Python kiu

### Dado el siguiente Sistema:
_Una compañía Aérea se dedica al negocio de transporte de cargas aéreas entre diferentes orígenes y destinos.
La compañía solo puede transportar paquetes de Clientes.
Por cada paquete transportado la compañía aérea cobra 10$
Debe existir un método que genere un reporte con el total de paquetes transportados y el total recaudado para un día determinado._
Se pide:
+ _Programar en Python las clases y responsabilidades del sistema, crear los testeos unitarios que consideren necesarios._
+ _No utilizar ningún framework en la solución (mantener una solución sencilla)._
___
### Se infieren las siguientes afirmaciones:

- En cuanto al enunciado "<ins> La compañía solo puede transportar paquetes de Clientes.</ins> " se toma por cliente a ambos entes encargados de enviar y recibir paquetes.
- Se presupone que para enviar un paquete ambos tienen que estar registrados en el sistema.
- Se podria crear tambien un tipo usuario para evitar ambiguedad.
- Se tomaron asumsiones tales como 

### Tareas realizadas.
- Se crearon los modelos Cliente, Package y Shipment utilizando dataclass.
- Se organizaron los estados por los cuales puede pasar el envio. (a posterior se podria armar una maquina de estados para controlar el flujo de los mismos.)
- Se conectaron los modelos a la bdd en postgres utilizando psycopg2.
- Se agrego un testeo estatico por flake8 y su configuracion
- Se crearon test de unidad y de integracion.
- Se alcanzo un 93% de coverage con los test
- Se agrego un workflow de github para aplicar los testeos en cada push al branch main.

### Para ejecutar el proyecto
```bash
docker compose up -d
python main.py
```