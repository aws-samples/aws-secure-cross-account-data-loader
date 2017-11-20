CREATE TABLE IF NOT EXISTS public.milk_food_enforcement 
(
    milk_flag int,
	address_1 VARCHAR(256) ENCODE lzo,
	address_2 VARCHAR(256),
	center_classification_date VARCHAR(256),
	city VARCHAR(256),
	classification VARCHAR(256),
	code_info VARCHAR(32600) ENCODE lzo,
	country VARCHAR(256) ENCODE lzo,
	distribution_pattern VARCHAR(1294) ENCODE lzo,
	event_id VARCHAR(256),
	initial_firm_notification VARCHAR(256) ENCODE lzo,
	more_code_info VARCHAR(9161),
	postal_code VARCHAR(256) ENCODE lzo,
	product_description VARCHAR(4001) ENCODE lzo,
	product_quantity VARCHAR(256) ENCODE lzo,
	product_type VARCHAR(256),
	reason_for_recall VARCHAR(1138) ENCODE lzo,
	recall_initiation_date VARCHAR(256),
	recall_number VARCHAR(256) ENCODE lzo,
	recalling_firm VARCHAR(256) ENCODE lzo,
	report_date VARCHAR(256),
	state VARCHAR(256),
	status VARCHAR(256),
	termination_date VARCHAR(256),
	voluntary_mandated VARCHAR(256) ENCODE lzo
)
DISTSTYLE EVEN;
COMMIT;
