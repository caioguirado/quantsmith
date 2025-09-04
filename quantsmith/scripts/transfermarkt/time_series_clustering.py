import requests
from bs4 import BeautifulSoup


cookies = {
    "kndctr_B21B678254F601E20A4C98A5_AdobeOrg_identity": "CiY0MzAzMTUzMDkzNzI2NzY5NjcyMDIxNTU4NDk3MjM5OTA1MDg2OFIRCNf-pZv0MRgBKgRJUkwxMAHwAdf-pZv0MQ==",
    "AMCV_B21B678254F601E20A4C98A5%40AdobeOrg": "MCMID|43031530937267696720215584972399050868",
    "_sp_v1_ss": "1:H4sIAAAAAAAAAItWqo5RKimOUbKKhjHySnNydGKUUpHYJWCJ6traWFwSSjqYBmFn5IEYBrhNoqKEUiwAqTzxSd8AAAA%3D",
    "_sp_v1_p": "771",
    "euconsent-v2": "CQFCpIAQFCpIAAGABCENBHFsAP_gAEPgABpYKENV_G__bXlj8X736ftkeY1f9_hz7sQxBhfJk-4FzLuW_JwX32EzNA36tqYKmRIAu1JBIQNlGIDUDUCgaogVrzDMaEWcoSNKJ6BkgFMRQ2dYCF5OmwtjeQKY5vp_d1d52R-t7dr83dzyz4VHv3YZXua1WJCdA58tDfv9bRObc9IKt_x8v4v0_N_rE2_eT1l_tAAAAAAAAAAAAAAAAAAAAAAABBQgAowAAAAIAAAAAAAAAgAAIACIACAAAAAAAFAAAAYIAAIGAQAggAAgBAACAACAABAAAAAAAAAEAAAAAIBAAAAABAACAAAAAAAQEAAIAJAQAAAAAkAFEACBQIAAIAACAIAAIAIIAUgAAAAIEEAIAiggAAAECBQAAAAAAIAAALAwDAAgJUJAAEgAIAAAQAIBBIAAAAAAAAAAAAAAAAAAAAAAAAICgSCQAAgABcAFAAVAA4AB4AEAAL4AZABqADwAIgATAAqgBvAD0AH4AQkAhgCJAEcAJYATQAwABhwDKAMsAbMA7gDvgHsAfEA-wD9gH-AgABFICLgIwARqAkQCSgFBgKgAq4BcwC9AGKANEAbQA3ABxAEOgJEATsAocBR4CkQFsALkAXeAvMBhoDJAGTgMuAZmAzmBq4GsgNvAbmA3UBwQDkwHLgPHAe0A_4CEIELQIXwQ9BD8ChAUAGAIoBdAD7AgBIADYAJAAjgEcAJSATQAnYB_QEygJsAUgArkBYgC3AF_gNqAfKBGAMACATYA2odBVAAXABQAFQAOAAggBcAF8AMgA1AB4AEQAJgAUwAqwBcAF0AMQAbwA9AB-gEMARIAlgBNACjAGAAMMAZQA0QBsgDvgHsAfEA-wD9AH_ARQBGICOgJKAUGAqICrgFiALnAXkBegDFAG0ANwAcQA6gB9gEOgIvASIAmQBOwChwFHgKaAVYAsWBbAFsgLdAXAAuQBdoC7wF5gL6AYaAx6BkYGSAMnAZVAywDLgGZgM5AarA1cDWAG3gN1AcWA5MBy4DxwHtAPrAfcA_sB_wEAQIWgQ6Ah6PABACKAfYOALgAXABIAEcAKAAfABHADkAI4ASkAnYB_QE2AK5AWIAtwBf4DaoG5gboA5YB8oEBAIGARgEAAwASAJsAbUKABAJsAbUMABAJsAbUQgSgALAAoAC4AGoAVQAuABiADeAHoARwAwIB3AHeAP8AigBKQCgwFRAVcAuYBigDaAHUAU0AqwBYoC0QFwALkAZGAycBnIDVQHjgP7AhQBC0CHQEPSIAIBMQD7CAAwAB4A5ACOAJsAWIAzwBtQDdAHLAQEAhmBGAlAoAAQAAsACgAHAAeABEACYAFUALgAYoBDAESAI4AUYAwABsgDvAH5AVEBVwC5gGKAOoAhABDoCLwEiAKPAU0AsUBbAC84GRgZIAycBnIDWAG3gPaAgCBA8CEIEPSYAEB9hIAcABcAI4BHAE2ALcAX-AywBngDdAHLAP9AgIBDMCMBSCIAAuACgAKgAcABAADQAHgARAAmABSACqAGIAP0AhgCJAFGAMAAZQA0QBsgDvgH4AfoBFgCMAEdAJKAUGAqICrgFzALyAYoA2gBuADqAHtAPsAh0BF4CRAE7AKHAUmApoBVgCxQFsALgAXIAu0BeYC-gGGwMjAyQBk8DLAMuAZzA1gDWQG3gN1AcEA5MB4oDxwHtAP7Af8BCECFoEM4Icgh0VACAAKATKA-wCORQAqABcAEgAMgAjgBbADaAOQAfYBBwCOAEpAQgAmwBUgC3AGeQNzA3QB_oEBAIXgRgLQCwAagDAAHcAXoA-wChwFNAKsAZmA8cCHoAA.YAAAAAAAAAAA",
    "consentUUID": "ce6117e4-837c-454d-b234-ef78bf988dbe_31_36",
    "_sp_v1_data": "74646",
}

headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    # 'cookie': 'kndctr_B21B678254F601E20A4C98A5_AdobeOrg_identity=CiY0MzAzMTUzMDkzNzI2NzY5NjcyMDIxNTU4NDk3MjM5OTA1MDg2OFIRCNf-pZv0MRgBKgRJUkwxMAHwAdf-pZv0MQ==; AMCV_B21B678254F601E20A4C98A5%40AdobeOrg=MCMID|43031530937267696720215584972399050868; _sp_v1_ss=1:H4sIAAAAAAAAAItWqo5RKimOUbKKhjHySnNydGKUUpHYJWCJ6traWFwSSjqYBmFn5IEYBrhNoqKEUiwAqTzxSd8AAAA%3D; _sp_v1_p=771; euconsent-v2=CQFCpIAQFCpIAAGABCENBHFsAP_gAEPgABpYKENV_G__bXlj8X736ftkeY1f9_hz7sQxBhfJk-4FzLuW_JwX32EzNA36tqYKmRIAu1JBIQNlGIDUDUCgaogVrzDMaEWcoSNKJ6BkgFMRQ2dYCF5OmwtjeQKY5vp_d1d52R-t7dr83dzyz4VHv3YZXua1WJCdA58tDfv9bRObc9IKt_x8v4v0_N_rE2_eT1l_tAAAAAAAAAAAAAAAAAAAAAAABBQgAowAAAAIAAAAAAAAAgAAIACIACAAAAAAAFAAAAYIAAIGAQAggAAgBAACAACAABAAAAAAAAAEAAAAAIBAAAAABAACAAAAAAAQEAAIAJAQAAAAAkAFEACBQIAAIAACAIAAIAIIAUgAAAAIEEAIAiggAAAECBQAAAAAAIAAALAwDAAgJUJAAEgAIAAAQAIBBIAAAAAAAAAAAAAAAAAAAAAAAAICgSCQAAgABcAFAAVAA4AB4AEAAL4AZABqADwAIgATAAqgBvAD0AH4AQkAhgCJAEcAJYATQAwABhwDKAMsAbMA7gDvgHsAfEA-wD9gH-AgABFICLgIwARqAkQCSgFBgKgAq4BcwC9AGKANEAbQA3ABxAEOgJEATsAocBR4CkQFsALkAXeAvMBhoDJAGTgMuAZmAzmBq4GsgNvAbmA3UBwQDkwHLgPHAe0A_4CEIELQIXwQ9BD8ChAUAGAIoBdAD7AgBIADYAJAAjgEcAJSATQAnYB_QEygJsAUgArkBYgC3AF_gNqAfKBGAMACATYA2odBVAAXABQAFQAOAAggBcAF8AMgA1AB4AEQAJgAUwAqwBcAF0AMQAbwA9AB-gEMARIAlgBNACjAGAAMMAZQA0QBsgDvgHsAfEA-wD9AH_ARQBGICOgJKAUGAqICrgFiALnAXkBegDFAG0ANwAcQA6gB9gEOgIvASIAmQBOwChwFHgKaAVYAsWBbAFsgLdAXAAuQBdoC7wF5gL6AYaAx6BkYGSAMnAZVAywDLgGZgM5AarA1cDWAG3gN1AcWA5MBy4DxwHtAPrAfcA_sB_wEAQIWgQ6Ah6PABACKAfYOALgAXABIAEcAKAAfABHADkAI4ASkAnYB_QE2AK5AWIAtwBf4DaoG5gboA5YB8oEBAIGARgEAAwASAJsAbUKABAJsAbUMABAJsAbUQgSgALAAoAC4AGoAVQAuABiADeAHoARwAwIB3AHeAP8AigBKQCgwFRAVcAuYBigDaAHUAU0AqwBYoC0QFwALkAZGAycBnIDVQHjgP7AhQBC0CHQEPSIAIBMQD7CAAwAB4A5ACOAJsAWIAzwBtQDdAHLAQEAhmBGAlAoAAQAAsACgAHAAeABEACYAFUALgAYoBDAESAI4AUYAwABsgDvAH5AVEBVwC5gGKAOoAhABDoCLwEiAKPAU0AsUBbAC84GRgZIAycBnIDWAG3gPaAgCBA8CEIEPSYAEB9hIAcABcAI4BHAE2ALcAX-AywBngDdAHLAP9AgIBDMCMBSCIAAuACgAKgAcABAADQAHgARAAmABSACqAGIAP0AhgCJAFGAMAAZQA0QBsgDvgH4AfoBFgCMAEdAJKAUGAqICrgFzALyAYoA2gBuADqAHtAPsAh0BF4CRAE7AKHAUmApoBVgCxQFsALgAXIAu0BeYC-gGGwMjAyQBk8DLAMuAZzA1gDWQG3gN1AcEA5MB4oDxwHtAP7Af8BCECFoEM4Icgh0VACAAKATKA-wCORQAqABcAEgAMgAjgBbADaAOQAfYBBwCOAEpAQgAmwBUgC3AGeQNzA3QB_oEBAIXgRgLQCwAagDAAHcAXoA-wChwFNAKsAZmA8cCHoAA.YAAAAAAAAAAA; consentUUID=ce6117e4-837c-454d-b234-ef78bf988dbe_31_36; _sp_v1_data=74646',
    "pragma": "no-cache",
    "priority": "u=1, i",
    # "referer": "https://www.transfermarkt.nl/teun-koopmeiners/profil/spieler/360518",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
}


