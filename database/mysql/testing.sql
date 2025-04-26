
/* New AI entry*/
CALL sow_new_ai_entry(342298, 1, 3, '2024-09-10', 'AI PIC 337');
CALL sow_new_ai_entry(342298, 1, 3, '2025-03-18', 'AI PIC 337');




CALL sow_new_ai_entry(342265, 1, 2, '2024-11-03', 'AI PIC 337');

CALL sow_new_ai_entry(342271, 1, 2, '2024-11-03', 'AI PIC 337');
CALL sow_new_ai_entry(342271, 1, 2, '2025-01-06', 'AI PIC 337');
CALL sow_new_ai_entry(342271, 1, 2, '2025-03-10', 'AI PIC 337');
CALL sow_new_ai_entry(342271, 2, 2, '2025-03-16', 'Kasta Landrace');

CALL sow_new_ai_entry(324478, 1, 2, '2025-01-09', 'AI PIC 337');

CALL sow_new_ai_entry(324658, 1, 2, '2025-02-06', 'AI PIC 337');
CALL sow_new_ai_entry(324658, 1, 2, '2025-02-24', 'AI PIC 337');




CALL sow_update_actual_birth_date(1, '2025-01-05', 4, 3, 6);



SELECT 
	a.id,
	a.ai_id,
	a.sow_number,
	b.description AS activity,
	a.date,
	a.date_2,
	a.days_since_ai,
	a.description

FROM sow_coming_activity a
LEFT OUTER JOIN coming_activity b 			ON a.coming_activity_id = b.id
LEFT OUTER JOIN artificial_insemination c  	ON a.ai_id = c.id
WHERE c.status_id = 1 AND (
	(a.date >= CURRENT_DATE AND a.date_2 IS NULL) OR 
	(a.date >= CURRENT_DATE AND a.date_2 <= CURRENT_DATE)
)
ORDER BY a.sow_number, a.id;
	

