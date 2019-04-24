class Image:

    def __init__(self, image_id=None, site_id=None, crawl_id=None, image_path=None, referrer_path=None, response_status=None, image_status=None, image_size=None, response_time=None, image_hash=None):
        self.image_id = image_id
        self.site_id = site_id
        self.crawl_id = crawl_id
        self.image_path = image_path
        self.referrer_path = referrer_path
        self.response_status = response_status
        self.image_status = image_status
        self.image_size = image_size
        self.response_time = response_time
        self.image_hash = image_hash