def parse_velue_dev_response(response):
    parsed_response = []
    values_list = response.json()["list"]
    for value in values_list:
        parsed_value = {}
        parsed_value["x"] = value.get("x", None)
        parsed_value["y"] = value.get("y", None)
        parsed_value["mw"] = value.get("mw", None)
        parsed_value["datum_mw"] = value.get("datum_mw", None)
        parsed_value["verein"] = value.get("verein", None)

        parsed_response.append(parsed_value)

    return parsed_response


def get_player_plot(player_id, headers):
    response = requests.get(
        f"https://www.transfermarkt.nl/ceapi/marketValueDevelopment/graph/{player_id}",
        # cookies=cookies,
        headers=headers,
    )
    return response


def get_players_page(page_no, headers):
    params = {
        "ajax": "yw1",
    }

    response = requests.get(
        f"https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop/mw/ajax/yw1/cpAuthError/access_denied/cpAuthErrorDescription/page/4/20/6/5/7/2/9/page/page/{page_no}",
        params=params,
        # cookies=cookies,
        headers=headers,
    )

    return response


def parse_players_page(players_table_response):
    parsed_response = []
    players_table_html = players_table_response.content
    soup = BeautifulSoup(players_table_html, "html.parser")
    a_tags = soup.select(".responsive-table .inline-table td.hauptlink > a")
    for a_tag in a_tags:
        parsed_value = {}
        parsed_value["name"] = a_tag.get("title", None)
        href = a_tag.get("href", None)
        parsed_value["player_id"] = href.split("/spieler/")[-1]
        parsed_response.append(parsed_value)

    return parsed_response


if __name__ == "__main__":
    import time
    import pickle
    from tqdm import tqdm

    # page_nos = [1, 3, 5, 7, 10]
    # player_ids = []
    # for page_no in tqdm(page_nos):
    #     players_table = get_players_page(page_no=page_no, headers=headers)
    #     parsed_player_ids = parse_players_page(players_table_response=players_table)
    #     player_ids += parsed_player_ids
    #     time.sleep(1)

    # with open("player_ids.pickle", "wb") as f:
    #     pickle.dump(player_ids, f)

    with open("player_ids.pickle", "rb") as f:
        player_ids = pickle.load(f)

    player_value_dev_curves = player_ids.copy()
    for player in tqdm(player_value_dev_curves):

        player_plot = get_player_plot(player_id=player["player_id"], headers=headers)
        parsed_player_value_dev = parse_velue_dev_response(response=player_plot)
        player["values"] = parsed_player_value_dev.copy()
        time.sleep(2)

    with open("player_values.pickle", "wb") as f:
        pickle.dump(player_value_dev_curves, f)
