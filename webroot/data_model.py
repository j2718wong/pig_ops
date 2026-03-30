
import datetime

from pydantic               import BaseModel


COUNTRY_ID_PHILIPPINES      = 1

class GoogleToken(BaseModel):
    token:                  str
    viewport_width:         int = None
    viewport_height:        int = None
    
    login_country_code:     str | None  = None
    login_country_name:     str | None  = None
    login_city:             str | None  = None
    login_region:           str | None  = None
    


class HasAddressLevel:
    country_hid:            str = None
    
    level_1_hid:            str = None
    level_2_hid:            str = None
    level_3_hid:            str = None
    
    
    country_id:             int = COUNTRY_ID_PHILIPPINES
    
    level_1_id:             int = 0
    level_2_id:             int = 0
    level_3_id:             int = 0
    
    latitude:               float = None
    longitude:              float = None
    
    
    
class HasContactDetails:
    contact_number:         str = None
    whatsapp:               str = None
    messenger:              str = None
    



class DataUserLogin(BaseModel):
    access_code_hid:        str = None
    
    email:                  str = None
    
    name:                   str = None
    name_last:              str = None
    name_first:             str = None
    
    viewport_width:         int = None
    viewport_height:        int = None
    ip_address:             str = None
    
    latitude:               float | None = None
    longitude:              float | None = None

    access_code_id:         int = None

    login_social_media_id:  int = 0
    social_media_user_id:   str = None
    
    login_country_code:     str | None  = None
    login_country_name:     str | None  = None
    login_city:             str | None  = None 
    login_region:           str | None  = None
    
    
    
    is_mobile:              int = None
    is_webview:             int = None
    
    browser:                str = None
    browser_version:        str = None
    webview_platform:       str = None
    os:                     str = None
    os_version:             str = None
    device:                 str = None
    device_type:            str = None




class DataUserEmailVerify(BaseModel):
    uhid:                   str = None
    uvuhid:                 str = None
    
    user_id:                int = 0
    unverified_user_id:     int = 0
    
    auth_code:              int = 0
    
    viewport_width:         int = None
    viewport_height:        int = None
    ip_address:             str = None


class DataApproveUserReq(BaseModel):
    uhid:                   str = None
    user_req_hid:           str = None 
    pig_farm_hid:           str = None
    
    user_id:                int = 0
    user_req_id:            int = 0
    pig_farm_id:            int = 0
    group_num:              int
    
    is_approved:            int = 1     # 0 = is_rejected
    

    


class DataAccount(BaseModel):
    uhid:                   str = None
    user_id:                int = 0
    name:                   str
    country_id:             int = COUNTRY_ID_PHILIPPINES


class DataAccountAccessCode(BaseModel):
    uhid:                   str = None
    access_code_hid:        str = None
    
    user_id:                int = 0
    group_num:              int = 0
    access_code_id:         int = 0
    

    

class DataAccountSettings(BaseModel):
    uhid:                   str = None
    user_id:                int = 0
    
    day_1_on_date_insem:    int = 0
    day_1_on_date_of_birth: int = 1
    
    days_wean:              int = 42
    days_harvest_from_birth:int = 142
    days_harvest_from_wean: int = 100
    
    weight_unit:            str = 'kg'  


class DataAccountSelection(BaseModel):
    uhid:                   str = None
    
    feed_brand_hid:         str = None
    feed_supplier_hid:      str = None
    semen_supplier_hid:     str = None
    
    user_id:                int = 0
    feed_brand_id:          int = 0
    feed_supplier_id:       int = 0
    semen_supplier_id:      int = 0
    

class DataCustomerFeedback(BaseModel):
    uhid:                   str = None
    
    user_id:                int = 0
    notes:                  str
    

class DataPigFarm(BaseModel, HasAddressLevel):
    uhid:                   str = None
    pig_farm_hid:           str = None
        
        
    user_id:                int = 0
    pig_farm_id:            int = 0
        
    new_country_code:       str = None
    new_country_name:       str = None
    
    
    name:                   str


