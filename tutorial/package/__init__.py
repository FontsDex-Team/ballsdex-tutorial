from typing import TYPE_CHECKING

from .cog import Tutorial

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot


async def setup(bot: "BallsDexBot") -> None:
    await bot.add_cog(Tutorial(bot))
