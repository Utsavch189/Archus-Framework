from .service import handel_user,handel_me

v1_urls=[
    {'path': '/users', 'method': ['GET'], 'handler': handel_user},
    {'path': '/me', 'method': ['GET','POST'], 'handler': handel_me}
]

