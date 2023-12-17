from django.db import connection
from iati_test.product.enums import SizeType

from iati_test.product.models import Cap, Material, Shirt


class ProductsBaseData:
    """
    Class containing the base data for the products and the logic to load them
    into the database when necessary.
    """

    MATERIALS = [
        {
            "name": "nylon",
        },
        {
            "name": "silk",
        },
        {
            "name": "wool",
        },
        {
            "name": "polyester",
        },
        {
            "name": "weed",
        },
        {
            "name": "linen",
        },
        {
            "name": "cotton",
        },
    ]

    CAPS = [
        {
            "id": 1,
            "main_color": "black",
            "secondary_color": "white",
            "brand": "Brixton",
            "picture_url": "https://hatstore.imgix.net/888588520734_1.jpg?auto=compress%2Cformat&w=544&h=435&fit=crop&q=50",
            "catalog_inclusion_date": "2021-04-01",
            "initial_stock": 10,
            "current_stock": 10,
            "price_per_unit": 29.99,
            "logo_color": "white",
        },
        {
            "id": 2,
            "main_color": "blue",
            "secondary_color": "brown",
            "brand": "Wigéns",
            "picture_url": "https://hatstore.imgix.net/7310651170292_1.jpg?auto=compress%2Cformat&w=544&h=435&fit=crop&q=50",
            "catalog_inclusion_date": "2021-02-01",
            "initial_stock": 10,
            "current_stock": 10,
            "price_per_unit": 104.99,
            "logo_color": "grey",
        },
        {
            "id": 3,
            "main_color": "blue",
            "secondary_color": "white",
            "brand": "47 Brand",
            "picture_url": "https://hatstore.imgix.net/053838503168_4.jpg?auto=compress%2Cformat&w=544&h=435&fit=crop&q=50",
            "catalog_inclusion_date": "2021-02-10",
            "initial_stock": 10,
            "current_stock": 10,
            "price_per_unit": 22.99,
            "logo_color": "white",
        },
        {
            "id": 4,
            "main_color": "green",
            "secondary_color": "orange",
            "brand": "Von Dutch",
            "picture_url": "https://hatstore.imgix.net/3614000768135_1.jpg?auto=compress%2Cformat&w=544&h=435&fit=crop&q=50",
            "catalog_inclusion_date": "2022-03-01",
            "initial_stock": 10,
            "current_stock": 10,
            "price_per_unit": 26.99,
            "logo_color": "orange",
        },
        {
            "id": 5,
            "main_color": "grey",
            "secondary_color": "black",
            "brand": "New Era",
            "picture_url": "https://hatstore.imgix.net/197706759995_1.jpg?auto=compress%2Cformat&w=544&h=435&fit=crop&q=50",
            "catalog_inclusion_date": "2021-01-01",
            "initial_stock": 10,
            "current_stock": 10,
            "price_per_unit": 34.99,
            "logo_color": "black",
        },
    ]

    SHIRTS = [
        {
            "id": 1,
            "main_color": "black",
            "secondary_color": "white",
            "brand": "Mister Tree",
            "picture_url": "https://www.snipes.es/dw/image/v2/BDCB_PRD/on/demandware.static/-/Sites-snse-master-eu/default/dw9bc8b5ea/1553665_P.jpg?sw=780&sh=780&sm=fit&sfrm=png",
            "price_per_unit": 19.99,
            "initial_stock": 10,
            "current_stock": 10,
            "catalog_inclusion_date": "2021-02-01",
            "size": "L",
            "size_type": SizeType.MAN.value,
            "sleeves": False,
            "materials": [
                {
                    "material": "cotton",
                    "percentage": 100,
                },
            ],
        },
        {
            "id": 2,
            "main_color": "white",
            "secondary_color": "green",
            "brand": "nike",
            "picture_url": "https://www.snipes.es/dw/image/v2/BDCB_PRD/on/demandware.static/-/Sites-snse-master-eu/default/dw4670d82e/2254784_P.jpg?sw=780&sh=780&sm=fit&sfrm=png",
            "price_per_unit": 39.99,
            "initial_stock": 10,
            "current_stock": 10,
            "catalog_inclusion_date": "2021-01-01",
            "size": "M",
            "size_type": SizeType.WOMAN.value,
            "sleeves": False,
            "materials": [
                {
                    "material": "polyester",
                    "percentage": 10,
                },
                {
                    "material": "cotton",
                    "percentage": 90,
                },
            ],
        },
        {
            "id": 3,
            "main_color": "red",
            "secondary_color": "brown",
            "brand": "Carhartt WIP",
            "picture_url": "https://www.snipes.es/dw/image/v2/BDCB_PRD/on/demandware.static/-/Sites-snse-master-eu/default/dwe68c8a75/2171351_P.jpg?sw=780&sh=780&sm=fit&sfrm=png",
            "price_per_unit": 99.99,
            "initial_stock": 10,
            "current_stock": 10,
            "catalog_inclusion_date": "2021-03-01",
            "size": "M",
            "size_type": SizeType.MAN.value,
            "sleeves": True,
            "materials": [
                {
                    "material": "wool",
                    "percentage": 80,
                },
                {
                    "material": "nylon",
                    "percentage": 20,
                },
            ],
        },
        {
            "id": 4,
            "main_color": "pink",
            "secondary_color": "white",
            "brand": "Converse",
            "picture_url": "https://www.snipes.es/dw/image/v2/BDCB_PRD/on/demandware.static/-/Sites-snse-master-eu/default/dw65c4716b/2069239_P.jpg?sw=780&sh=780&sm=fit&sfrm=png",
            "price_per_unit": 54.99,
            "initial_stock": 10,
            "current_stock": 10,
            "catalog_inclusion_date": "2021-04-01",
            "size": "M",
            "size_type": SizeType.UNISEX.value,
            "sleeves": False,
            "materials": [
                {
                    "material": "cotton",
                    "percentage": 100,
                },
            ],
        },
        {
            "id": 5,
            "main_color": "yellow",
            "secondary_color": "orange",
            "brand": "Carhartt WIP",
            "picture_url": "https://www.snipes.es/dw/image/v2/BDCB_PRD/on/demandware.static/-/Sites-snse-master-eu/default/dwb56a0d4d/2171637_P.jpg?sw=780&sh=780&sm=fit&sfrm=png",
            "price_per_unit": 49.99,
            "initial_stock": 10,
            "current_stock": 10,
            "catalog_inclusion_date": "2020-12-01",
            "size": "L",
            "size_type": SizeType.UNISEX.value,
            "sleeves": False,
            "materials": [
                {
                    "material": "cotton",
                    "percentage": 100,
                },
            ],
        },
    ]

    @classmethod
    def upload_data(cls):
        """
        Upload product startup data to the db, if it is not already there.
        """
        cls._upload_materials()
        cls._upload_caps()
        cls._upload_shirts()

    @classmethod
    def _upload_materials(cls):
        """
        Upload the materials to the db.
        """
        new_materials = []
        for material in cls.MATERIALS:
            if not Material.objects.filter(name=material["name"]).exists():
                new_materials.append(Material(**material))

        Material.objects.bulk_create(new_materials)

    @classmethod
    def _upload_caps(cls):
        """
        Upload the caps to the db.
        """
        new_caps = []
        max_id = 0
        for cap in cls.CAPS:
            if not Cap.objects.filter(id=cap["id"]).exists():
                new_caps.append(Cap(**cap))
                max_id = max(max_id, cap["id"])

        Cap.objects.bulk_create(new_caps)

        if max_id > 0:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT setval(pg_get_serial_sequence('cap', 'id'), {max_id + 1}, false);"
                )

    @classmethod
    def _upload_shirts(cls):
        """
        Upload the shirts to the db.
        """
        #: In the shirts case opted to not use the bulk create method because the amount of data is
        #: small and given that this model has a many to many relationship with the materials model
        #: it complicates the logic quite a bit and i'ts not worth it.
        max_id = 0
        for shirt_data in cls.SHIRTS:
            if not Shirt.objects.filter(id=shirt_data["id"]).exists():
                shirt = Shirt(**{k: v for k, v in shirt_data.items() if k != "materials"})
                max_id = max(max_id, shirt_data["id"])
                shirt.save()
                for material_data in shirt_data["materials"]:
                    material = Material.objects.get(name=material_data["material"])
                    shirt.materials.add(
                        material, through_defaults={"percentage": material_data["percentage"]}
                    )

        if max_id > 0:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT setval(pg_get_serial_sequence('shirt', 'id'), {max_id + 1}, false);"
                )
