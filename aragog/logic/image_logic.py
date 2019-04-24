import hashlib

from aragog.model.image import Image
from aragog.logic import crawl_logic

##############################################################
def get_image(db, image_id):

    image = None

    mycursor = db.cursor()

    sql = '''SELECT image_id, site_id_fk, crawl_id_fk, image_path, response_status, image_hash
            FROM aragog.image
            WHERE image_id = %s'''
    val = (image_id, )
    mycursor.execute(sql, val)

    row = mycursor.fetchone()

    if(row is not None):
        image = Image(row[0], row[1], row[2], row[3], row[4], row[5])

    return image

##############################################################
def find_image(db, site_id, crawl_id, image_path):

    image = None

    mycursor = db.cursor()

    sql = '''SELECT image_id, image_hash
            FROM aragog.image
            WHERE site_id_fk = %s and crawl_id_fk = %s and image_path = %s'''
    val = (site_id, crawl_id, image_path, )
    mycursor.execute(sql, val)

    row = mycursor.fetchone()

    if(row is not None):
        image = Image(image_id=row[0], image_hash=row[1])

    return image

##############################################################
def insert_image(db, site_id, crawl_id, image_path, referrer_path, user_name):

    image_id = None

    image = find_image(db, site_id, crawl_id, image_path)

    if(image == None):

        mycursor = db.cursor()

        sql = '''INSERT INTO aragog.image (site_id_fk, crawl_id_fk, image_path, referrer_path, created_by, created_date) 
                VALUES (%s, %s, %s, %s, %s, sysdate())'''
        val = (site_id, crawl_id, image_path, referrer_path, user_name, )
        mycursor.execute(sql, val)

        db.commit()

        image_id = mycursor.lastrowid
    else:
        image_id = image.image_id

    return image_id

##############################################################
def update_image(db, image_id, response_status, image_body, response_time, user_name):

    image = get_image(db, image_id)
    last_crawl = crawl_logic.last_site_crawl(db, image.site_id)
    last_image = None
    image_size = len(image_body)
    
    if(last_crawl is not None):
        last_image = find_image(db, image.site_id, last_crawl.crawl_id, image.image_path)

    last_hash = None
    image_status = 'New'

    new_image_hash = hashlib.sha256(image_body).hexdigest()

    if(last_image is None):
        image_status = 'New'
    else:
        last_hash = last_image.image_hash

        if(last_hash == new_image_hash):
            image_status = 'Unchanged'
        else:
            image_status = 'Changed'
    
    mycursor = db.cursor()

    sql = '''UPDATE aragog.image SET
                response_status = %s,
                image_status = %s,
                image_hash = %s,
                image_size = %s,
                response_time = %s,
                modified_by = %s, 
                modified_date = sysdate()
            WHERE image_id = %s'''
    val = (response_status, image_status, new_image_hash, image_size, response_time, user_name, image_id, )
    mycursor.execute(sql, val)

    db.commit()