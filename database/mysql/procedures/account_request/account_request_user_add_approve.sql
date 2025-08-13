DELIMITER $$

DROP PROCEDURE IF EXISTS account_request_user_add_approve $$
CREATE PROCEDURE account_request_user_add_approve(
    in_account_request_id       INT,
    in_approving_user_id        INT
    
)

BEGIN

/** 
 * Will add account_req_user_add; this is initiated by the user.
 * @author Jack Wong
 * @since August 11, 2025
 *
 */
 
DECLARE RES_NUM_SUCCESS                         INT             DEFAULT 0;
DECLARE RES_NUM_USER_IS_INACTIVE                INT             DEFAULT 1;
DECLARE RES_NUM_USER_NOT_EMAIL_VERIFIED         INT             DEFAULT 2;
DECLARE RES_NUM_USER_NOT_ACCOUNT_ADMIN          INT             DEFAULT 3;

DECLARE RES_NUM_ACCOUNT_DISABLED                INT             DEFAULT 4;
DECLARE RES_NUM_ACCOUNT_STATUS_TRIAL_EXPIRED    INT             DEFAULT 5;
DECLARE RES_NUM_ACCOUNT_STATUS_UNPAID_BILL      INT             DEFAULT 6;
DECLARE RES_NUM_ACC_REQ_USER_ADD_ALREADY_APPROVED   INT         DEFAULT 7;


/* user.flag bits*/
DECLARE FLAG_BIT_USER_IS_ACTIVE                 INT             DEFAULT 1;
DECLARE FLAG_BIT_USER_EMAIL_VERIFIED            INT             DEFAULT 2;
DECLARE FLAG_BIT_USER_MOBILE_NUM_VERIFIED       INT             DEFAULT 4;
DECLARE FLAG_BIT_USER_IS_DELETED                INT             DEFAULT 8;

DECLARE FLAG_BIT_USER_IS_ACCOUNT_ADMIN          INT             DEFAULT 16;


/* account.flag bits*/
DECLARE FLAG_BIT_ACCOUNT_ENABLE                 INT             DEFAULT 1;


DECLARE ACC_REQ_STATUS_REQUESTED                INT             DEFAULT 0;
DECLARE ACC_REQ_STATUS_APPROVED                 INT             DEFAULT 1;
DECLARE ACC_REQ_STATUS_REJECTED                 INT             DEFAULT 2;


DECLARE AUDIT_ACTION_ADD                        VARCHAR(3)      DEFAULT "ADD";
DECLARE AUDIT_ACTION_UPDATE                     VARCHAR(3)      DEFAULT "UPD";
DECLARE AUDIT_ACTION_DELETE                     VARCHAR(3)      DEFAULT "DEL";


DECLARE cur_acc_req_status                      INT             DEFAULT 0;
DECLARE cur_acc_req_account_id                  INT             DEFAULT 0;
DECLARE cur_acc_req_requesting_user_id          INT             DEFAULT 0;

DECLARE cur_user_flag                           INT             DEFAULT 0;
DECLARE cur_user_account_id                     INT             DEFAULT 0;
DECLARE cur_user_email                          VARCHAR(100);


DECLARE cur_account_flag                        INT             DEFAULT 0;
DECLARE cur_account_status                      INT             DEFAULT 0;
DECLARE cur_account_name                        VARCHAR(100); 
DECLARE cur_account_date_trial_start            DATE;
DECLARE cur_account_date_trial_end              DATE;

DECLARE cur_account_req_id                      INT             DEFAULT 0;


DECLARE cur_approving_user_username             VARCHAR(50)     DEFAULT NULL;
DECLARE cur_approving_user_name_last            VARCHAR(50)     DEFAULT NULL;
DECLARE cur_approving_user_name_first           VARCHAR(50)     DEFAULT NULL;


DECLARE cur_acc_req_dt_approved                 DATETIME        DEFAULT NULL;


DECLARE res_num                                 INT             DEFAULT 0;
DECLARE res_code                                VARCHAR(80)     DEFAULT '';
DECLARE res_desc                                VARCHAR(180)    DEFAULT '';

DECLARE description                             VARCHAR(200)    DEFAULT '';


SET res_num     = RES_NUM_SUCCESS;
SET res_code    = "SUCCESS";


SELECT  
        flag,
        email
INTO    
        cur_user_flag,
        cur_user_email
FROM    user 
WHERE   id = in_approving_user_id;


process_user : BEGIN

/* Check request status.*/
SELECT  
        status,
        account_id,
        requesting_user_id
INTO    
        cur_acc_req_status,
        cur_acc_req_account_id,
        cur_acc_req_requesting_user_id
        
FROM    account_request
WHERE   id = in_account_request_id;


IF cur_acc_req_status = ACC_REQ_STATUS_APPROVED THEN
    SET res_num     = RES_NUM_ACC_REQ_USER_ADD_ALREADY_APPROVED;
    SET res_code    = "RES_NUM_ACC_REQ_USER_ADD_ALREADY_APPROVED";

    LEAVE process_user;
END IF;


/* Check user. */
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


/* Check account. */
SELECT 
    flag,
    status,
    name
INTO
    cur_account_flag,
    cur_account_status,
    cur_account_name
    
FROM account
WHERE id = in_account_id;


IF cur_account_flag & FLAG_BIT_ACCOUNT_ENABLE = 0 THEN 
    SET res_num     = RES_NUM_ACCOUNT_DISABLED;
    SET res_code    = "RES_NUM_ACCOUNT_DISABLED";
    
    IF cur_account_status = ACCOUNT_STATUS_UNPAID_BILL THEN
        SET res_num     = RES_NUM_ACCOUNT_STATUS_UNPAID_BILL;
        SET res_code    = "RES_NUM_ACCOUNT_STATUS_UNPAID_BILL";
    
    END IF;
    
    LEAVE process_user;
END IF;


SELECT 

UPDATE account_request SET
    status              = ACC_REQ_STATUS_APPROVED,
    approved_by_user_id = in_approving_user_id,
    dt_approved         = CURRENT_TIMESTAMP
WHERE id = in_account_request_id;


/* Update approved user. */
UPDATE user SET
    account_id = cur_acc_req_account_id
WHERE id = cur_acc_req_requesting_user_id;



END process_user;


SELECT  
        a.status,
        b.username,
        b.name_last,
        b.name_first,
        a.dt_approved
INTO    
        cur_acc_req_status
        cur_approving_user_username,
        cur_approving_user_name_last,
        cur_approving_user_name_first,
        cur_acc_req_dt_approved
        
FROM    account_request a 
LEFT OUTER JOIN user b ON a.approved_by_user_id = b.id
WHERE   a.id = in_account_request_id;



SELECT
    flag,
    status,
    name
INTO 
    cur_account_flag,
    cur_account_status,
    cur_account_name
FROM account
WHERE id = in_account_id;

SELECT 
    res_num                             AS result_number,
    res_code                            AS result_code,
    res_desc                            AS result_desc,
    
    in_account_request_id               AS acc_req_id,
    cur_acc_req_status                  AS acc_req_status,
    cur_approving_user_username         AS approving_user_username,
    cur_approving_user_name_last        AS approving_user_name_last,
    cur_approving_user_name_first       AS approving_user_name_first,
    cur_acc_req_dt_approved             AS acc_req_dt_approved,
    
    cur_acc_req_requesting_user_id      AS requesting_user_id,
    cur_user_email                      AS requesting_user_email;


END $$

DELIMITER ;
