import json
import yaml
import os
import random
import sys
from glob import glob
from typing import Any, Dict, List, Union

import requests
from yaml import safe_load

from Jamal.config import BAHASA
from Jamal.database import mongodb

# ambil collection users (nyimpen bahasa user)
langs_db = mongodb["Jamal"]["language"]["users"]

# cache default/global language
cek_bahasa = None  

bahasa_ = {}
bahasa_present = {}
loc_lang = "langs/strings/{}.yml"


async def get_lang(user_id: int):
    """ambil bahasa user dari cache/db"""
    global cek_bahasa
    lang = cek_bahasa
    # coba ambil dari DB user
    user = await langs_db.find_one({"_id": user_id})
    if user:
        lang = user.get("lang", BAHASA)
    # kalau belum ada → fallback config default
    if not lang:
        lang = BAHASA
    return lang


async def set_lang(user_id: int, lang: str):
    """update bahasa user ke db"""
    await langs_db.update_one(
        {"_id": user_id},
        {"$set": {"lang": lang}},
        upsert=True
    )


def load(file):
    """load file yaml"""
    if not file.endswith(".yml"):
        return
    elif not os.path.exists(file):
        file = loc_lang.format("en")
    code = file.split("/")[-1].split("\\")[-1][:-4]
    try:
        with open(file, encoding="UTF-8") as f:
            bahasa_data = safe_load(f)
            bahasa_[code] = bahasa_data
    except Exception as er:
        print(f"Error in {file[:-4]}\n\n{er} language file")


def bhs(key, lang: str = None, _res: bool = True):
    """ambil string bahasa sesuai user"""
    lang = lang or cek_bahasa or "en"
    try:
        return bahasa_[lang][key]
    except KeyError:
        try:
            en_ = bahasa_["en"][key]
            tr = translate(en_, lang_tgt=lang).replace("\ N", "\n")
            if en_.count("{}") != tr.count("{}"):
                tr = en_
            if bahasa_.get(lang):
                bahasa_[lang][key] = tr
            else:
                bahasa_.update({lang: {key: tr}})
            return tr
        except KeyError as e:
            if not _res:
                print(f"Warning: could not load any string with the key `{key}` {e}")
                return
        except Exception as er:
            print(f"Warning: could not load any string with the key `{er}`")
        if not _res:
            return None
        return bahasa_["en"].get(key) or print(
            f"Failed to load language string '{key}'"
        )


def get_bhs(key):
    doc = bhs(f"{key}", _res=False)
    if doc:
        return cgr("cmds") + doc



def get_bahasa_() -> List[Dict[str, Union[str, List[str]]]]:
    bahasa_list = []
    for file in glob("langs/strings/*yml"):
        load(file)
    try:
        for code, data in bahasa_.items():
            if data is not None:
                bahasa_list.append(
                    {"code": code, "name": data.get("name", "")}
                )
        return bahasa_list
    except KeyError as e:
        print(f"KeyError: {e} not found in language file")


# init bahasa default (fallback)
for filename in os.listdir(r"./langs/strings/"):
    if "en" not in bahasa_:
        bahasa_["en"] = yaml.safe_load(
            open(r"./langs/strings/en.yml", encoding="utf8")
        )
        bahasa_present["en"] = bahasa_["en"]["name"]
    if filename.endswith(".yml"):
        language_name = filename[:-4]
        if language_name == "en":
            continue
        bahasa_[language_name] = yaml.safe_load(
            open(r"./langs/strings/" + filename, encoding="utf8")
        )
        for item in bahasa_["en"]:
            if item not in bahasa_[language_name]:
                bahasa_[language_name][item] = bahasa_["en"][item]
    try:
        bahasa_present[language_name] = bahasa_[language_name]["name"]
    except:
        print("There is some issue with the language file inside bot.")
        sys.exit(1)
