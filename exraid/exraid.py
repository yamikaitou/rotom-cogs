import discord
from redbot.core import commands, __version__, checks, Config
import sys
from typing import Union
import asyncio
import aiobotocore
import os
import aiofiles
from .emoji import *

try:
    from .awskey import *
except:
    awskey = False


class EXRaid(getattr(commands, "Cog", object)):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1_977_316_625)
        self.settings = Config.get_conf(None, identifier=602_700_309, cog_name="Info")
        self.config.register_guild(**{"active": []})

    async def on_message(self, message):
        if not awskey:
            pass

        if message.author.bot or isinstance(message.channel, discord.abc.PrivateChannel):
            return

        guild = message.guild
        chan = await self.settings.guild(guild).channel()
        if message.channel.id != chan["ex"]:
            return

        ctx = await self.bot.get_context(message)
        for attach in message.attachments:
            name, ext = os.path.splitext(attach.filename)
            file = "{}{}".format(attach.id, ext)
            await attach.save("/tmp/" + file)

            session = aiobotocore.get_session(loop=self.bot.loop)

            async with session.create_client(
                "s3",
                region_name=AWS_REGION,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                aws_access_key_id=AWS_ACCESS_KEY_ID,
            ) as s3client:

                async with aiofiles.open("/tmp/" + file, mode="rb") as f:
                    content = await f.read()
                await s3client.put_object(Bucket=AWS_S3_BUCKET, Key=file, Body=content)

                async with session.create_client(
                    "rekognition",
                    region_name=AWS_REGION,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                ) as client:

                    resp = await client.detect_text(
                        Image={"S3Object": {"Bucket": AWS_S3_BUCKET, "Name": file}}
                    )
                    top, when, where = None, None, None
                    for text in resp["TextDetections"]:
                        if text["Type"] == "LINE":
                            if text["DetectedText"] == "INVITATION":
                                top = True
                                continue

                            if top is True and when is None:
                                when = text["DetectedText"]
                                continue

                            if top is True and where is None:
                                where = text["DetectedText"]
                                continue

                            if top is True and when is not None and where is not None:
                                break

                    gym = await self.bot.get_cog("Gyms").findgym(where)

                    when2 = when.split()
                    time = when2[2].split(":")
                    if time[1] == "00":
                        time2 = time[0] + when2[3].lower()
                    else:
                        time2 = time[0] + time[1] + when2[3].lower()

                    if gym[2] == "":
                        where = gym[1]
                    else:
                        where = gym[2]

                    channel = "ex_{}-{}_{}_{}".format(
                        when2[0][:3], when2[1], where.replace(" ", "-").replace("'", ""), time2
                    ).lower()
                    cur = await self.config.guild(guild).active()
                    if channel in cur:
                        await ctx.message.delete()
                        return

                    newchan = await ctx.guild.create_text_channel(
                        channel, category=ctx.channel.category
                    )

                    embed = discord.Embed(
                        title="EX Raid @ {}".format(gym[1]),
                        colour=discord.Colour(0x58BA8B),
                        description="**Scheduled for {} {} @ {}**\n\n"
                        "{}\n"
                        "[Google Map Directions](https://www.google.com/maps/dir/?api=1&destination={})\n\n".format(
                            when2[0][:3], when2[1], time2, gym[3], gym[4]
                        ),
                    )
                    embed.set_thumbnail(url="https://www.serebii.net/art/th/386.png")
                    embed.add_field(
                        name="#386 Deoxys (Normal Mode)",
                        value=f"Type: {PSYCHIC}\n"
                        f"Weakness: {BUG} {GHOST} {DARK}\n"
                        f"Resists: {FIGHTING} {PSYCHIC}\n"
                        f"Perfect CP: 1570 / 1963",
                        inline=False,
                    )
                    # embed.add_field(name="Participants",
                    #                value=f"1:00 - 0 {VALOR} | 0 {MYSTIC} | 0 {INSTINCT}\n" \
                    #                      f"1:15 - 0 {VALOR} | 0 {MYSTIC} | 0 {INSTINCT}\n" \
                    #                      f"1:30 - 0 {VALOR} | 0 {MYSTIC} | 0 {INSTINCT}",
                    #                inline=False)

                    async with self.config.guild(guild).active() as act:
                        act.append(channel)

                    await ctx.message.delete()
                    await ctx.send(
                        "{} - {} {} = {}".format(gym[1], when2[0][:3], when2[1], newchan.mention)
                    )
                    await newchan.send(embed=embed)
