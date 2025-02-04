from src.service.feature_switch_service import FeatureSwitchService

class FeatureSwitchHandler:
    def __init__(self, service: FeatureSwitchService):
        self.service = service

    def check_registration_status(self) -> bool:
        return self.service.is_registration_open()