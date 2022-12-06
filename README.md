# portal_helper_cog

portal info submodule

## usage

import the cog with

```py
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Battlefield_2042_Private(bot))
```

or use it inside another cog

```py
class Battlefield_2042_Private(Battlefield_2042, name="bf2042"):
```