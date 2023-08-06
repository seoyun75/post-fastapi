from domain.user import User
from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from service.user_service import UserService
from tool.security.authorization import Authorization
from tool.session import SessionData, verify_session

router = APIRouter(prefix="/users")


def verify_authority_dependency(
    user: User,
    session_data: SessionData = Depends(verify_session),
    auth=Depends(Authorization),
):
    return auth.verify_authority(user, session_data.user_id)


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    user: User,
    service=Depends(UserService),
):
    """
    회원가입

    Parameters :
        User :
            id : 유저id
            password : 비밀번호
            nickname : 닉네임

    Returns:
        User :
            id : 유저id
            password : 비밀번호
            nickname : 닉네임
            created_at : 생성일자
    """
    new_user = service.create_user(user)
    return JSONResponse(
        content=jsonable_encoder("회원가입 성공"), status_code=status.HTTP_201_CREATED
    )


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update(user_id: str, user: User, service: UserService = Depends()):
    """
    유저 정보 수정

    Parameters :
        User :
            id : 유저id
            password : 비밀번호
            nickname : 닉네임

    Returns:
        User :
            id : 유저id
            password : 비밀번호
            nickname : 닉네임
            created_at : 생성일자
    """
    user.id = user_id
    signin_user = service.update_user(user)
    return JSONResponse(
        content=jsonable_encoder(signin_user), status_code=status.HTTP_200_OK
    )


@router.get("/posts", status_code=status.HTTP_200_OK)
async def get_posts(
    page: int,
    session_data: SessionData = Depends(verify_session),
    service: UserService = Depends(),
):
    """
    유저가 작성한 게시글 목록

    Parameters :
        id : 유저id
        page : 페이지번호

    Returns:
        List[Post]
    """
    user = User()
    user.id = id

    posts = service.get_posts(session_data.user_id, page)
    return JSONResponse(content=jsonable_encoder(posts), status_code=status.HTTP_200_OK)


@router.get("/comments", status_code=status.HTTP_200_OK)
async def get_comments(
    page: int,
    session_data: SessionData = Depends(verify_session),
    service: UserService = Depends(),
):
    """
    유저가 작성한 댓글 목록

    Parameters :
        id : 유저id
        page : 페이지번호

    Returns:
        List[Comment]
    """
    comments = service.get_comments(session_data.user_id, page)
    return JSONResponse(
        content=jsonable_encoder(comments), status_code=status.HTTP_200_OK
    )


@router.delete(
    "",
    dependencies=[Depends(verify_authority_dependency)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    password: str,
    session_data: SessionData = Depends(verify_session),
    service: UserService = Depends(),
):
    """
    유저 탈퇴

    Parameters :
        id : 유저id
        password : 비밀번호
    """
    user = User(id=session_data.user_id, password=password)
    service.delete_user(user)
    return JSONResponse(content=None, status_code=status.HTTP_204_NO_CONTENT)
