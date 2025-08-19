DELIMITER $$

DROP PROCEDURE IF EXISTS basic_user_check $$
CREATE PROCEDURE basic_user_check(
    in_user_id                  INT,
    in_user_must_have_account   INT,
    in_compare_to_account_id    INT,
    
    in_business_obj_to_access   INT, /* This must be a FLAG_BIT_BIZ value*/
    in_business_obj_operation   INT, /* This must be a FLAG_BIT_OPERATION value*/
    
    OUT out_user_account_id     INT,
    OUT out_user_group_id       INT,
    
    OUT res_num                 INT,
    OUT res_code                VARCHAR(80),
    OUT res_desc                VARCHAR(180)
)  

BEGIN

/** 
 * Will perform user flag checks, account checks and user group checks.
 * @author Jack Wong (j2718wong@gmail.com) 
 * @since August 18, 2025
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


DECLARE RES_NUM_USER_GROUP_HAS_NO_ACCESS        INT             DEFAULT 9;
 

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



/* user_group.flag_business_obj bits; new business objects add at the bottom*/
DECLARE FLAG_BIT_BIZ_OBJ_USER                   INT             DEFAULT 1;
DECLARE FLAG_BIT_BIZ_OBJ_ACCOUNT                INT             DEFAULT 2;
DECLARE FLAG_BIT_BIZ_OBJ_ACCOUNT_REQUEST        INT             DEFAULT 4;
DECLARE FLAG_BIT_BIZ_OBJ_USER_GROUP             INT             DEFAULT 8;

DECLARE FLAG_BIT_BIZ_OBJ_PIG_FARM               INT             DEFAULT 16;
DECLARE FLAG_BIT_BIZ_OBJ_SOW_BOAR               INT             DEFAULT 32;
DECLARE FLAG_BIT_BIZ_OBJ_SEMEN_SOURCE           INT             DEFAULT 64;
DECLARE FLAG_BIT_BIZ_OBJ_PIG_PROD               INT             DEFAULT 128;



DEFAULT FLAG_BIT_OPERATION_ADD                  INT             DEFAULT 1;
DEFAULT FLAG_BIT_OPERATION_UPDATE               INT             DEFAULT 2;
DEFAULT FLAG_BIT_OPERATION_DELETE               INT             DEFAULT 4;




DECLARE cur_user_flag                           INT             DEFAULT 0;


DECLARE cur_user_grp_flag_business_obj          INT             DEFAULT 0;
        
DECLARE cur_user_grp_flag_priv_user             INT             DEFAULT 0;
DECLARE cur_user_grp_flag_priv_account          INT             DEFAULT 0;
DECLARE cur_user_grp_flag_priv_account_request  INT             DEFAULT 0;
DECLARE cur_user_grp_flag_priv_user_group       INT             DEFAULT 0;
    
DECLARE cur_user_grp_flag_priv_pig_farm         INT             DEFAULT 0;
DECLARE cur_user_grp_flag_priv_sow_boar         INT             DEFAULT 0;
DECLARE cur_user_grp_flag_priv_semen_source     INT             DEFAULT 0;
DECLARE cur_user_grp_flag_priv_pig_prod         INT             DEFAULT 0;

DECLARE cur_account_flag                        INT             DEFAULT 0;
DECLARE cur_account_status_id                   INT             DEFAULT 0;



SET res_num     = RES_NUM_SUCCESS;
SET res_code    = "SUCCESS";


SELECT  
    a.flag,
    a.account_id,
    a.user_group_id,
    
    b.flag_business_obj,
    
    b.flag_priv_user,
    b.flag_priv_account,
    b.flag_priv_account_request,
    b.flag_priv_user_group,
    
    b.flag_priv_pig_farm,
    b.flag_priv_sow_boar,
    b.flag_priv_semen_source,
    b.flag_priv_pig_prod
        
INTO    
    cur_user_flag,
    out_user_account_id,
    out_user_group_id,
        
    cur_user_grp_flag_business_obj,
        
    cur_user_grp_flag_priv_user,
    cur_user_grp_flag_priv_account,
    cur_user_grp_flag_priv_account_request,
    cur_user_grp_flag_priv_user_group,
    
    cur_user_grp_flag_priv_pig_farm,
    cur_user_grp_flag_priv_sow_boar,
    cur_user_grp_flag_priv_semen_source,
    cur_user_grp_flag_priv_pig_prod
