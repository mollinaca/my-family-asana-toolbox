#!/usr/bin/env python3
import asana_functions
import discord_post

def main():
    new_task_found = False # 新タスクが発見されたら True にする
    answer = [] # 新タスクの uri を入れるリスト ("name","permalink_url") のタプルを一つの要素として入れる

    a = asana_functions.AsanaFunctions()
    task_gid_list = a.get_all_tasks()
    if not task_gid_list["ok"]:
        # 通知
        exit (1)

    for task_gid in task_gid_list["tasks"]:
        # bot-checked タグがついてるか確認する
        res = a.get_task_is_botchecked(task_gid)

        if not res["is_botchecked"]: # bot が未チェックのタスク（新タスク）を発見
            new_task_found = True
            r = res["response"]["response"]
            answer.append((r["name"], r["permalink_url"]))

            # タスクをチェック済みにする
            r = a.check_task_is_botchecked(task_gid)

    if new_task_found:
        message = "新しいタスクが作成されました。がんばってね。\n"
        message += "\n\n".join(f"{x}\n{y}" for x, y in answer)
        discord_post.post(message)

if __name__ == '__main__':
    main()
