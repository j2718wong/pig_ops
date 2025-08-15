from pydantic               import BaseModel


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
    name:               str
    country_id:         int = 1     # default to PH
    

class DataPigFarm(BaseModel):
    uhid:               str
    pig_farm_hid:       str = None
    
    name:               str
    country_id:         int = 1     # default to PH
    adrs_level_1_id:    int = 0
    adrs_level_2_id:    int = 0
    adrs_level_3_id:    int = 0
    latitude:           float = None
    longitude:          float = None
    
    
class DataSow(BaseModel):
    uhid:               str,
    pfhid:              str,
    production_id:      int = 0
    line_id:            int = 0
    
    sow_number:         str,
    sow_name:           str = None,
    date_of_birth:      str = None,
    description:        str = None
    
    