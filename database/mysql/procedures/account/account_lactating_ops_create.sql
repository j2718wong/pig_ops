DELIMITER $$

DROP PROCEDURE IF EXISTS account_lactating_ops_create $$
CREATE PROCEDURE account_lactating_ops_create(
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
DECLARE LACTATING_OPS_NUM_DAYS_INJECT_IRON_1    INT             DEFAULT 2;
DECLARE LACTATING_OPS_NUM_DAYS_INJECT_IRON_2    INT             DEFAULT 12;
DECLARE LACTATING_OPS_NUM_DAYS_INJECT_VITA_1    INT             DEFAULT 13;
DECLARE LACTATING_OPS_NUM_DAYS_INJECT_VITA_2    INT             DEFAULT 20;
DECLARE LACTATING_OPS_NUM_DAYS_CASTRATION       INT             DEFAULT 21;
DECLARE LACTATING_OPS_NUM_DAYS_DEWORM           INT             DEFAULT 24;



/* Create default gestating_operation for the account.*/
INSERT INTO account_lactating_ops (
    account_id,
    num_days_since_birth,
    name
) VALUES (
    in_account_id,
    LACTATING_OPS_NUM_DAYS_INJECT_IRON_1,
    "Inject Iron_1"
);

INSERT INTO account_lactating_ops (
    account_id,
    num_days_since_birth,
    name
) VALUES (
    in_account_id,
    LACTATING_OPS_NUM_DAYS_INJECT_IRON_2,
    "Inject Iron_2"
);

INSERT INTO account_lactating_ops (
    account_id,
    num_days_since_birth,
    name
) VALUES (
    in_account_id,
    LACTATING_OPS_NUM_DAYS_INJECT_VITA_2,
    "Inject Vitamins_2"
);


INSERT INTO account_lactating_ops (
    account_id,
    num_days_since_birth,
    name
) VALUES (
    in_account_id,
    LACTATING_OPS_NUM_DAYS_INJECT_VITA_1,
    "Inject Vitamins_1"
);


INSERT INTO account_lactating_ops (
    account_id,
    num_days_since_birth,
    name
) VALUES (
    in_account_id,
    LACTATING_OPS_NUM_DAYS_CASTRATION,
    "Castration"
);


INSERT INTO account_lactating_ops (
    account_id,
    num_days_since_birth,
    name
) VALUES (
    in_account_id,
    LACTATING_OPS_NUM_DAYS_DEWORM,
    "Deworm"
);


END $$

DELIMITER ;
