#-*-coding:utf-8 -*-

import tornado.options
from tornado.options import define, options

define("port", default = 8000, help  = "run on given port", type = int)
define("mysql_host", default = "localhost", help = "blog database host")
define("mysql_database", default = "rss_db", help = "rss server database name")
define("mysql_user", default = "thomas", help = "rss server database user")
define("mysql_password", default = "thomas", help="rss server database password")
define("mysql_port", default = 3036, help="rss server database port", type = int)