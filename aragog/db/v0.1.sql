/*
Reset back

DROP TABLE IF EXISTS aragog.setting;
DROP TABLE IF EXISTS aragog.user;
DROP TABLE IF EXISTS aragog.page_detail;
DROP TABLE IF EXISTS aragog.image;
DROP TABLE IF EXISTS aragog.page;
DROP TABLE IF EXISTS aragog.site_crawl;
DROP TABLE IF EXISTS aragog.site;
DROP TABLE IF EXISTS aragog.crawl;

*/

/**************************************************************************
Create new tables
***************************************************************************/
CREATE TABLE IF NOT EXISTS aragog.crawl (
	crawl_id			BIGINT			NOT NULL AUTO_INCREMENT PRIMARY KEY,
    crawl_start			DATETIME		NOT NULL,
    crawl_finish		DATETIME		NULL,
	created_by			VARCHAR(255)	NOT NULL,
    created_date		DATETIME		NOT NULL,
    modified_by			VARCHAR(255)	NULL,
    modified_date		DATETIME
);

CREATE TABLE IF NOT EXISTS aragog.site (
    site_id				BIGINT			NOT NULL AUTO_INCREMENT PRIMARY KEY,
    domain         		VARCHAR(255) 	NOT NULL,
    use_ssl				BOOLEAN			NOT NULL DEFAULT 1,
    active				BOOLEAN			NOT NULL DEFAULT 1,
    created_by			VARCHAR(255)	NOT NULL,
    created_date		DATETIME		NOT NULL,
    modified_by			VARCHAR(255)	NULL,
    modified_date		DATETIME
);

CREATE TABLE IF NOT EXISTS aragog.site_crawl (
	site_crawl_id		BIGINT			NOT NULL AUTO_INCREMENT PRIMARY KEY,
    site_id_fk			BIGINT			NOT NULL REFERENCES aragog.site(site_id),
    crawl_id_fk			BIGINT			NOT NULL REFERENCES aragog.crawl(crawl_id),
	created_by			VARCHAR(255)	NOT NULL,
    created_date		DATETIME		NOT NULL,
    modified_by			VARCHAR(255)	NULL,
    modified_date		DATETIME
);

ALTER TABLE aragog.site_crawl ADD INDEX site_crawl_site_crawl_index (site_id_fk, crawl_id_fk);

CREATE TABLE IF NOT EXISTS aragog.`page` (
    page_id				BIGINT			NOT NULL AUTO_INCREMENT PRIMARY KEY,
    site_id_fk			BIGINT			NOT NULL REFERENCES aragog.site(site_id),
    crawl_id_fk			BIGINT			NOT NULL REFERENCES aragog.crawl(crawl_id),
    page_path			VARCHAR(255) 	NOT NULL,
    referrer_path		VARCHAR(255)	NULL,
    response_status		INT				NULL,
    page_detail_id_fk	BIGINT			NULL REFERENCES aragog.page_detail(page_detail_id),
    page_status			VARCHAR(255)	NULL,
    page_change			DECIMAL(8,6)	NULL,
    page_size			BIGINT			NULL,
    response_time		DECIMAL(8,3)	NULL,
    created_by			VARCHAR(255)	NOT NULL,
    created_date		DATETIME		NOT NULL,
    modified_by			VARCHAR(255)	NULL,
    modified_date		DATETIME
);

ALTER TABLE aragog.`page` ADD INDEX site_crawl_page_index (site_id_fk, crawl_id_fk, page_path);

CREATE TABLE IF NOT EXISTS aragog.image (
    image_id			BIGINT			NOT NULL AUTO_INCREMENT PRIMARY KEY,
    site_id_fk			BIGINT			NOT NULL REFERENCES aragog.site(site_id),
    crawl_id_fk			BIGINT			NOT NULL REFERENCES aragog.crawl(crawl_id),
    image_path			VARCHAR(255) 	NOT NULL,
    referrer_path		VARCHAR(255)	NULL,
    response_status		INT				NULL,
    image_status		VARCHAR(255)	NULL,
    image_size			BIGINT			NULL,
    response_time		DECIMAL(8,3)	NULL,
    image_hash			VARCHAR(256)	NULL,
    created_by			VARCHAR(255)	NOT NULL,
    created_date		DATETIME		NOT NULL,
    modified_by			VARCHAR(255)	NULL,
    modified_date		DATETIME
);

ALTER TABLE aragog.image ADD INDEX site_crawl_image_index (site_id_fk, crawl_id_fk, image_path);

