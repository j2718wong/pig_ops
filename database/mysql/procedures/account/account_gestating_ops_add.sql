DELIMITER $$

DROP PROCEDURE IF EXISTS account_gestating_ops_add $$
CREATE PROCEDURE account_gestating_ops_add(
    in_user_id              INT,

    in_num_days_since_insem INT,
    
    in_name                 VARCHAR(50),
    in_description          VARCHAR(160)
)  

BEGIN

/** 
 * Will add account_gestating_ops entry.
 * 
 * @author Jack Wong (j2718wong@gmail.com) 
 * @since August 15, 2025
 *
 */

DECLARE RES_NUM_SUCCESS                         INT             DEFAULT 0;


DECLARE RES_NUM_DUPLICATE_ENTRY                 INT             DEFAULT 20;



DECLARE FLAG_BIT_BIZ_OBJ_ACC_GESTATING_OPS      INT             DEFAULT 256;

DECLARE FLAG_BIT_OPERATION_ADD                  INT             DEFAULT 1;
DECLARE FLAG_BIT_OPERATION_UPDATE               INT             DEFAULT 2;
DECLARE FLAG_BIT_OPERATION_DELETE               INT             DEFAULT 4;


DECLARE cur_user_account_id                     INT             DEFAULT 0;
DECLARE cur_user_group_id                       INT             DEFAULT 0;


DECLARE cur_acc_gestating_ops_id                INT             DEFAULT 0;
DECLARE cur_acc_gestating_ops_flag              INT             DEFAULT 0;
DECLARE cur_acc_gestating_ops_name              VARCHAR(50)     DEFAULT '';



DECLARE res_num                                 INT             DEFAULT 0;
DECLARE res_code                                VARCHAR(80)     DEFAULT '';
DECLARE res_desc                                VARCHAR(180)    DEFAULT '';


SET res_num     = RES_NUM_SUCCESS;
SET res_code    = "SUCCESS";


CALL basic_user_check(
    in_user_id, 
    1, /* user must have an account*/
    0,
    
    FLAG_BIT_BIZ_OBJ_ACC_GESTATING_OPS,
    FLAG_BIT_OPERATION_ADD,
    
    cur_user_account_id, 
    cur_user_group_id,
    res_num, 
    res_code, 
    res_desc);


process_user : BEGIN

IF res_num != RES_NUM_SUCCESS THEN 
    LEAVE process_user;
END IF;


/* Check for duplicate entry */
SELECT  id
INTO    cur_acc_gestating_ops_id
FROM    account_gestating_ops
WHERE   account_id  = cur_user_account_id   AND 
        UPPER(name) = UPPER(in_name)
LIMIT   1;

IF cur_acc_gestating_ops_id > 0 THEN 
    SET res_num     = RES_NUM_DUPLICATE_ENTRY;
    SET res_code    = "RES_NUM_DUPLICATE_ENTRY";
    
    LEAVE process_user;
END IF;



INSERT INTO account_gestating_ops(
    account_id,
    num_days_since_insem,
    
    name,
    description
) VALUES (
    cur_user_account_id,
    in_num_days_since_insem,
    
    in_name,
    in_description    
);

SELECT LAST_INSERT_ID() INTO cur_acc_gestating_ops_id;


END process_user;


SELECT
    flag,
    name
INTO 
    cur_acc_gestating_ops_flag,
    cur_acc_gestating_ops_name
FROM account_gestating_ops
WHERE id = cur_acc_gestating_ops_id;

SELECT 
    res_num                             AS result_number,
    res_code                            AS result_code,
    res_desc                            AS result_desc,
    
    cur_acc_gestating_ops_id            AS acc_gestating_ops_id,
    cur_acc_gestating_ops_flag          AS acc_gestating_ops_flag,
    cur_acc_gestating_ops_name          AS acc_gestating_ops_name;

END $$

DELIMITER ;
