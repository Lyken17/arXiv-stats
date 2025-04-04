from datetime import datetime
import json
from termcolor import colored

def main(
    tg_token: str = None,
    tg_chat_id: str = None,
) -> None:
    # Get current date/time in Eastern timezone
    year = datetime.now().strftime("%Y")
    month = datetime.now().strftime("%B") 
    day = datetime.now().strftime("%d")

    with open("info/%s-%s/%s/paper_info.json" % (year, month, day), "r") as fp:
        information = json.load(fp)

    watchlist_authors = [
        "Ji Lin",
        "Zhijian Liu",
        "Yao Lu",
        "Ligeng Zhu",
        "Ilya Sutskever",
        "Gao Huang", 
        "Song Han",
        "Hongxu Yin",
    ]
    watchlist_keywords = [
        "reason",
        "r1",
        "VILA", 
        "Sana",
        "Leakage",
        "Deepseek"
    ]
    watchlist_authors = [_.lower() for _ in watchlist_authors]
    watchlist_keywords = [_.lower() for _ in watchlist_keywords]

    import Echoo

    echo_msg = f""
    for info in information:
        count = 0
        reasons = ""
        w_authors = []
        w_keywords = []
        for author in info["authors"]:
            if author.lower() in watchlist_authors:
                count += 1
                w_authors.append(author)
        if len(w_authors) > 0:
            reasons += "\tAuthor: " + ", ".join(w_authors) + "\n"
            print("Author: ", colored(", ".join(w_authors), "yellow"))
        
        for key in watchlist_keywords:  
            if key in info["title"].lower():
                count += 1
                w_keywords.append(key)
        if len(w_keywords) > 0:
            reasons += "\tKeyword: " + ", ".join(w_keywords) + "\n"
            print("Keyword: ", colored(", ".join(w_keywords), "green"))
        
        if count > 0:
            print(info)
            print("-" * 100)
            url = "http://arxiv.org/abs/" + info["id"]
            echo_msg += f"**{info['title']}**\n" + reasons + "\t" + url + "\n"


    from markdown import markdown

    echo_msg_html = markdown(echo_msg)
    echo_msg_html = echo_msg_html.replace("<p>", "").replace("</p>", "")
    echo_msg_html = f"<blockquote>{year}-{month}-{day} update </blockquote>\n" + echo_msg_html
    Echoo.echoo_exec(echo_msg_html, parse_mode="HTML", no_escape=True, token=tg_token, chat_id=tg_chat_id)


if __name__ == "__main__":
    import fire
    fire.Fire(main)
