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
            users.id_cabang,
            users.password
            from users 
            where users.email = :email
        """
        login_bindparam = {'email': email}

        user = self.query().setRawQuery(login_query).bindparams(login_bindparam).execute().fetchone().result
        print(user)
        if not user:
            raise nonServerErrorException(401, "Email salah atau tidak ada")

        # Convert password input to bytes
        password_bytes = password.encode('utf-8')
        # Convert stored hash from database to bytes if it's not already
        stored_hash = user['password'].encode('utf-8') if isinstance(user['password'], str) else user['password']

        # Verify password using bcrypt
        if not bcrypt.checkpw(password_bytes, stored_hash):
            raise nonServerErrorException(401, "Password Salah")

        return user