if __name__ == "__main__":
    from project.models.cargo import Package, Shipment
    from project.models.client import Client

    client = Client(
        name="Fuerzas armadas de la república de la nueva granada",
        email="fuerzas@nueva_granada.com",
        phone="123456789",
        address="Rua Teste",
        is_active=True,
    )
    client.save()
    client2 = Client(
        name="Equipo de desarrollo de la nueva granada",
        email="equipo@nueva_granada.com",
        phone="123456789",
        address="Rua Teste",
        is_active=True,
    )
    client2.save()
    package = Package(
        description="Paquete de suministros",
        type_package="Caja",
        weight=10.0,
        size=(10, 10, 10),
    )
    package.save()
    shipment = client.send_package(client2, package)

    print(
        Shipment.get_total_shipments_per_day("2024-01-09"),
        Shipment.get_ammount_per_day("2024-01-09"),
    )
