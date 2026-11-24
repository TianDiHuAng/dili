# -*- coding: utf-8 -*-
"""第90轮：D143 审计周期——assess.py 全函数边界用例。"""
import sys,os,importlib
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import assess; importlib.reload(assess)
from assess import (is_data, is_alias, is_bad_type, has_content, strength,
                    count_entry, level_of, content_count, _nums, MIN_CITED, MIN_BODY)

FAIL=[]
def chk(name, got, want, note=""):
    ok = (got==want)
    if not ok: FAIL.append(name)
    print(f"  {'OK ' if ok else '⚠  '} {name}: got={got!r} want={want!r} {note}")

print("=== 1. is_data 前缀 ===")
for sid,exp in (("wb-aus-pop",True),("usgs-eq-x",True),("noaa-current-x",True),
                ("ats-parties-x",True),("wikidata-Q1",True),("openalex-W1",False),("s001-fao-org",False)):
    chk(f"is_data({sid})", is_data(sid), exp)

print("\n=== 2. is_alias ===")
for sid in ("britannica-regions","wikipedia-regions","un-m49","ap-human-geo","s010-unesco-org","livius-polis"):
    chk(f"is_alias({sid})", is_alias(sid), sid!="livius-polis")

print("\n=== 3. is_bad_type ===")
chk("书评", is_bad_type({"type":"书评"}), True)
chk("book-review", is_bad_type({"type":"book-review"}), True)
chk("学术文献", is_bad_type({"type":"学术文献"}), False)

print("\n=== 4. _nums 多值取最小（D142）===")
chk("多值", _nums("正文 5,455 字符。 正文 750 字符。"), (None,750))
chk("单值", _nums("摘要长度 1200 字符"), (None,1200))
chk("被引+正文", _nums("被引 42。正文 900 字符"), (42,900))

print("\n=== 5. has_content 门槛 ===")
chk("被引>=10", has_content("openalex-A", {"note":"被引 10。摘要长度 100 字符"}), True)
chk("被引9+正文799", has_content("openalex-B", {"note":"被引 9。摘要长度 799 字符"}), False)
chk("被引9+正文800", has_content("openalex-C", {"note":"被引 9。摘要长度 800 字符"}), True)
chk("空壳页", has_content("s008-x", {"note":"【空壳页判定】正文 218 字符。正文 137675 字符。"}), False)
chk("书评", has_content("openalex-D", {"note":"被引 50。","type":"书评"}), False)
chk("数据端点", has_content("wb-x", {"note":"被引 50。"}), False)

print("\n=== 6. strength 判定顺序 ===")
src={"note":"被引 50。摘要长度 900 字符。"}
chk("data→data", strength("wb-x", src, None), "data")
chk("alias→alias", strength("un-m49", src, None), "alias")
chk("bad_type→side", strength("openalex-X", {"note":"被引 50。","type":"书评"}, None), "side")
chk("空壳页→weak", strength("s008-x", {"note":"【空壳页判定】被引 50。摘要长度 900 字符。"}, None), "weak")
chk("强→strong", strength("openalex-Y", src, None), "strong")
chk("弱→weak", strength("openalex-Z", {"note":"被引 2。摘要长度 300 字符"}, None), "weak")
e_side={"pending_notes":"【第50轮】openalex-S 对象碰撞，剔除。","sources":["openalex-S"]}
chk("segment side", strength("openalex-S", src, e_side), "side")

print("\n=== 7. level_of + D141 ===")
def mk(sids):
    return {"title":"T","sources":sids,"pending_notes":"","tier":"重要"}
S={
 "openalex-1":{"note":"被引 50。摘要长度 900 字符"},
 "openalex-2":{"note":"被引 50。摘要长度 900 字符"},
 "s059-worldbank-org":{"note":"正文 10556 字符"},
 "wb-x":{"note":"数据端点"},
}
chk("A（2强）", level_of(mk(["openalex-1","openalex-2"]), S), "A")
chk("B（1学术强）", level_of(mk(["openalex-1"]), S), "B")
chk("D（1机构强+数据，D141）", level_of(mk(["s059-worldbank-org","wb-x"]), S), "D")
chk("B（1机构强无数据）", level_of(mk(["s059-worldbank-org"]), S), "B")
chk("C（0强0数据）", level_of(mk([]), S), "C")

print("\n=== 8. count_entry / content_count ===")
c=count_entry(mk(["openalex-1","s059-worldbank-org","wb-x","un-m49"]), S)
chk("counts.strong", c["strong"], 2)
chk("counts.data", c["data"], 1)
chk("counts.alias", c["alias"], 1)
chk("content_count", content_count(mk(["openalex-1","s059-worldbank-org","wb-x","un-m49"]), S), 2)

print("\n=== 9. 边界：D 级是否被 content_count 计入 ===")
d_entry=mk(["s059-worldbank-org","wb-x"])
chk("D级content_count", content_count(d_entry,S), 1)
chk("D级level", level_of(d_entry,S), "D")

print(f"\n{'='*50}\n失败项 {len(FAIL)}: {FAIL if FAIL else '无'}")
sys.exit(1 if FAIL else 0)