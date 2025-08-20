DELIMITER $$

DROP PROCEDURE IF EXISTS account_gestating_ops_update $$
CREATE PROCEDURE account_gestating_ops_update(
    in_user_id                  INT,
    
    in_acc_gestating_ops_id     INT,
    in_num_days_since_insem     INT,
    
    in_name                     VARCHAR(50),
    in_description              VARCHAR(160)
    
)

BEGIN

/** 
 * Will update account
 * @author Jack Wong
 * @since August 10, 2025
 *
 */
 
DECLARE RES_NUM_SUCCESS                         INT             DEFAULT 0;


DECLARE FLAG_BIT_BIZ_OBJ_ACC_GESTATING_OPS      INT             DEFAULT 256;

DECLARE AUDIT_ACTION_ADD                        VARCHAR(3)      DEFAULT "ADD";
DECLARE AUDIT_ACTION_UPDATE                     VARCHAR(3)      DEFAULT "UPD";
DECLARE AUDIT_ACTION_DELETE                     VARCHAR(3)      DEFAULT "DEL";


DECLARE cur_user_flag                           INT             DEFAULT 0;
DECLARE cur_user_account_id                     INT             DEFAULT 0;




DECLARE res_num                                 INT             DEFAULT 0;
DECLARE res_code                                VARCHAR(80)     DEFAULT '';
DECLARE res_desc                                VARCHAR(180)    DEFAULT '';



SET res_num     = RES_NUM_SUCCESS;
SET res_code    = "SUCCESS";


SELECT  account_id
INTO    cur_acc_gestating_ops_account_id
FROM    account_gestating_ops
WHERE   id = in_acc_gestating_ops_id
LIMIT   1;


CALL basic_user_check(
    in_user_id, 
    1, 
    cur_acc_gestating_ops_account_id,
    
    FLAG_BIT_BIZ_OBJ_ACC_GESTATING_OPS,
    FLAG_BIT_OPERATION_UPDATE,
    
    cur_user_account_id, 
    cur_user_group_id,
    res_num, 
    res_code, 
    res_desc);


process_user : BEGIN


UPDATE acc_gestating_ops SET
    num_days_since_insem = in_num_days_since_insem,
    
    name                = in_name,
    description         = in_description,
    
    last_update_user_id = in_user_id,
    dt_last_update      = CURRENT_TIMESTAMP
    
WHERE id =  in_acc_gestating_ops_id;

END process_user;


SELECT
    flag,
    name
INTO 
    cur_acc_gestating_ops_flag,
    cur_acc_gestating_ops_name
FROM acc_gestating_ops
WHERE id = in_acc_gestating_ops_id;

SELECT 
    res_num                             AS result_number,
    res_code                            AS result_code,
    res_desc                            AS result_desc,
    
    in_acc_gestating_ops_id             AS acc_gestating_ops_id,
    cur_acc_gestating_ops_flag          AS acc_gestating_ops_flag,
    cur_acc_gestating_ops_name          AS acc_gestating_ops_name;
    


END $$

DELIMITER ;
