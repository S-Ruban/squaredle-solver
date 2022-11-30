import asyncio
from time import perf_counter
import aiohttp


async def resolve(val):
    return val


async def fetch(s):
    try:
        async with s.post(
            "https://squaredle-solver.el.r.appspot.com/",
            data={"board": "ycsp-slah-mtat-hcyd"},
        ) as r:
            if r.status != 200:
                print(r.status)
            return await resolve(r.status)
    except:
        return -1


async def fetch_all(s):
    tasks = []
    for n in range(25000):
        task = asyncio.create_task(fetch(s))
        tasks.append(task)
    res = await asyncio.gather(*tasks)
    return res


async def main():
    async with aiohttp.ClientSession() as session:
        htmls = await fetch_all(session)
        # print(htmls)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    start = perf_counter()
    asyncio.run(main())
    stop = perf_counter()
    print("time taken:", stop - start)

# 10
# 50
# 100
# 500
# 1000
# 5000
# 10000
# 50000
# 100000
# 500000
