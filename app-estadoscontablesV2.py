############## FUNCIONANDO PERFECTO!!!!!!!!!!####################
#   Docs:   
#   https://platform.openai.com/docs/assistants/tools/file-search?context=without-streaming
#   https://github.com/openai/openai-python?tab=readme-ov-file#polling-helpers
#

"""Importar de bibliotecas para el modulo OpenAI, modulo rich y el modulo typer"""
import openai # pip install openai
import typer # pip install typer
from rich import print  # pip install rich
from rich.table import Table
import re
import os
import platform

# Get environment variables (file .env)
API_KEY = os.getenv('API_KEY_ACCESS')

#FILE_PATHS = ["394746.pdf"]
FILE_PATHS = ["PAMPA-2023-12.pdf"]


# estados contables IMUSA
#VECTOR_STORE_ID = 'vs_ksCsTaEgQ82o5sP1JgS7BBIq'
#ASSISTANT_ID = 'asst_Z4jtjrE3VEzP7T9dwLQh6CPF'

"""Definición de la lista de prompts que se utilizarán en el asistente"""
PROMPT_LIST = [{'Fecha/Año': 'Fecha/Año del informe y puede figurar 31.12. o 31-12-'},
                {'Caja y Bancos': 'Disponibilidades, puede figurar como Caja y Bancos'},
                {'Créditos por Ventas': 'Deudores por Ventas, también puede figurar como Creditos por ventas o Creditos por ventas y otros creditos'},
                {'Inventarios': 'Inventarios'},
                {'Inversiones': 'Inversiones'},
                {'Otros Créditos': 'Otros Créditos'},
                {'Bienes de Uso': 'Bienes de Uso'},
                {'Deudas Comerciales': 'Deudas Comerciales y otras deudas'},
                {'Deudas Bancarias y Financieras': 'Deudas Bancarias y Financieras'},
                {'Remuneraciones y Cargas Sociales': 'Remuneraciones y Cargas Sociales'},
                {'Deudas Fiscales': 'Deudas Fiscales'},
                {'Otras Deudas': 'Otras Deudas o Otras Deudas Nota'},
                {'Ingresos por Ventas': 'Ingresos por Ventas'},
                {'Costos por Ventas': 'Costos por Ventas'},
                {'C.M.V.': 'C.M.V. o Costo de servicios prestados'},
                {'Gastos Administrativos': 'Gastos Administrativos o Gastos de administración'},
                {'Gastos Comercialización': 'Gastos Comercialización'},
                {'Otros Egresos Operativos': 'Otros Egresos, puede figurar como Otros Egresos Operativos'},
                {'Otros Ingresos Operativos': 'Otros Ingresos, puede figurar como Otros Ingresos Operativos'},
                {'Impuesto a las Ganancias': 'Impuesto a las ganancias, puede figurar como Impuesto a las ganancias'},
                {'RECPAM': 'RECPAM, puede figurar como Resultados financieros o Resultados financieros, neto'},
                {'Capital o Acciones': 'Capital o Acciones o Capital Social'},
                {'Patrimonio Neto': 'Patrimonio Neto o Total del patrimonio'},
             ]

