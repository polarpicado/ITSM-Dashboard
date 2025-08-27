# ITSM Dashboard

Dashboard de IT Service Management (ITSM) usando SQL Server, Python y Power BI.

## Tecnologías usadas

- SQL Server (Docker)
- Python (Faker + pyodbc)
- Power BI
- Firebase (autenticación opcional)

## Qué muestra

- Incidentes por prioridad, departamento y estado
- Cumplimiento SLA con indicadores KPI
- Cambios por tipo
- Tendencia temporal de incidentes

## Capturas

![SLA KPI](screenshots/SLA_KPI.png)
![Incidentes por Prioridad](screenshots/Incidentes_Prioridad.png)
![Cambios por Tipo](screenshots/Cambios_Tendencia.png)

## Cómo ejecutar

1. Levantar SQL Server con Docker:
   ```bash
   docker-compose up -d
