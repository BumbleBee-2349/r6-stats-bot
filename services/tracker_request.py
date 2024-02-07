import requests
from bs4 import BeautifulSoup
from utils.constants import *
from core.embed import full_profile_title_message, failed_retrieving_stats_message, failed_retrieving_stats_invalid_message


def request_data(platform: str, nickname: str):
    platform_input = platform.lower()
    nickname_input = nickname

    url = f"{BASE_URL}{platform_input}/{nickname_input}/"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        player_name = soup.find('span', attrs={'class': 'trn-profile-header__name'}).text.strip()
        player_image_url = get_content_from_attrs(soup, CLASS, 'trn-profile-header__avatar').find('img')['src']
        general_stats = get_content_from_attrs(soup, CLASS, 'trn-defstats--width4')
        wins = get_content_from_attrs(general_stats, DATA_STAT, 'PVPMatchesWon').contents[0].strip()
        general_kd_ratio = get_content_from_attrs(general_stats, DATA_STAT, 'PVPKDRatio').contents[0].strip()
        pvp_deaths = get_content_from_attrs(soup, DATA_STAT, 'PVPDeaths').contents[0].strip()
        hs_percent = get_content_from_attrs(soup, DATA_STAT, 'PVPAccuracy').contents[0].strip()
        ranked_time = get_content_from_attrs(soup, DATA_STAT, 'RankedTimePlayed').contents[0].strip()
        stats_div = get_content_from_attrs(soup, CLASS, 'r6-season__stats')

        best_mmr = get_optional_info(soup, BEST_MMR, TRN_DEF_STAT__VALUE_STYLIZED)
        player_level = get_optional_info(soup, LEVEL, TRN_DEF_STAT__VALUE_STYLIZED)
        general_kills = get_optional_info(soup, KILLS, TRN_DEF_STAT__VALUE)

        try:
            stats = stats_div.find_all(DIV, attrs={CLASS: 'trn-defstat'})
        except:
            return failed_retrieving_stats_invalid_message(nickname_input)


        current_kd = ""
        current_kills_match = ""
        current_kills = ""
        current_deaths = ""
        current_win_percentage = ""
        current_wins = ""
        current_losses = ""
        current_abandons = ""
        current_rank = ""

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

        embed = full_profile_title_message(url)
        embed.set_author(name=player_name, icon_url=player_image_url)
        embed.add_field(name=GENERAL, value="", inline=False)
        embed.add_field(name=LEVEL, value=player_level, inline=True)

        ranked_time = "NA" if ranked_time == "" else ranked_time

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
        return failed_retrieving_stats_message(nickname_input)


def get_optional_info(soup, module: str, clazz: str):
    try:
        best_mmr = soup.find(DIV, string=module).find_next(DIV,
                                                           attrs={CLASS: clazz}).next.strip()
    except:
        best_mmr = "NA"
    return best_mmr


def get_content_from_attrs(html: any, attrs: str, value: str):
    return html.find(DIV, attrs={attrs: value})