DELIMITER $$

DROP PROCEDURE IF EXISTS account_update $$
CREATE PROCEDURE account_update(
    in_user_id                  INT,
    
    in_name                     VARCHAR(100)
    
)

BEGIN

/** 
 * Will update account
 * @author Jack Wong
 * @since August 10, 2025
 *
 */
 
DECLARE RES_NUM_SUCCESS                         INT             DEFAULT 0;
DECLARE RES_NUM_USER_IS_INACTIVE                INT             DEFAULT 1;
DECLARE RES_NUM_USER_HAS_NO_ACCOUNT             INT             DEFAULT 2;
DECLARE RES_NUM_ACCOUNT_DISABLED                INT             DEFAULT 3;
DECLARE RES_NUM_ACCOUNT_STATUS_TRIAL_EXPIRED    INT             DEFAULT 4;
DECLARE RES_NUM_ACCOUNT_STATUS_UNPAID_BILL      INT             DEFAULT 5;


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


DECLARE AUDIT_ACTION_ADD                        VARCHAR(3)      DEFAULT "ADD";
DECLARE AUDIT_ACTION_UPDATE                     VARCHAR(3)      DEFAULT "UPD";
DECLARE AUDIT_ACTION_DELETE                     VARCHAR(3)      DEFAULT "DEL";


DECLARE cur_user_flag                           INT             DEFAULT 0;
DECLARE cur_user_account_id                     INT             DEFAULT 0;


DECLARE cur_account_flag                        INT             DEFAULT 0;
DECLARE cur_account_status                      INT             DEFAULT 0;
DECLARE cur_account_name                        VARCHAR(100); 
DECLARE cur_account_date_trial_start            DATE;
DECLARE cur_account_date_trial_end              DATE;




DECLARE res_num                                 INT             DEFAULT 0;
DECLARE res_code                                VARCHAR(80)     DEFAULT '';
DECLARE res_desc                                VARCHAR(180)    DEFAULT '';

DECLARE description                             VARCHAR(200)    DEFAULT '';


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

/* Check user. */
IF cur_user_flag & FLAG_BIT_USER_IS_ACTIVE = 0 THEN 
    SET res_num     = RES_NUM_USER_IS_INACTIVE;
    SET res_code    = "RES_NUM_USER_IS_INACTIVE";

    LEAVE process_user;
    
END IF;


IF cur_user_account_id = 0 THEN 
    SET res_num     = RES_NUM_USER_HAS_NO_ACCOUNT;
    SET res_code    = "RES_NUM_USER_HAS_NO_ACCOUNT";

    LEAVE process_user;
    
END IF;


/* Check account. */
SELECT 
    flag,
    name
INTO
    cur_account_flag,
    cur_account_name
    
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


/* Check account duplicate. */

UPDATE account SET
    name            = in_name
WHERE id = cur_user_account_id;


SET description = CONCAT("old_acc_name = ", cur_account_name, "; new_acc_name = ",
    in_name);

INSERT INTO app_audit_log(
    user_id,
    action,
    description,
    date
) VALUES (
    in_user_id,
    AUDIT_ACTION_UPDATE,
    description,
    CURRENT_DATE
);


END process_user;


SELECT
    flag,
    status,
    name,
    date_trial_start,
    date_trial_end
INTO 
    cur_account_flag,
    cur_account_status,
    cur_account_name,
    cur_account_date_trial_start,
    cur_account_date_trial_end
FROM account
WHERE id = cur_user_account_id;

SELECT 
    res_num                             AS result_number,
    res_code                            AS result_code,
    res_desc                            AS result_desc,
    
    cur_user_account_id                 AS acc_id,
    cur_account_name                    AS acc_name,
    cur_account_flag                    AS acc_flag,
    cur_account_status                  AS acc_status,
    cur_account_date_trial_start        AS date_trial_start,
    cur_account_date_trial_end          AS date_trial_end;




END $$

DELIMITER ;
