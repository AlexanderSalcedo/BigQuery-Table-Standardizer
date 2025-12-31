from google.cloud import bigquery, storage
import json
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_provider(request):
    
    request_json = request.get_json(silent=True)
    provider_name = request_json.get("provider")

    logger.info(f"Iniciando proceso de aplanado para proveedor: {provider_name}")

    storage_client = storage.Client()
    bucket_name = request_json.get("bucket")
    temp_provider = f"demo_ocr/template_{provider_name.strip().lower().replace(' ','_')}.json"

    try:
        bucket = storage_client.bucket(bucket_name)
        temp_json = bucket.blob(temp_provider)
        dt = json.loads(temp_json.download_as_text())
    except Exception as e:
        logger.error(f"Error al leer el template {temp_provider}: {e}")
        raise e

    incremental_source = dt.get("incremental_source", "")
    incremental_target = dt.get("incremental_target", "")

    client = bigquery.Client()
    tables = list(dt['tables'].keys())

    t1 = time.time()

    for table in tables:
        target_table_name = dt['tables'][table].get("target_table_name")
        target = f"{dt['target_project']}.{dt['target_dataset']}.{target_table_name}"
        source = f"{dt['source_project']}.{dt['source_dataset']}.{table}"
        unnest_clause = dt['tables'][table].get("unnest_clause", "")

        cols_config = dt['tables'][table]['columns']
        columns_create = ",\n        ".join(f"SAFE_CAST({col['source']} AS STRING) AS {col['target']}" for col in cols_config)
        columns_target_list = ",\n        ".join(f"{col['target']}" for col in cols_config)
        columns_source_list = ",\n        ".join(f"SAFE_CAST({col['source']} AS STRING)" for col in cols_config)

        query = f"""
        BEGIN
            DECLARE last_update TIMESTAMP;
            --Verificamos si la tabla existe
            IF NOT EXISTS (
                SELECT table_name FROM `{dt['target_project']}.{dt['target_dataset']}.INFORMATION_SCHEMA.TABLES` 
                WHERE table_name = '{target_table_name}'
            ) THEN
                -- Si no existe -> Creamos la tabla
                CREATE TABLE `{target}` 
                PARTITION BY DATE(fec_procesamiento) 
                AS
                SELECT
                {columns_create},
                created_at AS fec_creacion_origen,
                CURRENT_TIMESTAMP() AS fec_procesamiento
                FROM `{source}` a
                {unnest_clause};
                
            ELSE
                --Si existe, insertamos los nuevos registros
                {"-- La tabla no es incremental, omitir" if not incremental_source else ""}
                
                {f'''
                SET last_update = (SELECT COALESCE(MAX({incremental_target}), TIMESTAMP('1900-01-01 00:00:00')) FROM `{target}` WHERE proveedor = '{provider_name}');

                INSERT INTO `{target}` (
                {columns_target_list},
                fec_creacion_origen,
                fec_procesamiento
                )
                SELECT {columns_source_list},
                created_at,
                CURRENT_TIMESTAMP()
                FROM `{source}` a
                {unnest_clause}
                WHERE {incremental_source} > last_update;
                ''' if incremental_source else "SELECT 'Omitir tabla ya que no es incremental';"}
            END IF;
        END;
        """

        job = client.query(query)
        job.result()

    t2 = time.time()

    return f"Procesamiento completado para proveedor {provider_name}.\nTiempo de procesamiento total {(t2-t1):.3f} segundos. \n", 200
