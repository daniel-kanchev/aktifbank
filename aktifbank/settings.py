BOT_NAME = 'aktifbank'
SPIDER_MODULES = ['aktifbank.spiders']
NEWSPIDER_MODULE = 'aktifbank.spiders'
LOG_LEVEL = 'WARNING'
ROBOTSTXT_OBEY = True
ITEM_PIPELINES = {
   'aktifbank.pipelines.DatabasePipeline': 300,
}