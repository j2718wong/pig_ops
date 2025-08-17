DELIMITER $$

DROP PROCEDURE IF EXISTS sow_add $$
CREATE PROCEDURE sow_add(
    in_user_id              INT,
    
    in_pig_farm_id          INT,
    in_birth_prod_id        INT,
    in_line_id              INT,
    in_sow_status_id        INT,
    
    in_sow_number           VARCHAR(10),
    in_sow_name             VARCHAR(20),    
    in_date_of_birth        VARCHAR(10),
    in_notes                VARCHAR(160)
)  

BEGIN

/** 
 * Will add sow entry.
 * 
 * @author Jack Wong (j2718wong@gmail.com) 
 * @since August 15, 2025
 *
 */

DECLARE RES_NUM_SUCCESS                         INT             DEFAULT 0;

DECLARE RES_NUM_USER_IS_INACTIVE                INT             DEFAULT 1;
DECLARE RES_NUM_USER_NOT_EMAIL_VERIFIED         INT             DEFAULT 2;
DECLARE RES_NUM_USER_NOT_ACCOUNT_ADMIN          INT             DEFAULT 3;
DECLARE RES_NUM_USER_NO_ACCOUNT_SET             INT             DEFAULT 4;

DECLARE RES_NUM_ACCOUNT_DISABLED                INT             DEFAULT 11;
DECLARE RES_NUM_ACCOUNT_STATUS_TRIAL_EXPIRED    INT             DEFAULT 12;
DECLARE RES_NUM_ACCOUNT_STATUS_UNPAID_BILL      INT             DEFAULT 13;
DECLARE RES_NUM_ACCOUNT_EXCEED_MAX_FARMS        INT             DEFAULT 14;
DECLARE RES_NUM_ACCOUNT_MISMATCH                INT             DEFAULT 15;


DECLARE RES_NUM_DUPLICATE_ENTRY                 INT             DEFAULT 50;


/* user.flag bits*/
DECLARE FLAG_BIT_USER_IS_ACTIVE                 INT             DEFAULT 1;
DECLARE FLAG_BIT_USER_EMAIL_VERIFIED            INT             DEFAULT 2;
DECLARE FLAG_BIT_USER_MOBILE_NUM_VERIFIED       INT             DEFAULT 4;
DECLARE FLAG_BIT_USER_IS_DELETED                INT             DEFAULT 8;

DECLARE FLAG_BIT_USER_IS_ACCOUNT_ADMIN          INT             DEFAULT 16;


/* account.flag bits*/
DECLARE FLAG_BIT_ACCOUNT_ENABLE                 INT             DEFAULT 1;

DECLARE ACCOUNT_STATUS_ID_ON_TRIAL              INT             DEFAULT 1;
DECLARE ACCOUNT_STATUS_ID_TRIAL_EXPIRED         INT             DEFAULT 2;
DECLARE ACCOUNT_STATUS_ID_UNPAID_BILL           INT             DEFAULT 3;


DECLARE cur_user_flag                           INT             DEFAULT 0;
DECLARE cur_user_account_id                     INT             DEFAULT 0;

DECLARE cur_account_flag                        INT             DEFAULT 0;
DECLARE cur_account_status_id                   INT             DEFAULT 0;
DECLARE cur_account_farm_01_id                  INT             DEFAULT 0;
DECLARE cur_account_farm_02_id                  INT             DEFAULT 0;
DECLARE cur_account_farm_03_id                  INT             DEFAULT 0;
DECLARE cur_account_farm_04_id                  INT             DEFAULT 0;
DECLARE cur_account_farm_05_id                  INT             DEFAULT 0;


DECLARE cur_pig_farm_account_id                 INT             DEFAULT 0;
DECLARE cur_pig_farm_last_sow_id                INT             DEFAULT 0;


DECLARE cur_sow_id                              INT             DEFAULT 0;

DECLARE res_num                                 INT             DEFAULT 0;
DECLARE res_code                                VARCHAR(80)     DEFAULT '';
DECLARE res_desc                                VARCHAR(180)    DEFAULT '';


SET res_num     = RES_NUM_SUCCESS;
SET res_code    = "SUCCESS";


SELECT  
        flag,
        account_id
INTO    
        cur_user_flag,
        cur_user_account_id
FROM    user 
WHERE   id = in_user_id;


process_user : BEGIN

