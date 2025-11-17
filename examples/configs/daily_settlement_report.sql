-- @keywords: trade, settlement, daily, reconciliation
-- @type: compliance_report
-- @description: Daily trade settlement reconciliation report for compliance

SELECT 
    t.trade_id,
    t.trade_date,
    t.settlement_date,
    t.trader_id,
    t.account_id,
    t.instrument,
    t.quantity,
    t.price,
    t.total_value,
    s.settlement_status,
    s.settlement_amount,
    CASE 
        WHEN s.settlement_status = 'FAILED' THEN 'ALERT'
        WHEN s.settlement_date > t.settlement_date + INTERVAL '1 day' THEN 'DELAYED'
        ELSE 'OK'
    END as compliance_flag
FROM trades t
LEFT JOIN settlements s ON t.trade_id = s.trade_id
WHERE t.trade_date = CURRENT_DATE - INTERVAL '1 day'
    AND (s.settlement_status != 'COMPLETE' 
         OR s.settlement_date > t.settlement_date + INTERVAL '1 day')
ORDER BY compliance_flag DESC, t.trade_id;
