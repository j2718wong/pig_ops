DELIMITER $$

DROP PROCEDURE IF EXISTS business_account_add $$
CREATE PROCEDURE business_account_add(
    in_name             	VARCHAR(50),
	
	in_user_id     			INT
)  

BEGIN

/** 
 * Will add business account entry.
 * 
 * @author Jack Wong (j2718wong@gmail.com) 
 * @since August 8, 2025
 *
 */

DECLARE LOV_ID_ACNT_NUMDAYS_TRIAL				INT             DEFAULT 0;


DECLARE RES_NUM_SUCCESS                         INT             DEFAULT 0;
DECLARE RES_NUM_DUPLICATE_ENTRY                 INT             DEFAULT 1;




DECLARE cur_num_days_trial						INT             DEFAULT 0;

DECLARE cur_user_account_id						INT 			DEFAULT 0;
DECLARE cur_account_id                          INT             DEFAULT 0;



DECLARE res_num                                 INT             DEFAULT 0;
DECLARE res_code                                VARCHAR(180)    DEFAULT '';


SET res_num         = RES_NUM_SUCCESS;

SELECT 	val_int 
INTO 	cur_num_days_trial
FROM 	a01_list_of_value
WHERE 	id = LOV_ID_ACNT_NUMDAYS_TRIAL;


SELECT  id
INTO    cur_account_id
FROM    business_account
WHERE   UPPER(name)     	= UPPER(in_name)
LIMIT   1;


process_user : BEGIN

/* Check for duplicate farm name*/
IF cur_account_id > 0 THEN 
    SET res_num     = RES_NUM_DUPLICATE_ENTRY;
    SET res_code    = "RES_NUM_DUPLICATE_ENTRY";
    
    LEAVE process_user;

END IF;


SELECT 	account_id 
INTO 	cur_user_account_id
FROM 	user 
WHERE	id = in_user_id;

IF 

INSERT INTO business_account(
    name,
    date_trial_start,
    date_trial_end
) VALUES (
    in_name,
    CURRENT_DATE,
    DATE_ADD("2017-06-15", INTERVAL 10 DAY);
);

SELECT LAST_INSERT_ID() INTO cur_account_id;

END process_user;

SELECT 
    res_num                             AS result_number,
    res_code                            AS result_code,
    
    cur_user_id                         AS user_id,
    0                                   AS user_flag;
    

END $$

DELIMITER ;