FROM  user a 
LEFT OUTER JOIN  user_group b ON  a.user_group_id = b.id
WHERE   a.id = in_user_id;


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


IF in_user_must_have_account = 0 THEN 
    LEAVE process_user;
END IF;


/* User must be associated to an account */


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


IF in_compare_to_account_id > 0 THEN 
    IF out_user_account_id != in_compare_to_account_id THEN 
        SET res_num     = RES_NUM_ACCOUNT_MISMATCH;
        SET res_code    = "RES_NUM_ACCOUNT_MISMATCH";

        LEAVE process_user;
    END IF;

END IF;


/* Check user.usergroup privileges. */


IF in_business_obj_to_access = FLAG_BIT_BIZ_OBJ_USER THEN 

    IF cur_user_grp_flag_business_obj & FLAG_BIT_BIZ_OBJ_USER =  0 THEN
        SET res_num     = RES_NUM_USER_GROUP_HAS_NO_ACCESS;
        SET res_code    = "RES_NUM_USER_GROUP_HAS_NO_ACCESS";

        LEAVE process_user;
    END IF;
    
    IF in_business_obj_operation = FLAG_BIT_OPERATION_ADD THEN 
        IF cur_user_grp_flag_priv_user & FLAG_BIT_OPERATION_ADD = 0 THEN 
            SET res_num     = RES_NUM_USER_GROUP_NO_ADD_PRIVILEGE;
            SET res_code    = "RES_NUM_USER_GROUP_NO_ADD_PRIVILEGE";
        
            LEAVE process_user;
        END IF;
    END IF;
    
    IF in_business_obj_operation = FLAG_BIT_OPERATION_UPDATE THEN 
        IF cur_user_grp_flag_priv_user & FLAG_BIT_OPERATION_UPDATE = 0 THEN 
            SET res_num     = RES_NUM_USER_GROUP_NO_UPDATE_PRIVILEGE;
            SET res_code    = "RES_NUM_USER_GROUP_NO_UPDATE_PRIVILEGE";
        
            LEAVE process_user;
        END IF;
    END IF;
    
    IF in_business_obj_operation = FLAG_BIT_OPERATION_DELETE THEN 
        IF cur_user_grp_flag_priv_user & FLAG_BIT_OPERATION_DELETE = 0 THEN 
            SET res_num     = RES_NUM_USER_GROUP_NO_DELETE_PRIVILEGE;
            SET res_code    = "RES_NUM_USER_GROUP_NO_DELETE_PRIVILEGE";
        
            LEAVE process_user;
        END IF;
    END IF;
    
END IF;


IF in_business_obj_to_access = FLAG_BIT_BIZ_OBJ_ACCOUNT THEN 

    IF cur_user_grp_flag_business_obj & FLAG_BIT_BIZ_OBJ_ACCOUNT =  0 THEN
        SET res_num     = RES_NUM_USER_GROUP_HAS_NO_ACCESS;
        SET res_code    = "RES_NUM_USER_GROUP_HAS_NO_ACCESS";

        LEAVE process_user;
    END IF;
    
    IF in_business_obj_operation = FLAG_BIT_OPERATION_ADD THEN 
        IF cur_user_grp_flag_priv_account & FLAG_BIT_OPERATION_ADD = 0 THEN 
            SET res_num     = RES_NUM_USER_GROUP_NO_ADD_PRIVILEGE;
            SET res_code    = "RES_NUM_USER_GROUP_NO_ADD_PRIVILEGE";
        
            LEAVE process_user;
        END IF;
    END IF;
    
    IF in_business_obj_operation = FLAG_BIT_OPERATION_UPDATE THEN 
        IF cur_user_grp_flag_priv_account & FLAG_BIT_OPERATION_UPDATE = 0 THEN 
            SET res_num     = RES_NUM_USER_GROUP_NO_UPDATE_PRIVILEGE;
            SET res_code    = "RES_NUM_USER_GROUP_NO_UPDATE_PRIVILEGE";
        
            LEAVE process_user;
        END IF;
    END IF;
    
    IF in_business_obj_operation = FLAG_BIT_OPERATION_DELETE THEN 
        IF cur_user_grp_flag_priv_account & FLAG_BIT_OPERATION_DELETE = 0 THEN 
            SET res_num     = RES_NUM_USER_GROUP_NO_DELETE_PRIVILEGE;
            SET res_code    = "RES_NUM_USER_GROUP_NO_DELETE_PRIVILEGE";
        
            LEAVE process_user;
        END IF;
    END IF;
    
