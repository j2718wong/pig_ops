from pydantic               import BaseModel


class DataUser(BaseModel):
    username:           str
    email:              str
    password:           str
    country_code:       int = 63    # default to PH
    mobile_num:         str

