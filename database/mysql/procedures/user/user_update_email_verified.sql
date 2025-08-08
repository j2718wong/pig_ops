DELIMITER $$

DROP PROCEDURE IF EXISTS user_update_email_verified $$
CREATE PROCEDURE user_update_email_verified(
    in_user_id              INT
)  

BEGIN

/** 
 * Will update user.flag.FLAG_BIT_IS_VERIFIED. 
 * 
 * @author Jack Wong (j2718wong@gmail.com) 
 * @since August 8, 2025
 *
 */

DECLARE RES_NUM_SUCCESS                         INT             DEFAULT 0;

DECLARE FLAG_BIT_USER_EMAIL_IS_ACTIVE       	INT             DEFAULT 1;
DECLARE FLAG_BIT_USER_EMAIL_VERIFIED       		INT             DEFAULT 2;
DECLARE FLAG_BIT_USER_MOBILE_NUM_VERIFIED  		INT             DEFAULT 4;

DECLARE cur_user_flag                           INT             DEFAULT 0;
DECLARE cur_user_farm_id                        INT             DEFAULT 0;



DECLARE res_num                                 INT             DEFAULT 0;
DECLARE res_code                                VARCHAR(180)    DEFAULT '';


SET res_num         = RES_NUM_SUCCESS;
SET res_code        = "SUCCESS";


UPDATE user SET 
    flag = flag | FLAG_BIT_USER_EMAIL_VERIFIED
WHERE id = in_user_id;

SELECT 
    flag,
    farm_id
INTO 
    cur_user_flag,
    cur_user_farm_id
FROM user 
WHERE id = in_user_id;


SELECT 
    res_num                             AS result_number,
    res_code                            AS result_code,
    
    in_user_id                          AS user_id,
    cur_user_flag                       AS user_flag,
    cur_user_farm_id                    AS user_farm_id;
    

END $$

DELIMITER ;
