if __name__ == "__main__":
    import sys

    print(sys.path)
    from database.connection import conn

    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS clients (
            id serial PRIMARY KEY,
            created_at timestamp,
            name varchar(100) NOT NULL,
            email varchar(100) NOT NULL,
            phone varchar(100) NOT NULL,
            address varchar(100) NOT NULL,
            is_active boolean NOT NULL
        )
        CREATE TABLE IF NOT EXISTS packages (
            id serial PRIMARY KEY,
            created_at timestamp,
            description varchar(100) NOT NULL,
            type_package varchar(100) NOT NULL,
            weight float NOT NULL,
            size varchar(100) NOT NULL
        )
        CREATE TABLE IF NOT EXISTS shipments (
            id serial PRIMARY KEY,
            created_at timestamp,
            source_id integer NOT NULL REFERENCES clients(id),
            destination_id integer NOT NULL REFERENCES clients(id),
            state varchar(100) NOT NULL,
            packages_id integer NOT NULL REFERENCES packages(id),
        )
        """
    )

    conn.commit()
