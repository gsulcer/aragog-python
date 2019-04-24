class Site:

    def __init__(self, site_id, domain, use_ssl, active):
        self.site_id = site_id
        self.domain = domain
        self.use_ssl = use_ssl
        self.active = active