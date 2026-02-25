from . import BaseServices
from apps.handler import handle_error

class Armada(BaseServices):

    @handle_error
    def getAllArmada(self):
        id_cabang = self.req('id_cabang')
        return self.query().setRawQuery('SELECT * FROM armada where id_cabang =:id_cabang').bindparams({
            "id_cabang": id_cabang
        }).execute().fetchall().get()