class DataPigFarmFeedBuy(BaseModel):
    uhid:                   str = None
    pig_farm_hid:           str = None
    feed_supplier_hid:      str = None
    pf_feed_buy_hid:        str = None
    
    
    user_id:                int = 0
    pf_feed_buy_id:         int = 0
    pig_farm_id:            int = 0
    feed_supplier_id:       int = 0
        
    date_buy:               str 
    
    other_cost:             float = None

    
    

class DataPigFarmFeedBuyItem(BaseModel):
    uhid:                   str = None
    
    pig_farm_feed_buy_hid:  str = None
    
    pf_feed_buy_item_hid:   str = None
    
    feed_type_hid:          str = None
    feed_brand_hid :        str = None
    
    
    user_id:                int = 0
    
    pig_farm_feed_buy_id:   int = 0
    pf_feed_buy_item_id:    int = 0
    
    
    feed_type_id:           int = 0
    feed_brand_id:          int = 0
    
    quantity:               int = 0
    unit_weight:            float
    
    unit_cost:              float
    total_cost:             float


    



class DataAccountPigOps(BaseModel):
    uhid:                   str = None
    account_pig_ops_hid:    str = None
    
    
    user_id:                int = 0
    account_pig_ops_id:     int = 0
    operation_type:         int
    
    is_medvac:              int = 0
        
        
    num_days_since:         int
    name:                   str
    short_name:             str = None
    description:            str = None 
    
    
class DataAccountMedVac(BaseModel):
    uhid:                   str = None
    account_medvac_hid:     str = None
    medvac_brand_hid:       str = None
    medvac_type_hid:        str = None
    
    
    user_id:                int = 0
    account_medvac_id:      int = 0
    medvac_brand_id:        int = 0
    medvac_type_id:         int = 0
    
    name:                   str
    
    
    
class DataAccountPigBuyer(BaseModel, HasAddressLevel, HasContactDetails):
    uhid:                   str = None
    account_pig_buyer_hid:  str = None
        
        
    user_id:                int = 0
    account_pig_buyer_id:   int = 0
        
    is_boar_customer:       int = 0
        
    name:                   str
    
    description:            str = None
    
    
    
class DataPigFarmStaff(BaseModel):
    uhid:                   str = None
        
    pig_farm_hid:           str
    pig_farm_staff_hid:     str = None

    
    set_user_as_staff:      int = 0
        
    user_id:                int = 0
    pig_farm_staff_id:      int = 0
    pig_farm_id:            int = 0
        
        
    name:                   str = None
    

    
class DataSowBoar(BaseModel):
    uhid:                   str = None
    pfhid:                  str = None
    sow_boar_hid:           str = None
    parent_sow_hid:         str = None
    parent_boar_hid:        str = None
        
        
    user_id:                int = 0
    sow_boar_id:            int = 0
    pig_farm_id:            int = 0
    parent_sow_id:          int = 0
    parent_boar_id:         int = 0
        
        
    farm_birth_prod_id:     int = 0
    line_id:                int = 0
    sow_status_id:          int = 1
        
    sex:                    str = 'F' # Sow = 'F';  Boar = 'M'
    num_nipples:            int = None
    is_external:            int = 0 # > 0 = not owned by the farm
    is_production_ready:    int = 0 # Needs to be explicitly set
    
    number:                 str = None
    name:                   str = None
    date_of_birth:          str = None
    date_eartag:            str = None
    notes:                  str = None


class DataBoarExternalMate(BaseModel):
    uhid:                   str = None
    boar_hid:               str = None
    boar_ext_mate_hid:      str = None
    boar_customer_hid:      str = None
        
        
    user_id:                int = 0
    boar_id:                int = 0
    boar_ext_mate_id:       int = 0
    boar_customer_id:       int = 0
    
    customer_sow_name:      str = None   
    date_mate:              str
    date_expected_birth:    str = None
    date_expected_payment:  str = None
    notes:                  str = None


    
    
class DataSowBoarDispose(BaseModel):
    uhid:                   str = None
    sow_boar_hid:           str
        
        
    user_id:                int = 0
    sow_boar_id:            int = 0
        
        
    dispose_status_id:      int
    date_dispose:           datetime.date
    dispose_notes:          str
    
    
