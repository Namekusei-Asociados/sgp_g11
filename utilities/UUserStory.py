class UUserStory:
    """
        Esta clase contiene utilidades generales para la logica relacionada a la app Sprint
    """
    STATUS_SUCCESS = "success"
    STATUS_PENDING = "pending"
    STATUS_FINISHED = "finished"
    STATUS_CANCELED = "canceled"
    STATUS_IN_EXECUTION = "in execution"
    # CUSTOM FIELDS LOGIC

    CUSTOM_FIELD_TYPE_DATE = 'Fecha'
    CUSTOM_FIELD_TYPE_TEXT = 'Texto'
    CUSTOM_FIELD_TYPE_NUMBER = 'Numero'

    CUSTOM_FIELDS_LIST = [CUSTOM_FIELD_TYPE_DATE, CUSTOM_FIELD_TYPE_TEXT, CUSTOM_FIELD_TYPE_NUMBER]

    @staticmethod
    def get_status_success():
        return UUserStory.STATUS_SUCCESS

    @staticmethod
    def get_status_in_progress():
        return UUserStory.STATUS_SUCCESS

    @staticmethod
    def get_status_finished():
        return UUserStory.STATUS_FINISHED
