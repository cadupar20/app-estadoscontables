## Python - Estados Contables
### Este codigo fue creado para leer documentos (PDF en este caso) de Estados Contables, obtener los items y sus montos, mostrarlo en consola. Tambien se agrego la opcion de generarlo un archivo tipo .csv

Basado en Python utilizando libreria OpenAI para crear un asistente de estados contables, donde lee desde un archivo la informacion que el usuario solicite basada en el prompts previamente definido de "montos de estados contables"

Devolviendo una tabla con los montos encontrados similar a esta:

| Monto Buscado  | Monto Encontrado |
| ------ | ------ |
| Caja y Bancos | 306409 |
| Deudores por Ventas | NA |
| Inventarios | NA |
| Inversiones | 603151532 |
| Otros Créditos | 3588025 |
| Bienes de Uso | 424761 |
| Deudas Comerciales | NA | 
| Deudas Bancarias y Financieras   |  NA | 
| Remuneraciones y Cargas Sociales |  NA |  
| Deudas Fiscales                  | NA               | 
| Otras Deudas                     | NA               | 
| Ingresos por Ventas              | NA               | 
| C.M.V.                           | NA               | 
| Gastos Administrativos           | NA               | 
| Gastos Comercialización          | NA               | 
| Otros Egresos                    | NA               | 
| Impuesto a las Ganancias         | NA               | 
| RECPAM                           | NA               | 
| Capital o Acciones               | NA               | 
| Patrimonio Neto                  | NA               | 

1) Activar Virtual Environment (recomendado):

❯ pip install virtualenv 
❯ virtualenv env 
❯ .\env\Scripts\activate 

2) Instalar los paquetes requeridos para el proyecto:

❯ pip install openai
❯ pip install typer
❯ pip install rich

(Tambien puede utilizar el comando pip install -r requirements.txt para que automaticamente se instalen todos los paquetes juntos, omisando el paso a paso número 2)

Luego, dentro del archivo .env se debe colocar valores de API_KEY_ACCESS:


API_KEY_ACCESS = "sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 


Para ejecutar el programa basta con escribir el comando: python app-EstadosContables-v2.py

Finalmente se ha agregado que el programa exporte la informacion a un archivo .csv llamado "resultados.csv". Ejemplo: resultados.csv

> Dato Buscado,Monto Encontrado
> Fecha/Año,31.12.2023
> Caja y Bancos,137.973
> Créditos por Ventas,238.294
> Inventarios,166.023
> Inversiones,7
> Otros Créditos,NA
> Bienes de Uso,2.056.974
> Deudas Comerciales,229101
> Deudas Bancarias y Financieras,181357
> Remuneraciones y Cargas Sociales,15.537
> Deudas Fiscales,44.614
> Otras Deudas,191.800
> Ingresos por Ventas,513.727
> Costos por Ventas,320.124
> C.M.V.,NA
> Gastos Administrativos,62.721
> Gastos Comercialización,19.338
> Otros Egresos Operativos,29.374
> Otros Ingresos Operativos,57.141
> Impuesto a las Ganancias,NA
> RECPAM,51.494
> Capital o Acciones,1.363.5
> Patrimonio Neto,1.950.696


## Licencia
*Free Software!*