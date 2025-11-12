## 1. Descripción del proyecto
Automatización del aplanado de tablas con estructuras STRUCT en BigQuery usando Cloud Functions y GCS.

## 2. Tecnologías utilizadas
- Google Cloud Platform (BigQuery, Cloud Functions, GCS)
- Python
- Shell
- JSON
## 3. Arquitectura
Incluye un diagrama simple (puedes hacerlo en draw.io o Excalidraw) que muestre:
- Entrada: tabla en BigQuery con STRUCT
- Proceso: Cloud Function lee, aplana y escribe
- Configuración: JSON en GCS
- Resultado: tabla estandarizada en BigQuery
## 4. Cómo desplegar
Explica cómo usar tu deploy.sh para subir la función:
gcloud functions deploy flatten_struct \
  --runtime python310 \
  --trigger-http \
  --entry-point main \
  --source ./cloud_function \
  --set-env-vars BUCKET_NAME=tu_bucket,PROJECT_ID=tu_proyecto


5. Ejemplo de uso
Incluye un ejemplo de tabla con STRUCT y cómo queda después del aplanado.
