from fastapi import HTTPException, status


def repeat(massage: str = "已存在，不能重复添加"):
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=massage)


def time_out(massage: str = "请求超时"):
    return HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail=massage)


def unauthorized(massage: str = "未授权"):
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=massage)


def not_validate_credentials(massage: str = "Could not validate credentials"):
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=massage)

def not_validate_credentials(massage: str = "Could not validate credentials"):
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=massage)

