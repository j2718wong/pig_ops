DELIMITER $$

DROP PROCEDURE IF EXISTS account_user_groups_create $$
CREATE PROCEDURE account_user_groups_create(
    in_account_id               INT
)  

BEGIN

/** 
 * 
 * @author Jack Wong (j2718wong@gmail.com) 
 * @since August 19, 2025
 *
 */


DECLARE ACCOUNT_USER_GROUP_ADMIN                INT             DEFAULT 1;
DECLARE ACCOUNT_USER_GROUP_MANAGEMENT           INT             DEFAULT 2;
DECLARE ACCOUNT_USER_GROUP_OPERATIONS           INT             DEFAULT 3;
DECLARE ACCOUNT_USER_GROUP_FARM_STAFF           INT             DEFAULT 4;


/* user_group.flag_business_obj bits; new business objects add at the bottom*/
DECLARE FLAG_BIT_BIZ_OBJ_USER                   INT             DEFAULT 1;
DECLARE FLAG_BIT_BIZ_OBJ_ACCOUNT                INT             DEFAULT 2;
DECLARE FLAG_BIT_BIZ_OBJ_ACCOUNT_REQUEST        INT             DEFAULT 4;
DECLARE FLAG_BIT_BIZ_OBJ_USER_GROUP             INT             DEFAULT 8;

DECLARE FLAG_BIT_BIZ_OBJ_PIG_FARM               INT             DEFAULT 16;
DECLARE FLAG_BIT_BIZ_OBJ_ACC_GESTATING_OPS      INT             DEFAULT 32;
DECLARE FLAG_BIT_BIZ_OBJ_PIG_RACE               INT             DEFAULT 64;
DECLARE FLAG_BIT_BIZ_OBJ_PIG_RACE_LINE          INT             DEFAULT 128;

DECLARE FLAG_BIT_BIZ_OBJ_SEMEN_SUPPLIER         INT             DEFAULT 256;
DECLARE FLAG_BIT_BIZ_OBJ_FEED_SUPPLIER          INT             DEFAULT 512;
DECLARE FLAG_BIT_BIZ_OBJ_FEED_BRAND             INT             DEFAULT 1024;

DECLARE FLAG_BIT_BIZ_OBJ_SOW_BOAR               INT             DEFAULT 2048;
DECLARE FLAG_BIT_BIZ_OBJ_SEMEN_SOURCE           INT             DEFAULT 4096;
DECLARE FLAG_BIT_BIZ_OBJ_PIG_PROD               INT             DEFAULT 8192;
DECLARE FLAG_BIT_BIZ_OBJ_PIG_PROD_AI            INT             DEFAULT 16384;

DECLARE FLAG_BIT_BIZ_OBJ_PROD_FEED_BUY          INT             DEFAULT 32768;
DECLARE FLAG_BIT_BIZ_OBJ_PROD_FEED_BAL          INT             DEFAULT 65536;

DECLARE FLAG_BIT_BIZ_OBJ_PROD_GESTATING_OPS     INT             DEFAULT 131072;



/* Admin users can access all business objects, 2^31 -1*/
DECLARE FLAG_BUSINESS_OBJ_ADMIN                 BIGINT          DEFAULT 2147483647;
DECLARE FLAG_BUSINESS_OBJ_MANAGEMENT            INT             DEFAULT 0;
DECLARE FLAG_BUSINESS_OBJ_OPERATIONS            INT             DEFAULT 0;
DECLARE FLAG_BUSINESS_OBJ_FARM_STAFF            INT             DEFAULT 0;



DECLARE FLAG_BIT_OPERATION_ADD                  INT             DEFAULT 1;
DECLARE FLAG_BIT_OPERATION_UPDATE               INT             DEFAULT 2;
DECLARE FLAG_BIT_OPERATION_DELETE               INT             DEFAULT 4;


DECLARE OPERATION_ADD_UPDATE_DELETE             INT             DEFAULT 7;
DECLARE OPERATION_ADD_UPDATE_ONLY               INT             DEFAULT 3;



SET FLAG_BUSINESS_OBJ_MANAGEMENT =  FLAG_BIT_BIZ_OBJ_USER +
                                    FLAG_BIT_BIZ_OBJ_ACCOUNT_REQUEST +
                                    
                                    FLAG_BIT_BIZ_OBJ_PIG_FARM +
                                    FLAG_BIT_BIZ_OBJ_ACC_GESTATING_OPS +
                                    FLAG_BIT_BIZ_OBJ_PIG_RACE +
                                    FLAG_BIT_BIZ_OBJ_PIG_RACE_LINE + 
                                    
                                    FLAG_BIT_BIZ_OBJ_SEMEN_SUPPLIER +
                                    FLAG_BIT_BIZ_OBJ_FEED_SUPPLIER +
                                    FLAG_BIT_BIZ_OBJ_FEED_BRAND +
                                    
                                    FLAG_BIT_BIZ_OBJ_SOW_BOAR + 
                                    FLAG_BIT_BIZ_OBJ_SEMEN_SOURCE +
                                    FLAG_BIT_BIZ_OBJ_PIG_PROD +
                                    
                                    FLAG_BIT_BIZ_OBJ_PROD_GESTATING_OPS;


SET FLAG_BUSINESS_OBJ_OPERATIONS =  FLAG_BIT_BIZ_OBJ_SOW_BOAR + 
                                    FLAG_BIT_BIZ_OBJ_SEMEN_SOURCE +
                                    FLAG_BIT_BIZ_OBJ_PIG_PROD + 
                                    
                                    FLAG_BIT_BIZ_OBJ_PIG_PROD_AI;


