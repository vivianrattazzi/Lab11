from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.prodotto import Prodotto


class DAO():

    @staticmethod
    def getAllNodes(colore):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        results = []
        query = '''select * from go_products gp where gp.Product_color = %s'''
        cursor.execute(query, (colore,))

        for row in cursor:
            results.append(Prodotto(**row))

        cursor.close()
        cnx.close()
        return results


    @staticmethod
    def getAnni():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor()

        results = []
        query = '''select distinct YEAR(gds.`Date`)
                    from go_daily_sales gds '''

        cursor.execute(query)
        for row in cursor:
            results.append(row[0])

        cursor.close()
        cnx.close()
        return results

    @staticmethod
    def getColori():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor()

        results = []
        query = '''select distinct gp.Product_color 
                from go_products gp '''

        cursor.execute(query)
        for row in cursor:
            results.append(row[0])

        cursor.close()
        cnx.close()
        return results

    @staticmethod
    def getAllEdges(anno, colore):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        results = []
        query = '''select t.p1, t.p2, count(*) as peso
                from (
                select gds1.Product_number as p1, gds2.Product_number as p2
                from go_daily_sales gds1, go_daily_sales gds2
                where gds1.Product_number < gds2.Product_number
                and gds1.Retailer_code = gds2.Retailer_code and gds2.`Date` = gds1.`Date`  and YEAR(gds2.`Date`) = %s and gds1.Product_number in (select gp.Product_number from go_products gp 
                where gp.Product_color = %s) and gds2.Product_number in (select gp.Product_number from go_products gp where gp.Product_color = %s)
                group by p1, p2, gds2.`Date` 
                ) as t
                group by p1, p2
                order by peso DESC
                '''
        cursor.execute(query, (anno, colore, colore))
        for row in cursor:
            results.append(Connessione(row["p1"], row["p2"], row["peso"]))

        cursor.close()
        cnx.close()
        return results

