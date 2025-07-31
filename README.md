# Softsign

**Softsign** trabaja en este proyecto de automatización de pruebas de servicios REST desarrollado con Python.  
Está diseñado para ejecutar pruebas funcionales sobre APIs utilizando un framework propio basado en `pytest`, `requests` y `python-dotenv`.  
Además, se integra con herramientas como **Allure** para la generación de reportes de ejecución.

Este repositorio contiene:

- Casos de prueba automatizados (positivos y negativos)
- Manejo de autenticación por token
- Estructura modular y reutilizable
- Soporte para ejecución local y en pipelines CI: GitHub Actions

---

## 🔧 Requisitos previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

- Python 3.13.x o superior
- pip (incluido con Python)
- Git (para clonar el repositorio)
- Allure CLI (opcional, para reportes visuales)

---

## 🚀 Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/Elv500/Softsign.git
cd Softsign
```

### 2. Crear un entorno virtual

Se recomienda trabajar en un entorno virtual para evitar conflictos con otras dependencias del sistema:

```bash
python -m venv venv
```

> En macOS o Linux puedes usar `python3 -m venv venv` si es necesario.

### 3. Activar el entorno virtual

- En **Windows**:

  ```bash
  .\venv\Scripts\activate
  ```

- En **macOS/Linux**:

  ```bash
  source venv/bin/activate
  ```

Verás que el prompt cambia indicando que el entorno está activo.

### 4. Instalar dependencias

Una vez activado el entorno, instala las librerías necesarias desde el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno

El proyecto usa un archivo `.env` para variables sensibles como tokens o URLs base. Para configurarlo:

1. Duplica el archivo de ejemplo:

   ```bash
   cp .env.example .env
   ```

   > En Windows:
   > ```cmd
   > copy .env.example .env
   > ```

2. Abre `.env` con tu editor de texto y completa los valores requeridos.

---

## ✅ Ejecución de pruebas

Con todo configurado, ya puedes correr las pruebas automatizadas.

### Ejecutar todos los tests

```bash
pytest
```

### Ejecutar tests con reporte Allure

```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

Esto abrirá un navegador con el reporte visual de los resultados.

---

## 📁 Estructura del proyecto (resumen)

```bash
Softsign/
├── tests/                  # Casos de prueba organizados por módulo
├── conftest.py             # Fixtures compartidas (ej. token de autenticación)
├── requirements.txt        # Dependencias del proyecto
├── .env.example            # Plantilla de variables de entorno
├── reports/                # Carpeta para resultados de Allure
└── README.md               # Documentación del proyecto
```

---

## 🧪 Objetivo del proyecto

Este proyecto forma parte de un diplomado especializado en aseguramiento de calidad (QA), cuyo enfoque principal es:

- Construir un framework de pruebas de servicios REST reutilizable
- Aplicar técnicas de prueba funcional como:
  - Particiones de equivalencia
  - Análisis de valores límites
  - Tablas de decisión
  - Pruebas basadas en riesgos
- Automatizar flujos comunes como login, consultas y validaciones de datos
- Integrar herramientas como GitHub Actions y Allure para ejecución continua y reporte

---

## 🤝 Contribuciones

Este proyecto es desarrollado por el equipo de **QA SoftSign** con enfoque en pruebas automatizadas de APIs REST.  
Si deseas colaborar, puedes crear un fork o enviar un pull request con mejoras o nuevos casos de prueba.

---

## 📄 Licencia

Este proyecto es de uso académico y no tiene una licencia pública aún definida.