import os
import re
import asyncio
from dotenv import load_dotenv
from bilibili_api import video, Credential
import requests

load_dotenv()
COOKIE = os.getenv("BILIBILI_COOKIE", "").strip()
VIDEO_INPUT = os.getenv("BILIBILI_VIDEO", "").strip()


def parse_cookie(cookie_str):
    """从整段 Cookie 中提取关键字段"""
    data = {}
    for item in cookie_str.split(";"):
        item = item.strip()
        if "=" in item:
            k, v = item.split("=", 1)
            data[k] = v
    return data


def resolve_bvid(value: str) -> str:
    """从 BV 号或视频 URL 中解析出 bvid"""
    value = value.strip()
    if not value:
        raise ValueError("请在 .env 中设置 BILIBILI_VIDEO（BV 号或视频 URL）")
    match = re.search(r"(BV[\w]+)", value, re.IGNORECASE)
    if not match:
        raise ValueError(f"无法从 BILIBILI_VIDEO 解析 BV 号: {value}")
    return match.group(1)


async def main():
    bvid = resolve_bvid(VIDEO_INPUT)
    output_dir = os.path.join("subtitles", bvid)
    os.makedirs(output_dir, exist_ok=True)

    cookie_dict = parse_cookie(COOKIE)
    credential = Credential(
        sessdata=cookie_dict.get("SESSDATA", ""),
        bili_jct=cookie_dict.get("bili_jct", ""),
        buvid3=cookie_dict.get("buvid3", ""),
    )

    v = video.Video(bvid=bvid, credential=credential)

    info = await v.get_info()
    pages = info.get("pages", [])
    print(f"目标视频: {bvid}")
    print(f"输出目录: {output_dir}")
    print(f"检测到视频包含 {len(pages)} 个分 P，开始提取字幕...\n")

    for p in pages:
        page_num = p["page"]
        title = re.sub(r'[\\/:*?"<>|]', "_", p["part"])
        cid = p["cid"]

        try:
            sub_info = await v.get_subtitle(cid=cid)
            sub_list = sub_info.get("subtitles", [])

            if not sub_list:
                print(f"[P{page_num:02d}] {title} -> 未获取到字幕数据")
                continue

            sub_url = sub_list[0].get("subtitle_url", "")
            if sub_url.startswith("//"):
                sub_url = "https:" + sub_url
            elif not sub_url.startswith("http"):
                sub_url = "https://" + sub_url

            sub_res = requests.get(sub_url).json()

            txt_path = os.path.join(output_dir, f"P{page_num:02d}_{title}.txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                for line in sub_res.get("body", []):
                    f.write(line["content"] + "\n")

            print(f"[P{page_num:02d}] {title} -> 提取成功！")

        except Exception as e:
            print(f"[P{page_num:02d}] {title} -> 提取异常: {e}")


if __name__ == "__main__":
    asyncio.run(main())
