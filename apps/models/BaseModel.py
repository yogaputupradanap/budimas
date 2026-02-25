from  apps.conn2  import  db
import sqlalchemy as sa
from typing import Dict, List, Tuple, Any
class BaseModel(db.Model) :
    __abstract__ = True
    id           = db.Column(db.Integer, primary_key=True)

    def foreign(reference) :
        return db.Column(db.Integer, db.ForeignKey(reference))

    def integer() :
        return db.Column(db.Integer)
    
    def bigInteger():
        return db.Column(db.BigInteger)
    
    def smallInteger():
        return db.Column(db.SmallInteger)

    def float() :
        return db.Column(db.Float)
    
    def string(length) :
        return db.Column(db.String(length))
    
    def date() :
        return db.Column(db.Date)
    
    def time() :
        return db.Column(db.Time)
    
    def one_to_many(ref_table, main_table, key) :
        return db.relationship(ref_table, backref=main_table, foreign_keys=key)
    
    def one_to_many_bi_ref(main_table, ref_table, key) :
        return db.relationship(main_table, back_populates=ref_table, foreign_keys=key)
        
    def one_to_many_bi_main(ref_table, main_table) :
        return db.relationship(ref_table, back_populates=main_table, lazy='dynamic')
    
    def add(self) :
        db.session.add(self)
        return self
    
    def flush(self) :
        db.session.flush()
        return self
    
    @classmethod
    def find(cls, id) :
        return cls.query.get(id)
    
    # @classmethod
    # def find_by(cls, **kwargs) :.
    #     return cls.query.filter_by(**kwargs).all()

    @classmethod
    def find_by(cls, **kwargs) :
        from sqlalchemy import and_
        exprs = []
        for k, v in kwargs.items():
            col = getattr(cls, k)
            if isinstance(v, (list, tuple, set)):
                exprs.append(col.in_(list(v)))
            else:
                exprs.append(col == v)
        return cls.query.filter(and_(*exprs)).all()
    
    @classmethod
    def find_by_composite_keys(cls, key_columns: List[str], key_tuples: list[Tuple]):
        if not key_tuples or not key_columns:
            return []
        
        from sqlalchemy import and_, or_

        try:
            cols = [getattr(cls, col_name) for col_name in key_columns]
        except AttributeError as e:
            raise Exception(f"Kolom tidak ditemukan di model {cls.__name__}: {e}")

        conditions = []

        for key_tuple in key_tuples:
            if len(key_tuple) != len(cols):
                # Skip tuple yang panjangnya tidak sesuai (data error?)
                continue 
            
            # Buat klausa AND untuk satu composite key
            # (col1 == val1 AND col2 == val2)
            and_clause = and_(*(col == val for col, val in zip(cols, key_tuple)))
            conditions.append(and_clause)

        if not conditions:
            return []
            
        # Gabungkan semua dengan OR: (clause1) OR (clause2) ...
        return cls.query.filter(or_(*conditions)).all()

    @classmethod
    def columns(cls):
        # ['id', 'nama', ...]
        return [c.name for c in cls.__table__.columns]

    @classmethod
    def column_map(cls):
        # {'id': <Column(...)>, 'nama': <Column(...)>, ...}
        return {c.name: c for c in cls.__table__.columns}
    
    @classmethod
    def to_dict(self, exclude: tuple = (), include: List[str] | None = None, rename: Dict[str,str] | None = None) -> Dict[str, Any]:
        """
        Konversi instance model ke dict.
        - exclude: kolom yang dibuang
        - include: jika diisi, hanya kolom ini yang disertakan
        - rename: peta nama kolom -> nama baru di output
        """
        ex   = set(exclude or ())
        inc  = set(include) if include else None
        ren  = rename or {}

        data = {}
        for c in self.__table__.columns:
            name = c.name
            if name in ex: 
                continue
            if inc is not None and name not in inc:
                continue
            val = getattr(self, name)
            data[ren.get(name, name)] = BaseModel._serialize_value(val)
        return data

    @staticmethod
    def get_columns_by_table(table_name, schema='public'):
        # Untuk nama tabel dinamis tanpa kelas model
        insp = sa.inspect(db.engine)
        cols = insp.get_columns(table_name, schema=schema)
        return [{
            'name': c['name'],
            'type': str(c['type']),
            'nullable': c.get('nullable', True),
            'default': c.get('default', None)
        } for c in cols]