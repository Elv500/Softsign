# DIPLOMADO INGENIERÍA DE CALIDAD DE SOFTWARE COMERCIAL (3ra Edición)
## CARRERA DE INGENIERÍA INFORMÁTICA

---

### QUINTO MÓDULO
### AUTOMATIZACIÓN DE PRUEBAS

---

# Grupo: SoftSign  
**Integrantes:**
- Alvarez Cayo Elvis
- Gutierrez Orellana Kevin
- Delgadillo Fernandez Pablo Enrique
- Navia Luna Edwin Efrain
- Quiroga Almendras Liliana
- Soto Diaz Erika Jhaelis

**Docente:** Espinoza Rina

**Ubicación:** Cochabamba - Bolivia

---

## ÍNDICE

1. [Introducción](#introducción)
2. [Descripción del producto](#descripción-del-producto)
3. [Objetivos](#objetivos)
   - [Objetivo general](#objetivo-general)
   - [Objetivos Específicos](#objetivos-específicos)
4. [Funcionalidades](#funcionalidades)
5. [Límites y Alcances](#límites-y-alcances)
6. [Herramientas](#herramientas)
7. [Tipos de prueba](#tipos-de-prueba)
8. [Metodología](#metodología)
9. [Recursos](#recursos)
10. [Cronograma](#cronograma)
11. [Lista de Test Cases Sprint #1](#lista-de-test-cases-sprint-1)

---

# Test Plan

## Introducción

El presente documento describe el Plan de Pruebas Backend para la validación de las API REST del sistema Sylius, en su entorno de demostración accesible desde https://demo.sylius.com/admin.

Las pruebas se centran en los módulos **Catalog**, **Customer**, **Tax Category**, que representan componentes clave para la gestión de productos y clientes dentro del sistema.

El objetivo de este plan es definir el enfoque, alcance, criterios y actividades necesarias para asegurar que las funcionalidades backend relacionadas a dichos módulos funcionen de manera correcta, estable y segura. Para ello, se utilizarán técnicas de pruebas funcionales, tanto manuales como automatizadas, a través de herramientas como Postman y scripts en Python, validando las respuestas del servidor, el cumplimiento de los requisitos funcionales y la consistencia de los datos gestionados por las API.

## Descripción del producto

**Sylius** es una plataforma de comercio electrónico de código abierto desarrollada en Symfony (PHP), orientada a negocios que requieren soluciones altamente personalizables. Ofrece un panel administrativo completo que permite gestionar catálogos de productos, clientes, pedidos, promociones, métodos de pago y más.

Su arquitectura basada en APIs RESTful permite la integración con aplicaciones externas, automatización de procesos y testing de servicios backend, facilitando tanto el desarrollo como la validación funcional del sistema.

## Objetivos

### Objetivo general

Validar la funcionalidad, integridad y estabilidad de las API REST de Sylius en los módulos **Catalog**, **Customer** y **Tax Category**, mediante pruebas estructuradas que aseguren el correcto comportamiento de las operaciones backend, garantizando que los datos gestionados por el sistema respondan adecuadamente a las acciones esperadas por los usuarios administrativos.

### Objetivos Específicos

1. **Verificar las operaciones CRUD** (crear, consultar, actualizar y eliminar) en los recursos de los módulos Catalog (Inventory, Attributes, Options, Association types) y Customer (Customers, Groups) a través de llamadas API.

2. **Probar las APIs del módulo Customer**, validando la creación, edición, consulta y eliminación de datos relacionados a clientes, direcciones y grupos de clientes.

3. **Evaluar las respuestas del servidor**, asegurando el uso correcto de los códigos de estado HTTP y la estructura esperada en los cuerpos de respuesta (JSON).

4. **Validar el manejo de errores y restricciones**, comprobando que el sistema rechace correctamente solicitudes inválidas o malformadas (por ejemplo, campos requeridos faltantes o datos duplicados).

5. **Verificar la seguridad y control de acceso** a las APIs mediante tokens de autenticación, asegurando que los endpoints estén protegidos frente a usuarios no autorizados.

6. **Automatizar pruebas clave del backend**, mediante herramientas como Postman o Python (usando requests/pytest), para asegurar la repetibilidad y cobertura de las pruebas.

7. **Detectar posibles defectos o comportamientos inesperados**, documentando y reportando cualquier inconsistencia encontrada durante la ejecución de los test cases.

## Funcionalidades

A continuación, se describen los módulos y submódulos que serán evaluados durante el proceso de pruebas:

### Módulo Login

Este módulo permite autenticar a los administradores mediante un endpoint que genera un token de acceso. Dicho token es necesario para utilizar cualquier otro recurso protegido dentro del sistema. Su correcto funcionamiento es esencial para garantizar la seguridad y el acceso autorizado.

### Módulo Catalog

Este módulo agrupa diversas funcionalidades que permiten gestionar los elementos principales del catálogo de productos:

#### Inventory
Inventory permite administrar las distintas fuentes de inventario disponibles, es decir, los lugares desde los cuales los productos pueden ser enviados o distribuidos. Incluye operaciones para listar, crear, editar y eliminar estas fuentes.

#### Attributes
Los atributos son características adicionales que se puede asignar a los productos dentro de la aplicación Sylius, en este menú se puede realizar las siguientes funciones: crear, listar, editar y eliminar atributos.

#### Options
El submódulo Options en Sylius permite administrar las opciones de productos, que son atributos personalizables que los clientes pueden seleccionar al comprar, como tallas, colores o materiales. En Options se puede crear, editar y eliminar opciones, así como definir sus valores posibles, lo que facilita la organización del catálogo y la personalización de productos.

#### Association Types
El submódulo Association Types permite administrar los tipos de asociación entre productos, como productos relacionados o accesorios. Desde este menú se pueden listar, crear, editar y eliminar tipos de asociación, lo que facilita la vinculación lógica entre productos dentro del catálogo.

### Módulo Customer

#### Groups
El submódulo Customer Groups permite la gestión de grupos de clientes, lo cual es útil para segmentar usuarios según distintos criterios, como nivel de fidelidad, tipo de cliente (minorista, mayorista), o políticas comerciales específicas.

### Módulo Configuration

#### Tax Categories
Las Tax Categories en el sistema son grupos que clasifican los distintos tipos de impuestos aplicables a productos o servicios. El módulo cuenta con endpoints RESTful (GET, POST, PUT, DELETE) que permiten listar, crear, actualizar y eliminar estas categorías, facilitando la gestión fiscal dentro de la plataforma. Las pruebas automatizadas verifican que estos endpoints funcionen correctamente y manejen adecuadamente los datos.

## Límites y Alcances

### Login/Autenticación (Elvis)
| Método | Endpoint |
|--------|----------|
| POST | `/api/v2/administrators/token` |

### Módulo Catalog

#### Inventory (Elvis)
| Método | Endpoint |
|--------|----------|
| GET | `/api/v2/admin/inventory-sources` |
| POST | `/api/v2/admin/inventory-sources` |
| GET | `/api/v2/admin/inventory-sources/{code}` |
| PUT | `/api/v2/admin/inventory-sources/{code}` |
| DELETE | `/api/v2/admin/inventory-sources/{code}` |

#### Attributes (Liliana)
| Método | Endpoint |
|--------|----------|
| GET | `/api/v2/admin/product-attributes` |
| POST | `/api/v2/admin/product-attributes/` |
| GET | `/api/v2/admin/product-attributes/{code}` |
| PUT | `/api/v2/admin/product-attributes/{code}` |
| DELETE | `/api/v2/admin/product-attributes/{code}` |

#### Options (Erika)
| Método | Endpoint |
|--------|----------|
| GET | `/api/v2/admin/product-options` |
| POST | `/api/v2/admin/product-options` |
| GET | `/api/v2/admin/product-options/{code}` |
| PUT | `/api/v2/admin/product-options/{code}` |
| DELETE | `/api/v2/admin/product-options/{code}` |

#### Association Types (Edwin)
| Método | Endpoint |
|--------|----------|
| GET | `/api/v2/admin/product-association-types` |
| POST | `/api/v2/admin/product-association-types` |
| GET | `/api/v2/admin/product-association-types/{code}` |
| PUT | `/api/v2/admin/product-association-types/{code}` |
| DELETE | `/api/v2/admin/product-association-types/{code}` |

### Módulo Customer

#### Groups (Pablo)
| Método | Endpoint |
|--------|----------|
| GET | `/api/v2/admin/customer-groups` |
| POST | `/api/v2/admin/customer-groups` |
| GET | `/api/v2/admin/customer-groups/{code}` |
| PUT | `/api/v2/admin/customer-groups/{code}` |
| DELETE | `/api/v2/admin/customer-groups/{code}` |

### Módulo Configuration

#### Tax Categories (Kevin)
| Método | Endpoint |
|--------|----------|
| GET | `/api/v2/admin/tax-categories` |
| POST | `/api/v2/admin/tax-categories` |
| GET | `/api/v2/admin/tax-categories/{code}` |
| PUT | `/api/v2/admin/tax-categories/{code}` |
| DELETE | `/api/v2/admin/tax-categories/{code}` |

> **Nota:** Cualquier otra funcionalidad o endpoint que no esté mencionado en la anterior lista, se encuentra fuera del scope definido.

## Herramientas

### Pytest + Requests (Python)
Estas herramientas permitirán automatizar las pruebas funcionales, especialmente aquellas con múltiples combinaciones de datos o flujos repetitivos.

### Postman
Nos permitirán realizar las pruebas exploratorias, especialmente aquellas con múltiples combinaciones de datos o flujos repetitivos.

### GitHub Actions
Se integrará para ejecutar las pruebas automatizadas de forma continua al realizar cambios en el repositorio, asegurando así la calidad desde las primeras etapas.

Aplicando CI/CD, donde CI será la ejecución automatica al hacer push a la rama development o manual desde la rama main y generar el reporte respectivo. Y CD en nuestros terminos, será el despliegue automático del reporte para su respectiva visualización en tiempo real al terminar la ejecución.

### VS Code / PyCharm
Entorno de desarrollo (IDE) utilizado para escribir y organizar los scripts de pruebas en Python.

### Taiga
Es una herramienta para gestionar proyectos, en este caso se aplicará para la creación de los sprints, y el product backlog.

### Qase
Es una herramienta para gestionar pruebas, desde la creación de casos de prueba hasta el reporte de defectos.

### Allure
Generador de reportes visuales que se integrará al pipeline para mostrar los resultados de las pruebas automatizadas de manera clara y detallada.

## Tipos de prueba

### Smoke Testing
Validación básica y rápida de los endpoints clave del sistema, como login y recursos principales, para asegurar que el sistema responde correctamente antes de ejecutar pruebas más complejas.

### Functional Testing
Verificación de que cada endpoint cumple con el comportamiento esperado ante entradas válidas. Se aseguran respuestas correctas, estructuras de datos adecuadas y cumplimiento de la lógica de negocio.

### Negative Testing
Evaluación del sistema frente a entradas incorrectas, formatos inválidos, parámetros faltantes o rutas erróneas. Permite identificar fallos de validación o manejo inadecuado de errores.

### Regression Testing
Verificación de todos los casos de pruebas para garantizar que las funcionalidades principales se mantengan estables frente a futuras ejecuciones, incluso si no se realizan cambios directos por parte del equipo.

### Security Testing
Validación del acceso restringido a los recursos mediante autenticación y autorización. Se verifica que no se pueda acceder a endpoints protegidos sin token o con permisos insuficientes, también validando que ninguno rompa la URL con params incompletos o erróneos.

### Domain Testing
Pruebas enfocadas en evaluar el comportamiento del sistema frente a clases de equivalencia válidas e inválidas, incluyendo sus valores límite. Se busca cubrir un conjunto representativo de casos para asegurar que todas las categorías de entrada definidas en el dominio sean manejadas correctamente.

### Boundary Testing
Pruebas para validar el comportamiento de la aplicación ante entradas en los valores límite y en sus adyacentes, cubriendo tanto extremos válidos como inválidos.

### Stress Testing
Pruebas para validar el comportamiento y estabilidad de la aplicación bajo cargas muy altas o condiciones extremas, observando su capacidad de recuperación.

### Performance Testing
Pruebas para validar el rendimiento de la aplicación en términos de velocidad de respuesta, consumo de recursos y capacidad de procesamiento bajo diferentes cargas.

### E2E
Pruebas end-to-end para validar flujos completos del sistema, desde el inicio hasta el fin del proceso, abarcando la interacción de múltiples componentes.

### Inventory
Pruebas end-to-end para validar el flujo completo del módulo Catalog – Inventario, incluyendo creación, actualización, consulta y eliminación de registros.

### Tax Category
Pruebas end-to-end para validar el flujo completo del módulo Configuration – Tax Category, cubriendo todas sus operaciones principales.

### Customer Group
Pruebas end-to-end para validar el flujo completo del módulo Customer – Group, asegurando la correcta gestión de grupos de clientes.

## Metodología

**Scrum** es un marco de trabajo (framework) ágil utilizado para gestionar y desarrollar proyectos, especialmente en el ámbito del desarrollo de software. Se basa en ciclos cortos e iterativos llamados sprints, que suelen durar de una a cuatro semanas, en los cuales se entrega una parte funcional del producto.

Scrum promueve la colaboración continua entre los miembros del equipo, la adaptación al cambio y la entrega frecuente de valor. Se apoya en roles definidos (Product Owner, Scrum Master, Development Team y QA Team), eventos regulares (como Daily Scrum, Sprint Planning, Sprint Review y Sprint Retrospective) y artefactos como el Product Backlog y el Sprint Backlog.

Su objetivo principal es mejorar la eficiencia del equipo, fomentar la transparencia y adaptarse rápidamente a las necesidades del cliente.

### Endpoints para el Sprint 1

| Método | Endopoint | Responsable |
|----|--------|-------------|
| POST | `/api/v2/administrators/token` | Elvis Alvarez |
| GET | `/api/v2/admin/inventory-sources` | Elvis Alvarez |
| POST | `/api/v2/admin/inventory-sources` | Elvis Alvarez |
| GET | `/api/v2/admin/inventory-sources/{code}` | Elvis Alvarez |
| GET | `/api/v2/admin/product-attributes` | Liliana Quiroga  |
| POST | `/api/v2/admin/product-attributes/` | Liliana Quiroga  |
| GET | `/api/v2/admin/product-attributes/{code}` | Liliana Quiroga  |
| GET | `/api/v2/admin/product-options` | Erika Soto |
| POST | `/api/v2/admin/product-options` | Erika Soto |
| GET | `/api/v2/admin/product-options/{code}` | Erika Soto |
| GET | `/api/v2/admin/product-association-types` | Edwin Navia |
| POST | `/api/v2/admin/product-association-types` | Edwin Navia |
| GET | `/api/v2/admin/product-association-types/{code}` | Edwin Navia |
| GET | `/api/v2/admin/customer-groups` | Pablo Delgadillo |
| POST | `/api/v2/admin/customer-groups` | Pablo Delgadillo |
| GET | `/api/v2/admin/customer-groups/{code}` | Pablo Delgadillo |
| GET | `/api/v2/admin/tax-categories` | Kevin Gutierrez |
| POST | `/api/v2/admin/tax-categories` | Kevin Gutierrez |
| GET | `/api/v2/admin/tax-categories/{code}` | Kevin Gutierrez |


### Historias de Usuario para el Sprint 1

| ID | Título | Responsable |
|----|--------|-------------|
| 1 | HU-00: Inicio de sesión como administrador | Elvis Alvarez |
| 2 | HU-01: Consultar lista de "Customer - Group" | Pablo Delgadillo |
| 3 | HU-02: Crear un nuevo "Customer - Group" | Pablo Delgadillo |
| 4 | HU-07: Obtener la lista de todas las asociaciones del tipo de Productos | Edwin Navia |
| 5 | HU-04: Consultar listado de grupo de inventario | Elvis Alvarez |
| 6 | HU-05: Crear nueva fuente de inventario | Elvis Alvarez |
| 7 | HU-17: Crear un nuevo tipo de Asociación de productos | Edwin Navia |
| 8 | HU-09: Obtener la lista de attributes del módulo | Liliana Quiroga |
| 9 | HU-10: Listado de opciones de producto | Erika Soto |
| 10 | HU-11: Creación de una nueva opción de producto | Erika Soto |
| 11 | HU-12: Actualizar la información de un attribute | Liliana Quiroga |
| 13 | HU-07: Configuración - Consultar listado de Tax Category | Kevin Gutierrez |
| 14 | HU-14: Crear nuevo Tax Category | Kevin Gutierrez |

### Endpoints para el Sprint 2

| Método | Endopoint | Responsable |
|----|--------|-------------|
| PUT | `/api/v2/admin/inventory-sources/{code}` | Elvis Alvarez |
| DELETE | `/api/v2/admin/inventory-sources/{code}` | Elvis Alvarez |
| PUT | `/api/v2/admin/product-attributes/{code}` | Liliana Quiroga  |
| DELETE | `/api/v2/admin/product-attributes/{code}` | Liliana Quiroga  |
| PUT | `/api/v2/admin/product-options/{code}` | Erika Soto |
| DELETE | `/api/v2/admin/product-options/{code}` | Erika Soto |
| PUT | `/api/v2/admin/product-association-types/{code}` | Edwin Navia |
| DELETE | `/api/v2/admin/product-association-types/{code}` | Edwin Navia |
| PUT | `/api/v2/admin/customer-groups/{code}` | Pablo Delgadillo |
| DELETE | `/api/v2/admin/customer-groups/{code}` | Pablo Delgadillo |
| PUT | `/api/v2/admin/tax-categories/{code}` | Kevin Gutierrez |
| DELETE | `/api/v2/admin/tax-categories/{code}` | Kevin Gutierrez |

### Historias de Usuario para el Sprint 2

| ID | Título | Responsable |
|----|--------|-------------|
| 1 | HU-06: Eliminar una fuente de inventario existente | Elvis Alvarez |
| 2 | HU-15: Actualizar fuente de inventario | Elvis Alvarez |
| 3 | HU-13: Crear un nuevo attribute | Liliana Quiroga |
| 4 | HU-23: Eliminar un attribute existente | Liliana Quiroga |
| 5 | HU-03: Actualizar "Customer - Group" existente | Pablo Delgadillo |
| 6 | HU-16: Eliminar "Customer-Group" existente | Pablo Delgadillo |
| 7 | HU25: Actualizar una opción de producto | Erika Soto |
| 8 | HU26: Eliminar una opción de producto | Erika Soto |
| 9 | HU27: Actualizar un tipo de Asociación de productos existente | Edwin Navia |
| 10 | HU28: Eliminar un tipo de Asociación de productos existente | Edwin Navia |
| 11 | HU-22: Eliminar tax Category | Kevin Gutierrez |
| 12 | HU-29: Editar Tax Category | Kevin Gutierrez |

## Recursos

### Asignación por Módulo

| Módulo | Submódulo | Responsable |
|--------|-----------|-------------|
| **Catalog** | Inventory | Elvis Alvarez Cayo |
|  | Attributes | Liliana Quiroga Almendras |
|  | Options | Erika Jhaelis Soto Díaz |
|  | Association types | Edwin Efraín Navia Luna |
| **Customer** | Groups | Pablo Enrique Delgadillo Fernandez |
| **Configuration** | Tax Categories | Kevin Gutierrez Orellana |

### Roles del Equipo

| Rol | Nombre |
|-----|--------|
| **QA Lead** | Kevin Gutierrez Orellana |
| **QA Team** | Elvis Alvarez Cayo |
|  | Pablo Enrique Delgadillo Fernandez |
|  | Kevin Gutierrez Orellana |
|  | Edwin Efraín Navia Luna |
|  | Liliana Quiroga Almendras |
|  | Erika Jhaelis Soto Díaz |

### Enlaces de Recursos

Los test cases para este proyecto se encuentran detallados en el siguiente link:

**Link Taiga:** https://tree.taiga.io/project/guti_kevin-softsign-m5/taskboard/sprint-1-24565

**Link Qase:** https://app.qase.io/project/TC

**Credenciales Qase:**
- Email: dsolutions123A@gmail.com
- Password: Cocodrilo12345!

## Lista de Test Cases Sprint #1

### Test Cases - SoftSign

#### HU-02: Crear un nuevo "Customer - Group" (POST)

| ID | Título | Prioridad |
|----|--------|-----------|
| 153 | Admin > Customer - Group > Crear grupo de clientes con datos válidos | High |
| 154 | Admin > Customer - Group > Verificar estructura del JSON devuelto al crear | High |
| 155 | Admin > Customer - Group > Verificar que no permita crear grupo con código duplicado | High |
| 156 | Admin > Customer - Group > Verificar que no permita crear grupo sin campo obligatorio 'code' | High |
| 157 | Admin > Customer - Group > Crear grupo sin campo obligatorio 'name' | High |
| 158 | Admin > Customer - Group > Verificar que no permita crear grupo con código vacío | Medium |
| 159 | Admin > Customer - Group > Verificar que no permita crear grupo con nombre vacío | Medium |
| 160 | Admin > Customer - Group > Crear grupo con código inválido más de 255 caracteres | Medium |
| 161 | Admin > Customer - Group > Crear grupo con nombre inválido más de 255 caracteres | Medium |
| 162 | Admin > Customer - Group > Crear grupo con caracteres especiales no permitidos en código | Medium |
| 163 | Admin > Customer - Group > Verificar que permita crear grupo con caracteres especiales en nombre | Medium |
| 164 | Admin > Customer - Group > Verificar que no permita crear grupo sin token de autenticación | High |
| 165 | Admin > Customer - Group > Verificar que no permita crear grupo con token inválido | High |
| 166 | Admin > Customer - Group > Verificar que no permita crear grupo con body JSON malformado | Medium |
| 167 | Admin > Customer - Group > Verificar que no permita crear grupo con Content-Type incorrecto | Medium |
| 168 | Admin > Customer - Group > Verificar que el tiempo de respuesta al crear sea menor a 3 segundos | Medium |
| 169 | Admin > Customer - Group > Verificar que permita crear múltiples grupos simultáneamente | Low |
| 170 | Admin > Customer - Group > Verificar que permita crear grupo con código en límite superior (255 chars) | Low |
| 171 | Admin > Customer - Group > Verificar que permita crear grupo con nombre en límite superior (255 chars) | Low |
| 172 | Admin > Customer - Group > Verificar headers de respuesta | Low |
| 173 | Admin > Customer - Group > Verificar que permita crear grupo con código de 1 carácter | Medium |

#### HU-01: Consultar lista de "Customer - Group" (GET)

| ID | Título | Prioridad |
|----|--------|-----------|
| 176 | Admin > Customer - Group > Verificar que se puede obtener la lista de grupos de clientes código 200 | High |
| 177 | Admin > Customer - Group > Verificar estructura del JSON devuelto | High |
| 178 | Admin > Customer - Group > Verificar que se puede obtener un grupo específico usando un código existente | High |
| 179 | Admin > Customer - Group > Verificar campos obligatorios en cada grupo (id, code, name) | High |
| 180 | Admin > Customer - Group > Verificar que los campos code y name no sean nulos o vacíos | Medium |
| 181 | Admin > Customer - Group > Validar paginación básica con page y itemsPerPage | Medium |
| 182 | Admin > Customer - Group > Verificar paginación con página fuera de rango (ej. page=9999) | Low |
| 183 | Admin > Customer - Group > Verificar paginación con itemsPerPage = 0 | Medium |
| 184 | Admin > Customer - Group > Verificar paginación con valores negativos | Medium |
| 185 | Admin > Customer - Group > Verificar paginación con límite 1000 | Low |
| 186 | Admin > Customer - Group > Verificar que no permita el acceso sin token de autenticación | High |
| 187 | Admin > Customer - Group > Verificar que no permita el acceso con token inválido | High |
| 188 | Admin > Customer - Group > Verificar que no permita el acceso con token expirado | High |
| 189 | Admin > Customer - Group > Verificar que no permita un header de Authorization mal formado | Medium |
| 190 | Admin > Customer - Group > Verificar que no permita obtener grupo con código inexistente | Medium |
| 191 | Admin > Customer - Group > Verificar que no acepte un método HTTP no permitido (POST) | Medium |
| 192 | Admin > Customer - Group > Verificar respuesta con parámetros itemsPerPage malformados | Medium |
| 193 | Admin > Customer - Group > Verificar respuesta con parámetros page malformados | Medium |
| 194 | Admin > Customer - Group > Verificar unicidad de IDs y códigos | High |
| 195 | Admin > Customer - Group > Verificar formato de datos de cada campo | Medium |
| 196 | Admin > Customer - Group > Verificar límites de longitud de campos | Low |
| 197 | Admin > Customer - Group > Verificar tiempo de respuesta aceptable (2 seg) | Medium |
| 198 | Admin > Customer - Group > Verificar headers de respuesta HTTP | Low |

#### HU08: Consultar Listado de "Tax Category" GET

| ID | Título | Prioridad |
|----|--------|-----------|
| 60 | Admin > Configuration > Tax Categories – Crear categoría de impuesto exitosamente | High |
| 61 | Admin > Configuration > Tax Categories – Validar error por campo faltante (code vacío) | High |
| 62 | Admin > Configuration > Tax Categories – Validar error por duplicación del campo code | High |
| 63 | Admin > Configuration > Tax Categories – Verificar encabezados de respuesta tras creación | Medium |
| 64 | Admin > Configuration > Tax Categories – Verificar formato y tipos de datos en respuesta JSON | Medium |
| 65 | Admin > Configuration > Tax Categories – Validar límite de longitud en campo code | Medium |
| 66 | Admin > Configuration > Tax Categories – Validar caracteres especiales no permitidos en code | Medium |
| 67 | Admin > Configuration > Tax Categories – Verificar comportamiento ante campo description vacío | Medium |
| 68 | Admin > Configuration > Tax Categories – Verificar respuesta del output sin autenticación | High |
| 150 | Admin > Configuration > Tax Categories – Verificar respuesta con token inválido | High |
| 205 | Admin > Configuration > Tax category - No debe permitir crear una categoría con nombre menor a 2 caracteres | Medium |
| 220 | Admin > Configuration > Tax Categories - No debe permitir crear una categoría de impuesto con un nombre mayor a 255 caracteres | Medium |
| 221 | Admin > Configuration > Tax Categories > verificar que no deje crear categoria sin campo nombre | Medium |

#### HU14: Crear Tax Category POST

| ID | Título | Prioridad |
|----|--------|-----------|
| 234 | Admin > Configuration > Tax Category - Obtener listado de categorias de impuestos del endpoint get | High |
| 235 | Admin > Configuration > Tax Category - Verificar codigo de respueta 200ok al hacer una peticion | High |
| 236 | Admin > Configuration > tax category - Validar que se puede obtener una categoría de impuesto filtrando por código | High |
| 237 | Admin > Configuration > Tax Category - Verifica que la respuesta cumple con el formato JSON-LD | Medium |
| 238 | Admin > Configuration > Tax Category - Valida la estructura básica del JSON de respuesta | High |
| 239 | Admin > Configuration > Tax Category - Verifica que obtener una categoría de impuesto con un code inexistente responde 404 | Medium |
| 240 | Admin > Configuration > Tax Category - Verificar respuesta de token invalido o sin autenticacion | High |
| 241 | Admin > configuration > Tax Category - Validar paginacion basica con page e itemsPerPage | Medium |
| 242 | Admin > Configuration > Tax Category - Verificar campos no vacios en tax category | High |
| 243 | Admin > Configuration > Tax Categories - Verificar que no permita el acceso a tax categories con token expirado | High |
| 244 | Admin > Configuration > Tax Categories - Verificar que los headers de respuesta sean correctos para tax categories | Medium |

#### HU-00: Inicio de sesión como administrador (POST)

| ID | Título | Prioridad |
|----|--------|-----------|
| 55 | Login > Admin - Autenticación exitosa usando email y contraseña válidos | High |
| 56 | Login > Admin - Autenticación fallida con email y contraseña inválidos | High |
| 57 | Login > Admin - Autenticación fallida con email inválido y contraseña válida | High |
| 58 | Login > Admin - Autenticación fallida con email válido y contraseña inválida | High |
| 59 | Login > Admin - Autenticación fallida con email y contraseña vacíos | High |
| 151 | Login > Admin - Autenticación fallida con email vacío y contraseña válida | High |
| 152 | Login > Admin - Autenticación fallida con contraseña vacía y email válido | High |

#### HU-04: Consultar listado de grupo de inventario (GET)

| ID | Título | Prioridad |
|----|--------|-----------|
| 23 | Admin > Catalog > Inventory - Obtener lista completa de fuentes de inventario | High |
| 24 | Admin > Catalog > Inventory - Verificar error al obtener fuente de inventario con CODE inexistente | High |
| 25 | Admin > Catalog > Inventory - Obtener fuente de inventario por CODE existente | High |
| 26 | Admin > Catalog > Inventory - Verificar error al acceder a lista sin autenticación | High |
| 206 | Admin > Catalog > Inventory - Verificar error al acceder a fuente específica sin autenticación | High |
| 207 | Admin > Catalog > Inventory - Verificar rechazo con token expirado al acceder a lista de inventario | High |
| 208 | Admin > Catalog > Inventory - Verificar rechazo con token expirado al acceder a fuente de inventario | High |
| 209 | Admin > Catalog > Inventory - Obtener inventarios con página mínima válida y cantidad mínima válida | High |
| 210 | Admin > Catalog > Inventory - Verificar error al usar página igual a 0 y cantidad válida | Medium |
| 211 | Admin > Catalog > Inventory - Verificar error al usar página negativa y cantidad válida | Medium |
| 212 | Admin > Catalog > Inventory - Verificar error al usar página decimal y cantidad válida | Medium |
| 213 | Admin > Catalog > Inventory - Verificar error al usar string como página y cantidad válida | Medium |
| 214 | Admin > Catalog > Inventory - Verificar error al usar valor vacío como página y cantidad válida | Medium |
| 215 | Admin > Catalog > Inventory - Verificar error al usar cantidad de elementos igual a 0 y página válida | Medium |
| 216 | Admin > Catalog > Inventory - Verificar error al usar cantidad de elementos negativa y página válida | Medium |
| 217 | Admin > Catalog > Inventory - Verificar error al usar cantidad de elementos decimal y página válida | Medium |
| 218 | Admin > Catalog > Inventory - Verificar error al usar string como cantidad de elementos y página válida | Medium |
| 219 | Admin > Catalog > Inventory - Verificar error al usar valor vacío como cantidad de elementos y página válida | Medium |

#### HU-09: Obtener lista de atributos (GET)

| ID | Título | Prioridad |
|----|--------|-----------|
| 38 | Admin > Catálogo > Attributes > Obtener el listado de atributos registrados en el sistema Sylius | High |
| 39 | Admin > Catálogo > Attributes > Realizar la busqueda de un atributo por el code | High |
| 40 | Admin > Catálogo > Attributes > Verificar que no se obtenga la lista de atributos si no se genero correctamente el token | High |
| 41 | Admin > Catálogo > Attributes > Verificar que no se permita obtener el resultado de un atributo que no existe | Medium |
| 42 | Admin > Catálogo > Attributes > Verificar la paginacion de la lista de atributos | Medium |
| 200 | Admin > Catálogo > Attributes > Validar el schema del response del metodo GET | Medium |
| 201 | Admin > Catálogo > Attributes > Verificar los headers de respuesta del metodo GET | Medium |
| 202 | Admin > Catálogo > Attributes > Verificar que no se obtenga el atributo cuando el codigo no existe | High |
| 203 | Admin > Catálogo > Attributes > Verificar que no se obtenga la lista de atributos si no se genera el token existosamente | High |
| 204 | Admin > Catálogo > Attributes > Verificar que no se obtenga la lista de atributos si se genera un token invalido | High |
| 47 | Admin > Catalogo > Attributes > Verificar que no permitar actualizar un atributo inexistente | Medium |
| 48 | Admin > Catalogo > Attributes > Verificar que no se permita actualizar un atributo sin token | Medium |
| 233 | Admin > Catalogo > Attributes > Verificar que no se actualice un atributo con datos invalidos | Medium |

#### HU-10: Listado de opciones de producto (GET)

| ID | Título | Prioridad |
|----|--------|-----------|
| 103 | Admin > Catalog > Options > Validar la estructura JSON de la respuesta | High |
| 104 | Admin > Catalog > Options > Verificar respuesta 401 sin token de autenticación | High |
| 105 | Admin > Catalog > Options > Verificar codigo 404 al buscar codigo inexistente | High |
| 106 | Admin > Catalog > Options > Verificar que busqueda por codigo sea exitosa | Medium |
| 107 | Admin > Catalog > Options > Verificar que búsqueda por nombre existente sea exitosa | Medium |
| 149 | Admin > Catalog > Options > Verificar respuesta 401 con token de autenticación inválido | High |
| 245 | Admin > Catalog > Options > Verificar paginacion de lista de opciones | Medium |
| 246 | Admin > Catalog > Options > Verificar paginacion con parametros invalidos | Medium |
| 247 | Admin > Catalog > Options > Verificar paginación con page inválido | Medium |
| 248 | Admin > Catalog > Options > Verificar paginación con items_per_page inválido | Medium |

#### HU-11: Creación de una nueva opción de producto (POST)

| ID | Título | Prioridad |
|----|--------|-----------|
| 108 | Admin > Catalog > Options > Verificar creación de opción exitosamente con datos válidos | High |
| 109 | Admin > Catalog > Options > Verificar error 422 al crear opción sin campos obligatorios | High |
| 110 | Admin > Catalog > Options > Verificar error 422 al crear opción sin el campo obligatorio code | High |
| 111 | Admin > Catalog > Options > Verificar error 422 al crear opción sin el campo obligatorio name | High |
| 112 | Admin > Catalog > Options > Verificar creación de opción con código existente | High |
| 113 | Admin > Catalog > Options > Verificar error al crear opción con code con espacios | Medium |
| 222 | Admin > Catalog > Options > Verificar que el campo code acepte máximo 255 caracteres | Medium |
| 223 | Admin > Catalog > Options > Verificar error al crear option name con menos de 2 caracteres | Medium |
| 224 | Admin > Catalog > Options > Verificar error al crear option name con más de 255 caracteres | Medium |
| 225 | Admin > Catalog > Options > Verificar error al crear un position que no sea entero | Medium |
| 226 | Admin > Catalog > Options > Verificar error al crear opción con position negativo | Medium |
| 227 | Admin > Catalog > Options > Verificar error al crear opción con position mayor a 999999999 | Medium |
| 228 | Admin > Catalog > Options > Verificar creación de opción sin autenticación | High |
| 229 | Admin > Catalog > Options > Verificar creación de opción con token inválido | High |
| 230 | Admin > Catalog > Options > Verificar creación de opción con idioma no soportado | Medium |
| 231 | Admin > Catalog > Options > Verificar creación de opción con values | High |

#### HU-05: Crear nueva fuente de inventario (POST)

| ID | Título | Prioridad |
|----|--------|-----------|
| 27 | Admin > Catalog > Inventory - Crear inventory con todos los campos válidos | High |
| 28 | Admin > Catalog > Inventory - Crear inventory solo con campos requeridos | High |
| 29 | Admin > Catalog > Inventory - Crear inventory con valor de prioridad 0 | Medium |
| 30 | Admin > Catalog > Inventory - Crear inventory con code duplicado | High |
| 31 | Admin > Catalog > Inventory - Crear inventory sin campo code | High |
| 252 | Admin > Catalog > Inventory - Crear inventory sin campo name | High |
| 253 | Admin > Catalog > Inventory - Crear inventory con code como vacío ("") | High |
| 254 | Admin > Catalog > Inventory - Crear inventory con name como vacío ("") | High |
| 255 | Admin > Catalog > Inventory - Crear inventory con prioridad negativa | Medium |
| 256 | Admin > Catalog > Inventory - Crear inventory con priority como texto | High |
| 257 | Admin > Catalog > Inventory - Crear inventory con priority como decimal | Medium |
| 258 | Admin > Catalog > Inventory - Crear inventory con address válido | Medium |
| 259 | Admin > Catalog > Inventory - Crear inventory sin address | Medium |
| 260 | Admin > Catalog > Inventory - Crear inventory sin campo countryCode en address | High |
| 261 | Admin > Catalog > Inventory - Crear inventory con countryCode inválido | High |
| 262 | Admin > Catalog > Inventory - Crear inventory con estructura inválida de address | High |
| 263 | Admin > Catalog > Inventory - Crear inventory sin channels | Medium |
| 264 | Admin > Catalog > Inventory - Crear inventory con channels inválido (formato incorrecto) | High |
| 265 | Admin > Catalog > Inventory - Crear inventory con código y nombre de longitud máxima válida | High |
| 266 | Admin > Catalog > Inventory - Crear inventory con name extremadamente largo | High |
| 267 | Admin > Catalog > Inventory - Crear inventory con code extremadamente largo | High |
| 268 | Admin > Catalog > Inventory - Crear inventory sin payload | High |

---

*Documento generado para el proyecto SoftSign - Diplomado en Ingeniería de Calidad de Software Comercial*