class DataPigRaceLine(BaseModel):
    uhid:                   str = None
    pig_race_line_hid:      str = None
        
        
    user_id:                int = 0
    pig_race_line_id:       int = 0
        
        
    pig_race_id:            int
    name:                   str
    description:            str =  None
    

class DataPigPen(BaseModel):
    uhid:                   str = None
    pig_pen_hid:            str = None
        
        
    user_id:                int = 0
    pig_pen_id:             int = 0
        
        
    pig_pen_type_id:        int
    name:                   str


class DataPublicReport(BaseModel):
    uhid:                   str = None
    supplier_hid:           str = None
        
        
    user_id:                int = 0
    supplier_id:            int = 0
    
    report_type:            int 
    notes:                  str = None


class DataCommonSupplier(BaseModel, HasAddressLevel, HasContactDetails):
    uhid:                   str = None
    supplier_hid:           str = None
        
        
    user_id:                int = 0
    supplier_id:            int = 0
    
    is_feed_supplier:       int = 0
    is_gilt_supplier:       int = 0
    is_semen_supplier:      int = 0
        
    name:                   str



class DataSemenSupplier(BaseModel, HasAddressLevel, HasContactDetails):
    uhid:                   str = None
    semen_supplier_hid:     str = None
        
        
    user_id:                int = 0
    semen_supplier_id:      int = 0
        
        
    name:                   str


class DataSemenSupplierSemen(BaseModel):
    uhid:                   str = None
    semen_supplier_hid:     str = None
    semen_sup_semen_hid:    str = None
    
    user_id:                int = 0
    semen_supplier_id:      int = 0
    semen_sup_semen_id:     int = 0
        
    name:                   str

    


class DataFeedBrand(BaseModel):
    uhid:                   str = None
    feed_brand_hid:         str = None
        
        
    user_id:                int = 0
    feed_brand_id:          int = 0
        
        
    country_id:             int = COUNTRY_ID_PHILIPPINES
    name:                   str


class DataFeedSupplier(BaseModel, HasAddressLevel, HasContactDetails):
    uhid:                   str = None
    feed_supplier_hid:      str = None
        
        
    user_id:                int = 0
    feed_supplier_id:       int = 0
        
        
    name:                   str


class DataFeedStartDate(BaseModel):
    uhid:                   str = None
    
    pig_prod_hid:           str = None
    pig_prod_group_hid:     str = None
    feed_type_hid:          str = None
    
    
    user_id:                int = 0
    pig_prod_id:            int = 0
    pig_prod_group_id:      int = 0
    
    feed_type_id:           int = 0
    date_start:             str
    

class DataFeedBuy(BaseModel):
    uhid:                   str = None
    
    pig_farm_hid:           str = None
    pig_prod_hid:           str = None
    pig_prod_group_hid:     str = None
    feed_buy_hid:           str = None
    
    feed_type_hid:          str = None
    feed_brand_hid :        str = None
    feed_supplier_hid:      str = None
    
    
    user_id:                int = 0
    pig_farm_id:            int = 0
    pig_prod_id:            int = 0
    pig_prod_group_id:      int = 0
    feed_buy_id:            int = 0
    
    
    date_buy:               str
    feed_type_id:           int = 0
    feed_brand_id:          int = 0
    feed_supplier_id:       int = 0
    quantity:               int = 0
    unit_weight:            float
    
    unit_cost:              float
    total_cost:             float
    

class DataSemenSource(BaseModel):
    uhid:                   str = None
        
    semen_source_hid:       str = None
    pfhid:                  str = None
    boar_hid:               str = None
    semen_supplier_hid:     str = None
    pig_race_line_hid:      str = None
    
        
    user_id:                int = 0
    semen_source_id:        int = 0
    pig_farm_id:            int = 0
        
    
    boar_id:                int = None
    semen_supplier_id:      int = None
    pig_race_line_id:       int = None
    
    
    name:                   str
    description:            str =  None
    
    
