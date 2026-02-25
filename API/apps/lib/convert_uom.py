"""
melakukan konversi dari uom satu ke uom lainnya
@param `uom` merupakan object atau dictionary dengan
interface : { pieces?: number, box?: number, karton?: number }
@param `factor` merupakan object atau dictionary dengan
interface : { pieces?: number, box?: number, karton?: number }
@return dictionary dengan value sesuai convert uom yang diinginkan '{`uom`: number}'
"""
from math import floor

class convert_uom():
    def __init__(self, uom, factor):
        self.arr_uom = ['pieces', 'box', 'karton']

        self.uom = {}
        self.pieces_uom = 0
        self.faktorKonversi = {}
        self.result = {}

        self.__set_uom(uom)
        self.__set_factor_conversion(factor)

    def __set_uom(self, uom):
        for key in self.arr_uom:
            self.uom[key] = uom[key] if key in uom else 0

    def __set_factor_conversion(self, fk):
        for key in self.arr_uom:
            self.faktorKonversi[key] = fk[key] if key in fk else 1

    def __get_conversion_factor(self, uom):
        faktor = {}
        faktorKonversi = self.faktorKonversi[uom]

        for key in self.uom.keys():
            if key != uom:
                faktor[key] = self.faktorKonversi[key] / faktorKonversi

        return faktor

    def __get_conversion_calc(self, to, factor):
        result = 0

        for key, value in self.uom.items():
            if key != to:
                result += value * factor[key]

        return result + self.uom[to]

    def __get_uoms_conversion_factor(self):
        faktor = {}

        for key, value in self.faktorKonversi.items():
            if key != 'pieces':
                if key == 'box':
                    faktor['pieces_per_box'] = value
                elif key == 'karton':
                    faktor['boxes_per_carton'] = value / self.faktorKonversi['box']

        return faktor

    def __get_per_uom_conversion(self, fk):
        boxes = self.pieces_uom // fk['pieces_per_box']
        leftover_pieces = self.pieces_uom - (boxes * fk['pieces_per_box'])

        carton = boxes // fk['boxes_per_carton']
        leftover_box = boxes - (carton * fk['boxes_per_carton'])

        self.result["pieces"] = int(leftover_pieces)
        self.result['box'] = int(leftover_box)
        self.result['carton'] = int(carton)

        return self

    def include_tag_end(self):
        with_tag_end = {}

        for key, value in self.result.items():
            tag_end = round(value % 1, 1) * 10
            with_tag_end[key] = { 'value': floor(value), 'tag_end': tag_end }

        self.result = with_tag_end

        return self

    def convert_to(self, uom):
        faktorKonversi = self.__get_conversion_factor(uom)
        self.result[uom] = self.__get_conversion_calc(uom, faktorKonversi)
        self.pieces_uom = self.result[uom]

        return self

    def to_uoms(self):
        faktorKonversi = self.__get_uoms_conversion_factor()
        self.__get_per_uom_conversion(faktorKonversi)

        return self

    def get(self): return self.result