DELIMITER $$

DROP PROCEDURE IF EXISTS account_create_sow_operations $$
CREATE PROCEDURE account_create_sow_operations(
    in_account_id               INT
)  

BEGIN

/** 
 * 
 * @author Jack Wong (j2718wong@gmail.com) 
 * @since August 19, 2025
 *
 */


/* Default account sow operation*/
DECLARE SOW_OPERATION_NUM_DAYS_CHECK_PREGNANT   INT             DEFAULT 21;
DECLARE SOW_OPERATION_NUM_DAYS_INJECT_IRON      INT             DEFAULT 80;
DECLARE SOW_OPERATION_NUM_DAYS_DEWORM           INT             DEFAULT 100;



/* Create default sow_operation for the account.*/
INSERT INTO sow_operation (
    account_id,
    order_num,
    num_days_since_insem,
    name
) VALUES (
    in_account_id,
    1,
    SOW_OPERATION_NUM_DAYS_CHECK_PREGNANT,
    "Check if pregnant"
);

INSERT INTO sow_operation (
    account_id,
    order_num,
    num_days_since_insem,
    name
) VALUES (
    in_account_id,
    2,
    SOW_OPERATION_NUM_DAYS_INJECT_IRON,
    "Inject Iron"
);

INSERT INTO sow_operation (
    account_id,
    order_num,
    num_days_since_insem,
    name
) VALUES (
    in_account_id,
    3,
    SOW_OPERATION_NUM_DAYS_DEWORM,
    "Deworm"
);


END $$

DELIMITER ;
