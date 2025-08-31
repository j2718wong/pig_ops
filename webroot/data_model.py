
import datetime

from pydantic               import BaseModel


COUNTRY_ID_PHILIPPINES      = 1

class DataUser(BaseModel):
    username:           str
    name_last:          str
    name_first:         str
    email:              str
    password:           str
    country_code:       int = 63    # default to PH
    mobile_num:         str


class DataAccount(BaseModel):
    uhid:               str
    user_id:            int = 0
    name:               str
    country_id:         int = COUNTRY_ID_PHILIPPINES
    

class DataAccountPigOps(BaseModel):
    uhid:               str
    account_pig_ops_hid: str = None
    
    
    user_id:            int = 0
    account_pig_ops_id: int = 0
    operation_type:     int
    
    
    num_days_since:     int
    name:               str
    description:        str = None 
    

class DataPigFarm(BaseModel):
    uhid:               str
    pig_farm_hid:       str = None
    
    
    user_id:            int = 0
    pig_farm_id:        int = 0
    
    
    name:               str
    country_id:         int = 1     # default to PH
    adrs_level_1_id:    int = 0
    adrs_level_2_id:    int = 0
    adrs_level_3_id:    int = 0
    latitude:           float = None
    longitude:          float = None
    
    
class DataPigFarmStaff(BaseModel):
    uhid:               str
    
    pig_farm_hid:       str
    pig_farm_staff_hid: str = None
    
    
    user_id:            int = 0
    pig_farm_staff_id:  int = 0
    pig_farm_id:        int = 0
    
    
    name:               str
    

    
class DataSowBoar(BaseModel):
    uhid:               str
    pfhid:              str = None
    sow_boar_hid:       str = None
    
    
    user_id:            int = 0
    sow_boar_id:        int = 0
    pig_farm_id:        int = 0
    
    
    farm_birth_prod_id: int = 0
    line_id:            int = 0
    sow_status_id:      int = 2
    
    sex:                str = 'F' # Sow = 'F';  Boar = 'M'  
    
    number:             str = None
    name:               str = None
    date_of_birth:      str = None
    notes:              str = None
    
    
class DataSowBoarDispose(BaseModel):
    uhid:               str
    sow_boar_hid:       str
    
    
    user_id:            int = 0
    sow_boar_id:        int = 0
    
    
    dispose_status_id:  int
    date_dispose:       datetime.date
    dispose_notes:      str
    
    
class DataPigRaceLine(BaseModel):
    uhid:               str
    pig_race_line_hid:  str = None
    
    
    user_id:            int = 0
    pig_race_line_id:   int = 0
    
    
    pig_race_id:        int
    name:               str
    description:        str =  None


class DataSemenSupplier(BaseModel):
    uhid:               str
    semen_supplier_hid: str = None
    
    
    user_id:            int = 0
    semen_supplier_id:  int = 0
    
    
    country_id:         int = COUNTRY_ID_PHILIPPINES
    address_level_1_id: int
    address_level_2_id: int
    name:               str


class DataFeedBrand(BaseModel):
    uhid:               str
    feed_brand_hid:     str = None
    
    
    user_id:            int = 0
    feed_brand_id:      int = 0
    
    
    country_id:         int = COUNTRY_ID_PHILIPPINES
    name:               str


class DataFeedSupplier(BaseModel):
    uhid:               str
    feed_supplier_hid:  str = None
    
    
    user_id:            int = 0
    feed_supplier_id:   int = 0
    
    
    country_id:         int = COUNTRY_ID_PHILIPPINES
    address_level_1_id: int
    address_level_2_id: int
    name:               str


class DataSemenSource(BaseModel):
    uhid:               str
    
    semen_source_hid:   str = None
    pfhid:              str = None
    boar_hid:           str = None
    semen_supplier_hid: str = None
    pig_race_line_hid:  str = None

    
    user_id:            int = 0
    semen_source_id:    int = 0
    pig_farm_id:        int = 0
    

    boar_id:            int = None
    semen_supplier_id:  int = None
    pig_race_line_id:   int = None
    
    
    name:               str
    description:        str =  None
    
    
