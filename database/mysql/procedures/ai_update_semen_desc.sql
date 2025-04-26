DELIMITER $$

DROP PROCEDURE IF EXISTS ai_update_semen_desc $$
CREATE PROCEDURE ai_update_semen_desc()  

BEGIN

/** 
 * Will update artificial_insemination.semen_desc.
 * 
 * @author Jack Wong (neoaspilet11@gmail.com, zhaoshan99@gmail.com) 
 * @since April 26, 2025
 *
 */
 
DECLARE cur_ai_id                               INT             DEFAULT 0;
DECLARE cur_semen_source_id                     INT             DEFAULT 0;

DECLARE cur_is_ai                               INT             DEFAULT 0;
DECLARE cur_semen_source_name                   VARCHAR(50)     DEFAULT '';
DECLARE cur_pig_race_name                       VARCHAR(50)     DEFAULT '';

DECLARE cur_semen_desc                          VARCHAR(100)    DEFAULT '';


DECLARE l_last_row_fetched TINYINT;
DECLARE c_ai CURSOR FOR
    SELECT  id,
            semen_source_id
    FROM    artificial_insemination; 

DECLARE CONTINUE HANDLER FOR NOT FOUND SET l_last_row_fetched=1; 
 
    
SET l_last_row_fetched=0;
OPEN c_ai;   
    

loop_here: LOOP
    FETCH   c_ai 
    INTO    cur_ai_id,
            cur_semen_source_id;

	IF l_last_row_fetched=1 THEN LEAVE loop_here; END IF;

    
    SELECT  a.is_ai,
            a.name,
            b.name

    INTO    cur_is_ai,
            cur_semen_source_name,
            cur_pig_race_name
    FROM    semen_source a 
    LEFT OUTER JOIN pig_race b ON a.pig_race_id = b.id
    WHERE   a.id = cur_semen_source_id;

    IF cur_is_ai > 0 THEN 
        SET cur_semen_desc = CONCAT(cur_pig_race_name, ' FROM ');
        SET cur_semen_desc = CONCAT(cur_semen_desc, cur_semen_source_name);
    ELSE
        SET cur_semen_desc = CONCAT(cur_pig_race_name, ' TAKAL FROM ');
        SET cur_semen_desc = CONCAT(cur_semen_desc, cur_semen_source_name);
    END IF;
    
    UPDATE artificial_insemination SET
        semen_desc = cur_semen_desc
    WHERE id = cur_ai_id;


END LOOP loop_here;
 
CLOSE c_ai;
SET l_last_row_fetched=0;   

SELECT 1 AS result_code;

    

END $$

DELIMITER ;
