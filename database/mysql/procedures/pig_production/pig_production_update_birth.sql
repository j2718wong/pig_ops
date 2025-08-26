DELIMITER $$

DROP PROCEDURE IF EXISTS pig_production_update_birth $$
CREATE PROCEDURE pig_production_update_birth(
    in_user_id              		INT,
    
    in_pig_production_id    		INT,
    
	in_date_actual_birth    		VARCHAR(10),  /* in YYYY-MM-DD format*/
	in_num_piglets_dead_at_birth	INT,
	in_num_piglets_live_male		INT,
	in_num_piglets_live_female		INT,
	
	in_birth_attending_staff_id		INT
    
)

BEGIN

/** 
 * Will update pig_production at piglets birth entry.
 * @author Jack Wong
 * @since August 23, 2025
 *
 */
 
DECLARE RES_NUM_SUCCESS                         INT             DEFAULT 0;


DECLARE BUSINESS_OBJ_ID_PIG_PRODUCTION          INT             DEFAULT 17;

DECLARE FLAG_BIT_OPERATION_ADD                  INT             DEFAULT 1;
DECLARE FLAG_BIT_OPERATION_UPDATE               INT             DEFAULT 2;
DECLARE FLAG_BIT_OPERATION_DELETE               INT             DEFAULT 4;


DECLARE PRODUCTION_STATUS_ID_GESTATING          INT             DEFAULT 1;
DECLARE PRODUCTION_STATUS_ID_NOT_PREGNANT       INT             DEFAULT 3;
DECLARE PRODUCTION_STATUS_ID_LACTATING          INT             DEFAULT 4;



DECLARE cur_user_account_id                     INT             DEFAULT 0;
DECLARE cur_user_group_id                       INT             DEFAULT 0;


DECLARE cur_pig_production_id                    INT             DEFAULT 0;
DECLARE cur_pig_production_account_id            INT             DEFAULT 0;



DECLARE res_num                                 INT             DEFAULT 0;
DECLARE res_code                                VARCHAR(80)     DEFAULT '';
DECLARE res_desc                                VARCHAR(180)    DEFAULT '';



SET res_num     = RES_NUM_SUCCESS;
SET res_code    = "SUCCESS";


SELECT  account_id
INTO    cur_pig_production_account_id
FROM    pig_production
WHERE   id = in_pig_production_id
LIMIT   1;


CALL basic_user_check(
    in_user_id, 
    1, /* user must have an account*/
    cur_pig_production_account_id, /* compare user.account_id to this account_id*/
    
    BUSINESS_OBJ_ID_PIG_PRODUCTION,
    FLAG_BIT_OPERATION_UPDATE,
    
    cur_user_account_id, 
    cur_user_group_id,
    res_num, 
    res_code, 
    res_desc);


process_user : BEGIN

IF res_num != RES_NUM_SUCCESS THEN 
    LEAVE process_user;
END IF;




UPDATE pig_production SET 
    date_actual_birth       = in_date_actual_birth,
    num_days_actual         = DATEDIFF(in_date_actual_birth, date_insemination),
    status_id               = PRODUCTION_STATUS_ID_LACTATING,
    num_piglets_dead_at_birth 	= in_num_piglets_dead,
    num_piglets_live_male   	= in_num_piglets_live_male,
    num_piglets_live_female 	= in_num_piglets_live_female,
	
	num_piglets_current_male 	= in_num_piglets_live_male,
	num_piglets_current_female 	= num_piglets_current_female,
	
	last_update_user_id = in_user_id,
    dt_last_update      = CURRENT_TIMESTAMP
    
WHERE id =  in_pig_production_id;

END process_user;


SELECT
    flag,
    name
INTO 
    cur_pig_production_flag,
    cur_pig_production_name
FROM pig_production
WHERE id = in_pig_production_id;

SELECT 
    res_num                             AS result_number,
    res_code                            AS result_code,
    res_desc                            AS result_desc,
    
    in_pig_production_id                AS pig_production_id;


END $$

DELIMITER ;
