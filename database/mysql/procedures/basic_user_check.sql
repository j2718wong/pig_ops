DELIMITER $$

DROP PROCEDURE IF EXISTS basic_user_check $$
CREATE PROCEDURE basic_user_check(
    in_user_id                  INT,
    in_user_must_be_admin       INT,
    in_check_account_id         INT,
    
    OUT out_user_account_id     INT,
    OUT out_user_group_id       INT,
    
    OUT res_num                 INT,
    OUT res_code                VARCHAR(80),
    OUT res_desc                VARCHAR(180)
)  

BEGIN

/** 
 * 
 * @author Jack Wong (j2718wong@gmail.com) 
 * @since January 5, 2025
 *
 */

DECLARE RES_NUM_SUCCESS                         INT             DEFAULT 0;

DECLARE RES_NUM_USER_IS_INACTIVE                INT             DEFAULT 1;
DECLARE RES_NUM_USER_NOT_EMAIL_VERIFIED         INT             DEFAULT 2;
DECLARE RES_NUM_USER_NOT_ACCOUNT_ADMIN          INT             DEFAULT 3;
DECLARE RES_NUM_USER_NO_ACCOUNT_SET             INT             DEFAULT 4;
DECLARE RES_NUM_USER_NO_USER_GROUP_SET          INT             DEFAULT 5;


DECLARE RES_NUM_ACCOUNT_DISABLED                INT             DEFAULT 6;
DECLARE RES_NUM_ACCOUNT_STATUS_TRIAL_EXPIRED    INT             DEFAULT 7;
DECLARE RES_NUM_ACCOUNT_MISMATCH                INT             DEFAULT 8;



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


DECLARE cur_account_flag                        INT             DEFAULT 0;
DECLARE cur_account_status_id                   INT             DEFAULT 0;



SET res_num     = RES_NUM_SUCCESS;
SET res_code    = "SUCCESS";


SELECT  
        flag,
        account_id,
        user_group_id
INTO    
        cur_user_flag,
        out_user_account_id,
        out_user_group_id
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


IF in_user_must_be_admin > 0 THEN 
    IF cur_user_flag & FLAG_BIT_USER_IS_ACCOUNT_ADMIN = 0 THEN 
        SET res_num     = RES_NUM_USER_NOT_ACCOUNT_ADMIN;
        SET res_code    = "RES_NUM_USER_NOT_ACCOUNT_ADMIN";

        LEAVE process_user;
    END IF;
END IF;


IF out_user_account_id = 0 THEN 
    SET res_num     = RES_NUM_USER_NO_ACCOUNT_SET;
    SET res_code    = "RES_NUM_USER_NO_ACCOUNT_SET";

    LEAVE process_user;
END IF;


IF out_user_group_id = 0 THEN 
    SET res_num     = RES_NUM_USER_NO_USER_GROUP_SET;
    SET res_code    = "RES_NUM_USER_NO_USER_GROUP_SET";

    LEAVE process_user;
END IF;




/* Check account*/
SELECT 
    flag,
    status_id
INTO
    cur_account_flag,
    cur_account_status_id
    
FROM account
WHERE id = out_user_account_id;



IF cur_account_flag & FLAG_BIT_ACCOUNT_ENABLE = 0 THEN 
    SET res_num     = RES_NUM_ACCOUNT_DISABLED;
    SET res_code    = "RES_NUM_ACCOUNT_DISABLED";
    
    IF cur_account_status_id = ACCOUNT_STATUS_ID_UNPAID_BILL THEN
        SET res_num     = RES_NUM_ACCOUNT_STATUS_UNPAID_BILL;
        SET res_code    = "RES_NUM_ACCOUNT_STATUS_UNPAID_BILL";
    
    END IF;
    
    LEAVE process_user;
END IF;


IF in_check_account_id > 0 THEN 
    IF out_user_account_id != in_check_account_id THEN 
        SET res_num     = RES_NUM_ACCOUNT_MISMATCH;
        SET res_code    = "RES_NUM_ACCOUNT_MISMATCH";

        LEAVE process_user;
    END IF;

END IF;


END process_user;





END $$

DELIMITER ;