SET FLAG_BUSINESS_OBJ_FARM_STAFF =  FLAG_BIT_BIZ_OBJ_SOW_BOAR + 
                                    FLAG_BIT_BIZ_OBJ_SEMEN_SOURCE +
                                    FLAG_BIT_BIZ_OBJ_PIG_PROD +
                                    
                                    FLAG_BIT_BIZ_OBJ_PIG_PROD_AI +
                                    
                                    FLAG_BIT_BIZ_OBJ_PROD_GESTATING_OPS;


/* Create account default user_groups. Each account will have a fix 
number of user groups*/
INSERT INTO user_group(
    account_id,
    group_num,
    flag_business_obj,
    name,
    
    flag_priv_user,
    flag_priv_account,
    flag_priv_account_request,
    flag_priv_user_group,
    
    flag_priv_pig_farm,
    flag_priv_account_gestating_ops,
    flag_priv_pig_race,
    flag_priv_pig_race_line,
    
    flag_priv_semen_supplier,
    flag_priv_feed_supplier,
    flag_priv_feed_brand,
    
    flag_priv_sow_boar,
    flag_priv_semen_source,
    flag_priv_pig_prod,    
    flag_priv_prod_gestating_ops

) VALUES (
    in_account_id,
    ACCOUNT_USER_GROUP_ADMIN,
    FLAG_BUSINESS_OBJ_ADMIN,
    'Admin',
    
    OPERATION_ADD_UPDATE_DELETE,
    OPERATION_ADD_UPDATE_DELETE,
    OPERATION_ADD_UPDATE_DELETE,
    OPERATION_ADD_UPDATE_DELETE,
    
    OPERATION_ADD_UPDATE_DELETE,
    OPERATION_ADD_UPDATE_DELETE,
    OPERATION_ADD_UPDATE_DELETE,
    OPERATION_ADD_UPDATE_DELETE,
    
    OPERATION_ADD_UPDATE_DELETE,
    OPERATION_ADD_UPDATE_DELETE,
    OPERATION_ADD_UPDATE_DELETE,
    
    OPERATION_ADD_UPDATE_DELETE,
    OPERATION_ADD_UPDATE_DELETE,
    OPERATION_ADD_UPDATE_DELETE,
    OPERATION_ADD_UPDATE_DELETE
);


INSERT INTO user_group(
    account_id,
    group_num,
    flag_business_obj,
    name,
    
    flag_priv_user,
    flag_priv_account,
    flag_priv_account_request,
    flag_priv_user_group,
    
    flag_priv_pig_farm,
    flag_priv_account_gestating_ops,
    flag_priv_pig_race,
    flag_priv_pig_race_line,
    
    flag_priv_semen_supplier,
    flag_priv_feed_supplier,
    flag_priv_feed_brand,
    
    flag_priv_sow_boar,
    flag_priv_semen_source,
    flag_priv_pig_prod,    
    flag_priv_prod_gestating_ops
    
) VALUES (
    in_account_id,
    ACCOUNT_USER_GROUP_MANAGEMENT,
    FLAG_BUSINESS_OBJ_MANAGEMENT,
    'Management',
    
    OPERATION_ADD_UPDATE_ONLY,
    0,
    OPERATION_ADD_UPDATE_DELETE,
    0,
    
    OPERATION_ADD_UPDATE_ONLY,
    OPERATION_ADD_UPDATE_DELETE,
    OPERATION_ADD_UPDATE_DELETE,
    OPERATION_ADD_UPDATE_DELETE,

    OPERATION_ADD_UPDATE_DELETE,
    OPERATION_ADD_UPDATE_DELETE,
    OPERATION_ADD_UPDATE_DELETE,
    
    OPERATION_ADD_UPDATE_DELETE,
    OPERATION_ADD_UPDATE_DELETE,
    OPERATION_ADD_UPDATE_DELETE,
    
    OPERATION_ADD_UPDATE_DELETE,
    OPERATION_ADD_UPDATE_DELETE,
    OPERATION_ADD_UPDATE_DELETE,
    OPERATION_ADD_UPDATE_DELETE
    
    
    
);


INSERT INTO user_group(
    account_id,
    group_num,
    flag_business_obj,
    name,
    
    flag_priv_user,
    flag_priv_account,
    flag_priv_account_request,
    flag_priv_user_group,
    
    flag_priv_pig_farm,
    flag_priv_sow_boar,
    flag_priv_semen_source,
    flag_priv_pig_prod,
    
    flag_priv_account_gestating_ops
    
) VALUES (
    in_account_id,
    ACCOUNT_USER_GROUP_OPERATIONS,
    FLAG_BUSINESS_OBJ_OPERATIONS,
    'Operations',
    
    0,
    0,
    0,
    0,
    
    0,
    OPERATION_ADD_UPDATE_ONLY,
    OPERATION_ADD_UPDATE_ONLY,
    OPERATION_ADD_UPDATE_ONLY,
    
    0
);


INSERT INTO user_group(
    account_id,
    group_num,
    flag_business_obj,
    name,
    
    flag_priv_user,
    flag_priv_account,
    flag_priv_account_request,
    flag_priv_user_group,
    
    flag_priv_pig_farm,
    flag_priv_sow_boar,
    flag_priv_semen_source,
    flag_priv_pig_prod,
    
    flag_priv_account_gestating_ops
    
) VALUES (
    in_account_id,
    ACCOUNT_USER_GROUP_FARM_STAFF,
    FLAG_BUSINESS_OBJ_FARM_STAFF,
    'Farm Staff',
    
    0,
    0,
    0,
    0,
    
    0,
    OPERATION_ADD_UPDATE_ONLY,
    OPERATION_ADD_UPDATE_ONLY,
    OPERATION_ADD_UPDATE_ONLY,
    
    0
);





END $$

DELIMITER ;
