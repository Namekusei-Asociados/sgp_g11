class UProject:
    """
        Esta clase contiene utilidades generales para la logica relacionada a la app Project
    """
    STATUS_SUCCESS = "success"
    STATUS_PENDING = "pending"
    STATUS_FINISHED = "finished"

    @staticmethod
    def get_status_success():
        return UProject.STATUS_SUCCESS

    @staticmethod
    def get_status_in_progress():
        return UProject.STATUS_SUCCESS

    @staticmethod
    def get_status_finished():
        return UProject.STATUS_FINISHED


