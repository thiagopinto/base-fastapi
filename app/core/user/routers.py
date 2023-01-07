from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.models import Status
from app.core.user.models import Users
from app.core.user.serializers import UserIn, UserOut, UserPydantic
from app.core.user.services import Auth, Protect

protect = Protect.end_point_by_password()

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[UserOut])
async def get_users(token: str = Depends(protect)):
    print(token)
    return await UserOut.from_queryset(Users.all())


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    try:
        return await UserOut.from_queryset_single(Users.get(id=user_id))
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.post("/", response_model=UserOut)
async def create_user(user: UserIn):
    if await Users.get_or_none(email=user.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    user_dict = user.dict()
    user_dict["password_hash"] = Users.get_hashed_password(
        user_dict["password"])
    user_dict.pop("password")
    user_obj = await Users.create(**user_dict)
    return await UserOut.from_tortoise_orm(user_obj)


@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user: UserPydantic, token: str = Depends(protect)):
    print(token)
    try:
        await Users.filter(id=user_id).update(**user.dict(exclude_unset=True))
        return await UserOut.from_queryset_single(Users.get(id=user_id))
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.delete("/{user_id}", response_model=Status)
async def delete_user(user_id: int, token: str = Depends(protect)):
    print(token)
    deleted_count = await Users.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User {user_id} not found")
    return Status(message=f"Deleted user {user_id}")


@router.post("/auth/login")
async def login(form_login: OAuth2PasswordRequestForm = Depends()):
    response = await Auth.authenticate(form_login.email, form_login.password)
    return response


@router.post("/auth/refresh")
async def refresh(token: str = Depends(protect)):
    return {"status": True}