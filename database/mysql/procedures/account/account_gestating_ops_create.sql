DELIMITER $$

DROP PROCEDURE IF EXISTS account_gestating_ops_create $$
CREATE PROCEDURE account_gestating_ops_create(
    in_account_id               INT
)  

BEGIN

/** 
 * 
 * @author Jack Wong (j2718wong@gmail.com) 
 * @since August 19, 2025
 *
 */



/* Default account gestating operation*/
DECLARE GESTATING_OPS_NUM_DAYS_CHECK_PREGNANT   INT             DEFAULT 21;
DECLARE GESTATING_OPS_NUM_DAYS_INJECT_IRON      INT             DEFAULT 80;
DECLARE GESTATING_OPS_NUM_DAYS_DEWORM           INT             DEFAULT 100;



/* Create default gestating_operation for the account.*/
INSERT INTO account_gestating_ops (
    account_id,
    num_days_since_insem,
    name
) VALUES (
    in_account_id,
    GESTATING_OPS_NUM_DAYS_CHECK_PREGNANT,
    "Check if pregnant"
);

INSERT INTO account_gestating_ops (
    account_id,
    num_days_since_insem,
    name
) VALUES (
    in_account_id,
    GESTATING_OPS_NUM_DAYS_INJECT_IRON,
    "Inject Iron"
);

INSERT INTO account_gestating_ops (
    account_id,
    num_days_since_insem,
    name
) VALUES (
    in_account_id,
    GESTATING_OPS_NUM_DAYS_DEWORM,
    "Deworm"
);


END $$

DELIMITER ;
