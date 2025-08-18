# DIPLOMADO INGENIERÍA DE CALIDAD DE SOFTWARE COMERCIAL (3ra Edición)
## CARRERA DE INGENIERÍA INFORMÁTICA

---

### QUINTO MÓDULO
### AUTOMATIZACIÓN DE PRUEBAS

---

# Grupo: SoftSign  
**Integrantes:**
- Alvarez Cayo Elvis [![GitHub](https://img.shields.io/badge/GitHub-Elv500-blue?logo=github)](https://github.com/Elv500)
- Gutierrez Orellana Kevin - Guti1712k
- Delgadillo Fernandez Pablo Enrique - EDelgadillo
- Navia Luna Edwin Efrain - Edwin Navia
- Quiroga Almendras Liliana - lili-QA28
- Soto Diaz Erika Jhaelis - EJhaelis

**Docente:** Espinoza Rina

**Ubicación:** Cochabamba - Bolivia

---

**Softsign** trabaja en este proyecto de automatización de pruebas de servicios REST desarrollado con Python.  
Está diseñado para ejecutar pruebas funcionales sobre APIs utilizando un framework propio basado en `pytest`y `requests`
Además, se integra con herramientas como **Allure** para la generación de reportes de ejecución y **Github Actioncs** para crear el pipelin CI/CD.

Este repositorio contiene:

- Casos de prueba automatizados (positivos y negativos)
- Manejo de autenticación por token
- Estructura modular y reutilizable
- Soporte para ejecución local y en pipelines CI/CD: GitHub Actions

---

## 🔧 Requisitos previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

- Python 3.13.x o superior
- pip (incluido con Python)
- Git (para clonar el repositorio)
- Allure CLI (opcional, para reportes visuales)
- IDE VSCode o PyCharm

---

## 🚀 Instalación y configuración

### Paso 1. Clonar el repositorio

```bash
git clone https://github.com/Elv500/Softsign.git
cd Softsign
```

### Paso 2. Crear un entorno virtual

Se recomienda trabajar en un entorno virtual para evitar conflictos con otras dependencias del sistema:

```bash
python -m venv venv
```

> En macOS o Linux puedes usar `python3 -m venv venv` si es necesario.

### Paso 3. Activar el entorno virtual

- En **Windows**:

  ```bash
  .\venv\Scripts\activate
  ```

- En **macOS/Linux**:

  ```bash
  source venv/bin/activate
  ```

Verás que el prompt cambia indicando que el entorno está activo.

### Paso 4. Instalar dependencias

Una vez activado el entorno, instala las librerías necesarias desde el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Paso 5. Configurar variables de entorno

El proyecto usa un archivo `.env` para variables sensibles como tokens o URLs base. Para configurarlo:

1. Duplica el archivo de ejemplo:

   ```bash
   cp .env.example .env
   ```

   > En Windows:
   > ```cmd
   > copy .env.example .env
   > ```

2. Abre `.env` con tu editor de texto y completa los valores requeridos:
   ```bash
   BASE_URL = https://demo.sylius.com
   ADMIN_USERNAME = api@example.com
   ADMIN_PASSWORD = sylius-api
   ```
---

## ✅ Ejecución de pruebas (Localmente)

Con todo configurado, ya puedes correr las pruebas automatizadas de las siguientes maneras:

   > Si nota que su IDE ejecuta lento los tests, puede agregar el siguiente parametro a cualquier comando de ejecución:

   ```bash
   --cache-clear
   ```
   > Si desea ver con más detalles la ejecución, puede agregar el siguiente parametro a cualquier comando de ejecución:

   ```bash
   -v
   ```

### Ejecutar Regression

Para ejecutar los tests de regresión, que incluyen todos:

   ```bash
   pytest
   ```

### Ejecutar por tipo de testing:

Para ejecutar por tipo de prueba, utilice la opción `-m` de pytest junto con la marca correspondiente:
```bash
Ejm: pytest -m smoke
```

| Tipo Testing | Comando |
|--------|----------|
| Smoke | `pytest -m smoke` |
| Functional | `pytest -m functional` |
| Negative | `pytest -m negative` |
| Security | `pytest -m security` |
| Boundary | `pytest -m boundary` |
| Domain | `pytest -m domain` |
| Stress | `pytest -m stress` |
| Performance | `pytest -m performance` |
| E2E | `pytest -m e2e` |
| Inventory | `pytest -m inventory` |
| Tax Category | `pytest -m tax_category` |
| Customer Group | `pytest -m customer_group` |
| Options | `pytest -m options` |
| Attributes | `pytest -m attributes` |
| High | `pytest -m high` |
| Medium | `pytest -m medium` |
| Low | `pytest -m low` |

### Ejecutar por sub-módulo:

Para ejecutar por sub-módulo se puede combinar con los demás parámetros, agregando el directorio del submodulo:
```bash
Ejm: pytest .\tests\ -m smoke -v
```

| Módulo| Sub-módulo | Comando |
|-------|------------|---------|
| Catálogo | Association Types | `pytest .\tests\catalog\association_types\` |
|  | Attributes | `pytest .\tests\catalog\attributes\` |
|  | Inventory | `pytest .\tests\catalog\inventory\` |
|  | Options | `pytest .\tests\catalog\options\` |
| Configuration | Tax Category | `pytest .\tests\tax_categories\` |
| Customer | Group | `pytest .\tests\customer\groups\` |
| Login | Autenticacion | `pytest .\tests\login\` |

### Ejecutar tests con reporte Allure

Para generar el reporte de ejecución se tiene dos alternativas:

### Opción 1:
Se puede optar por reporte rapido con `pytest-html` que ya viene instalado con `requirements.txt`:
```bash
pytest --html=reports/reports_general.html 
```
### Opción 2:
Hay otra opción con la que se puede generar un reporte más detallado con `Allure`.
Primero se debe generar el report con `Allure` que ya viene instalado con `requirements.txt`:
```bash
pytest --alluredir=reports/allure-results 
```
Luego se debe tener instalado `Allure CLI` previamente para poder generar un reporte HTML o levantarlo un servidor local y ver el reporte directamente:
> Puede revisar el siguiente enlace para Allure CLI: https://github.com/allure-framework/allure2/releases/tag/2.34.1
```bash
allure serve reports/allure-results
```
Tambien se puede generar el `Reporte Allure HTML`
```bash
allure generate reports/allure-results --clean -o reports/allure-report-html
allure open reports/allure-report-html 
```
> Se agrega el `--clean -o` para que no se acumule todos los reportes y se actualice a la última versión.

Esto abrirá un navegador con el reporte visual de los resultados.

---
## ✅ Ejecución de pruebas (Github Actions)

Tambien se puede ejecutar manualmente desde el Action del proyecto.
> Desde la pestaña de Actions y la rama main, se muestra un botón desplegable **"Run Workflow"**

Donde hay dos campos, uno es para seleccionar la rama (Main por defecto) y un campo de texto. Aquí se debe ingresar uno o más parametros de lo que se quiere ejecutar.

### Ejecutar Regression

Para ejecutar los tests de regresión, que incluyen simplemente **seleccionar la rama y darle a ejecutar.**

### Ejecutar por tipo de testing:

Para ejecutar por tipo de prueba, utilice la opción `-m` de pytest junto con la marca correspondiente:
```bash
Ejm: -m smoke
```

| Tipo Testing | Comando |
|--------|----------|
| Smoke | `-m smoke` |
| Functional | `-m functional` |
| Negative | `-m negative` |
| Security | `-m security` |
| Boundary | `-m boundary` |
| Domain | `-m domain` |
| Stress | `-m stress` |
| Performance | `-m performance` |
| E2E | `-m e2e` |
| Inventory | `-m inventory` |
| Tax Category | `-m tax_category` |
| Customer Group | `-m customer_group` |
| Options | `-m options` |
| Attributes | `-m attributes` |
| High | `-m high` |
| Medium | `-m medium` |
| Low | `-m low` |

### Ejecutar por sub-módulo:

Para ejecutar por sub-módulo se puede combinar con los demás parámetros, agregando el directorio del submodulo:
```bash
Ejm: pytest .\tests\ -m smoke -v
```

| Módulo| Sub-módulo | Comando |
|-------|------------|---------|
| Catálogo | Association Types | `tests/catalog/association_types` |
|  | Attributes | `tests/catalog/attributes` |
|  | Inventory | `tests/catalog/inventory` |
|  | Options | `tests/catalog/options` |
| Configuration | Tax Category | `tests/configuration/tax_categories` |
| Customer | Group | `tests/customer/groups` |
| Login | Autenticacion | `tests/login` |

> **NOTA: Se puede combinar ambos parametros como marca y suite/submódulo**<br>Por ejemplo: **tests/catalog/inventory -m smoke**

---

## 📁 Estructura del proyecto (resumen)

```bash
Softsign/
├── src/                    # Recursos del framework para reutilizar (Assertions, data, schemas, payloads)
├── tests/                  # Casos de prueba organizados por módulo
├── conftest.py             # Fixtures compartidas (ej. token de autenticación)
├── requirements.txt        # Dependencias del proyecto
├── .env.example            # Plantilla de variables de entorno
├── reports/                # Carpeta para resultados de Allure/Pytest-html
├── TEST_PLAN.md/           # Documentación del Test Plan para éste proyecto
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
- Integrar herramientas como GitHub Actions y Allure para ejecución continua y despliegue de reporte

---

## 🤝 Contribuciones

Este proyecto es desarrollado por el equipo de **QA SoftSign** con enfoque en pruebas automatizadas de APIs REST.  
Si deseas colaborar, puedes crear un fork o enviar un pull request con mejoras o nuevos casos de prueba.

---

## 📄 Licencia

Este proyecto es de uso académico y no tiene una licencia pública aún definida.