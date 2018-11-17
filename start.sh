#!/usr/bin/env bash
cd /opt/zhihu_spider
source venv/bin/activate
nohup scrapy crawl zhihu --set JOBDIR=crawls/project_saved > /var/log/zhihu_spider.log 2>&1 &
deactivate