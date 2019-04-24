from aragog.model.crawl import Crawl

##############################################################
def start_crawl(db, user_name):
    crawl_id = None

    mycursor = db.cursor()

    sql = '''INSERT INTO aragog.crawl (crawl_start, created_by, created_date) 
                VALUES (sysdate(), %s, sysdate())'''
    val = (user_name,)
    mycursor.execute(sql, val)

    db.commit()

    crawl_id = mycursor.lastrowid

    return crawl_id

##############################################################
def start_site_crawl(db, site_id, crawl_id, user_name):
    site_crawl_id = None

    mycursor = db.cursor()

    sql = '''INSERT INTO aragog.site_crawl (site_id_fk, crawl_id_fk, created_by, created_date) 
                VALUES (%s, %s, %s, sysdate())'''
    val = (site_id, crawl_id, user_name,)
    mycursor.execute(sql, val)

    db.commit()

    site_crawl_id = mycursor.lastrowid

    return site_crawl_id

##############################################################
def finish_crawl(db, crawl_id, user_name):

    mycursor = db.cursor()

    sql = '''UPDATE aragog.crawl SET
                crawl_finish = sysdate(),
                modified_by = %s,
                modified_date = sysdate()
            WHERE crawl_id = %s'''
    val = (user_name, crawl_id)
    mycursor.execute(sql, val)

    db.commit()

##############################################################
def last_site_crawl(db, site_id):

    crawl = None

    mycursor = db.cursor()

    sql = '''SELECT 
                c.crawl_id, c.crawl_start, c.crawl_finish, s.site_id
            FROM
                aragog.site_crawl sc
                    LEFT JOIN
                aragog.site s ON sc.site_id_fk = s.site_id
                    LEFT JOIN
                aragog.crawl c ON sc.crawl_id_fk = c.crawl_id
            WHERE
                s.site_id = %s AND c.crawl_finish IS NOT NULL
            ORDER BY c.crawl_start DESC
            LIMIT 1'''
    val = (site_id, )
    mycursor.execute(sql, val)

    row = mycursor.fetchone()

    if(row is not None):
        crawl = Crawl(row[0], row[1], row[2], row[3])

    mycursor.close()

    return crawl