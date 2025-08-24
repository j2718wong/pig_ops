DELIMITER $$

DROP PROCEDURE IF EXISTS pig_production_add $$
CREATE PROCEDURE pig_production_add(
    in_user_id              INT,
    
    in_sow_boar_id          INT,
    in_semen_source_id      INT,
    in_staff_id             INT,
    in_date_insemination    VARCHAR(10)  /* in YYYY-MM-DD format*/
)  

BEGIN

/** 
 * Will create sow_coming_activity entries from a given sow insemination entry.
 * 
 * @author Jack Wong (j2718wong@gmail.com) 
 * @since August 17, 2025
 *
 */

DECLARE RES_NUM_SUCCESS                         INT             DEFAULT 0;


DECLARE RES_NUM_DUPLICATE_ENTRY                 INT             DEFAULT 20;


DECLARE FLAG_BIT_BIZ_OBJ_PIG_PROD               INT             DEFAULT 8192;

DECLARE FLAG_BIT_OPERATION_ADD                  INT             DEFAULT 1;
DECLARE FLAG_BIT_OPERATION_UPDATE               INT             DEFAULT 2;
DECLARE FLAG_BIT_OPERATION_DELETE               INT             DEFAULT 4;



DECLARE PRODUCTION_STATUS_ID_GESTATING          INT             DEFAULT 1;
DECLARE PRODUCTION_STATUS_ID_NOT_PREGNANT       INT             DEFAULT 90;



DECLARE cur_user_account_id                     INT             DEFAULT 0;
DECLARE cur_user_group_id                       INT             DEFAULT 0;


DECLARE cur_sow_boar_account_id                 INT             DEFAULT 0;
DECLARE cur_sow_boar_pig_farm_id                INT             DEFAULT 0;
DECLARE cur_sow_boar_farm_sow_id                INT             DEFAULT 0;
DECLARE cur_sow_boar_last_prod_id               INT             DEFAULT 0;




DECLARE cur_is_ai                               INT             DEFAULT 0;
DECLARE cur_semen_source_name                   VARCHAR(50)     DEFAULT '';
DECLARE cur_pig_race_name                       VARCHAR(50)     DEFAULT '';

DECLARE cur_semen_desc                          VARCHAR(100)    DEFAULT '';


DECLARE cur_coming_activity_id                  INT             DEFAULT 0;

DECLARE cur_production_id                       INT             DEFAULT 0;


DECLARE res_num                                 INT             DEFAULT 0;
DECLARE res_code                                VARCHAR(80)     DEFAULT '';
DECLARE res_desc                                VARCHAR(180)    DEFAULT '';


SET res_num     = RES_NUM_SUCCESS;
SET res_code    = "SUCCESS";


SELECT  a.account_id,
        a.pig_farm_id,
        a.farm_sow_id,
        a.last_prod_id,
        b.status_id
INTO    cur_sow_boar_account_id,
        cur_sow_boar_pig_farm_id,
        cur_sow_boar_farm_sow_id,
        cur_sow_boar_last_prod_id
        cur_last_production_status
FROM    sow_boar a
LEFT OUTER JOIN pig_production b ON a.last_prod_id = b.id
WHERE   id = in_sow_boar_id
LIMIT   1;


CALL basic_user_check(
    in_user_id, 
    1, /* user must have an account*/
    cur_sow_boar_account_id,
    
    FLAG_BIT_BIZ_OBJ_PIG_PROD,
    FLAG_BIT_OPERATION_ADD,
    
    cur_user_account_id, 
    cur_user_group_id,
    res_num, 
    res_code, 
    res_desc);


process_user : BEGIN


IF res_num != RES_NUM_SUCCESS THEN 
    LEAVE process_user;
END IF;


SELECT  id
INTO    cur_production_id
FROM    pig_production
WHERE   sow_id              = in_sow_boar_id     AND 
        date_insemination   = in_date_insemination 
LIMIT   1;


IF cur_production_id > 0 THEN
    SET res_num     = RES_NUM_DUPLICATE_ENTRY;
    SET res_code    = "RES_NUM_DUPLICATE_ENTRY";
    
    LEAVE process_user;
END IF;


/* Set previous pig_production of this sow to not pregnant, if status is gestating*/
IF cur_last_production_status = PRODUCTION_STATUS_ID_GESTATING THEN 
    UPDATE pig_production SET 
        prod_status_id = PRODUCTION_STATUS_ID_NOT_PREGNANT
    WHERE id = cur_sow_boar_last_prod_id;
END IF;


INSERT INTO pig_production (
    account_id,
    pig_farm_id,
    
    sow_id,
    date_insemination,
    date_expected_birth,
    semen_source_id,
    prod_status_id,
    staff_id
) VALUES (
    cur_user_account_id,
    cur_sow_boar_pig_farm_id,
    
    in_sow_boar_id,
    in_date_insemination,
    DATE_ADD(in_date_insemination, INTERVAL 115 DAY),
    in_semen_source_id,
    PRODUCTION_STATUS_ID_GESTATING,
    in_staff_id
);

SELECT LAST_INSERT_ID() INTO cur_production_id;

UPDATE sow_boar SET
    last_prod_id    = cur_production_id,
    sow_status_id   = ?
WHERE id = in_sow_boar_id;






END process_user;

SELECT 
    res_num                             AS result_number,
    res_code                            AS result_code,
    res_desc                            AS result_desc,
    
    cur_production_id                   AS pig_prod_id,
    is_sow_boar_id                      AS sow_boar_id,
    cur_sow_boar_farm_sow_id            AS farm_sow_id;
    

END $$

DELIMITER ;
