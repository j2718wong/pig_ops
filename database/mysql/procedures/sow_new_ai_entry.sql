DELIMITER $$

DROP PROCEDURE IF EXISTS sow_new_ai_entry $$
CREATE PROCEDURE sow_new_ai_entry(
    in_sow_number           INT,
    
    in_semen_source_id      INT,
    in_staff_id             INT,
    in_date_ai              VARCHAR(10),  /* in YYYY-MM-DD format*/
    in_description          VARCHAR(200)
)  

BEGIN

/** 
 * Will create sow_coming_activity entries from a given sow AI entry.
 * 
 * @author Jack Wong (neoaspilet11@gmail.com, zhaoshan99@gmail.com) 
 * @since January 4, 2025
 *
 */

DECLARE RES_NUM_SUCCESS                         INT             DEFAULT 0;
DECLARE RES_NUM_DUPLICATE_ENTRY                 INT             DEFAULT 1;


DECLARE AI_STATUS_ID_ON_GOING                   INT             DEFAULT 1;


DECLARE COMING_ACT_ID_ARTIFICAL_INSEMINATION    INT             DEFAULT 1;
DECLARE COMING_ACT_ID_AFTER_AI                  INT             DEFAULT 2;
DECLARE COMING_ACT_ID_BACK_NORMAL_FEEDING       INT             DEFAULT 3;
DECLARE COMING_ACT_ID_INJECT_IRON               INT             DEFAULT 4;
DECLARE COMING_ACT_ID_DEWORM                    INT             DEFAULT 5;
DECLARE COMING_ACT_ID_BEFORE_LABOR              INT             DEFAULT 6;
DECLARE COMING_ACT_ID_EXPECTED_LABOR            INT             DEFAULT 7;
DECLARE COMING_ACT_ID_AFTER_BIRTH               INT             DEFAULT 8;
DECLARE COMING_ACT_ID_SOW_PROCESSING            INT             DEFAULT 9;
DECLARE COMING_ACT_ID_PIGLET_PROCESSING         INT             DEFAULT 10;
DECLARE COMING_ACT_ID_PIGLET_VITAMINS           INT             DEFAULT 11;
DECLARE COMING_ACT_ID_PIGLET_IRON_2             INT             DEFAULT 12;
DECLARE COMING_ACT_ID_WEANING                   INT             DEFAULT 13;
DECLARE COMING_ACT_ID_CHECK_IF_PREGNANT         INT             DEFAULT 14;

DECLARE COMING_ACT_ID_NATURAL_COUPLING          INT             DEFAULT 15;


DECLARE cur_is_ai                               INT             DEFAULT 0;
DECLARE cur_coming_activity_id                  INT             DEFAULT 0;

DECLARE cur_artificial_insemination_id          INT             DEFAULT 0;

DECLARE cur_sow_coming_act_id                   INT             DEFAULT 0;


DECLARE res_num                                 INT             DEFAULT 0;
DECLARE res_code                                VARCHAR(180)    DEFAULT '';


SET res_num         = RES_NUM_SUCCESS;


SELECT  id
INTO    cur_artificial_insemination_id
FROM    artificial_insemination
WHERE   sow_number      = in_sow_number     AND 
        date_ai         = in_date_ai 
LIMIT   1;


process_user : BEGIN

IF cur_artificial_insemination_id > 0 THEN
    SET res_num     = RES_NUM_DUPLICATE_ENTRY;
    SET res_code    = "RES_NUM_DUPLICATE_ENTRY";
    
    LEAVE process_user;
END IF;





INSERT INTO artificial_insemination (
    sow_number,
    date_ai,
    date_expected_birth,
    semen_source_id,
    status_id,
    staff_id
) VALUES (
    in_sow_number,
    in_date_ai,
    DATE_ADD(in_date_ai, INTERVAL 115 DAY),
    in_semen_source_id,
    AI_STATUS_ID_ON_GOING,
    in_staff_id
);

SELECT LAST_INSERT_ID() INTO cur_artificial_insemination_id;


SELECT  is_ai
INTO    cur_is_ai
FROM    semen_source
WHERE   id = in_semen_source_id;

IF cur_is_ai > 0 THEN 
    SET cur_coming_activity_id  = COMING_ACT_ID_ARTIFICAL_INSEMINATION;
ELSE
    SET cur_coming_activity_id  = COMING_ACT_ID_NATURAL_COUPLING;
