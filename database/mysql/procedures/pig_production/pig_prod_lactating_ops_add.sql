DELIMITER $$

DROP PROCEDURE IF EXISTS pig_prod_lactating_ops_add $$
CREATE PROCEDURE pig_prod_lactating_ops_add(
    in_user_id              INT,
    
    in_account_id           INT,
    in_pig_prod_id          INT,
    in_date_birth           VARCHAR(10)
)  

BEGIN

/** 
 * A sub procedure to create prod_lactating_ops entries.
 * 
 * @author Jack Wong (j2718wong@gmail.com) 
 * @since August 30, 2025
 *
 */
 
DECLARE cur_acc_lactating_ops_id                INT             DEFAULT 0;
DECLARE cur_acc_lactating_ops_num_days          INT             DEFAULT 0;


DECLARE l_last_row_fetched TINYINT;
DECLARE c_acc_lactating_ops CURSOR FOR
    SELECT  id,
            num_days_since_birth
    FROM    account_lactating_ops
    WHERE   account_id = in_account_id AND (flag & 1) = 0
    ORDER BY num_days_since_birth ASC; 

DECLARE CONTINUE HANDLER FOR NOT FOUND SET l_last_row_fetched=1; 


    
SET l_last_row_fetched=0;
OPEN c_acc_lactating_ops;   
    

loop_here: LOOP
    FETCH c_acc_lactating_ops INTO 
        cur_acc_lactating_ops_id,
        cur_acc_lactating_ops_num_days;
        
    IF l_last_row_fetched=1 THEN LEAVE loop_here; END IF;

    INSERT INTO prod_lactating_ops(
        pig_prod_id,
        acc_lactating_ops_id,
        date_target
    ) VALUES (
        in_pig_prod_id,
        cur_acc_lactating_ops_id,
        DATE_ADD(in_date_birth, INTERVAL cur_acc_lactating_ops_num_days DAY)
    );
    

END LOOP loop_here;
 
CLOSE c_acc_lactating_ops;
SET l_last_row_fetched=0;   

END $$

DELIMITER ;
