from mysql.connector import IntegrityError

from Classes.clsCat import ClsCat
from Classes.clsDog import ClsDog
from Classes.clsReportByHealthStatus import ClsReportByHealthStatus
from Model.DbData import DbData


class ModelPet:
    def __init__(self, animal_type):
        if animal_type not in ("Dog", "Cat"):
            raise ValueError(f"Unsupported animal type: {animal_type}")

        self.animal_type = animal_type
        self.db_data = DbData()
        self.detail_table = "tb_dog" if animal_type == "Dog" else "tb_cat"
        self.detail_id = "id"

    def _get_connection(self):
        return self.db_data.get_connection()

    def _build_pet(self, row):
        pet_id, code, name, born_year, color, health_status, detail_id, breed = row[:8]
        if self.animal_type == "Dog":
            return ClsDog(
                dog_id=detail_id,
                breed=breed,
                pedigree=bool(row[8]),
                pet_id=pet_id,
                code=code,
                name=name,
                born_year=born_year,
                color=color,
                health_status=health_status,
            )

        return ClsCat(
            cat_id=detail_id,
            breed=breed,
            pet_id=pet_id,
            code=code,
            name=name,
            born_year=born_year,
            color=color,
            health_status=health_status,
        )

    def create_pet(self, pet) -> bool:
        connection = self._get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO tb_pet (code, name, born_year, color, health_status)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    pet.get_code(),
                    pet.get_name(),
                    pet.get_born_year(),
                    pet.get_color(),
                    pet.get_health_status(),
                ),
            )
            pet_id = cursor.lastrowid

            if self.animal_type == "Dog":
                cursor.execute(
                    "INSERT INTO tb_dog (breed, pedigree, id_pet) VALUES (%s, %s, %s)",
                    (pet.get_breed(), int(pet.is_pedigree()), pet_id),
                )
            else:
                cursor.execute(
                    "INSERT INTO tb_cat (breed, id_pet) VALUES (%s, %s)",
                    (pet.get_breed(), pet_id),
                )

            connection.commit()
            return True
        except IntegrityError:
            connection.rollback()
            return False
        finally:
            cursor.close()
            connection.close()

    def search_pet(self, code: str):
        connection = self._get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"""
                SELECT p.id, p.code, p.name, p.born_year, p.color, p.health_status,
                       d.{self.detail_id}, d.breed
                       {", d.pedigree" if self.animal_type == "Dog" else ""}
                FROM tb_pet AS p
                INNER JOIN {self.detail_table} AS d ON p.id = d.id_pet
                WHERE p.code = %s
                ORDER BY p.id
                LIMIT 1
                """,
                (code,),
            )
            row = cursor.fetchone()
            return self._build_pet(row) if row else None
        finally:
            cursor.close()
            connection.close()

    def edit_pet(self, pet) -> bool:
        connection = self._get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT id FROM tb_pet WHERE id = %s", (pet.get_pet_id(),))
            if cursor.fetchone() is None:
                connection.rollback()
                return False

            detail_key = pet.get_dog_id() if self.animal_type == "Dog" else pet.get_cat_id()
            cursor.execute(
                f"SELECT id FROM {self.detail_table} WHERE id = %s AND id_pet = %s",
                (detail_key, pet.get_pet_id()),
            )
            if cursor.fetchone() is None:
                connection.rollback()
                return False

            cursor.execute(
                """
                UPDATE tb_pet
                SET code = %s, name = %s, born_year = %s, color = %s, health_status = %s
                WHERE id = %s
                """,
                (
                    pet.get_code(),
                    pet.get_name(),
                    pet.get_born_year(),
                    pet.get_color(),
                    pet.get_health_status(),
                    pet.get_pet_id(),
                ),
            )

            if self.animal_type == "Dog":
                cursor.execute(
                    "UPDATE tb_dog SET breed = %s, pedigree = %s WHERE id = %s AND id_pet = %s",
                    (
                        pet.get_breed(),
                        int(pet.is_pedigree()),
                        pet.get_dog_id(),
                        pet.get_pet_id(),
                    ),
                )
            else:
                cursor.execute(
                    "UPDATE tb_cat SET breed = %s WHERE id = %s AND id_pet = %s",
                    (pet.get_breed(), pet.get_cat_id(), pet.get_pet_id()),
                )

            connection.commit()
            return True
        except IntegrityError:
            connection.rollback()
            return False
        finally:
            cursor.close()
            connection.close()

    def delete_pet(self, pet) -> bool:
        connection = self._get_connection()
        cursor = connection.cursor()
        try:
            detail_key = pet.get_dog_id() if self.animal_type == "Dog" else pet.get_cat_id()
            cursor.execute(
                f"DELETE FROM {self.detail_table} WHERE {self.detail_id} = %s AND id_pet = %s",
                (detail_key, pet.get_pet_id()),
            )
            if cursor.rowcount == 0:
                connection.rollback()
                return False

            cursor.execute("DELETE FROM tb_pet WHERE id = %s", (pet.get_pet_id(),))
            if cursor.rowcount == 0:
                connection.rollback()
                return False

            connection.commit()
            return True
        finally:
            cursor.close()
            connection.close()

    def list_pet(self) -> list:
        connection = self._get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"""
                SELECT p.id, p.code, p.name, p.born_year, p.color, p.health_status,
                       d.{self.detail_id}, d.breed
                       {", d.pedigree" if self.animal_type == "Dog" else ""}
                FROM tb_pet AS p
                INNER JOIN {self.detail_table} AS d ON p.id = d.id_pet
                ORDER BY p.id
                """
            )
            return [self._build_pet(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            connection.close()

    def list_pet_by_health_status(self) -> list:
        return self._list_by_health_status()

    def list_animal_by_health_status(self) -> list:
        return self._list_by_health_status(self.animal_type)

    def _list_by_health_status(self, animal_type=None) -> list:
        connection = self._get_connection()
        cursor = connection.cursor()
        try:
            if animal_type:
                cursor.execute(
                    f"""
                    SELECT p.health_status, COUNT(DISTINCT p.id)
                    FROM tb_pet AS p
                    INNER JOIN {self.detail_table} AS d ON p.id = d.id_pet
                    GROUP BY p.health_status
                    ORDER BY p.health_status
                    """
                )
            else:
                cursor.execute(
                    """
                    SELECT health_status, COUNT(*)
                    FROM tb_pet
                    GROUP BY health_status
                    ORDER BY health_status
                    """
                )
            return [
                ClsReportByHealthStatus(status, amount)
                for status, amount in cursor.fetchall()
            ]
        finally:
            cursor.close()
            connection.close()
