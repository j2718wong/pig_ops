DELIMITER $$

DROP PROCEDURE IF EXISTS pig_farm_update $$
CREATE PROCEDURE pig_farm_update(
    in_user_id              INT,
    in_pig_farm_id          INT,

    in_name                 VARCHAR(50),
    
    in_country_id           INT, 
    in_adrs_level_1_id      INT,
    in_adrs_level_2_id      INT,
    in_adrs_level_3_id      INT,
    in_latitude             DECIMAL(10,5),
    in_longitude            DECIMAL(10,5)
    
)  

BEGIN

/** 
 * Will add pig farm entry.
 * 
 * @author Jack Wong (j2718wong@gmail.com) 
 * @since August 10, 2025
 *
 */

DECLARE RES_NUM_SUCCESS                         INT             DEFAULT 0;
DECLARE RES_NUM_USER_IS_INACTIVE                INT             DEFAULT 1;
DECLARE RES_NUM_USER_NOT_EMAIL_VERIFIED         INT             DEFAULT 2;
DECLARE RES_NUM_USER_NOT_ACCOUNT_ADMIN          INT             DEFAULT 3;
DECLARE RES_NUM_USER_NO_ACCOUNT_SET             INT             DEFAULT 4;

DECLARE RES_NUM_ACCOUNT_MISMATCH                INT             DEFAULT 5;
DECLARE RES_NUM_ACCOUNT_DISABLED                INT             DEFAULT 6;
DECLARE RES_NUM_ACCOUNT_STATUS_TRIAL_EXPIRED    INT             DEFAULT 7;
DECLARE RES_NUM_ACCOUNT_STATUS_UNPAID_BILL      INT             DEFAULT 8;


/* user.flag bits*/
DECLARE FLAG_BIT_USER_IS_ACTIVE                 INT             DEFAULT 1;
DECLARE FLAG_BIT_USER_EMAIL_VERIFIED            INT             DEFAULT 2;
DECLARE FLAG_BIT_USER_MOBILE_NUM_VERIFIED       INT             DEFAULT 4;
DECLARE FLAG_BIT_USER_IS_DELETED                INT             DEFAULT 8;

DECLARE FLAG_BIT_USER_IS_ACCOUNT_ADMIN          INT             DEFAULT 16;


/* account.flag bits*/
DECLARE FLAG_BIT_ACCOUNT_ENABLE                 INT             DEFAULT 1;

DECLARE ACCOUNT_STATUS_ON_TRIAL                 INT             DEFAULT 1;
DECLARE ACCOUNT_STATUS_TRIAL_EXPIRED            INT             DEFAULT 2;
DECLARE ACCOUNT_STATUS_UNPAID_BILL              INT             DEFAULT 3;


DECLARE cur_user_flag                           INT             DEFAULT 0;
DECLARE cur_user_account_id                     INT             DEFAULT 0;

DECLARE cur_account_flag                        INT             DEFAULT 0;
DECLARE cur_account_status                      INT             DEFAULT 0;

DECLARE cur_farm_account_id                     INT             DEFAULT 0;


DECLARE cur_pig_farm_id                         INT             DEFAULT 0;
DECLARE cur_pig_farm_flag                       INT             DEFAULT 0;
DECLARE cur_pig_farm_name                       VARCHAR(50)     DEFAULT '';



DECLARE res_num                                 INT             DEFAULT 0;
DECLARE res_code                                VARCHAR(80)     DEFAULT '';
DECLARE res_desc                                VARCHAR(180)    DEFAULT '';


SET res_num         = RES_NUM_SUCCESS;


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


IF cur_user_flag & FLAG_BIT_USER_IS_ACCOUNT_ADMIN = 0 THEN 
    SET res_num     = RES_NUM_USER_NOT_ACCOUNT_ADMIN;
    SET res_code    = "RES_NUM_USER_NOT_ACCOUNT_ADMIN";

    LEAVE process_user;
    
END IF;


IF cur_user_account_id = 0 THEN 
    SET res_num     = RES_NUM_USER_NO_ACCOUNT_SET;
    SET res_code    = "RES_NUM_USER_NO_ACCOUNT_SET";

    LEAVE process_user;
END IF;


/* Check account*/
SELECT 
    flag,
    status
INTO
    cur_account_flag,
    cur_account_status
    
FROM account
WHERE id = cur_user_account_id;



IF cur_account_flag & FLAG_BIT_ACCOUNT_ENABLE = 0 THEN 
    SET res_num     = RES_NUM_ACCOUNT_DISABLED;
    SET res_code    = "RES_NUM_ACCOUNT_DISABLED";
    
    IF cur_account_status = ACCOUNT_STATUS_UNPAID_BILL THEN
        SET res_num     = RES_NUM_ACCOUNT_STATUS_UNPAID_BILL;
        SET res_code    = "RES_NUM_ACCOUNT_STATUS_UNPAID_BILL";
    
    END IF;
    
    LEAVE process_user;
END IF;


SELECT  account_id
INTO    cur_farm_account_id
WHERE   id = in_pig_farm_id;


IF cur_user_account_id != cur_farm_account_id THEN 
    SET res_num     = RES_NUM_ACCOUNT_MISMATCH;
    SET res_code    = "RES_NUM_ACCOUNT_MISMATCH";

    LEAVE process_user;
END IF;


UPDATE pig_farm SET
    name                = in_name,
    
    country_id          = in_country_id,
    adrs_level_1_id     = in_adrs_level_1_id,
    adrs_level_2_id     = in_adrs_level_2_id,
    adrs_level_3_id     = in_adrs_level_3_id,
    latitude            = in_latitude,
    longitude           = in_longitude
WHERE id =  in_pig_farm_id;

END process_user;


SELECT
    flag,
    name
INTO 
    cur_pig_farm_flag,
    cur_pig_farm_name
FROM pig_farm
WHERE id = cur_pig_farm_id;

SELECT 
    res_num                             AS result_number,
    res_code                            AS result_code,
    res_desc                            AS result_desc,
    
    cur_pig_farm_id                     AS pig_farm_id,
    cur_pig_farm_name                   AS pig_farm_name,
    cur_pig_farm_flag                   AS pig_farm_flag;
    

END $$

DELIMITER ;
