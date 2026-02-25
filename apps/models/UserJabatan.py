from  apps.models  import  BaseModel


class UserJabatan(BaseModel) :
    __tablename__ = 'jabatan'
    kode          = BaseModel.string(10)
    nama          = BaseModel.string(50)
    departemen_id = BaseModel.integer()

    def __repr__(self) :
        return f"data('{self.id}')"