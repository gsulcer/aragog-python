
from aragog.model.site import Site

##############################################################
def load_sites(db):
    
    sites = []

    try:

        query = '''SELECT site_id, domain, use_ssl, active
                FROM aragog.site'''

        query_cursor = db.cursor()

        query_cursor.execute(query)

        for row in query_cursor:

            s = Site(row[0], row[1], row[2], row[3])

            sites.append(s)

    except dbapi.Error as e:
        print(e)

    return sites