END IF;

/* Record for artificial insemination or natural coupling*/
INSERT INTO sow_coming_activity (
    ai_id,
    
    sow_number,
    coming_activity_id,
    date,
    description
    
) VALUES(
    cur_artificial_insemination_id,

    in_sow_number,
    cur_coming_activity_id,
    in_date_ai,
    CONCAT(in_description, '; walay kaon, tubig ra')
);

/* Record for after artificial insemination*/
INSERT INTO sow_coming_activity (
    ai_id,
    
    sow_number,
    coming_activity_id,
    date,
    date_2,
    description
    
) VALUES(
    cur_artificial_insemination_id,
    
    in_sow_number,
    COMING_ACT_ID_AFTER_AI,
    DATE_ADD(in_date_ai, INTERVAL 1 DAY),
    DATE_ADD(in_date_ai, INTERVAL 4 DAY),
    "1.5 kg per day gestating"
);

/* Record for back to normal feeding*/
INSERT INTO sow_coming_activity (
    ai_id,
    
    sow_number,
    coming_activity_id,
    date,
    days_since_ai,
    description
    
) VALUES(
    cur_artificial_insemination_id,

    in_sow_number,
    COMING_ACT_ID_BACK_NORMAL_FEEDING,
    DATE_ADD(in_date_ai, INTERVAL 5 DAY),
    5,
    "3.0 kg per day gestating"
);

/* Record for check if buntis*/
INSERT INTO sow_coming_activity (
    ai_id,
    
    sow_number,
    coming_activity_id,
    date,
    days_since_ai,
    description
    
) VALUES(
    cur_artificial_insemination_id,

    in_sow_number,
    COMING_ACT_ID_CHECK_IF_PREGNANT,
    DATE_ADD(in_date_ai, INTERVAL 21 DAY),
    21,
    "3.0 kg per day gestating"
);

/* Record for check if buntis*/
INSERT INTO sow_coming_activity (
    ai_id,
    
    sow_number,
    coming_activity_id,
    date,
    days_since_ai,
    description
    
) VALUES(
    cur_artificial_insemination_id,

    in_sow_number,
    COMING_ACT_ID_CHECK_IF_PREGNANT,
    DATE_ADD(in_date_ai, INTERVAL 42 DAY),
    42,
    "3.0 kg per day gestating"
);

/* Record for check if buntis*/
INSERT INTO sow_coming_activity (
    ai_id,
    
    sow_number,
    coming_activity_id,
    date,
    days_since_ai,
    description
    
) VALUES(
    cur_artificial_insemination_id,

    in_sow_number,
    COMING_ACT_ID_CHECK_IF_PREGNANT,
    DATE_ADD(in_date_ai, INTERVAL 63 DAY),
    63,
    "3.0 kg per day gestating"
);



/* Record for inject iron*/
INSERT INTO sow_coming_activity (
    ai_id,
    
    sow_number,
    coming_activity_id,
    date,
    days_since_ai,
    description
    
) VALUES(
    cur_artificial_insemination_id,
    
    in_sow_number,
    COMING_ACT_ID_INJECT_IRON,
    DATE_ADD(in_date_ai, INTERVAL 80 DAY),
    80,
    "3.0 kg per day gestating"
);

/* Record for deworm*/
INSERT INTO sow_coming_activity (
    ai_id,
    
    sow_number,
    coming_activity_id,
    date,
    days_since_ai,
    description
    
) VALUES(
    cur_artificial_insemination_id,
    
    in_sow_number,
    COMING_ACT_ID_DEWORM,
    DATE_ADD(in_date_ai, INTERVAL 100 DAY),
    100,
    "3.0 kg per day gestating"
);

/* Record for before labor*/
INSERT INTO sow_coming_activity (
    ai_id,
    
    sow_number,
    coming_activity_id,
    date,
    days_since_ai,
    description
    
) VALUES(
    cur_artificial_insemination_id,
    
    in_sow_number,
    COMING_ACT_ID_BEFORE_LABOR,
    DATE_ADD(in_date_ai, INTERVAL 111 DAY),
    111,
    "2.0 kg per day gestating"
);

