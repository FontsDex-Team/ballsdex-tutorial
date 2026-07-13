from __future__ import annotations

import asyncio
import inspect
import logging
import random
from datetime import timedelta
from django.utils import timezone
from typing import TYPE_CHECKING, Any

import discord
from discord import app_commands
from discord.ext import commands
from settings.models import settings
from ballsdex.packages.guildconfig.cog import Config
from ballsdex.packages.trade.cog import Trade

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot

log = logging.getLogger("ballsdex.packages.tutorial")

class Tutorial(commands.Cog):
    """Tutorial command."""
    def __init__(self, bot: "BallsDexBot"):
        self.bot = bot

    @app_commands.command()
    async def tutorial(self, interaction: discord.Interaction):
        """
        View a descriptive tutorial of the bot.
        """
        trade_begin = Trade.start.extras.get("mention", "/trade begin")
        trade_add = Trade.add.extras.get("mention", "/trade add")
        config_channel = Config.channel.extras.get("mention", "/config channel")
        embed = discord.Embed(
            title=f"{settings.bot_name.title()} Tutorial", color=discord.Color.blurple()
        )
        embed.add_field(
            name="What can I do with this bot?",
            value=(
                f"You can collect {settings.plural_collectible_name}, exchange them with friends "
                "and build a big and strong collection!"
            ),
            inline=False,
        )
        embed.add_field(
            name="How can I configure the bot?",
            value=(
                f"To enable the spawning of {settings.plural_collectible_name}, you "
                "need to configure the bot. To do that, you need to run the command "
                f"{config_channel}. You must have the `Manage Guild` "
                "permission to use this command."
            ),
            inline=False,
        )
        embed.add_field(
            name=f"How can I catch {settings.plural_collectible_name} and when do they spawn?",
            value=(
                f"{settings.plural_collectible_name.title()} spawn depending on the server's "
                "activity. If there's high activity, they will spawn more quickly. To catch them,"
                " tap the blue 'Catch Me' button when one spawns, then guess the name of the "
                f"{settings.collectible_name}, and if your guess is correct, the "
                f"{settings.collectible_name} will be added to your inventory! Keep in mind, "
                f"{settings.plural_collectible_name} are unable of being caught if "
                "three minutes pass from the time it spawned."
            ),
            inline=False,
        )
        embed.add_field(
            name=f"How can I exchange {settings.plural_collectible_name}?",
            value=(
                f"First, you need to begin a trade using {trade_begin}. "
                f"Once the trade has started, add the {settings.plural_collectible_name} you "
                f"want with the command {trade_add}. Then, tap the button named 'Lock Proposal', "
                "and tap the 'Accept' button to end the trade and finish the exchange."
            ),
            inline=False,
        )
        embed.set_footer(text="We hope you enjoy the bot!")
        if self.bot.user and self.bot.user.display_avatar:
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
