
import datetime

from pydantic               import BaseModel


COUNTRY_ID_PHILIPPINES      = 1


class HasAddressLevel:
    country_id:             int = 1     # default to PH
    level_1_hid:            str = None
    level_2_hid:            str = None
    level_3_hid:            str = None
    
    level_1_id:             int = 0
    level_2_id:             int = 0
    level_3_id:             int = 0
    
    latitude:               float = None
    longitude:              float = None
    
    
    
class HasContactDetails:
    contact_number:         str = None
    whatsapp:               str = None
    messenger:              str = None
    



class DataUser(BaseModel):
    name_last:              str
    name_first:             str
    email:                  str
    country_code:           int = 63    # default to PH
    mobile_num:             str


class DataAccount(BaseModel):
    uhid:                   str
    user_id:                int = 0
    name:                   str
    country_id:             int = COUNTRY_ID_PHILIPPINES
    

class DataAccountSettings(BaseModel):
    uhid:                   str
    user_id:                int = 0
    
    day_1_on_date_of_birth: int = 1
    day_1_on_date_insem:    int = 0
    days_wean:              int = 42
    days_harvest_from_birth:int = 142
    days_harvest_from_wean: int = 100


class DataAccountSelection(BaseModel):
    uhid:                   str
    
    feed_brand_hid:         str = None
    feed_supplier_hid:      str = None
    semen_supplier_hid:     str = None
    
    user_id:                int = 0
    feed_brand_id:          int = 0
    feed_supplier_id:       int = 0
    semen_supplier_id:      int = 0
    

class DataPigFarm(BaseModel, HasAddressLevel):
    uhid:                   str
    pig_farm_hid:           str = None
        
        
    user_id:                int = 0
    pig_farm_id:            int = 0
        
        
    name:                   str
    
    latitude:               float = None
    longitude:              float = None


class DataAccountPigOps(BaseModel):
    uhid:                   str
    account_pig_ops_hid:    str = None
    
    
    user_id:                int = 0
    account_pig_ops_id:     int = 0
    operation_type:         int
        
        
    num_days_since:         int
    name:                   str
    short_name:             str = None
    description:            str = None 
    
    
class DataAccountPigBuyer(BaseModel, HasAddressLevel, HasContactDetails):
    uhid:                   str
    account_pig_buyer_hid:  str = None
        
        
    user_id:                int = 0
    account_pig_buyer_id:   int = 0
        
        
    name:                   str
    contact_number:         str = None
    whatsapp:               str = None
    messenger:              str = None
    description:            str = None
    
    
    
class DataPigFarmStaff(BaseModel):
    uhid:                   str
        
    pig_farm_hid:           str
    pig_farm_staff_hid:     str = None

    
    set_user_as_staff:      int = 0
        
    user_id:                int = 0
    pig_farm_staff_id:      int = 0
    pig_farm_id:            int = 0
        
        
    name:                   str = None
    

    
class DataSowBoar(BaseModel):
    uhid:                   str
    pfhid:                  str = None
    sow_boar_hid:           str = None
        
        
    user_id:                int = 0
    sow_boar_id:            int = 0
    pig_farm_id:            int = 0
        
        
    farm_birth_prod_id:     int = 0
    line_id:                int = 0
    sow_status_id:          int = 2 # This needs to be properly set
        
    sex:                    str = 'F' # Sow = 'F';  Boar = 'M'
    num_nipples:            int = None
    is_external:            int = 0 # > 0 = not owned by the farm
    is_production_ready:    int = 0 # Needs to be explicitly set
    
    number:                 str = None
    name:                   str = None
    date_of_birth:          str = None
    date_eartag:            str = None
    notes:                  str = None
    
    
class DataSowBoarDispose(BaseModel):
    uhid:                   str
    sow_boar_hid:           str
        
        
    user_id:                int = 0
    sow_boar_id:            int = 0
        
        
    dispose_status_id:      int
    date_dispose:           datetime.date
    dispose_notes:          str
    
    
class DataPigRaceLine(BaseModel):
    uhid:                   str
    pig_race_line_hid:      str = None
        
        
    user_id:                int = 0
    pig_race_line_id:       int = 0
        
        
    pig_race_id:            int
    name:                   str
    description:            str =  None
    

class DataPigPen(BaseModel):
    uhid:                   str
    pig_pen_hid:            str = None
        
        
    user_id:                int = 0
    pig_pen_id:             int = 0
        
        
    pig_pen_type_id:        int
    name:                   str


class DataSemenSupplier(BaseModel, HasAddressLevel, HasContactDetails):
    uhid:                   str
    semen_supplier_hid:     str = None
        
        
    user_id:                int = 0
    semen_supplier_id:      int = 0
        
        
    name:                   str


class DataSemenSupplierSemen(BaseModel):
    uhid:                   str
    semen_supplier_hid:     str = None
    semen_sup_semen_hid:    str = None
    
    user_id:                int = 0
    semen_supplier_id:      int = 0
    semen_sup_semen_id:     int = 0
        
    name:                   str

    


