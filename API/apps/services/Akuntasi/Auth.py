import bcrypt
from apps.services import BaseServices
from apps.handler import nonServerErrorException, handle_error

class Auth(BaseServices):
    def __init__(self):
        super().__init__()
    
    @handle_error
    def login(self):
        email = self.req('email')
        password_input = self.req('password') # Password dari form login
        
        login_query = """
            SELECT users.tokens, users.id, users.nama, users.email, 
                   users.id_jabatan, users.password
            FROM users 
            WHERE users.email = :email
            AND users.id_jabatan IN (15, 16, 2)
        """
        
        user = self.query().setRawQuery(login_query).bindparams({'email': email}).execute().fetchone().result
        
        if not user:
            raise nonServerErrorException(401, "Email salah atau tidak ditemukan")
        
        # --- VERIFIKASI BCRYPT ---
        # Password di DB biasanya disimpan dalam format: $2b$12$R9h/cIPz...
        hashed_password_db = user['password'].encode('utf-8') 
        
        # Cek apakah password input cocok dengan hash di DB
        if not bcrypt.checkpw(password_input.encode('utf-8'), hashed_password_db):
            raise nonServerErrorException(401, "Password Salah")
        
        # Hapus hash password dari dictionary sebelum dikirim ke frontend demi keamanan
        user.pop('password', None)
        
        return user