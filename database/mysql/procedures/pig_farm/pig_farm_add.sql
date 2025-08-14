DELIMITER $$

DROP PROCEDURE IF EXISTS pig_farm_add $$
CREATE PROCEDURE pig_farm_add(
    in_user_id              INT,

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

DECLARE RES_NUM_ACCOUNT_DISABLED                INT             DEFAULT 5;
DECLARE RES_NUM_ACCOUNT_STATUS_TRIAL_EXPIRED    INT             DEFAULT 6;
DECLARE RES_NUM_ACCOUNT_STATUS_UNPAID_BILL      INT             DEFAULT 7;
DECLARE RES_NUM_ACCOUNT_EXCEED_MAX_FARMS        INT             DEFAULT 8;


DECLARE RES_NUM_DUPLICATE_ENTRY                 INT             DEFAULT 1;


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
DECLARE cur_account_status_id                   INT             DEFAULT 0;
DECLARE cur_account_farm_id_1                   INT             DEFAULT 0;
DECLARE cur_account_farm_id_2                   INT             DEFAULT 0;
DECLARE cur_account_farm_id_3                   INT             DEFAULT 0;
DECLARE cur_account_farm_id_4                   INT             DEFAULT 0;
DECLARE cur_account_farm_id_5                   INT             DEFAULT 0;

DECLARE is_added_to_account                     INT             DEFAULT 0;

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


IF cur_user_flag & FLAG_BIT_USER_EMAIL_VERIFIED = 0 THEN 
    SET res_num     = RES_NUM_USER_NOT_EMAIL_VERIFIED;
    SET res_code    = "RES_NUM_USER_NOT_EMAIL_VERIFIED";

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
    status_id,
    farm_id_1,
    farm_id_2,
    farm_id_3,
    farm_id_4,
    farm_id_5
INTO
    cur_account_flag,
    cur_account_status_id
    cur_account_farm_id_1,
    cur_account_farm_id_2,
    cur_account_farm_id_3,
    cur_account_farm_id_4,
    cur_account_farm_id_5
    
FROM account
WHERE id = cur_user_account_id;



IF cur_account_flag & FLAG_BIT_ACCOUNT_ENABLE = 0 THEN 
    SET res_num     = RES_NUM_ACCOUNT_DISABLED;
    SET res_code    = "RES_NUM_ACCOUNT_DISABLED";
    
    IF cur_account_status_id = ACCOUNT_STATUS_UNPAID_BILL THEN
        SET res_num     = RES_NUM_ACCOUNT_STATUS_UNPAID_BILL;
        SET res_code    = "RES_NUM_ACCOUNT_STATUS_UNPAID_BILL";
    
    END IF;
    
    LEAVE process_user;
END IF;


IF  cur_account_farm_id_1 > 0 AND 
    cur_account_farm_id_2 > 0 AND 
    cur_account_farm_id_3 > 0 AND 
    cur_account_farm_id_4 > 0 AND 
    cur_account_farm_id_5 > 0 THEN 
    
    
    SET res_num     = RES_NUM_ACCOUNT_EXCEED_MAX_FARMS;
    SET res_code    = "RES_NUM_ACCOUNT_EXCEED_MAX_FARMS";
    
    LEAVE process_user;
END IF;


SELECT  id
INTO    cur_pig_farm_id
FROM    pig_farm
WHERE   account_id = cur_user_account_id AND UPPER(name)  = UPPER(in_name)
LIMIT   1;


/* Check for duplicate farm name*/
IF cur_pig_farm_id > 0 THEN 
    SET res_num     = RES_NUM_DUPLICATE_ENTRY;
    SET res_code    = "RES_NUM_DUPLICATE_ENTRY";
    
    LEAVE process_user;
END IF;



INSERT INTO pig_farm(
    account_id,
    flag,
    name,
    added_by_user_id,
    
    country_id,
    adrs_level_1_id,
    adrs_level_2_id,
    adrs_level_3_id,
    latitude,
    longitude
) VALUES (
    cur_user_account_id,
    1,    
    in_name,
    in_user_id,
    
    in_country_id,
    in_adrs_level_1_id,
    in_adrs_level_2_id,
    in_adrs_level_3_id,
    in_latitude,
    in_longitude
    
);

SELECT LAST_INSERT_ID() INTO cur_pig_farm_id;



IF is_added_to_account = 0 AND cur_account_farm_id_1 = 0 THEN
    UPDATE account SET 
        farm_id_1 = cur_pig_farm_id
    WHERE id = cur_user_account_id;
    
    SET is_added_to_account = 1;
END IF;

IF is_added_to_account = 0 AND  cur_account_farm_id_2 = 0 THEN
    UPDATE account SET 
        farm_id_2 = cur_pig_farm_id
    WHERE id = cur_user_account_id;

    SET is_added_to_account = 1;
END IF;

IF is_added_to_account = 0 AND  cur_account_farm_id_3 = 0 THEN
    UPDATE account SET 
        farm_id_3 = cur_pig_farm_id
    WHERE id = cur_user_account_id;

    SET is_added_to_account = 1;
END IF;

IF is_added_to_account = 0 AND  cur_account_farm_id_4 = 0 THEN
    UPDATE account SET 
        farm_id_4 = cur_pig_farm_id
    WHERE id = cur_user_account_id;

    SET is_added_to_account = 1;
END IF;

IF is_added_to_account = 0 AND  cur_account_farm_id_5 = 0 THEN
    UPDATE account SET 
        farm_id_5 = cur_pig_farm_id
    WHERE id = cur_user_account_id;

    SET is_added_to_account = 1;
END IF;



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
