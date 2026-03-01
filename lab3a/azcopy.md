# 📦 Laboratorio: Carga de datos en Azure Data Lake con AzCopy

Este laboratorio muestra cómo autenticarse en Azure y copiar un archivo CSV a **Azure Data Lake Storage Gen2** utilizando **AzCopy**.

---

## 🧰 Requisitos previos

- AzCopy instalado en el equipo
- Acceso a una suscripción de Azure
- Permisos de escritura en la cuenta de Data Lake (Storage Blob Data Contributor)
- Archivo `sales.csv` disponible en local

---

## 🔹 Paso 1: Iniciar sesión en Azure con AzCopy

azcopy login --tenant-id "SUSTITUIR_POR_TU_TENANT_ID"


## 🔹 Paso 2: Ejecuta la copia masiva hacia el endpoint DFS de ADLS Gen2
azcopy copy "SUSTITUIR_RUTA_LOCAL\2025.csv" "https://SUSTITUIR_NOMBRE_CUENTA.dfs.core.windows.net/datalake/bronze/2025.csv"
