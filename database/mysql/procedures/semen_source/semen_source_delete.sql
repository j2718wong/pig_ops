DELIMITER $$

DROP PROCEDURE IF EXISTS semen_source_delete $$
CREATE PROCEDURE semen_source_delete(
    in_user_id              INT,
    
    in_semen_source_id      INT
)  

BEGIN

/** 
 * Will delete semen_source entry.
 * 
 * @author Jack Wong (j2718wong@gmail.com) 
 * @since August 18, 2025
 *
 */

DECLARE RES_NUM_SUCCESS                         INT             DEFAULT 0;


/* semen_source.flag bits*/
DECLARE FLAG_BIT_SEMEN_SOURCE_IS_DELETED        INT             DEFAULT 1;


DECLARE cur_user_account_id                     INT             DEFAULT 0;
DECLARE cur_user_group_id                       INT             DEFAULT 0;


DECLARE cur_semen_source_account_id             INT             DEFAULT 0;


DECLARE cur_pig_farm_id                         INT             DEFAULT 0;
DECLARE cur_pig_farm_flag                       INT             DEFAULT 0;
DECLARE cur_pig_farm_name                       VARCHAR(50)     DEFAULT '';



DECLARE res_num                                 INT             DEFAULT 0;
DECLARE res_code                                VARCHAR(80)     DEFAULT '';
DECLARE res_desc                                VARCHAR(180)    DEFAULT '';


DECLARE s_desc                                  VARCHAR(200)    DEFAULT '';


SET res_num     = RES_NUM_SUCCESS;
SET res_code    = "SUCCESS";


SELECT  account_id
INTO    cur_semen_source_account_id
FROM    semen_source
WHERE   id = in_semen_source_id
LIMIT   1;


CALL basic_user_check(in_user_id, 0, cur_semen_source_account_id,
    cur_user_account_id, 
    cur_user_group_id,
    res_num, 
    res_code, 
    res_desc);


process_user : BEGIN


UPDATE semen_source SET
    flag         		= flag | FLAG_BIT_SEMEN_SOURCE_IS_DELETED
WHERE id =  in_semen_source_id;


/* Insert app_audit_log. */
SET s_desc = CONCAT("old_acc_name = ", cur_account_name, "; new_acc_name = ",
    in_name);

INSERT INTO app_audit_log(
    user_id,
    account_id,
    action,
    description,
    date
) VALUES (
    in_user_id,
    cur_user_account_id,
    AUDIT_ACTION_UPDATE,
    s_desc,
    CURRENT_DATE
);


END process_user;


SELECT
    flag,
    name
INTO 
    cur_semen_source_flag,
    cur_semen_source_name
FROM semen_source
WHERE id = in_semen_source_id;

SELECT 
    res_num                             AS result_number,
    res_code                            AS result_code,
    res_desc                            AS result_desc,
    
    in_semen_source_id                  AS semen_source_id,
    cur_semen_source_flag               AS semen_source_flag,
    cur_semen_source_name               AS semen_source_name;
    

END $$

DELIMITER ;
