-- Grain: month x service channel. Closed cases belong to the closure month.
-- SLA compliance is volume weighted; never average channel percentages.
SELECT month,
       SUM(closed_cases) AS closed_cases,
       SUM(within_sla) AS within_sla,
       ROUND(100.0 * SUM(within_sla) / NULLIF(SUM(closed_cases), 0), 2) AS sla_pct
FROM service_operations
GROUP BY month
ORDER BY month;
