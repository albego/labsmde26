SELECT Year, Month, count(*) Total_sales
FROM [LK_MDE].[silver].[fact_sale] GROUP by Year, Month order by Year, Month
