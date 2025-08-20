DELIMITER $$

DROP PROCEDURE IF EXISTS pig_production_add $$
CREATE PROCEDURE pig_production_add(
	in_user_id				INT,
	in_sow_id           	INT,
    
    in_semen_source_id      INT,
    in_staff_id             INT,
    in_date_insemination    VARCHAR(10),  /* in YYYY-MM-DD format*/
    in_description          VARCHAR(200)
)  

BEGIN

/** 
 * Will create sow_coming_activity entries from a given sow insemination entry.
 * 
 * @author Jack Wong (neoaspilet11@gmail.com, zhaoshan99@gmail.com) 
 * @since August 17, 2025
 *
 */

DECLARE RES_NUM_SUCCESS                         INT             DEFAULT 0;
DECLARE RES_NUM_DUPLICATE_ENTRY                 INT             DEFAULT 1;


DECLARE INSEMINATION_STATUS_ID_GESTATING        INT             DEFAULT 1;
DECLARE INSEMINATION_STATUS_ID_WEANING          INT             DEFAULT 5;


DECLARE cur_sow_account_id						INT             DEFAULT 0;
DECLARE cur_sow_id                              INT             DEFAULT 0;

DECLARE cur_is_ai                               INT             DEFAULT 0;
DECLARE cur_semen_source_name                   VARCHAR(50)     DEFAULT '';
DECLARE cur_pig_race_name                       VARCHAR(50)     DEFAULT '';

DECLARE cur_semen_desc                          VARCHAR(100)    DEFAULT '';


DECLARE cur_coming_activity_id                  INT             DEFAULT 0;

DECLARE cur_production_id                       INT             DEFAULT 0;


DECLARE res_num                                 INT             DEFAULT 0;
DECLARE res_code                                VARCHAR(80)     DEFAULT '';
DECLARE res_desc                                VARCHAR(180)    DEFAULT '';


SET res_num    	= RES_NUM_SUCCESS;
SET res_code    = "SUCCESS";


SELECT  account_id
INTO    cur_sow_account_id
FROM    pig_farm
WHERE   id = in_pig_farm_id
LIMIT   1;


CALL basic_user_check(
    in_user_id, 
    1, /* user must have an account*/
    cur_pig_farm_account_id,
    
    FLAG_BIT_BIZ_OBJ_SEMEN_SOURCE,
    FLAG_BIT_OPERATION_ADD,
    
    cur_user_account_id, 
    cur_user_group_id,
    res_num, 
    res_code, 
    res_desc);


SELECT  id
INTO    cur_production_id
FROM    pig_production
WHERE   sow_number          = in_sow_number     AND 
        date_insemination   = in_date_insemination 
LIMIT   1;


process_user : BEGIN

IF cur_production_id > 0 THEN
    SET res_num     = RES_NUM_DUPLICATE_ENTRY;
    SET res_code    = "RES_NUM_DUPLICATE_ENTRY";
    
    LEAVE process_user;
END IF;


SELECT  id 
INTO    cur_sow_id
FROM    sow 
WHERE   sow_number = in_sow_number;

UPDATE pig_production SET 
    status = INSEMINATION_STATUS_ID_GESTATING
WHERE sow_id = cur_sow_id AND status = INSEMINATION_STATUS_ID_WEANING;


SELECT  a.is_ai,
        a.name,
        b.name

INTO    cur_is_ai,
        cur_semen_source_name,
        cur_pig_race_name
FROM    semen_source a 
LEFT OUTER JOIN pig_race b ON a.pig_race_id = b.id
WHERE   a.id = in_semen_source_id;

IF cur_is_ai > 0 THEN 
    SET cur_semen_desc = CONCAT(cur_pig_race_name, ' FROM ');
    SET cur_semen_desc = CONCAT(cur_semen_desc, cur_semen_source_name);
ELSE
    SET cur_semen_desc = CONCAT(cur_pig_race_name, ' TAKAL FROM ');
    SET cur_semen_desc = CONCAT(cur_semen_desc, cur_semen_source_name);
END IF;




INSERT INTO pig_production (
    sow_id,
    sow_number,
    date_insemination,
    date_expected_birth,
    semen_source_id,
    semen_desc,
    status_id,
    staff_id
) VALUES (
    cur_sow_id,
    in_sow_number,
    in_date_insemination,
    DATE_ADD(in_date_insemination, INTERVAL 115 DAY),
    in_semen_source_id,
    cur_semen_desc,
    INSEMINATION_STATUS_ID_GESTATING,
    in_staff_id
);

SELECT LAST_INSERT_ID() INTO cur_production_id;

UPDATE sow SET
    last_prod_id = cur_production_id
WHERE id = cur_sow_id;


SELECT  is_ai
INTO    cur_is_ai
FROM    semen_source
WHERE   id = in_semen_source_id;

IF cur_is_ai > 0 THEN 
    SET cur_coming_activity_id  = COMING_ACT_ID_ARTIFICIAL_INSEMINATION;
ELSE
    SET cur_coming_activity_id  = COMING_ACT_ID_NATURAL_COUPLING;
END IF;




END process_user;

SELECT 
    res_num                             AS result_number,
    res_code                            AS result_code,
    
    cur_production_id      AS ai_id;
    

END $$

DELIMITER ;