/* Record for before labor*/
INSERT INTO sow_coming_activity (
    ai_id,
    
    sow_number,
    coming_activity_id,
    date,
    days_since_ai,
    description
    
) VALUES(
    cur_artificial_insemination_id,
    in_sow_number,
    COMING_ACT_ID_BEFORE_LABOR,
    DATE_ADD(in_date_ai, INTERVAL 112 DAY),
    112,
    "2.0 kg per day gestating"
);

/* Record for before labor*/
INSERT INTO sow_coming_activity (
    ai_id,
    
    sow_number,
    coming_activity_id,
    date,
    days_since_ai,
    description
    
) VALUES(
    cur_artificial_insemination_id,
    
    in_sow_number,
    COMING_ACT_ID_BEFORE_LABOR,
    DATE_ADD(in_date_ai, INTERVAL 113 DAY),
    113,
    "1.0 kg per day gestating"
);

/* Record for before labor*/
INSERT INTO sow_coming_activity (
    ai_id,
    
    sow_number,
    coming_activity_id,
    date,
    days_since_ai,
    description
    
) VALUES(
    cur_artificial_insemination_id,
    
    in_sow_number,
    COMING_ACT_ID_BEFORE_LABOR,
    DATE_ADD(in_date_ai, INTERVAL 114 DAY),
    114,
    "1.0 kg per day gestating"
);

/* Record for expected labor*/
INSERT INTO sow_coming_activity (
    ai_id,
    
    sow_number,
    coming_activity_id,
    date,
    days_since_ai,
    description
    
) VALUES(
    cur_artificial_insemination_id,
    
    in_sow_number,
    COMING_ACT_ID_EXPECTED_LABOR,
    DATE_ADD(in_date_ai, INTERVAL 115 DAY),
    115,
    "walay kaon, tubig lang"
);


/* Record for after birth*/
INSERT INTO sow_coming_activity (
    ai_id,
    
    sow_number,
    coming_activity_id,
    date,
    description
    
) VALUES(
    cur_artificial_insemination_id,
    
    in_sow_number,
    COMING_ACT_ID_AFTER_BIRTH,
    DATE_ADD(in_date_ai, INTERVAL 116 DAY),
    "3.0 kg per day lactating"
);


/* Record for sow processing*/
INSERT INTO sow_coming_activity (
    ai_id,
    
    sow_number,
    coming_activity_id,
    date,
    description
    
) VALUES(
    cur_artificial_insemination_id,
    
    in_sow_number,
    COMING_ACT_ID_SOW_PROCESSING,
    DATE_ADD(in_date_ai, INTERVAL 116 DAY),
    "3.0 kg per day lactating"
);



/* Record for piglet processing*/
INSERT INTO sow_coming_activity (
    ai_id,
    
    sow_number,
    coming_activity_id,
    date,
    description
    
) VALUES(
    cur_artificial_insemination_id,
    
    in_sow_number,
    COMING_ACT_ID_PIGLET_PROCESSING,
    DATE_ADD(in_date_ai, INTERVAL 118 DAY),
    "baktin kapon, pangil, ikog, bakuna, iron"
);


/* Record for piglet vitamins*/
INSERT INTO sow_coming_activity (
    ai_id,
    
    sow_number,
    coming_activity_id,
    date,
    description
    
) VALUES(
    cur_artificial_insemination_id,
    
    in_sow_number,
    COMING_ACT_ID_PIGLET_VITAMINS,
    DATE_ADD(in_date_ai, INTERVAL 125 DAY),
    "inject baktin vitamins after 7 days"
);


/* Record for piglet processing*/
INSERT INTO sow_coming_activity (
    ai_id,
    
    sow_number,
    coming_activity_id,
    date,
    description
    
) VALUES(
    cur_artificial_insemination_id,
    
    in_sow_number,
    COMING_ACT_ID_PIGLET_IRON_2,
    DATE_ADD(in_date_ai, INTERVAL 129 DAY),
    "inject baktin iron, after 14 days"
);


/* Record for weaning*/
INSERT INTO sow_coming_activity (
    ai_id,
    
    sow_number,
    coming_activity_id,
    date,
    description
    
) VALUES(
    cur_artificial_insemination_id,
    
    in_sow_number,
    COMING_ACT_ID_WEANING,
    DATE_ADD(in_date_ai, INTERVAL 160 DAY),
    "3.0 kg per day"
);




END process_user;

SELECT 
    res_num                             AS result_number,
    res_code                            AS result_code,
    
    cur_artificial_insemination_id      AS ai_id;
    

END $$

DELIMITER ;
