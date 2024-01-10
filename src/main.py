if __name__ == "__main__":
    from datetime import datetime

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
    print(client.shipments)
    # client.delete()

    # -------------------------------
    client2 = Client(
        name="Equipo de desarrollo de la nueva granada",
        email="equipo@nueva_granada.com",
        phone="123456789",
        address="Rua Teste",
        is_active=True,
    )
    client2.save()

    # -------------------------------
    package = Package(
        description="Paquete de suministros",
        type_package="Caja",
        weight=10.0,
        size=(10, 10, 10),
    )
    package.save()

    # -------------------------------
    shipment = client.send_package(client2, package)
    print(shipment.state, end="-->")
    shipment.mark_as_delivered()
    print(shipment.state)

    # -------------------------------
    today = datetime.now().strftime("%Y-%m-%d")
    print(
        Shipment.get_total_shipments_per_day(today),
        "units",
    )
    print(
        "$",
        Shipment.get_ammount_per_day(today),
    )
