import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from utils.constants import *
import discord


current_kd = ""
current_kills_match = ""
current_kills = ""
current_deaths = ""
current_win_percentage = ""
current_wins = ""
current_losses = ""
current_abandons = ""
current_rank = ""


def get_content_from_attrs(html: any, attrs: str, value: str):
    return html.find(DIV, attrs={attrs: value})


def request_data(platform: str, nickname: str):
    platform_input = platform.lower()
    nickname_input = nickname

    url = f"{BASE_URL}{platform_input}/{nickname_input}/"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        player_name = soup.find('span', attrs={'class': 'trn-profile-header__name'}).text.strip()
        player_image_url = get_content_from_attrs(soup, CLASS,'trn-profile-header__avatar').find('img')['src']
        general_stats = get_content_from_attrs(soup, CLASS, 'trn-defstats--width4')
        wins = get_content_from_attrs(general_stats, DATA_STAT, 'PVPMatchesWon').contents[0].strip()
        general_kd_ratio = get_content_from_attrs(general_stats, DATA_STAT, 'PVPKDRatio').contents[0].strip()
        win_percentage = get_content_from_attrs(general_stats, DATA_STAT, 'PVPWLRatio').contents[0].strip()
        pvp_deaths = get_content_from_attrs(soup, DATA_STAT, 'PVPDeaths').contents[0].strip()
        hs_percent = get_content_from_attrs(soup, DATA_STAT, 'PVPAccuracy').contents[0].strip()
        ranked_time = get_content_from_attrs(soup, DATA_STAT, 'RankedTimePlayed').contents[0].strip()
        stats_div = get_content_from_attrs(soup, CLASS, 'r6-season__stats')

        ranked_kd = stats_div.find(DIV, attrs={CLASS: TRN_DEF_STAT__NAME}, string=KD).find_next_sibling(
            DIV).text.strip()

        best_mmr = soup.find(DIV, string=BEST_MMR).find_next(DIV,
                                                             attrs={CLASS: TRN_DEF_STAT__VALUE_STYLIZED}).next.strip()
        player_level = soup.find(DIV, string=LEVEL).find_next(DIV,
                                                              attrs={CLASS: TRN_DEF_STAT__VALUE_STYLIZED}).next.strip()
        general_kills = soup.find(DIV, string=KILLS).find_next(DIV, attrs={CLASS: TRN_DEF_STAT__VALUE}).next.strip()
        stats = stats_div.find_all(DIV, attrs={CLASS: 'trn-defstat'})

        for stat in stats:

            name = get_content_from_attrs(stat, CLASS, TRN_DEF_STAT__NAME).text.strip()
            current_stat = get_content_from_attrs(stat, CLASS, TRN_DEF_STAT__VALUE)

            if not current_stat:
                continue

            current_stat = current_stat.text.strip()

            if name == KD:
                current_kd = current_stat
            elif name == KILLS_MATCH:
                current_kills_match = current_stat
            elif name == KILLS:
                current_kills = current_stat
            elif name == DEATHS:
                current_deaths = current_stat
            elif name == WIN_PERCENT:
                current_win_percentage = current_stat
            elif name == WINS:
                current_wins = current_stat
            elif name == LOSSES:
                current_losses = current_stat
            elif name == ABANDONS:
                current_abandons = current_stat
            elif name == RANK:
                current_rank = current_stat

        embed = discord.Embed(title="Click to see full profile", url=url, color=0x7289DA)
        embed.set_author(name=player_name, icon_url=player_image_url)
        embed.add_field(name=GENERAL, value="", inline=False)
        embed.add_field(name=LEVEL, value=player_level, inline=True)
    
        general_stats = (
            (BEST_MMR, best_mmr),
            ("Total Ranked Time Played", ranked_time),
            (WINS, wins),
            (HEADSHOT_PERCENT, hs_percent),
            (KILLS, general_kills),
            (DEATHS, pvp_deaths),
            (KD, general_kd_ratio),
        )
        for stat, value in general_stats:
            embed.add_field(name=stat, value=value, inline=True)

        embed.add_field(name="", value="\u200b", inline=False)
        embed.add_field(name="Current Season [Ranked]", value="", inline=False)

        # Current Season [Ranked]
        current_season_stats = (
            ('Win', current_wins),
            (KILLS_MATCH, current_kills_match),
            (KILLS, current_kills),
            (DEATHS, current_deaths),
            (KD, current_kd),
            (WIN_PERCENT, current_win_percentage),
            (LOSSES, current_losses),
            (ABANDONS, current_abandons),
            (RANK, current_rank),
        )
        for stat, value in current_season_stats:
            embed.add_field(name=stat, value=value, inline=True)

        return embed

    else:
        return discord.Embed(title=f"Failed to retrieve the stats for nickname -> {nickname_input}", color=0x7289DA)
