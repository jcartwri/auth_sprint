
async def delete_all_data_from_tables(session, settings):
    await session.delete(settings.SERVICE_URL + 'users')
    await session.delete(settings.SERVICE_URL + 'auth/history')
    await session.delete(settings.SERVICE_URL + 'role/delete/all')
    await session.delete(settings.SERVICE_URL + "delete_user_role/all")
