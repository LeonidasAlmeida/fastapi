import asyncio


async def q():
    print("why can't programmer tell jokes ?")
    await asyncio.sleep(10)


async def a():
    print("Timing!")


def r():
    print("sem pressa!")


async def main():
    await asyncio.gather(q(), a())
    r()


asyncio.run(main())
