DELIMITER $$

DROP PROCEDURE IF EXISTS account_register $$
CREATE PROCEDURE account_register(
    in_user_id              INT,
    
    in_country_id           INT,
    in_name                 VARCHAR(100)
)  

BEGIN

/** 
 * Will add account entry.
 * 
 * @author Jack Wong (j2718wong@gmail.com) 
 * @since August 8, 2025
 *
 */

DECLARE LOV_ID_ACCOUNT_NUMDAYS_FREE_TRIAL       INT             DEFAULT 1;


DECLARE RES_NUM_SUCCESS                             INT         DEFAULT 0;
DECLARE RES_NUM_USER_IS_INACTIVE                    INT         DEFAULT 1;
DECLARE RES_NUM_ACCOUNT_ALREADY_REGISTERED_FOR_USER INT         DEFAULT 2;
DECLARE RES_NUM_DUPLICATE_ENTRY                     INT         DEFAULT 3;


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


DECLARE cur_num_days_trial                      INT             DEFAULT 0;


DECLARE cur_account_id                          INT             DEFAULT 0;
DECLARE cur_account_flag                        INT             DEFAULT 0;
DECLARE cur_account_status_id                   INT             DEFAULT 0;
DECLARE cur_account_status_name                 VARCHAR(50);
DECLARE cur_account_name                        VARCHAR(100); 
DECLARE cur_account_date_trial_start            DATE;
DECLARE cur_account_date_trial_end              DATE;



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


IF cur_user_account_id > 0 THEN
    SET res_num     = RES_NUM_ACCOUNT_ALREADY_REGISTERED_FOR_USER;
    SET res_code    = "RES_NUM_ACCOUNT_ALREADY_REGISTERED_FOR_USER";
    
    LEAVE process_user;
END IF;


SELECT  val_int 
INTO    cur_num_days_trial
FROM    a01_list_of_values
WHERE   id = LOV_ID_ACCOUNT_NUMDAYS_FREE_TRIAL;


/* Check account duplicate. */
SELECT  id
INTO    cur_account_id
FROM    account
WHERE   country_id = in_country_id AND UPPER(name)  = UPPER(in_name)
LIMIT   1;


IF cur_account_id > 0 THEN 
    SET res_num     = RES_NUM_DUPLICATE_ENTRY;
    SET res_code    = "RES_NUM_DUPLICATE_ENTRY";
    
    LEAVE process_user;

END IF;





INSERT INTO account(
    name,
    country_id,
    flag,
    status_id,
    date_trial_start,
    date_trial_end
) VALUES (
    in_name,
    in_country_id,
    1,
    ACCOUNT_STATUS_ID_ON_TRIAL,
    CURRENT_DATE,
    DATE_ADD(CURRENT_DATE, INTERVAL cur_num_days_trial DAY)
);

SELECT LAST_INSERT_ID() INTO cur_account_id;


/* The user that registers the account is an account admin. */
UPDATE user SET
    account_id  = cur_account_id,
    flag        = flag | FLAG_BIT_USER_IS_ACCOUNT_ADMIN
WHERE id = in_user_id;

END process_user;


SELECT
    a.name,
    a.flag,
    a.status_id,
    b.name,
    a.date_trial_start,
    a.date_trial_end
INTO
    cur_account_name,
    cur_account_flag,
    cur_account_status_id,
    cur_account_status_name,
    cur_account_date_trial_start,
    cur_account_date_trial_end
FROM account a
LEFT OUTER JOIN account_status b ON a.status_id = b.id
WHERE id = cur_account_id;

SELECT 
    res_num                             AS result_number,
    res_code                            AS result_code,
    res_desc                            AS result_desc,
    
    cur_account_id                      AS acc_id,
    cur_account_name                    AS acc_name,
    cur_account_flag                    AS acc_flag,
    cur_account_status_id               AS acc_status_id,
    cur_account_status_name             AS acc_status_name,
    cur_account_date_trial_start        AS date_trial_start,
    cur_account_date_trial_end          AS date_trial_end;

END $$

DELIMITER ;
