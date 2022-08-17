import os
import redis
import random
import logging
from dataclasses import dataclass

from dotenv import load_dotenv
load_dotenv()

log = logging.getLogger(__name__)


@dataclass
class Phonenumbers:
    r = redis.from_url(os.getenv("REDIS_URL"))
    if r:
        log.info("Connected to Redis")
    db: list = ('+17633702428', '+12622217505')


    def _search(self, number):
        if number not in self.db:
            log.info(f'Number {number} not found in number DB.')
            return True
        else:
            log.info(f'Number {number} found in number DB.')
            return False
    
    def _generate_code(self):
        return random.randint(10000, 99999)
    
    def _save_code(self, number: str, sms_code: str):
        response = self.r.set(number, sms_code)
        if response:
            log.info(f'Saved phone number:{number} with code:{sms_code} to Redis')
        else:
            log.info(f'Failed to save phone number:{number} with code:{sms_code} to Redis')

    def create_validate(self, number):
        """ Used to start and save the code for each 
            number entered. 
        """
        
        employee_verification = self._search(number)
        if employee_verification:
            sms_code = self._generate_code()
            self._save_code(number=number, sms_code=sms_code)
            return {'response': sms_code}
        else:
            return False

    def verify(self, number: str, sms_code: str):
        """ Used to validate that the code entered on the 
            webpage is what was set.  
        """
        try:
            stored_sms_code = self.r.get(number).decode()
            if stored_sms_code == sms_code:
                return True
            else:
                return f"Entered code {sms_code} does not match stored code {stored_sms_code}."
        except:
            return "Could not get entered phone number stored code."

            
