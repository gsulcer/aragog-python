import hashlib
from difflib import SequenceMatcher
from aragog.model.page import Page

from aragog.logic import crawl_logic

##############################################################
def get_page(db, page_id):

    page = None

    mycursor = db.cursor()

    sql = '''SELECT page_id, site_id_fk, crawl_id_fk, page_path, response_status, page_detail_id_fk, page_status, page_hash
            FROM aragog.page p LEFT OUTER JOIN aragog.page_detail d on p.page_detail_id_fk = d.page_detail_id
            WHERE page_id = %s'''
    val = (page_id, )
    mycursor.execute(sql, val)

    row = mycursor.fetchone()

    if(row is not None):
        page = Page(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])

    return page

##############################################################
def get_page_body(db, page_detail_id):

    page_body = None

    mycursor = db.cursor()

    sql = '''SELECT page_body
            FROM aragog.page_detail
            WHERE page_detail_id = %s'''
    val = (page_detail_id, )
    mycursor.execute(sql, val)

    row = mycursor.fetchone()

    if(row is not None):
        page_body = row[0]

    return page_body

##############################################################
def find_page(db, site_id, crawl_id, page_path):

    page = None

    mycursor = db.cursor()

    sql = '''SELECT page_id, page_hash, page_detail_id
            FROM aragog.page p LEFT OUTER JOIN aragog.page_detail d on p.page_detail_id_fk = d.page_detail_id
            WHERE site_id_fk = %s and crawl_id_fk = %s and page_path = %s'''
    val = (site_id, crawl_id, page_path, )
    mycursor.execute(sql, val)

    row = mycursor.fetchone()

    if(row is not None):
        page = Page(page_id=row[0], page_hash=row[1], page_detail_id=row[2])

    return page

##############################################################
def insert_page(db, site_id, crawl_id, page_path, referrer_path, user_name):

    page_id = None

    page = find_page(db, site_id, crawl_id, page_path)

    if(page == None):

        mycursor = db.cursor()

        sql = '''INSERT INTO aragog.page (site_id_fk, crawl_id_fk, page_path, referrer_path, created_by, created_date) 
                VALUES (%s, %s, %s, %s, %s, sysdate())'''
        val = (site_id, crawl_id, page_path, referrer_path, user_name, )
        mycursor.execute(sql, val)

        db.commit()

        page_id = mycursor.lastrowid
    else:
        page_id = page.page_id

    return page_id

##############################################################
def update_page(db, page_id, response_status, page_body, response_time, user_name):

    page = get_page(db, page_id)
    last_crawl = crawl_logic.last_site_crawl(db, page.site_id)
    last_page = None
    page_change = 1.0
    page_size = len(page_body)
    
    if(last_crawl is not None):
        last_page = find_page(db, page.site_id, last_crawl.crawl_id, page.page_path)

    page_detail_id = None
    last_hash = None
    page_status = 'New'

    new_page_hash = hashlib.sha256(page_body).hexdigest()

    if(last_page is None):
        page_status = 'New'
    else:
        last_hash = last_page.page_hash
        page_detail_id = last_page.page_detail_id

        if(last_hash == new_page_hash):
            page_status = 'Unchanged'
            page_change = 0
        else:
            last_page_body = get_page_body(db, last_page.page_detail_id)

            if(page_body is not None and last_page_body is not None):
                matcher = SequenceMatcher(None, str(page_body, 'utf-8'), last_page_body)
                page_change = matcher.ratio()
                #page_change = 1 - (jellyfish.jaro_distance(str(page_body, 'utf-8'), last_page_body))

                if(page_change < 0.90):
                    page_status = 'Changed'
                else:
                    page_status = 'Minimal Changed'

    if(page_status == 'New' or page_status == 'Changed'):
        mycursor = db.cursor()

        sql = '''INSERT INTO aragog.page_detail (page_hash, page_body, created_by, created_date) 
                VALUES (%s, %s, %s, sysdate())'''
        val = (new_page_hash, str(page_body, 'utf-8'), user_name, )
        mycursor.execute(sql, val)

        db.commit()

        page_detail_id = mycursor.lastrowid

    mycursor = db.cursor()

    sql = '''UPDATE aragog.page SET
                response_status = %s,
                page_detail_id_fk = %s,
                page_status = %s,
                page_change = %s,
                page_size = %s,
                response_time = %s,
                modified_by = %s, 
                modified_date = sysdate()
            WHERE page_id = %s'''
    val = (response_status, page_detail_id, page_status, page_change, page_size, response_time, user_name, page_id, )
    mycursor.execute(sql, val)

    db.commit()
