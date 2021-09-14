import psycopg2
from psycopg2 import sql
from app.services import configs


class Anime:

    def __init__(self, fields ) -> None:
        self.id, self.anime, self.released_date, self.seasons = fields


    @staticmethod
    def save(data):

        data['anime'] = data['anime'].title()

        conn = psycopg2.connect(**configs)
        cur = conn.cursor()
        query = """
        INSERT INTO animes
        VALUES (DEFAULT, (%s), (%s), (%s))
        RETURNING *
        """
        cur.execute(query, tuple(item for item in data.values()))
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        serialized_data = Anime(result).__dict__

        return serialized_data
    
    @staticmethod
    def show():

        conn = psycopg2.connect(**configs)
        cur = conn.cursor()
        query = """
        SELECT *
        FROM
        animes
        
        """
        cur.execute(query)
        fetch_result = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()

        serialized_data = [Anime(ani).__dict__ for ani in fetch_result]

        return serialized_data


    @staticmethod
    def show_anime_by_id(anime_id: int):
        
        conn = psycopg2.connect(**configs)
        cur = conn.cursor()
        query = """
        SELECT *
        FROM
        animes
        WHERE id = (%s);
        """
        cur.execute(query, (anime_id, ))
        fetch_result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        serialized_data = Anime(fetch_result).__dict__ 

        return serialized_data




    @staticmethod
    def update(id: int, data):

        if "anime" in data.keys():
            data['anime'] = data['anime'].title()

        conn = psycopg2.connect(**configs)
        cur = conn.cursor()

        columns = [sql.Identifier(key) for key in data.keys()]
        values = [sql.Literal(value) for value in data.values()]

        query = sql.SQL(
            """
                UPDATE
                    animes
                SET
                    ({columns}) = row({values})
                WHERE
                    id={id}
                RETURNING *
            """).format(id=sql.Literal(str(id)),
                       columns=sql.SQL(',').join(columns),
                       values=sql.SQL(',').join(values))
        
        
        cur.execute(query)

        fetch_result = cur.fetchone()
      
        conn.commit()
        cur.close()
        conn.close()
        
        serialized_data = Anime(fetch_result).__dict__

        return serialized_data

    
    @staticmethod
    def delete(id):
        
        conn = psycopg2.connect(**configs)
        cur = conn.cursor()

        cur.execute(""" DELETE FROM
                            animes
                        WHERE
                            id=(%s)
                        RETURNING *;""", (id, ))

        fetch_result = cur.fetchone()
      
        conn.commit()
        cur.close()
        conn.close()
        
        serialized_data = Anime(fetch_result).__dict__

        return serialized_data



