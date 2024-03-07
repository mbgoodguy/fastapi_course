# @app.get('/users/{user_id}')
# def get_user_by_id(user_id: int):
#     merged_fake_data = {k: v for user_dict in fake_db for k, v in user_dict.items()}
#     print(merged_fake_data)
#     if user_id in merged_fake_data:
#         return {'user_id': user_id, 'user_name': merged_fake_data[user_id]}
#     else:
#         return {'error': f'No such user with id {user_id}'}
#
#
# @app.get('/fake_users')
# def get_fake_users(limit: int = 5):
#     return fake_db[:limit]


# @app.post('/create_user')
# async def create_user(user: UserCreate):
#     users.append(user)
#     return user
#
#
# @app.get('/users')
# async def get_users():
#     return users
