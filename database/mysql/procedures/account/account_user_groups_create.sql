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


/* This is read from a02_business_object table. */
DECLARE BUSINESS_OBJ_ID_USER                    INT             DEFAULT 1;
DECLARE BUSINESS_OBJ_ID_ACCOUNT                 INT             DEFAULT 2;
DECLARE BUSINESS_OBJ_ID_ACCOUNT_REQUEST         INT             DEFAULT 3;
DECLARE BUSINESS_OBJ_ID_USER_GROUP              INT             DEFAULT 4;

DECLARE BUSINESS_OBJ_ID_ACC_TRANSLATION         INT             DEFAULT 5;


DECLARE BUSINESS_OBJ_ID_PIG_FARM                INT             DEFAULT 6;
DECLARE BUSINESS_OBJ_ID_PIG_FARM_STAFF          INT             DEFAULT 7;
DECLARE BUSINESS_OBJ_ID_PIG_RACE                INT             DEFAULT 8;
DECLARE BUSINESS_OBJ_ID_PIG_RACE_LINE           INT             DEFAULT 9;


DECLARE BUSINESS_OBJ_ID_ACC_PIG_OPERATION       INT             DEFAULT 10;
/*reserver 11*/
/*reserver 12*/

DECLARE BUSINESS_OBJ_ID_SEMEN_SUPPLIER          INT             DEFAULT 13;
DECLARE BUSINESS_OBJ_ID_FEED_SUPPLIER           INT             DEFAULT 14;
DECLARE BUSINESS_OBJ_ID_FEED_BRAND              INT             DEFAULT 15;
DECLARE BUSINESS_OBJ_ID_FEED_TYPE               INT             DEFAULT 16;


DECLARE BUSINESS_OBJ_ID_SOW_BOAR                INT             DEFAULT 17;
DECLARE BUSINESS_OBJ_ID_SEMEN_SOURCE            INT             DEFAULT 18;
DECLARE BUSINESS_OBJ_ID_PIG_PRODUCTION          INT             DEFAULT 19;
DECLARE BUSINESS_OBJ_ID_PIG_PROD_AI             INT             DEFAULT 20;

DECLARE BUSINESS_OBJ_ID_PIG_PROD_FEED_BUY       INT             DEFAULT 21;
DECLARE BUSINESS_OBJ_ID_PIG_PROD_FEED_BAL       INT             DEFAULT 22;

DECLARE BUSINESS_OBJ_ID_PROD_GESTATING_OPS      INT             DEFAULT 23;

DECLARE BUSINESS_OBJ_ID_PROD_PIG_DEAD           INT             DEFAULT 26;
DECLARE BUSINESS_OBJ_ID_PROD_PIG_HARVEST        INT             DEFAULT 27;

DECLARE BUSINESS_OBJ_ID_PROD_NOTES              INT             DEFAULT 28;



/* Admin users can access all business objects, 2^31 -1*/
DECLARE FLAG_BUSINESS_OBJ_ADMIN                 BIGINT          DEFAULT 2147483647;
DECLARE FLAG_BUSINESS_OBJ_MANAGEMENT            INT             DEFAULT 0;
DECLARE FLAG_BUSINESS_OBJ_OPERATIONS            INT             DEFAULT 0;



DECLARE FLAG_BIT_OPERATION_ADD                  INT             DEFAULT 1;
DECLARE FLAG_BIT_OPERATION_UPDATE               INT             DEFAULT 2;
DECLARE FLAG_BIT_OPERATION_DELETE               INT             DEFAULT 4;


DECLARE OPERATION_ADD_UPDATE_DELETE             INT             DEFAULT 7;
DECLARE OPERATION_ADD_UPDATE_ONLY               INT             DEFAULT 3;

        

DECLARE cur_flag_business_obj_management        INT             DEFAULT 0;


SELECT SUM(a.flag_val)
INTO FLAG_BUSINESS_OBJ_MANAGEMENT
FROM (
    SELECT  POWER(2, bit_num) AS flag_val
    FROM    a02_business_object
    WHERE   id IN ( BUSINESS_OBJ_ID_USER,
                    BUSINESS_OBJ_ID_ACCOUNT_REQUEST,
                    
                    BUSINESS_OBJ_ID_ACC_TRANSLATION,
                                        
                    BUSINESS_OBJ_ID_PIG_FARM,
                    BUSINESS_OBJ_ID_PIG_FARM_STAFF,
                    BUSINESS_OBJ_ID_PIG_RACE,
                    BUSINESS_OBJ_ID_PIG_RACE_LINE, 
                    
                    BUSINESS_OBJ_ID_ACCOUNT_PIG_OPERATION,
                    BUSINESS_OBJ_ID_ACC_LACTATING_OPS,
                    
                    BUSINESS_OBJ_ID_SEMEN_SUPPLIER,
                    BUSINESS_OBJ_ID_FEED_SUPPLIER,
                    BUSINESS_OBJ_ID_FEED_BRAND,
                    BUSINESS_OBJ_ID_FEED_TYPE,
                    
                    BUSINESS_OBJ_ID_SOW_BOAR, 
                    BUSINESS_OBJ_ID_SEMEN_SOURCE,
                    BUSINESS_OBJ_ID_PIG_PRODUCTION,
                    BUSINESS_OBJ_ID_PIG_PROD_AI,
                    
                    BUSINESS_OBJ_ID_PIG_PROD_FEED_BUY,
                    BUSINESS_OBJ_ID_PIG_PROD_FEED_BAL,
                    
                    BUSINESS_OBJ_ID_PROD_GESTATING_OPS,
                    BUSINESS_OBJ_ID_PROD_LACTATING_OPS,
                    BUSINESS_OBJ_ID_PROD_PIG_DEAD,
                    BUSINESS_OBJ_ID_PROD_PIG_HARVEST,
                    
                    BUSINESS_OBJ_ID_PROD_NOTES
                    
                )
    ) a;
    
    
    
