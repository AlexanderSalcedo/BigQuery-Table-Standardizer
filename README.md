# BQStructFlattener

Automatización del aplanado y estandarización de tablas `NO ESTRUCTURADAS` en BigQuery, utilizando Cloud Functions, Google Cloud Storage y Python. Este proyecto permite transformar tablas complejas en esquemas planos estandarizados de forma automática y escalable.

---

## 🚀 Tecnologías utilizadas

![Google Cloud](https://img.shields.io/badge/Google%20Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![BigQuery](https://img.shields.io/badge/BigQuery-1A73E8?style=for-the-badge&logo=google-big-query&logoColor=white)
![Cloud Functions](https://img.shields.io/badge/Cloud%20Functions-34A853?style=for-the-badge&logo=google-cloud&logoColor=white)
![Cloud Storage](https://img.shields.io/badge/Cloud%20Storage-F9AB00?style=for-the-badge&logo=google-cloud&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Shell](https://img.shields.io/badge/Shell-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)

---

## 🏗️ Arquitectura del proyecto

![Arquitectura del proyecto](docs/arquitectura.png)

Este proyecto automatiza el proceso de estandarización de datos provenientes de un único proveedor (AUNA), que son almacenados en BigQuery con esquemas complejos tipo `STRUCT`. La arquitectura se compone de los siguientes pasos:

1. **Ingesta de datos estructurados**
   - Se reciben datos batch en **10 tablas origen** en BigQuery.
   - Cada tabla contiene información con campos tipo `STRUCT`.

2. **Carga de insumos desde Cloud Shell**
   - Se cargan dos archivos clave:
     - `template_auna.json`: define la plantilla de estandarización.
     - `demo_ocr.zip`: contiene el `main.py` y `requirements.txt` para la Cloud Function.

3. **Ejecución de la Cloud Function**
   - La función se activa automáticamente al finalizar la ingesta batch.
   - Lee los datos desde las tablas origen en BigQuery.
   - Aplana la estructura `STRUCT` según el esquema definido en el JSON.
   - Escribe los datos estandarizados en **nuevas tablas BigQuery**.

4. **Almacenamiento y trazabilidad**
   - Los archivos de configuración y código se almacenan en **Google Cloud Storage**.
   - El proceso completo se ejecuta desde **Google Cloud Shell**, permitiendo despliegue y control centralizado.

---

## ⚙️ Despliegue

Comando para desplegar la Cloud Function desde Google Cloud Shell:

```bash
gcloud functions deploy FUNCTION_NAME \
  --gen2 \
  --runtime=python310 \
  --region=REGION \
  --source=SOURCE_PATH \
  --entry-point=process_provider \
  --trigger-http \
  --service-account=SERVICE_ACCOUNT

