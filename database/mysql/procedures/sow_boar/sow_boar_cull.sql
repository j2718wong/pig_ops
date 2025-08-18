DELIMITER $$

DROP PROCEDURE IF EXISTS sow_boar_cull $$
CREATE PROCEDURE sow_boar_cull(
    in_user_id              INT,
    
    in_sow_boar_id          INT,
    in_date_culled          VARCHAR(10),
    in_cull_notes           VARCHAR(160)
)  

BEGIN

/** 
 * Will cull sow_boar entry.
 * 
 * @author Jack Wong (j2718wong@gmail.com) 
 * @since August 17, 2025
 *
 */

DECLARE RES_NUM_SUCCESS                         INT             DEFAULT 0;


DECLARE RES_NUM_ACCOUNT_MISMATCH                INT             DEFAULT 20;


DECLARE cur_user_account_id                     INT             DEFAULT 0;
DECLARE cur_user_group_id                       INT             DEFAULT 0;


DECLARE cur_pig_farm_account_id                 INT             DEFAULT 0;
DECLARE cur_pig_farm_last_sow_id                INT             DEFAULT 0;


DECLARE res_num                                 INT             DEFAULT 0;
DECLARE res_code                                VARCHAR(80)     DEFAULT '';
DECLARE res_desc                                VARCHAR(180)    DEFAULT '';


SET res_num     = RES_NUM_SUCCESS;
SET res_code    = "SUCCESS";


CALL basic_user_check(in_user_id, 0,
    cur_user_account_id, 
    cur_user_group_id,
    res_num, 
    res_code, 
    res_desc);


process_user : BEGIN



SELECT  
        account_id
INTO    
        cur_pig_farm_account_id
FROM    sow
WHERE   id = in_sow_boar_id
LIMIT   1;


IF cur_user_account_id != cur_pig_farm_account_id THEN 
    SET res_num     = RES_NUM_ACCOUNT_MISMATCH;
    SET res_code    = "RES_NUM_ACCOUNT_MISMATCH";
    
    LEAVE process_user;
END IF;



UPDATE sow SET
    date_culled         = in_date_culled,
    cull_notes          = in_cull_notes,
    
    last_update_user_id = in_user_id,
    dt_last_update      = CURRENT_TIMESTAMP
    
WHERE 
    id = in_sow_boar_id;


END process_user;



SELECT 
    res_num                             AS result_number,
    res_code                            AS result_code,
    res_desc                            AS result_desc,
    
    in_sow_boar_id                           AS sow_id;
    

END $$

DELIMITER ;
