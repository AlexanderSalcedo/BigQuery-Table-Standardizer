# BQStructFlattener

Automatización del aplanado y estandarización de tablas con estructuras `STRUCT` en BigQuery, utilizando Cloud Functions, Google Cloud Storage y Python. Este proyecto permite transformar tablas complejas en esquemas planos estandarizados de forma automática y escalable.

---

## 🚀 Tecnologías utilizadas

![Google Cloud](https://img.shields.io/badge/Google%20Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![BigQuery](https://img.shields.io/badge/BigQuery-1A73E8?style=for-the-badge&logo=google-big-query&logoColor=white)
![Cloud Functions](https://img.shields.io/badge/Cloud%20Functions-34A853?style=for-the-badge&logo=google-cloud&logoColor=white)
![Cloud Storage](https://img.shields.io/badge/Cloud%20Storage-F9AB00?style=for-the-badge&logo=google-cloud&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Shell](https://img.shields.io/badge/Shell-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)

---

## 📂 Estructura del proyecto

gcp-bigquery-flattening/ ├── cloud_function/ │   ├── main.py │   ├── requirements.txt │   └── README.md ├── schemas/ │   └── ejemplo_schema.json ├── deploy/ │   └── deploy.sh ├── docs/ │   ├── arquitectura.png │   └── flujo_proceso.md ├── LICENSE ├── .gitignore └── README.md

---

## ⚙️ Despliegue

Usa el siguiente comando para desplegar la Cloud Function desde Google Cloud Shell:

```bash
gcloud functions deploy flatten_struct \
  --runtime python310 \
  --trigger-http \
  --entry-point main \
  --source ./cloud_function \
  --set-env-vars BUCKET_NAME=tu_bucket,PROJECT_ID=tu_proyecto
