from apps.services.BaseServices import BaseServices
from apps.handler import nonServerErrorException, handle_error
import bcrypt

class Auth(BaseServices):
    def __init__(self):
        super().__init__()
    
    @handle_error
    def login(self):
        email = self.req('email')
        password = self.req('password')
        
        login_query = f"""
            select 
            users.tokens AS token,
            users.id AS id_user,
            users.nama AS nama_user,
            users.email AS user_email,
            users.id_jabatan,
            users.password
            from users 
            where users.email = :email
            and users.id_jabatan in (21,2)
        """
        login_bindparam = {'email': email}
        
        user = self.query().setRawQuery(login_query).bindparams(login_bindparam).execute().fetchone().result
        print("user", user)
        if not user:
            raise nonServerErrorException(401, "Email salah atau tidak ada")
        
        if not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            raise nonServerErrorException('Password salah', 403)
        
        return user