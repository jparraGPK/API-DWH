import azure.functions as func
import logging
import os
import pyodbc
import json
import datetime

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="query")
def query_sql(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Iniciando ejecución de consulta sobre SQL Pool")

    query = req.params.get('query')
    if not query:
        return func.HttpResponse(
            "Falta el parámetro 'query'. Ejemplo: ?query=SELECT+TOP+10+*+FROM+yc.wellproddaily",
            status_code=400
        )

    try:
        conn_str = os.environ.get("DB_CONNECTION_STRING")
        if not conn_str:
            return func.HttpResponse("No se encontró la variable DB_CONNECTION_STRING.", status_code=500)

        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            results = [dict(zip(columns, row)) for row in rows]

        def convert(obj):
            if isinstance(obj, (datetime.datetime, datetime.date)):
                return obj.isoformat()
            return str(obj)

        return func.HttpResponse(
            json.dumps(results, default=convert),
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Error ejecutando la consulta: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
