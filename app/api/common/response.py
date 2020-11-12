class ApiResponse:
    @staticmethod
    def __respond(data: dict):
        return data

    @staticmethod
    def api_status(status, data: dict):
        data.update({"status": status})
        return ApiResponse.__respond(data)

    @staticmethod
    def api_failed(message):
        return ApiResponse.api_message(message, "error")

    @staticmethod
    def api_message(message, status: str = "success"):
        return ApiResponse.api_status(status, {"message": message})

    @staticmethod
    def api_success(data, status: str = "success"):
        return ApiResponse.api_status(status, {"data": data})