class DataPigProd(BaseModel):
    uhid:                   str = None
        
    pig_prod_hid:           str = None
    sow_hid:                str = None
    boar_hid:               str = None
    
    semen_supplier_hid:     str = None
    semen_sup_semen_hid:    str = None
    semen_ai_boar_hid:      str = None
    
    insem_staff_hid:        str = None
        
    user_id:                int = 0
    pig_prod_id:            int = 0
    sow_id:                 int = 0
    boar_id:                int = None
    
    semen_supplier_id:      int = None
    semen_sup_semen_id:     int = None
    semen_ai_boar_id:       int = None
        
    semen_cost:             float = None
    insem_cost:             float = 0.0
    insem_notes:            str = None
        
    insem_staff_id:         int = 0
    done_by_user:           int = 0
    
    insem_date:             str
    
    
    
    
class DataPigProdAI(BaseModel):
    uhid:                   str = None
        
    pig_prod_ai_hid:        str = None
    pig_prod_hid:           str = None
    semen_source_hid:       str = None
        
    date_extracted:         str = None
    date_expiry:            str
    date_insemination:      str = None
    hour_insemination:      int
        
    staff_id:               int = None
    date_insemination:      str
    

class DataPigProdBirth(BaseModel):
    uhid:                   str = None
        
    pig_prod_hid:           str
    birth_staff_hid:        str = None
        
    user_id:                int = 0
    pig_prod_id:            int = 0  
    date_actual_birth:      str
    num_pigs_dead:          int = 0
        
    num_pigs_male:          int = 0
    num_pigs_female:        int = 0
        
    birth_staff_id:         int = 0
    done_by_user:           int = 0
    
    
class DataPigProdWeaning(BaseModel):
    uhid:                   str = None
        
    pig_prod_hid:           str
        
        
    user_id:                int = 0
    pig_prod_id:            int = 0  
    date_weaning:           str
        
    num_pigs_male:          int = None
    num_pigs_female:        int = None
    
    num_pigs:               int = None
        
    total_weight:           float = None
    weight_pp:              str = None
    
    
class DataPigProdStatus(BaseModel):
    uhid:                   str = None
        
    pig_prod_hid:           str
        
    user_id:                int = 0
    pig_prod_id:            int = 0
    prod_status_id:         int = 0
    date_status:            str
    notes:                  str = None
    
    
class DataPigProdFattening(BaseModel):
    uhid:                   str = None
        
    pig_farm_hid:           str = None
    
    
    user_id:                int = 0
    pig_farm_id:            int = 0
    num_pigs:               int
    
    date_weaning:           str
    date_added:             str
    
    
class DataPigProdDeadPig(BaseModel):
    uhid:                   str = None
    
    pig_prod_hid:           str = None
    pig_prod_group_hid:     str = None
    pig_prod_pig_dead_hid:  str = None
    pig_dead_type_hid:      str
    
    user_id:                int = 0
    pig_prod_id:            int = 0
    pig_prod_group_id:      int = 0
    pig_prod_pig_dead_id:   int = 0
    pig_dead_type_id:       int = 0
    
    date_dead:              str
    num_pigs_dead:          int = 1
    notes:                  str = None
    
    
class DataPigProdNotes(BaseModel):
    uhid:                   str = None
        
    pig_prod_hid:           str = None
    sow_boar_hid:           str = None
    pig_prod_notes_hid:     str = None
        
    is_health_issue:        int = 0
        
    user_id:                int = 0
    pig_prod_id:            int = 0
    sow_boar_id:            int = 0
    production_group_id:    int = 0
    pig_prod_notes_id:      int = 0
    date_notes:             str = None
    notes:                  str


class DataPigProdFeed(BaseModel):
    uhid:                   str = None
        
    pig_prod_feed_hid:      str = None
    pig_prod_hid:           str = None
    pig_farm_feed_buy_hid:  str = None
    
    
    user_id:                int = 0
    pig_prod_feed_id:       int = 0
    pig_prod_id:            int = 0
    pig_farm_feed_buy_id:   int = 0
    
    
    date_add:               str
    
    
    num_gesta:              int = None
    num_lacta:              int = None
    num_booster:            int = None
    num_prestarter:         int = None
    num_starter:            int = None
    num_grower:             int = None
    num_finisher:           int = None

    


class DataMedVacBrand(BaseModel):
    uhid:                   str = None
    medvac_brand_hid:       str = None
    country_hid:            str = None
        
    user_id:                int = 0
    medvac_brand_id:        int = 0
        
        
    country_id:             int = COUNTRY_ID_PHILIPPINES
    name:                   str


