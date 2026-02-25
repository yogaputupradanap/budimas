from . import BaseServices
from apps.handler import handle_error
from apps.lib.convert_uom import convert_uom

class ProdukUOM(BaseServices):
    def getFactorKonversi(self, id_produk):
        return (
            self.query().setRawQuery(
                f"""
                    select faktor_konversi as fk, level
                    from produk_uom
                    where id_produk = { id_produk }
                    order by level asc
                """
            )
            .execute()
            .fetchall()
            .get()
        )

    def converterObj(self, sourceObj):
        id_produk = sourceObj["id_produk"]
        uom_1 = sourceObj["uom_1"]
        uom_2 = sourceObj["uom_2"]
        uom_3 = sourceObj["uom_3"]

        produk_uoms = self.getFactorKonversi(id_produk)
        fk = [uom['fk'] for uom in produk_uoms]

        uom_obj = {'pieces': uom_3, 'box': uom_2, 'karton': uom_1}
        fk_obj = {'pieces': fk[0], 'box': fk[1], 'karton': fk[2]}

        return {"uom_obj": uom_obj, "fk_obj": fk_obj}

    @handle_error
    def convertUom(self, to, convert_obj):
        obj = self.converterObj(convert_obj)
        uom_obj = obj['uom_obj']
        fk_obj = obj['fk_obj']

        jumlah = convert_uom(uom_obj, fk_obj).convert_to(to).get()

        return jumlah[to]

    @handle_error
    def getUoms(self, methodProducts = None):
        products = self.req("products") or methodProducts
        result = []

        for product in products:
            obj = self.converterObj(product)
            uom_obj = obj['uom_obj']
            fk_obj = obj['fk_obj']

            uoms = convert_uom(uom_obj, fk_obj).convert_to('pieces').to_uoms().get()
            product_uom = {}

            for key, value in uoms.items():
                product_uom[key] = value

            result.append(product_uom)

        return result