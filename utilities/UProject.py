class UProject:
    """
        Esta clase contiene utilidades generales para la logica relacionada a la app Project
    """
    STATUS_SUCCESS = "success"
    STATUS_PENDING = "pending"
    STATUS_FINISHED = "finished"

    # CUSTOM FIELDS LOGIC

    CUSTOM_FIELD_TYPE_DATE = 'Fecha'
    CUSTOM_FIELD_TYPE_TEXT = 'Texto'
    CUSTOM_FIELD_TYPE_NUMBER = 'Numero'

    CUSTOM_FIELDS_LIST = [
        CUSTOM_FIELD_TYPE_DATE,
        CUSTOM_FIELD_TYPE_TEXT,
        CUSTOM_FIELD_TYPE_NUMBER
    ]

    @staticmethod
    def get_status_success():
        return UProject.STATUS_SUCCESS

    @staticmethod
    def get_status_in_progress():
        return UProject.STATUS_SUCCESS

    @staticmethod
    def get_status_finished():
        return UProject.STATUS_FINISHED