CREATE TABLE IF NOT EXISTS aragog.page_detail (
    page_detail_id		BIGINT			NOT NULL AUTO_INCREMENT PRIMARY KEY,
    page_hash			VARCHAR(256)	NOT NULL,
    page_body			LONGTEXT			NULL,
    created_by			VARCHAR(255)	NOT NULL,
    created_date		DATETIME		NOT NULL,
    modified_by			VARCHAR(255)	NULL,
    modified_date		DATETIME
);

CREATE TABLE IF NOT EXISTS aragog.user (
    user_id				BIGINT			NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_name			VARCHAR(256)	NOT NULL,
    active				BOOLEAN			NOT NULL DEFAULT 1,
    created_by			VARCHAR(255)	NOT NULL,
    created_date		DATETIME		NOT NULL,
    modified_by			VARCHAR(255)	NULL,
    modified_date		DATETIME
);

CREATE TABLE IF NOT EXISTS aragog.setting (
    setting_id			BIGINT			NOT NULL AUTO_INCREMENT PRIMARY KEY,
    setting_name		VARCHAR(256)	NOT NULL,
    setting_value		VARCHAR(255)	NULL,
    active				BOOLEAN			NOT NULL DEFAULT 1,
    created_by			VARCHAR(255)	NOT NULL,
    created_date		DATETIME		NOT NULL,
    modified_by			VARCHAR(255)	NULL,
    modified_date		DATETIME
);

/**************************************************************************
Insert Data
***************************************************************************/
INSERT INTO aragog.site
(domain, use_ssl, active, created_by, created_date)
VALUES
('1850coffee.com', true, false, 'gsulcer', sysdate()),
('9lives.com', true, false, 'gsulcer', sysdate()),
('adamspeanutbutter.com', true, true, 'gsulcer', sysdate()),
('cafebustelo.com', true, false, 'gsulcer', sysdate()),
('cafepilon.com', true, false, 'gsulcer', sysdate()),
('caninecarryouts.com', true, false, 'gsulcer', sysdate()),
('crisco.com', true, false, 'gsulcer', sysdate()),
('crosseandblackwell.com', true, false, 'gsulcer', sysdate()),
('dickinsonsfamily.com', true, false, 'gsulcer', sysdate()),
('dunkinathome.com', true, false, 'gsulcer', sysdate()),
('folgerscoffee.com', true, false, 'gsulcer', sysdate()),
('gravytraindog.com', true, false, 'gsulcer', sysdate()),
('hungryjack.com', true, false, 'gsulcer', sysdate()),
('jif.com', true, false, 'gsulcer', sysdate()),
('kibblesnbits.com', true, false, 'gsulcer', sysdate()),
('knottsberryfarmfoods.com', true, false, 'gsulcer', sysdate()),
('laurascudderspeanutbutter.com', true, false, 'gsulcer', sysdate()),
('lovepbj.com', true, false, 'gsulcer', sysdate()),
('marthawhite.com', true, false, 'gsulcer', sysdate()),
('medagliadoro.com', true, false, 'gsulcer', sysdate()),
('meowmix.com', true, false, 'gsulcer', sysdate()),
('milkbone.com', true, false, 'gsulcer', sysdate()),
('miloskitchen.com', true, false, 'gsulcer', sysdate()),
('naturalbalanceinc.com', true, false, 'gsulcer', sysdate()),
('natural-brew.com', true, false, 'gsulcer', sysdate()),
('naturesrecipe.com', true, false, 'gsulcer', sysdate()),
('nonesuchrecipes.com', true, false, 'gsulcer', sysdate()),
('pillsburybaking.com', true, false, 'gsulcer', sysdate()),
('pouncetreats.com', true, false, 'gsulcer', sysdate()),
('pupperoni.com', true, false, 'gsulcer', sysdate()),
('rwknudsenfamily.com', true, false, 'gsulcer', sysdate()),
('sahalesnacks.com', true, false, 'gsulcer', sysdate()),
('santacruzorganic.com', true, false, 'gsulcer', sysdate()),
('smuckerawayfromhome.com', true, false, 'gsulcer', sysdate()),
('smuckers.com', true, false, 'gsulcer', sysdate()),
('smuckersuncrustables.com', true, false, 'gsulcer', sysdate()),
('snausages.com', true, false, 'gsulcer', sysdate()),
('thenoseprint.com', true, false, 'gsulcer', sysdate()),
('truroots.com', true, false, 'gsulcer', sysdate()),
('whitelily.com', true, false, 'gsulcer', sysdate())
;

INSERT INTO aragog.user
(user_name, active, created_by, created_date)
VALUES
('aragog', true, 'script', sysdate()),
('gsulcer', true, 'script', sysdate());

INSERT INTO aragog.setting
(setting_name, setting_value, created_by, created_date)
VALUES
('change_threshold', '0.98', 'script', sysdate());