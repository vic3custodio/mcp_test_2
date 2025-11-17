-- @keywords: transaction, audit, compliance, investigation
-- @type: investigation_query
-- @description: Transaction audit trail for compliance investigations

SELECT 
    t.transaction_id,
    t.timestamp,
    t.user_id,
    u.user_name,
    u.department,
    t.action_type,
    t.account_id,
    a.account_name,
    t.instrument_id,
    i.instrument_name,
    t.quantity,
    t.price,
    t.ip_address,
    t.session_id
FROM transactions t
JOIN users u ON t.user_id = u.user_id
JOIN accounts a ON t.account_id = a.account_id
LEFT JOIN instruments i ON t.instrument_id = i.instrument_id
WHERE t.timestamp BETWEEN :start_date AND :end_date
    AND (
        t.account_id = :account_id 
        OR t.user_id = :user_id
        OR t.transaction_id = :transaction_id
    )
ORDER BY t.timestamp DESC;