class DataFeedBrand(BaseModel):
    uhid:                   str
    feed_brand_hid:         str = None
        
        
    user_id:                int = 0
    feed_brand_id:          int = 0
        
        
    country_id:             int = COUNTRY_ID_PHILIPPINES
    name:                   str


class DataFeedSupplier(BaseModel, HasAddressLevel, HasContactDetails):
    uhid:                   str
    feed_supplier_hid:      str = None
        
        
    user_id:                int = 0
    feed_supplier_id:       int = 0
        
        
    name:                   str


class DataFeedStartDate(BaseModel):
    uhid:                   str
    
    pig_prod_hid:           str = None
    pig_prod_group_hid:     str = None
    feed_type_hid:          str = None
    
    
    user_id:                int = 0
    pig_prod_id:            int = 0
    pig_prod_group_id:      int = 0
    
    feed_type_id:           int = 0
    date_start:             str
    

class DataFeedBuy(BaseModel):
    uhid:                   str
    
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
    uhid:                   str
        
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
    uhid:                   str
        
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
        
    insem_staff_id:         int = None
    insem_date:             str
    
    
class DataPigProdAI(BaseModel):
    uhid:                   str
        
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
    uhid:                   str
        
    pig_prod_hid:           str
    birth_staff_hid:        str
        
    user_id:                int = 0
    pig_prod_id:            int = 0  
    date_actual_birth:      str
    num_pigs_dead:          int = 0
        
    num_pigs_male:          int = 0
    num_pigs_female:        int = 0
        
    birth_staff_id:         int = 0
    
    
class DataPigProdWeaning(BaseModel):
    uhid:                   str
        
    pig_prod_hid:           str
        
        
    user_id:                int = 0
    pig_prod_id:            int = 0  
    date_weaning:           str
        
    num_pigs_male:          int = 0
    num_pigs_female:        int = 0
        
    total_weight:           int = None
    
    
class DataPigProdStatus(BaseModel):
    uhid:                   str
        
    pig_prod_hid:           str
    prod_status_hid:        str
        
    user_id:                int = 0
    pig_prod_id:            int = 0
    prod_status_id:         int = 0
    date_status:            str
    notes:                  str = None
    
    
class DataPigProdFattening(BaseModel):
    uhid:                   str
        
    pig_farm_hid:           str = None
    
    
    user_id:                int = 0
    pig_farm_id:            int = 0
    num_pigs:               int
    
    date_weaning:           str
    date_added:             str
    
    
class DataPigProdDeadPig(BaseModel):
    uhid:                   str
    
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
    uhid:                   str
        
    pig_prod_hid:           str = None
    sow_boar_hid:           str = None
    pig_prod_notes_hid:     str = None
        
        
    user_id:                int = 0
    pig_prod_id:            int = 0
    sow_boar_id:            int = 0
    production_group_id:    int = 0
    pig_prod_notes_id:      int = 0
    date_notes:             str = None
    notes:                  str
    
    
class DataPigProdPigCount(BaseModel):
    uhid:                   str
        
    pig_prod_hid:           str = None
        
        
    user_id:                int = 0
    pig_prod_id:            int = 0
    num_pigs:               int
    date_notes:             str = None
    notes:                  str

    
class DataPigProdPigOps(BaseModel):
    uhid:                   str
    
    pig_prod_pig_ops_hid:   str = None
    staff_hid:              str
    
    user_id:                int = 0
    pig_prod_pig_ops_id:    int = 0
    staff_id:               int = 0
    
    date:                   str
    notes:                  str = None
    
 
class DataProdFeedBal(BaseModel):
    uhid:                   str
    
    pig_prod_hid:           str = None
    pig_prod_group_hid:     str = None
    feed_balance_hid:       str = None
    
    
    user_id:                int = 0
    pig_prod_id:            int = 0
    pig_prod_group_id:      int = 0
    feed_balance_id:        int = 0
    
    
    date_balance:           str
    
    num_pigs:               int = None
    
    num_gestating:          float = None
    num_lactating:          float = None
    num_booster:            float = None
    num_prestarter:         float = None
    num_starter:            float = None
    num_grower:             float = None
    num_finisher:           float = None
    
    
class DataProductionHarvest:
    uhid:                   str
    
    pig_prod_hid:           str = None
    production_group_hid:   str = None
    acc_pig_buyer_hid:      str = None
    production_harvest_hid: str = None
    
    
    user_id:                int = 0
    pig_prod_id:            int = 0
    production_group_id:    int = 0
    acc_pig_buyer_id:       int = 0
    production_harvest_id:  int = 0
    
    date_harvest:           str
    num_pigs_harvest:       int
    harvest_type_id:        int
    
    live_weight:            float = None
    live_price_per_unit:    float = None
    
    slaughter_weight:       float = None
    slaughter_net_weight:   float = None
    slaughter_price_per_unit: float = None
    
    net_sales:              float = None
    harvest_cost:           float = None
    comments:               str = None
    
    