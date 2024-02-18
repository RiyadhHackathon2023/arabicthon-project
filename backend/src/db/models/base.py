from sqlalchemy.orm import declarative_base



class BaseProvider:
    _instance = None                                                                                                                    
                                                                                                                                        
    def __new__(cls, *args, **kwargs):                                                                                                  
        if not cls._instance:                                                                                                           
            cls._instance = super().__new__(cls)                                                                                        
        return cls._instance
    
    def __init__(self) -> None:
        self.Base = declarative_base()
    

base_provider = BaseProvider()