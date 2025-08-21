# February 3, 2020
# Jack Wong (zhaoshan99@gmail.com)



LOG_DEBUG               = 0
LOG_WARNING             = 1
LOG_ERROR               = 2
LOG_FATAL               = 3



BUSINESS_OBJ_ID_USER_REGISTER                       = 1


# user.flag bits
FLAG_BIT_USER_IS_ACTIVE                             = 1
FLAG_BIT_USER_EMAIL_VERIFIED                        = 2
FLAG_BIT_USER_MOBILE_NUM_VERIFIED                   = 4
FLAG_BIT_USER_IS_DELETED                            = 8

FLAG_BIT_USER_IS_ACCOUNT_ADMIN                      = 16


MFA_CHANNEL_ID_EMAIL                                = 1
MFA_CHANNEL_ID_PHONE_NUMBER                         = 2

MFA_VERIFICATION_CODE_MIN                           = 100000
MFA_VERIFICATION_CODE_MAX                           = 999999


MFA_SEND_SUCCESS                                    = 0



NUM_MINUTES_EXPIRE_USER_REG_EMAIL_VERIFY            = 5


INS_STATUS_ID_TERMINATED                            = 2


ERROR_DATABASE_ERROR                                = 0x01
ERROR_SERVER_ERROR                                  = 0x02


ERROR_USER_INVALID_USER_HASHID                      = 0x20
ERROR_USER_INVALID_USER_INACTIVE                    = 0x21
ERROR_USER_INVALID_USER_NOT_EMAIL_VERIFIED          = 0x22
ERROR_USER_ALREADY_CONNECTED_TO_ACCOUNT             = 0x23


ERROR_ACCOUNT_INVALID_NAME                          = 0x30
ERROR_ACCOUNT_INVALID_HASHID                        = 0x31



ERROR_ACCOUNT_REQUEST_INVALID_USER_HASHID           = 0x40
ERROR_ACCOUNT_REQUEST_INVALID_ACCOUNT_HASHID        = 0x41
ERROR_ACCOUNT_REQUEST_INVALID_HASHID                = 0x42




ERROR_PIG_FARM_INVALID_NAME                         = 0x40
ERROR_PIG_FARM_INVALID_HASHID                       = 0x41
ERROR_PIG_FARM_INVALID_ACCOUNT_HASHID               = 0x42



ERROR_SOW_BOAR_INVALID_SOW_NUMBER                   = 0x51


ERROR_ACC_GESTATING_OPS_INVALID_NAME                = 0x60
ERROR_ACC_GESTATING_OPS_INVALID_USER_HASHID         = 0x61