/* Check user*/
IF cur_user_flag & FLAG_BIT_USER_IS_ACTIVE = 0 THEN 
    SET res_num     = RES_NUM_USER_IS_INACTIVE;
    SET res_code    = "RES_NUM_USER_IS_INACTIVE";

    LEAVE process_user;    
END IF;


IF cur_user_flag & FLAG_BIT_USER_EMAIL_VERIFIED = 0 THEN 
    SET res_num     = RES_NUM_USER_NOT_EMAIL_VERIFIED;
    SET res_code    = "RES_NUM_USER_NOT_EMAIL_VERIFIED";

    LEAVE process_user;    
END IF;


/* TODO  evaluate if non- admin users can add sow entry
IF cur_user_flag & FLAG_BIT_USER_IS_ACCOUNT_ADMIN = 0 THEN 
    SET res_num     = RES_NUM_USER_NOT_ACCOUNT_ADMIN;
    SET res_code    = "RES_NUM_USER_NOT_ACCOUNT_ADMIN";

    LEAVE process_user;    
END IF;
*/


IF cur_user_account_id = 0 THEN 
    SET res_num     = RES_NUM_USER_NO_ACCOUNT_SET;
    SET res_code    = "RES_NUM_USER_NO_ACCOUNT_SET";

    LEAVE process_user;
END IF;



/* Check account*/
SELECT 
    flag,
    status_id,
    farm_01_id,
    farm_02_id,
    farm_03_id,
    farm_04_id,
    farm_05_id
INTO
    cur_account_flag,
    cur_account_status_id,
    cur_account_farm_01_id,
    cur_account_farm_02_id,
    cur_account_farm_03_id,
    cur_account_farm_04_id,
    cur_account_farm_05_id
    
FROM account
WHERE id = cur_user_account_id;


IF cur_account_flag & FLAG_BIT_ACCOUNT_ENABLE = 0 THEN 
    SET res_num     = RES_NUM_ACCOUNT_DISABLED;
    SET res_code    = "RES_NUM_ACCOUNT_DISABLED";
    
    IF cur_account_status_id = ACCOUNT_STATUS_ID_UNPAID_BILL THEN
        SET res_num     = RES_NUM_ACCOUNT_STATUS_UNPAID_BILL;
        SET res_code    = "RES_NUM_ACCOUNT_STATUS_UNPAID_BILL";
    
    END IF;
    
    LEAVE process_user;
END IF;


SELECT  
        account_id,
        last_sow_id
INTO    
        cur_pig_farm_account_id,
        cur_pig_farm_last_sow_id
FROM    pig_farm
WHERE   id = in_pig_farm_id
LIMIT   1;


IF cur_user_account_id != cur_pig_farm_account_id THEN 
    SET res_num     = RES_NUM_ACCOUNT_MISMATCH;
    SET res_code    = "RES_NUM_ACCOUNT_MISMATCH";
    
    LEAVE process_user;
END IF;


/* Check for duplicate entry. */
SELECT  id
INTO    cur_sow_id
FROM    sow
WHERE   account_id  = cur_user_account_id   AND
        pig_farm_id = in_pig_farm_id        AND
        sow_number  = in_sow_number;

IF cur_sow_id > 0 THEN 
    SET res_num     = RES_NUM_DUPLICATE_ENTRY;
    SET res_code    = "RES_NUM_DUPLICATE_ENTRY";
    
    LEAVE process_user;
END IF;


SET cur_pig_farm_last_sow_id = cur_pig_farm_last_sow_id + 1;


INSERT INTO sow(
    account_id,
    pig_farm_id,
    farm_sow_id,
    added_by_user_id,
    birth_prod_id,
    line_id,
    sow_status_id,
    
    sow_number,
    sow_name,
    date_of_birth,
    notes
) VALUES (
    cur_user_account_id,
    in_pig_farm_id,
    cur_pig_farm_last_sow_id,
    in_user_id,
    in_birth_prod_id,
    in_line_id,
    in_sow_status_id,
    
    in_sow_number,
    in_sow_name,
    in_date_of_birth,
    in_notes
);

SELECT LAST_INSERT_ID() INTO cur_sow_id;

UPDATE pig_farm SET 
    last_sow_id     = cur_pig_farm_last_sow_id
WHERE id = in_pig_farm_id;


END process_user;



SELECT 
    res_num                             AS result_number,
    res_code                            AS result_code,
    res_desc                            AS result_desc,
    
    cur_sow_id                          AS sow_id,
    cur_pig_farm_last_sow_id            AS farm_sow_id;
    

END $$

DELIMITER ;
