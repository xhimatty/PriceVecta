from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# 1. Load your project settings (ensures user-agents and middlewares are active)
settings = get_project_settings()

# 2. Initialize the crawler process with those settings
process = CrawlerProcess(settings)

# 3. Schedule both spiders to run
process.crawl('konga')
process.crawl('jumia')
process.crawl('solatonline')

# 4. Start the execution engine (this blocks until both spiders are finished)
process.start()