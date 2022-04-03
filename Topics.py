'''
Conatins the topic used by mqtt protocols
'''


class Topic_Wrapper():
    def __init__(self, center_name: str, group_name: str = 'G9'):
        self.center_name = center_name
        self.group_name = group_name

    def __call__(self, topic: str) -> str:
        return f"{self.group_name}/{self.center_name}/{topic}"


class CCC:
    _ccc = Topic_Wrapper('CCC')

    ###Topics
    TEMPERATURE = _ccc("TEMPERATURE")  ###ccc->
    SYS_ERR = _ccc("SYS_ERR")  # ccc->
    MORSE_SEND = _ccc("MORSE_CODE")  # ccc->
    MORSE_ACCESS = _ccc("MORSE_VALIDATE")  # ->cc
    ALARM_ON = _ccc("ALARM_ON") # ->ccc
    RAISE_ALARM = _ccc("ALARM_RAISE") # ccc->
    LOCKDOWN = _ccc("LOCKDOWN")
    STATUS = _ccc("STATUS")
    #Topic Payloads
    ACESS_GRANTED = "GRANTED"
    ACESS_DENIED = "DENIED"
    LOCKED = "LOCKED"
    UNLOCKED = "UNLOCKED"
    SECURE = "SECURE"
    INSECURE = "INSECURE"


class CCS:
    _ccs = Topic_Wrapper('CCS')

    SYS_ERR = _ccs("SYS_ERR")


class PO:
    _po = Topic_Wrapper('PO')

    TEMPERATURE = _po("TEMPERATURE")
    SYS_ERR = _po("SYS_ERR")
    KNOCK_SEND = _po("KNOCK_CODE")
    KNOCK_ACCESS = _po("KNOCK_ACCESS")
    ALARM_ON = _po("ALARM_ON")
    RAISE_ALARM = _po("ALARM_RAISE")
    PANIC_BUTTON = _po("PANIC_BUTTON")
    LOCKDOWN = _po("LOCKDOWN")

class CDR:

    _cdr = Topic_Wrapper('CDR')

    ###Topics
    TEMPERATURE = _cdr("TEMPERATURE")
    LIGHT_INTENSITY = _cdr("LIGHT_INTENSITY")
    FLOOR_PRESSURE = _cdr("FLOOR_PRESSURE") ####
    SYS_ERR = _cdr("SYS_ERR")
    SEQ_SEND = _cdr("SEQ_SEND")
    SEQ_ACCESS = _cdr("SEQ_ACCESS")
    ALARM_ON = _cdr("ALARM_ON")
    RAISE_ALARM = _cdr("ALARM_RAISE")
    LOCKDOWN = _cdr("LOCKDOWN") ####

    #Topic Payloads
    GRANTED_TOPSECRET = "GRANTED TOP SECRET"
    GRANTED_SECRET = "GRANTED SECRET"
    GRANTED_CONFIDENTIAL = "GRANTED CONFIDENTIAL"
    ACCESS_DENIED = "DENIED"
###############################################################


########################DASHBOARD###############################
_dashboard = Topic_Wrapper('DASHBOARD')


#############################################################
