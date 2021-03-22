import asyncio

from crawl.aio_request import AioRequestClient
from crawl.run_sql import complex_url, run_alchemy

async def get_url(url):
    client = AioRequestClient()
    async with client.get(url) as response:
        html = await response.text()
        run_alchemy(html)

    await client.close()

async def main():
    task = [asyncio.create_task(i) for i in [get_url(j) for j in complex_url('http://www.kehuan.net.cn/book.html')]]

    done = await asyncio.wait(task)

asyncio.run(main())