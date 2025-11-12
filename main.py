from google.cloud import bigquery, storage
import json

def process_provider(request):
    
    request_json = request.get_json(silent=True)
    provider_name = request_json.get("provider", "AUNA")

    storage_client = storage.Client()
    bucket_name = request_json.get("bucket")
    temp_provider = f"demo_ocr/template_{provider_name.lower()}.json"

    bucket = storage_client.bucket(bucket_name)
    temp_json = bucket.blob(temp_provider)
    dt = json.loads(temp_json.download_as_text())
    incremental_source = dt.get("incremental_source", "")
    incremental_target = dt.get("incremental_target", "")

    client = bigquery.Client()
    tables = list(dt['tables'].keys())

    def extract_columns(table_name):
        columns_target = [col['target'] for col in dt['tables'][table_name]['columns']]
        columns_source = [col['source'] for col in dt['tables'][table_name]['columns']]
        columns = ",\n        ".join(f"{src} AS {tgt}" for src, tgt in zip(columns_source, columns_target))
        col_t = ",\n        ".join(f"{col}" for col in columns_target)
        col_s = ",\n        ".join(f"{col}" for col in columns_source)
        return columns, col_t, col_s

    for table in tables:
        target = f"{dt['target_project']}.{dt['target_dataset']}.{table}"
        source = f"{dt['source_project']}.{dt['source_dataset']}.{table}"
        unnest_clause = dt['tables'][table].get("unnest_clause", "")

        try:
            client.get_table(target)
            table_exists = True
        except Exception:
            table_exists = False

        columns, col_t, col_s = extract_columns(table)

        if not col_t:
            print(f"No hay columnas definidas para {table}. Omitiendo.")
            continue

        if not table_exists:
            query = f'''
                CREATE TABLE IF NOT EXISTS `{target}` AS
                SELECT
                {columns}
                FROM `{source}` a
                {unnest_clause};
            '''
            print(f"Creando tabla {target}")
        else:
            if not incremental_source:
                print(f"La tabla {target} ya existe y no es incremental. Omitiendo.")
                continue

            query = f'''
                DECLARE last_update TIMESTAMP;

                SET last_update = (
                                   SELECT(COALESCE(MAX({incremental_target}), TIMESTAMP('1900-01-01 00:00:00')))
                                   FROM `{target}`
                                  );

                INSERT INTO `{target}`
                (
                {col_t}
                )
                SELECT
                {col_s}
                FROM `{source}` a
                {unnest_clause}
                WHERE {incremental_source} > last_update;
            '''
            print(f"Insert incremental en tabla {target}")

        print(f"Ejecutando ingesta para {target}")
        job = client.query(query)
        job.result()

    return f"Procesamiento completado para proveedor {provider_name}", 200
