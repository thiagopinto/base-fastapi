from app.core.user.models import Users, Scopes

async def run():

    scope_all = Scopes(name='*', description="Permissions allowed to all resources")
    await scope_all.save()

    password_hash = Users.get_hashed_password('secret')

    user_admin = Users(name='Thiago Pinto Dias', email='thiago@codebr.dev', password_hash=password_hash, verified_is=True)
    await user_admin.save()
    await scope_all.users.add(user_admin)
 
    user = await Users.get_or_none(id=1)
    scope_admin = Scopes(name='admin:all', description="Permissions allowed to administrations resources")
    await scope_admin.save()
    await user.scopes.add(scope_admin)
    await user.save()
    print(user)
    async for scope in user.scopes:
        print(scope)

