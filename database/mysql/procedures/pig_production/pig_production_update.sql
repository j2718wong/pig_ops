DELIMITER $$

DROP PROCEDURE IF EXISTS pig_production_update $$
CREATE PROCEDURE pig_production_update(
    in_user_id                  INT,
    
    in_pig_production_id         INT,
    in_pig_race_id              INT,
    
    in_name                     VARCHAR(50),
    in_description              VARCHAR(160)
    
)

BEGIN

/** 
 * Will update pig_production entry.
 * @author Jack Wong
 * @since August 23, 2025
 *
 */
 
DECLARE RES_NUM_SUCCESS                         INT             DEFAULT 0;


DECLARE BUSINESS_OBJ_ID_PIG_RACE_LINE           INT             DEFAULT 8;

DECLARE FLAG_BIT_OPERATION_ADD                  INT             DEFAULT 1;
DECLARE FLAG_BIT_OPERATION_UPDATE               INT             DEFAULT 2;
DECLARE FLAG_BIT_OPERATION_DELETE               INT             DEFAULT 4;


DECLARE AUDIT_ACTION_ADD                        VARCHAR(3)      DEFAULT "ADD";
DECLARE AUDIT_ACTION_UPDATE                     VARCHAR(3)      DEFAULT "UPD";
DECLARE AUDIT_ACTION_DELETE                     VARCHAR(3)      DEFAULT "DEL";


DECLARE cur_user_account_id                     INT             DEFAULT 0;
DECLARE cur_user_group_id                       INT             DEFAULT 0;


DECLARE cur_pig_production_id                    INT             DEFAULT 0;
DECLARE cur_pig_production_account_id            INT             DEFAULT 0;
DECLARE cur_pig_production_flag                  INT             DEFAULT 0;
DECLARE cur_pig_production_name                  VARCHAR(50)     DEFAULT NULL;


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
    
    BUSINESS_OBJ_ID_PIG_RACE_LINE,
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


/* Check for duplicate entry */
SELECT  id
INTO    cur_pig_production_id
FROM    pig_production
WHERE   id                  != in_pig_production_id  AND
        account_id          = cur_user_account_id   AND
        UPPER(name)         = UPPER(in_name)
LIMIT   1;

IF cur_pig_production_id > 0 THEN 
    SET res_num     = RES_NUM_DUPLICATE_ENTRY;
    SET res_code    = "RES_NUM_DUPLICATE_ENTRY";
    
    LEAVE process_user;
END IF;



UPDATE pig_production SET
    pig_race_id         = in_pig_race_id,
    
    name                = in_name,
    description         = in_description,
    
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
    
    in_pig_production_id                 AS pig_production_id,
    cur_pig_production_flag              AS pig_production_flag,
    cur_pig_production_name              AS pig_production_name;
    


END $$

DELIMITER ;
