DELIMITER $$

DROP PROCEDURE IF EXISTS trucate_for_testing $$
CREATE PROCEDURE trucate_for_testing()  

BEGIN

/** 
 * WARNING: This will truncate tables; be sure to not include this in production
 *      databases. This is used for testing.
 * 
 * @author Jack Wong (neoaspilet11@gmail.com, zhaoshan99@gmail.com) 
 * @since January 5, 2025
 *
 */

TRUNCATE TABLE account;
TRUNCATE TABLE pig_farm;
TRUNCATE TABLE sow_boar;
TRUNCATE TABLE sow_operation;
TRUNCATE TABLE semen_source;
TRUNCATE TABLE user_group;
TRUNCATE TABLE pig_production;

UPDATE user SET account_id = 0, user_group_id = 0;


END $$

DELIMITER ;
