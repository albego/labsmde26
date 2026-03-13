SELECT Year, Month, count(*) Total_sales
FROM [LH_NEGOCIO].[silver].[fact_sale] GROUP by Year, Month order by Year, Month
