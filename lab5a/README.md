
### Landing Data

https://stalandingdevneu01.dfs.core.windows.net/landing?sp=rl&st=2026-03-09T20:19:00Z&se=2026-03-30T03:34:00Z&sv=2024-11-04&sr=c&sig=nvOkG7vFXm3Bx%2BCmz4YxXxRvg6lg5cZOv0rtKIyZCg4%3D

## Create Lakehouse -> Lakehouse
## Copy Bronze -> ADF
## Bronze To Silver -> Notebook
## Silver To Gold -> Notebook
## Orchestrator with notifications -> ADF
## Scheduler -> ADF
## Lakehouse - > SQL Endpoint -> Query and Visual Query
## Lakehouse - > SQL Endpoint -> Semantic Model
## PowerBI -> Auto create report

| Drag from fact_sale | To table | To column |
| :--- | :--- | :--- |
| StockItemKey | dimension_stock_item | StockItemKey |
| SalespersonKey | dimension_employee | EmployeeKey |
| CustomerKey | dimension_customer | CustomerKey |
| InvoiceDateKey | dimension_date | Date |
| CityKey | dimension_city | CityKey |
