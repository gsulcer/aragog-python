class Page:

    def __init__(self, page_id=None, site_id=None, crawl_id=None, page_path=None, referrer_path=None, response_status=None, page_detail_id=None, page_status=None, page_change=None, page_hash=None, page_size=None, response_time=None):
        self.page_id = page_id
        self.site_id = site_id
        self.crawl_id = crawl_id
        self.page_path = page_path
        self.referrer_path = referrer_path
        self.response_status = response_status
        self.page_detail_id = page_detail_id
        self.page_status = page_status
        self.page_change = page_change
        self.page_hash = page_hash
        self.page_size = page_size
        self.response_time = response_time