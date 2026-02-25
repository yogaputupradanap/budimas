from faker import Faker
from faker.providers import DynamicProvider
from sqlalchemy import create_engine


def seed_database():
    fake = Faker()


    url = "postgresql+pg8000://postgres:postgres@localhost:5432/budimas-local"
    engine = create_engine(url)
    connection = engine.connect()

    id_armada_povider = DynamicProvider(
        provider_name="id_armada",
        elements=[13, 29]
    )

    id_produk_provider = DynamicProvider(
        provider_name="id_produk",
        elements=[24, 40]
    )

    id_cabang_provider = DynamicProvider(
        provider_name="id_cabang",
        elements=[{"name": "solo", "id": 5},{"name": "wonogiri", "id": 6},{"name": "klaten", "id": 7},{"name": "salatiga", "id": 14}]
    )

    status_provider = DynamicProvider(
        provider_name="status",
        elements=[-2,-1,0,2,3,4,5,6]
    )


    fake.add_provider(id_armada_povider)
    fake.add_provider(id_cabang_provider)
    fake.add_provider(status_provider)
    fake.add_provider(id_produk_provider)

    for i in range(28, 100):
        id_cabang_awal = fake.id_cabang()
        id_cabang_tujuan = fake.id_cabang()

        query = f"""
            insert into stock_transfer
            (nota_stock_transfer,id_cabang_awal,id_cabang_tujuan,status,nama_cabang_awal,nama_cabang_tujuan,id_armada, created_at)
            values
            ('{fake.domain_word()}',{id_cabang_awal['id']},{id_cabang_tujuan['id']},0,'{id_cabang_awal['name']}','{id_cabang_tujuan['name']}',{fake.id_armada()}, '{fake.date()}');
        """

        detail_query = f"""
            insert into stock_transfer_detail
            (id_stock_transfer, id_principal, id_produk, jumlah)
            values
            ({i}, 6, {fake.id_produk()}, {fake.random_int(min=40, max=200)})
        """
        try:
            # connection.execute(query)
            connection.execute(detail_query)
            print('executed')
        except Exception as e:
            print(e)

    connection.close()


# seed_database()