"""Función principal del programa"""
def main():
    file_streams = [open(path, "rb") for path in FILE_PATHS]
    """Creación de un cliente OpenAI con la llave de API"""
    client = openai.OpenAI(api_key=API_KEY)

    if 'ASSISTANT_ID' in globals():
        print(f'Using existing Assitant {ASSISTANT_ID}')
        assistant = client.beta.assistants.retrieve(ASSISTANT_ID)
        print(assistant)
    else:
        #-------- CREACION DE UN NUEVO ASISTENTE -----------
        assistant = client.beta.assistants.create(
                    name="Analisis de Estados Contables",
                    instructions="Se subirá un archivo pdf con el Estado Contable de una empresa y debes localizar los montos que el usuario solicite luego. Las respuestas deben ser en formato numérico sin texto adicional. Responder a cada monto anteponiendo el mismo numero de la pregunta, seguido de dos puntos, por ejemplo, 1: 1000 \n \
    Si un monto no es encontrado responder con un la palabra NA, por ejemplo, 3: NA \n \
    Los numero negativos se pueden encontrar encerrados entre paréntesis, en ese caso indicar los mismos anteponiendo el signo menos al monto, por ejemplo, 5: -560",
                    model="gpt-4-turbo",
                    tools=[{"type": "file_search"}],
                    )   
        #----- INFORMACION DEL NUEVO ASISTENTE -----------
        print(f'New Assistant ID: {assistant.id}')
    
    if 'VECTOR_STORE_ID' in globals():
        print(f'Using existing vector store {VECTOR_STORE_ID} for analisis')
        vector_store = client.beta.vector_stores.retrieve(
                            vector_store_id=VECTOR_STORE_ID)
        print(vector_store)
    else:    
        #----- UPLOAD DE ARCHIVO(S) A VECTOR STORE --------
        print(f'Uploading file {FILE_PATHS[0]} for analisis')
        vector_store = client.beta.vector_stores.create(name="EstadosContables")
        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
        )
        
        print(f'File upload status: {file_batch.status}')
        print(f'File upload count: {file_batch.file_counts}')
        print(f'New Vector Store ID: {vector_store.id}')
        
        #----- ACTUALIZACION DE ASISTENTE -----------
        assistant = client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
        )
    
    #-------- CREACION DE UN NUEVO THREAD -----------
    thread = client.beta.threads.create()

    #----- INFORMACION DEL NUEVO THREAD -----------
    msg_content='Localizar y mostrar los siguientes montos: \n'
    i=1
    for prompt in PROMPT_LIST:
        msg_content += f'{i}: {prompt[list(prompt.keys())[0]]} \n'
        i+=1
    #-------- CREACION DE UN NUEVO MENSAJE -----------
    message = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=msg_content,
            )
    #-------- EJECUCION DEL MENSAJE EN EL THREAD -----------
    run = client.beta.threads.runs.create_and_poll(
                thread_id=thread.id,
                assistant_id=assistant.id,
            )
    #-------- OBTENCION DE MENSAJES DE RESPUESTA  -----------
    messages = client.beta.threads.messages.list(thread_id=thread.id, limit=1)
    #-------- IMPRESION DE MENSAJES DE RESPUESTA  -----------
    print(messages)

    reply = messages.to_dict()['data'][0]['content'][0]['text']['value']
    #-------- IMPRESION DE RESPUESTA  -----------
    print(reply)

    #-------- IMPRESION DE TABLA DE RESUMEN  -----------
    print("[bold green]Summary Table[/bold green]")
    table = Table("Dato Buscado", "Monto Encontrado")
    for line in reply.split('\n'):
        #-------- CREACION de ReMatchObject and Store Results  -----------
        parse_txt = re.search(r'^(\d+):\s*([a-zA-Z0-9,\.\-\$]+).*', line)
        #print(parse_txt)
        if parse_txt and len(parse_txt.groups()) == 2:
            table.add_row(list(PROMPT_LIST[int(parse_txt.group(1))-1].keys())[0], parse_txt.group(2))
    print(table)

    #-------- EXPORTAR DATOS ENCONTRADOS a CSV  -----------
    import csv
    with open('resultados.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Dato Buscado', 'Monto Encontrado'])
        for line in reply.split('\n'):
            #-------- CREACION de ReMatchObject and Store Results  -----------
            parse_txt = re.search(r'^(\d+):\s*([a-zA-Z0-9,\.\-\$]+).*', line)
            if parse_txt and len(parse_txt.groups()) == 2:
                writer.writerow([list(PROMPT_LIST[int(parse_txt.group(1))-1].keys())[0], parse_txt.group(2)])


def delAssistant(client):
    #Borra todos los asistentes (menos el último)
    my_assistants = client.beta.assistants.list(
                    order="desc",
                    limit="20",
                )
    for i in range(1, len(my_assistants.data)):
        # my_assistants.data[-1] --> es el asistente mas viejo
        response = client.beta.assistants.delete(my_assistants.data[i].id)
        print(response)


def delVectorStores(client):
    vector_stores = client.beta.vector_stores.list()
    for i in range(1, len(vector_stores.data)):
        # my_assistants.data[-1] --> es el asistente mas viejo
        response = client.beta.vector_stores.delete(vector_store_id=vector_stores.data[i].id)
        print(response)


if __name__ == "__main__":
    typer.run(main)
