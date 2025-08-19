DELIMITER $$

DROP PROCEDURE IF EXISTS semen_source_add $$
CREATE PROCEDURE semen_source_add(
    in_user_id              INT,

    in_pig_farm_id          INT,
    in_is_ai                INT,
    in_pig_race_id          INT,
    in_boar_id              INT,
    
    in_name                 VARCHAR(50),
    in_description          VARCHAR(160)
)  

BEGIN

/** 
 * Will add semen_source entry.
 * 
 * @author Jack Wong (j2718wong@gmail.com) 
 * @since August 15, 2025
 *
 */

DECLARE RES_NUM_SUCCESS                         INT             DEFAULT 0;


DECLARE RES_NUM_DUPLICATE_ENTRY                 INT             DEFAULT 20;


/* semen_source.flag bits*/
DECLARE FLAG_BIT_SEMEN_SOURCE_IS_DELETED        INT             DEFAULT 1;

DECLARE FLAG_BIT_BIZ_OBJ_SEMEN_SOURCE           INT             DEFAULT 64;

DECLARE FLAG_BIT_OPERATION_ADD                  INT             DEFAULT 1;
DECLARE FLAG_BIT_OPERATION_UPDATE               INT             DEFAULT 2;
DECLARE FLAG_BIT_OPERATION_DELETE               INT             DEFAULT 4;


DECLARE cur_user_account_id                     INT             DEFAULT 0;
DECLARE cur_user_group_id                       INT             DEFAULT 0;


DECLARE cur_pig_farm_account_id                 INT             DEFAULT 0;


DECLARE cur_semen_source_id                     INT             DEFAULT 0;
DECLARE cur_semen_source_flag                   INT             DEFAULT 0;
DECLARE cur_semen_source_name                   VARCHAR(50)     DEFAULT '';



DECLARE res_num                                 INT             DEFAULT 0;
DECLARE res_code                                VARCHAR(80)     DEFAULT '';
DECLARE res_desc                                VARCHAR(180)    DEFAULT '';


SET res_num     = RES_NUM_SUCCESS;
SET res_code    = "SUCCESS";


SELECT  account_id
INTO    cur_pig_farm_account_id
FROM    pig_farm
WHERE   id = in_pig_farm_id
LIMIT   1;


CALL basic_user_check(
    in_user_id, 
    1, /* user must have an account*/
    cur_pig_farm_account_id,
    
    FLAG_BIT_BIZ_OBJ_SEMEN_SOURCE,
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
INTO    cur_semen_source_id
FROM    semen_source
WHERE   account_id  = cur_user_account_id   AND 
        pig_farm_id = in_pig_farm_id        AND 
        UPPER(name) = UPPER(in_name)
LIMIT   1;

IF cur_semen_source_id > 0 THEN 
    SET res_num     = RES_NUM_DUPLICATE_ENTRY;
    SET res_code    = "RES_NUM_DUPLICATE_ENTRY";
    
    LEAVE process_user;
END IF;



INSERT INTO semen_source(
    account_id,
    pig_farm_id,
    is_ai,
    pig_race_id,
    boar_id,
    added_by_user_id,
    
    name,
    description
) VALUES (
    cur_user_account_id,
    in_pig_farm_id,
    in_is_ai,
    in_pig_race_id,
    in_boar_id,
    in_user_id,
    
    in_name,
    in_description    
);

SELECT LAST_INSERT_ID() INTO cur_semen_source_id;


END process_user;


SELECT
    flag,
    name
INTO 
    cur_semen_source_flag,
    cur_semen_source_name
FROM semen_source
WHERE id = cur_semen_source_id;

SELECT 
    res_num                             AS result_number,
    res_code                            AS result_code,
    res_desc                            AS result_desc,
    
    cur_semen_source_id                 AS semen_source_id,
    cur_semen_source_flag               AS semen_source_flag,
    cur_semen_source_name               AS semen_source_name;

END $$

DELIMITER ;
