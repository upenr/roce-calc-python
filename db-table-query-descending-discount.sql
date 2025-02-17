SELECT TICKER, NAME, CURRENTPRICE, DCFPRICE, DISCOUNTINPERCENT
FROM dcf_analysis_upen
WHERE DISCOUNTINPERCENT BETWEEN 0.5 AND 1
ORDER BY DISCOUNTINPERCENT DESC;


SELECT TICKER
FROM companies_meeting_metrics_final
WHERE NUMBEROFMETRICSMET BETWEEN 4 AND 6
ORDER BY NUMBEROFMETRICSMET DESC;