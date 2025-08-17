DELIMITER $$

DROP PROCEDURE IF EXISTS semen_source_add $$
CREATE PROCEDURE semen_source_add(
    in_user_id              INT,

    in_pig_farm_id          INT,
    in_is_ai                INT,
    in_pig_race_id          INT,
    in_boar_id              INT,
    
    in_name                 VARCHAR(50),
    in_description          VARCHAR(160)
)  

BEGIN

/** 
 * Will add semen_source entry.
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

/* semen_source.flag bits*/
DECLARE FLAG_BIT_SEMEN_SOURCE_IS_DELETED        INT             DEFAULT 1;


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

DECLARE is_added_to_account                     INT             DEFAULT 0;

DECLARE cur_semen_source_id                     INT             DEFAULT 0;
DECLARE cur_semen_source_flag                   INT             DEFAULT 0;
DECLARE cur_semen_source_name                   VARCHAR(50)     DEFAULT '';



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


/* Check for duplicate entry */
SELECT  id
INTO    cur_semen_source_id
FROM    semen_source
WHERE   account_id 	= cur_user_account_id   AND 
        pig_farm_id = in_pig_farm_id       	AND 
        UPPER(name) = UPPER(in_name)
LIMIT   1;

IF cur_semen_source_id > 0 THEN 
    SET res_num     = RES_NUM_DUPLICATE_ENTRY;
    SET res_code    = "RES_NUM_DUPLICATE_ENTRY";
    
    LEAVE process_user;
END IF;



INSERT INTO semen_source(
    account_id,
    pig_farm_id,
    is_ai,
    pig_race_id,
    boar_id,
    added_by_user_id,
    
    name,
    description
) VALUES (
    cur_user_account_id,
    in_pig_farm_id,
    in_is_ai,
    in_pig_race_id,
    in_boar_id,
    in_user_id,
    
    in_name,
    in_description
    
);

SELECT LAST_INSERT_ID() INTO cur_semen_source_id;




END process_user;


SELECT
    flag,
    name
INTO 
    cur_semen_source_flag,
    cur_semen_source_name
FROM semen_source
WHERE id = cur_semen_source_id;

SELECT 
    res_num                             AS result_number,
    res_code                            AS result_code,
    res_desc                            AS result_desc,
    
    cur_semen_source_id                 AS semen_source_id,
    cur_semen_source_flag               AS semen_source_flag,
    cur_semen_source_name               AS semen_source_name;

END $$

DELIMITER ;
