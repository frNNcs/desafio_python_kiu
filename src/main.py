from project.models.cargo import Package, Shipment
from project.models.client import Client

if __name__ == "__main__":
    client = Client(
        name="Fuerzas armadas de la república de la nueva granada",
        email="fuerzas@nueva_granada.com",
        phone="123456789",
        address="Rua Teste",
        is_active=True,
    )
    client2 = Client(
        name="Equipo de desarrollo de la nueva granada",
        email="equipo@nueva_granada.com",
        phone="123456789",
        address="Rua Teste",
        is_active=True,
    )
    package = Package(
        description="Paquete de suministros",
        type_package="Caja",
        weight=10.0,
        size=(10, 10, 10),
    )
    client.send_package(client2, package)
    print(Shipment.get_total_shipments())
    print(Shipment.total_collected_per_day("2024-01-09"))