SELECT SUM(a.flag_val)
INTO FLAG_BUSINESS_OBJ_OPERATIONS
FROM (
    SELECT  POWER(2, bit_num) AS flag_val
    FROM    a02_business_object
    WHERE   id IN ( BUSINESS_OBJ_ID_SOW_BOAR,
                    BUSINESS_OBJ_ID_PIG_PRODUCTION,
                    BUSINESS_OBJ_ID_PIG_PROD_AI,
                    
                    BUSINESS_OBJ_ID_PIG_PROD_FEED_BAL,
                    
                    BUSINESS_OBJ_ID_PROD_GESTATING_OPS,
                    BUSINESS_OBJ_ID_PROD_LACTATING_OPS,
                    BUSINESS_OBJ_ID_PROD_PIG_DEAD,
                    BUSINESS_OBJ_ID_PROD_PIG_HARVEST,
                    
                    BUSINESS_OBJ_ID_PROD_NOTES
                )
    ) a;




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
    flag_priv_pig_farm_staff,
    flag_priv_pig_race,
    flag_priv_pig_race_line,
    
    flag_priv_acc_gestating_ops,
    flag_priv_acc_lactating_ops,
    
    flag_priv_semen_supplier,
    flag_priv_feed_supplier,
    flag_priv_feed_brand,
    flag_priv_feed_type,
    
    flag_priv_sow_boar,
    flag_priv_semen_source,
    flag_priv_pig_production,
    flag_priv_pig_prod_ai,
    
    flag_priv_pig_prod_feed_buy,
    flag_priv_pig_prod_feed_bal,
    
    flag_priv_prod_gestating_ops,
    flag_priv_prod_lactating_ops,
    flag_priv_prod_pig_dead,
    flag_priv_prod_pig_harvest,
    
    flag_priv_prod_notes

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
    flag_priv_pig_farm_staff,
    flag_priv_pig_race,
    flag_priv_pig_race_line,
    
    flag_priv_acc_gestating_ops,
    flag_priv_acc_lactating_ops,
    
    flag_priv_semen_supplier,
    flag_priv_feed_supplier,
    flag_priv_feed_brand,
    flag_priv_feed_type,
    
    flag_priv_sow_boar,
    flag_priv_semen_source,
    flag_priv_pig_production,
    flag_priv_pig_prod_ai,
    
    flag_priv_pig_prod_feed_buy,
    flag_priv_pig_prod_feed_bal,
    
    flag_priv_prod_gestating_ops,
    flag_priv_prod_lactating_ops,
    flag_priv_prod_pig_dead,
    flag_priv_prod_pig_harvest,
    
    flag_priv_prod_notes


) VALUES (
    in_account_id,
    ACCOUNT_USER_GROUP_MANAGEMENT,
    FLAG_BUSINESS_OBJ_MANAGEMENT,
    'Management',
    
    OPERATION_ADD_UPDATE_ONLY,
    0,
    OPERATION_ADD_UPDATE_DELETE,
    0,
    
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
    
    
    flag_priv_sow_boar,
    flag_priv_pig_production,
    
    flag_priv_pig_prod_feed_bal,
    
    flag_priv_prod_gestating_ops,
    flag_priv_prod_lactating_ops,
    flag_priv_prod_pig_dead,
    flag_priv_prod_pig_harvest,
    
    flag_priv_prod_notes
    
) VALUES (
    in_account_id,
    ACCOUNT_USER_GROUP_OPERATIONS,
    FLAG_BUSINESS_OBJ_OPERATIONS,
    'Operations',
    
   
    OPERATION_ADD_UPDATE_ONLY,
    OPERATION_ADD_UPDATE_ONLY,
    
    OPERATION_ADD_UPDATE_ONLY,
    
    OPERATION_ADD_UPDATE_ONLY,
    OPERATION_ADD_UPDATE_ONLY,
    OPERATION_ADD_UPDATE_ONLY,
    OPERATION_ADD_UPDATE_ONLY,
    
    OPERATION_ADD_UPDATE_ONLY
);





END $$

DELIMITER ;