class DataPigProd(BaseModel):
    uhid:               str
    
    pig_prod_hid:       str = None
    sow_hid:            str = None
    boar_hid:           str = None
    semen_source_hid:   str = None
    insem_staff_hid:    str = None
    
    user_id:            int = 0
    pig_prod_id:        int = 0
    sow_id:             int = 0
    boar_id:            int = None
    semen_source_id:    int = None
    
    semen_cost:         float = 0.0
    insemination_cost:  float = 0.0
    insem_cost_comments: str = None
    
    insem_staff_id:     int = None
    date_insemination:  str
    
    
class DataPigProdAI(BaseModel):
    uhid:               str
    
    pig_prod_ai_hid:    str = None
    pig_prod_hid:       str = None
    semen_source_hid:   str = None
    
    date_extracted:     str = None
    date_expiry:        str
    date_insemination:  str = None
    hour_insemination:  int
    
    staff_id:           int = None
    date_insemination:  str
    

class DataPigProdBirth(BaseModel):
    uhid:               str
    
    pig_prod_hid:       str
    birth_staff_hid:    str
    
    user_id:            int = 0
    pig_prod_id:        int = 0  
    date_actual_birth:  str
    num_pigs_dead:      int = 0
    
    num_pigs_male:      int = 0
    num_pigs_female:    int = 0
    
    birth_staff_id:     int = 0
    
    
class DataPigProdWeaning(BaseModel):
    uhid:               str
    
    pig_prod_hid:       str
    
    
    user_id:            int = 0
    pig_prod_id:        int = 0  
    date_weaning:       str
    
    num_pigs_male:      int = 0
    num_pigs_female:    int = 0
    
    total_weight:       int = None
    

class DataPigProdPigCount(BaseModel):
    uhid:               str
    
    pig_prod_hid:       str
    
    
    pig_prod_id:        int = 0  
    
    num_pigs_male:      int = 0
    num_pigs_female:    int = 0
    
    
class DataPigProdDeadPig(BaseModel):
    uhid:               str
    
    pig_prod_hid:       str = None
    pig_prod_pig_dead_hid:  str = None
    
    
    user_id:                int = 0
    pig_prod_id:            int = 0
    pig_prod_pig_dead_id:   int = 0
    date_dead:          str
    dead_type_id:       int = 0
    sex:                str = 'F'
    comments:           str = None
    
    
class DataPigProdNotes(BaseModel):
    uhid:               str
    
    pig_prod_hid:       str = None
    pig_prod_notes_hid: str = None
    
    
    user_id:            int = 0
    pig_prod_id:        int = 0
    pig_prod_notes_id:  int = 0
    notes:              str
    
    
class DataProdGestatingOps(BaseModel):
    uhid:               str
    
    prod_gestating_ops_hid: str = None
    staff_hid:          str
    
    user_id:            int = 0
    prod_gestating_ops_id:  int = 0
    staff_id:           int = 0
    date:               str
    notes:              str = None
    
    
class DataProdLactatingOps(BaseModel):
    uhid:               str
    
    prod_lactating_ops_hid: str = None
    staff_hid:          str
    
    user_id:            int = 0
    prod_lactating_ops_id:  int = 0
    staff_id:           int = 0
    date:               str
    notes:              str = None
    
    
class DataProdFeedBuy(BaseModel):
    uhid:               str
    
    pig_prod_hid:       str = None
    prod_feed_buy_hid:  str = None
    
    
    user_id:            int = 0
    pig_prod_id:        int = 0
    prod_feed_buy_id:   int = 0
    
    
    date_buy:           str
    feed_type_id:       int
    feed_brand_id:      int
    feed_supplier_id:   int
    kg_per_quantity:    float
    
    unit_cost:          float
    total_cost:         float
    