END IF;


IF in_business_obj_to_access = FLAG_BIT_BIZ_OBJ_ACCOUNT_REQUEST THEN 

    IF cur_user_grp_flag_business_obj & FLAG_BIT_BIZ_OBJ_ACCOUNT_REQUEST =  0 THEN
        SET res_num     = RES_NUM_USER_GROUP_HAS_NO_ACCESS;
        SET res_code    = "RES_NUM_USER_GROUP_HAS_NO_ACCESS";

        LEAVE process_user;
    END IF;
    
    IF in_business_obj_operation = FLAG_BIT_OPERATION_ADD THEN 
        IF cur_user_grp_flag_priv_account_request & FLAG_BIT_OPERATION_ADD = 0 THEN 
            SET res_num     = RES_NUM_USER_GROUP_NO_ADD_PRIVILEGE;
            SET res_code    = "RES_NUM_USER_GROUP_NO_ADD_PRIVILEGE";
        
            LEAVE process_user;
        END IF;
    END IF;
    
    IF in_business_obj_operation = FLAG_BIT_OPERATION_UPDATE THEN 
        IF cur_user_grp_flag_priv_account_request & FLAG_BIT_OPERATION_UPDATE = 0 THEN 
            SET res_num     = RES_NUM_USER_GROUP_NO_UPDATE_PRIVILEGE;
            SET res_code    = "RES_NUM_USER_GROUP_NO_UPDATE_PRIVILEGE";
        
            LEAVE process_user;
        END IF;
    END IF;
    
    IF in_business_obj_operation = FLAG_BIT_OPERATION_DELETE THEN 
        IF cur_user_grp_flag_priv_account_request & FLAG_BIT_OPERATION_DELETE = 0 THEN 
            SET res_num     = RES_NUM_USER_GROUP_NO_DELETE_PRIVILEGE;
            SET res_code    = "RES_NUM_USER_GROUP_NO_DELETE_PRIVILEGE";
        
            LEAVE process_user;
        END IF;
    END IF;
    
END IF;


IF in_business_obj_to_access = FLAG_BIT_BIZ_OBJ_USER_GROUP THEN 

    IF cur_user_grp_flag_business_obj & FLAG_BIT_BIZ_OBJ_USER_GROUP =  0 THEN
        SET res_num     = RES_NUM_USER_GROUP_HAS_NO_ACCESS;
        SET res_code    = "RES_NUM_USER_GROUP_HAS_NO_ACCESS";

        LEAVE process_user;
    END IF;
    
    IF in_business_obj_operation = FLAG_BIT_OPERATION_ADD THEN 
        IF cur_user_grp_flag_priv_user_group & FLAG_BIT_OPERATION_ADD = 0 THEN 
            SET res_num     = RES_NUM_USER_GROUP_NO_ADD_PRIVILEGE;
            SET res_code    = "RES_NUM_USER_GROUP_NO_ADD_PRIVILEGE";
        
            LEAVE process_user;
        END IF;
    END IF;
    
    IF in_business_obj_operation = FLAG_BIT_OPERATION_UPDATE THEN 
        IF cur_user_grp_flag_priv_user_group & FLAG_BIT_OPERATION_UPDATE = 0 THEN 
            SET res_num     = RES_NUM_USER_GROUP_NO_UPDATE_PRIVILEGE;
            SET res_code    = "RES_NUM_USER_GROUP_NO_UPDATE_PRIVILEGE";
        
            LEAVE process_user;
        END IF;
    END IF;
    
    IF in_business_obj_operation = FLAG_BIT_OPERATION_DELETE THEN 
        IF cur_user_grp_flag_priv_user_group & FLAG_BIT_OPERATION_DELETE = 0 THEN 
            SET res_num     = RES_NUM_USER_GROUP_NO_DELETE_PRIVILEGE;
            SET res_code    = "RES_NUM_USER_GROUP_NO_DELETE_PRIVILEGE";
        
            LEAVE process_user;
        END IF;
    END IF;
    