class DataMedVacType(BaseModel):
    uhid:                   str = None
    medvac_type_hid:        str = None
        
    user_id:                int = 0
    medvac_type_id:        int = 0
        
        
    name:                   str





class DataPigMedvac(BaseModel):
    uhid:                   str = None
    pig_medvac_hid:         str = None
        
    sow_boar_hid:           str = None
    pig_prod_hid:           str = None
    pig_prod_pig_ops_hid:   str = None
    health_issue_hid:       str = None
    
    staff_hid:              str = None
    
    medvac_brand_hid:       str = None
    medvac_type_hid:        str = None
    acc_medvac_hid:         str = None
    
    date_medvac:            str
    
    user_id:                int = 0
    pig_medvac_id:          int = 0
    sow_boar_id:            int = 0
    pig_prod_id:            int = 0
    pig_prod_pig_ops_id:    int = 0
    health_issue_id:        int = 0
    
    
    medvac_brand_id:        int = 0
    medvac_type_id:         int = 0
    acc_medvac_id:          int = 0
    
    
    staff_id:               int = 0
    done_by_user:           int = 0
    
    notes:                  str = None
   


class DataPigProdPigCount(BaseModel):
    uhid:                   str = None
        
    pig_prod_hid:           str = None
        
        
    user_id:                int = 0
    pig_prod_id:            int = 0
    num_pigs:               int
    date_notes:             str = None
    notes:                  str

    
class DataPigProdPigOps(BaseModel):
    uhid:                   str = None
    
    pig_prod_pig_ops_hid:   str = None
    staff_hid:              str = None
    
    medvac_brand_hid:       str = None
    medvac_type_hid:        str = None
    acc_medvac_hid:         str = None
    
    
    user_id:                int = 0
    pig_prod_pig_ops_id:    int = 0
    staff_id:               int = 0
    done_by_user:           int = 0
    
    
    medvac_brand_id:        int = 0
    medvac_type_id:         int = 0
    acc_medvac_id:          int = 0
    
    
    date:                   str
    notes:                  str = None
    
 
class DataFeedBalance(BaseModel):
    uhid:                   str = None
    
    pig_farm_hid:           str = None
    pig_prod_hid:           str = None
    pig_prod_group_hid:     str = None
    feed_balance_hid:       str = None
    
    
    user_id:                int = 0
    pig_farm_id:            int = 0
    pig_prod_id:            int = 0
    pig_prod_group_id:      int = 0
    feed_balance_id:        int = 0
    
    
    date_balance:           str
    
    num_pigs:               int = None
    
    num_gesta:              float | None = None
    num_lacta:              float | None = None
    num_booster:            float | None = None
    num_prestarter:         float | None = None
    num_starter:            float | None = None
    num_grower:             float | None = None
    num_finisher:           float | None = None
    
    
class DataProductionHarvest(BaseModel):
    uhid:                   str = None
    
    pig_prod_hid:           str = None
    production_group_hid:   str = None
    harvest_type_hid:       str = None 
    acc_pig_buyer_hid:      str = None
    prod_harvest_hid:       str = None
    
    
    user_id:                int = 0
    pig_prod_id:            int = 0
    production_group_id:    int = 0
    acc_pig_buyer_id:       int = 0
    prod_harvest_id:        int = 0
    
    date_harvest:           str
    num_pigs:               int
    harvest_type_id:        int = 0
    
    live_weight:            float = None
    live_price:             float = None
    
    slaughter_weight:       float = None
    slaughter_minus_weight: float = None
    slaughter_price:        float = None
    
    net_sales:              float = None
    harvest_cost:           float = None
    comments:               str = None
    
    weight_pp_lw_csv:       str = None
    weight_pp_sw_csv:       str = None
    
    
class DataReport(BaseModel):
    uhid:                   str = None
    report_hid:             str = None
    pig_farm_hid:           str = None
    
    user_id:                int = 0
    report_id:              int = 0
    report_type_id:         int
    
    language:               str = None
    
    report_date:            str = None
    notes:                  str = None
    file_path:              str = None
    
