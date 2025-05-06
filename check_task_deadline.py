#!/usr/bin/env python3
from datetime import datetime, timedelta
import asana_functions
import discord_post

def main():
    deadline_task_found = False # 期日が近いタスクが発見されたら True にする
    answer = [] # 期日が近いタスクの uri を入れるリスト ("name : due_on","permalink_url") のタプルを一つの要素として入れる
    today = datetime.today().date()

    a = asana_functions.AsanaFunctions()
    task_gid_list = a.get_all_tasks()
    if not task_gid_list["ok"]:
        # 通知
        exit (1)

    for task_gid in task_gid_list["tasks"]:
        # タスクの期日を取得する
        res = a.get_task_deadline(task_gid)
        if not res["ok"]:
            # 通知
            exit (1)
        else:
            res = res["response"]["response"]

        due_on = res["due_on"]

        if due_on is None:
            continue

        date_deadline = datetime.strptime(due_on, "%Y-%m-%d").date()
        week_before_due = date_deadline - timedelta(days=7)

        if week_before_due <= today <= date_deadline:
            deadline_task_found = True
            answer.append((f"{res["name"]} : {due_on}", res["permalink_url"]))

    if deadline_task_found:
        message = "期日が近いタスクがあります。\n\n"
        message += "\n\n".join(f"{x}\n{y}" for x, y in answer)
        discord_post.post(message)
        print ("check_task_deadline completed")
        exit (0)
    else:
        print ("no deadline task found, exit script.")
        exit (0)

if __name__ == '__main__':
    main()