END IF;


IF in_business_obj_to_access = FLAG_BIT_BIZ_OBJ_PIG_FARM THEN 

    IF cur_user_grp_flag_business_obj & FLAG_BIT_BIZ_OBJ_PIG_FARM =  0 THEN
        SET res_num     = RES_NUM_USER_GROUP_HAS_NO_ACCESS;
        SET res_code    = "RES_NUM_USER_GROUP_HAS_NO_ACCESS";

        LEAVE process_user;
    END IF;
    
    IF in_business_obj_operation = FLAG_BIT_OPERATION_ADD THEN 
        IF cur_user_grp_flag_priv_pig_farm & FLAG_BIT_OPERATION_ADD = 0 THEN 
            SET res_num     = RES_NUM_USER_GROUP_NO_ADD_PRIVILEGE;
            SET res_code    = "RES_NUM_USER_GROUP_NO_ADD_PRIVILEGE";
        
            LEAVE process_user;
        END IF;
    END IF;
    
    IF in_business_obj_operation = FLAG_BIT_OPERATION_UPDATE THEN 
        IF cur_user_grp_flag_priv_pig_farm & FLAG_BIT_OPERATION_UPDATE = 0 THEN 
            SET res_num     = RES_NUM_USER_GROUP_NO_UPDATE_PRIVILEGE;
            SET res_code    = "RES_NUM_USER_GROUP_NO_UPDATE_PRIVILEGE";
        
            LEAVE process_user;
        END IF;
    END IF;
    
    IF in_business_obj_operation = FLAG_BIT_OPERATION_DELETE THEN 
        IF cur_user_grp_flag_priv_pig_farm & FLAG_BIT_OPERATION_DELETE = 0 THEN 
            SET res_num     = RES_NUM_USER_GROUP_NO_DELETE_PRIVILEGE;
            SET res_code    = "RES_NUM_USER_GROUP_NO_DELETE_PRIVILEGE";
        
            LEAVE process_user;
        END IF;
    END IF;
    
END IF;


IF in_business_obj_to_access = FLAG_BIT_BIZ_OBJ_SOW_BOAR THEN 

    IF cur_user_grp_flag_business_obj & FLAG_BIT_BIZ_OBJ_SOW_BOAR =  0 THEN
        SET res_num     = RES_NUM_USER_GROUP_HAS_NO_ACCESS;
        SET res_code    = "RES_NUM_USER_GROUP_HAS_NO_ACCESS";

        LEAVE process_user;
    END IF;
    
    IF in_business_obj_operation = FLAG_BIT_OPERATION_ADD THEN 
        IF cur_user_grp_flag_priv_sow_boar & FLAG_BIT_OPERATION_ADD = 0 THEN 
            SET res_num     = RES_NUM_USER_GROUP_NO_ADD_PRIVILEGE;
            SET res_code    = "RES_NUM_USER_GROUP_NO_ADD_PRIVILEGE";
        
            LEAVE process_user;
        END IF;
    END IF;
    
    IF in_business_obj_operation = FLAG_BIT_OPERATION_UPDATE THEN 
        IF cur_user_grp_flag_priv_sow_boar & FLAG_BIT_OPERATION_UPDATE = 0 THEN 
            SET res_num     = RES_NUM_USER_GROUP_NO_UPDATE_PRIVILEGE;
            SET res_code    = "RES_NUM_USER_GROUP_NO_UPDATE_PRIVILEGE";
        
            LEAVE process_user;
        END IF;
    END IF;
    
    IF in_business_obj_operation = FLAG_BIT_OPERATION_DELETE THEN 
        IF cur_user_grp_flag_priv_sow_boar & FLAG_BIT_OPERATION_DELETE = 0 THEN 
            SET res_num     = RES_NUM_USER_GROUP_NO_DELETE_PRIVILEGE;
            SET res_code    = "RES_NUM_USER_GROUP_NO_DELETE_PRIVILEGE";
        
            LEAVE process_user;
        END IF;
    END IF;
    
