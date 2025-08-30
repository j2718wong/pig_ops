DELIMITER $$

DROP PROCEDURE IF EXISTS pig_prod_gestating_ops_add $$
CREATE PROCEDURE pig_prod_gestating_ops_add(
    in_user_id              INT,
    
    in_account_id           INT,
    in_pig_prod_id          INT,
    in_date_insemination    VARCHAR(10)
)  

BEGIN

/** 
 * A sub procedure to create production_gestating_notes entries.
 * 
 * @author Jack Wong (j2718wong@gmail.com) 
 * @since August 30, 2025
 *
 */
 
DECLARE cur_acc_gestating_ops_id                INT             DEFAULT 0;
DECLARE cur_acc_gestating_ops_num_days          INT             DEFAULT 0;


DECLARE l_last_row_fetched TINYINT;
DECLARE c_acc_gestating_ops CURSOR FOR
    SELECT  id,
            num_days_since_insem
    FROM    account_gestating_ops
    WHERE   account_id = in_account_id AND (flag & 1) = 0
    ORDER BY num_days_since_insem ASC; 

DECLARE CONTINUE HANDLER FOR NOT FOUND SET l_last_row_fetched=1; 


    
SET l_last_row_fetched=0;
OPEN c_acc_gestating_ops;   
    

loop_here: LOOP
    FETCH c_acc_gestating_ops INTO 
        cur_acc_gestating_ops_id,
        cur_acc_gestating_ops_num_days;
        
    IF l_last_row_fetched=1 THEN LEAVE loop_here; END IF;

    INSERT INTO prod_gestating_ops(
        pig_prod_id,
        acc_gestating_ops_id,
        date_target
    ) VALUES (
        in_pig_prod_id,
        cur_acc_gestating_ops_id,
        DATE_ADD(in_date_insemination, INTERVAL cur_acc_gestating_ops_num_days DAY)
    );
    

END LOOP loop_here;
 
CLOSE c_acc_gestating_ops;
SET l_last_row_fetched=0;   

END $$

DELIMITER ;