END IF;


IF in_business_obj_to_access = FLAG_BIT_BIZ_OBJ_SEMEN_SOURCE THEN 

    IF cur_user_grp_flag_business_obj & FLAG_BIT_BIZ_OBJ_SEMEN_SOURCE =  0 THEN
        SET res_num     = RES_NUM_USER_GROUP_HAS_NO_ACCESS;
        SET res_code    = "RES_NUM_USER_GROUP_HAS_NO_ACCESS";

        LEAVE process_user;
    END IF;
    
    IF in_business_obj_operation = FLAG_BIT_OPERATION_ADD THEN 
        IF cur_user_grp_flag_priv_semen_source & FLAG_BIT_OPERATION_ADD = 0 THEN 
            SET res_num     = RES_NUM_USER_GROUP_NO_ADD_PRIVILEGE;
            SET res_code    = "RES_NUM_USER_GROUP_NO_ADD_PRIVILEGE";
        
            LEAVE process_user;
        END IF;
    END IF;
    
    IF in_business_obj_operation = FLAG_BIT_OPERATION_UPDATE THEN 
        IF cur_user_grp_flag_priv_semen_source & FLAG_BIT_OPERATION_UPDATE = 0 THEN 
            SET res_num     = RES_NUM_USER_GROUP_NO_UPDATE_PRIVILEGE;
            SET res_code    = "RES_NUM_USER_GROUP_NO_UPDATE_PRIVILEGE";
        
            LEAVE process_user;
        END IF;
    END IF;
    
    IF in_business_obj_operation = FLAG_BIT_OPERATION_DELETE THEN 
        IF cur_user_grp_flag_priv_semen_source & FLAG_BIT_OPERATION_DELETE = 0 THEN 
            SET res_num     = RES_NUM_USER_GROUP_NO_DELETE_PRIVILEGE;
            SET res_code    = "RES_NUM_USER_GROUP_NO_DELETE_PRIVILEGE";
        
            LEAVE process_user;
        END IF;
    END IF;
    
END IF;


IF in_business_obj_to_access = FLAG_BIT_BIZ_OBJ_PIG_PROD THEN 

    IF cur_user_grp_flag_business_obj & FLAG_BIT_BIZ_OBJ_PIG_PROD =  0 THEN
        SET res_num     = RES_NUM_USER_GROUP_HAS_NO_ACCESS;
        SET res_code    = "RES_NUM_USER_GROUP_HAS_NO_ACCESS";

        LEAVE process_user;
    END IF;
    
    IF in_business_obj_operation = FLAG_BIT_OPERATION_ADD THEN 
        IF cur_user_grp_flag_priv_pig_prod & FLAG_BIT_OPERATION_ADD = 0 THEN 
            SET res_num     = RES_NUM_USER_GROUP_NO_ADD_PRIVILEGE;
            SET res_code    = "RES_NUM_USER_GROUP_NO_ADD_PRIVILEGE";
        
            LEAVE process_user;
        END IF;
    END IF;
    
    IF in_business_obj_operation = FLAG_BIT_OPERATION_UPDATE THEN 
        IF cur_user_grp_flag_priv_pig_prod & FLAG_BIT_OPERATION_UPDATE = 0 THEN 
            SET res_num     = RES_NUM_USER_GROUP_NO_UPDATE_PRIVILEGE;
            SET res_code    = "RES_NUM_USER_GROUP_NO_UPDATE_PRIVILEGE";
        
            LEAVE process_user;
        END IF;
    END IF;
    
    IF in_business_obj_operation = FLAG_BIT_OPERATION_DELETE THEN 
        IF cur_user_grp_flag_priv_pig_prod & FLAG_BIT_OPERATION_DELETE = 0 THEN 
            SET res_num     = RES_NUM_USER_GROUP_NO_DELETE_PRIVILEGE;
            SET res_code    = "RES_NUM_USER_GROUP_NO_DELETE_PRIVILEGE";
        
            LEAVE process_user;
        END IF;
    END IF;
    
END IF;



END process_user;





END $$

DELIMITER ;
