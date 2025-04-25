#!/usr/bin/env python3
import asana_functions
import discord_post

def main():
    task_is_moved = False # 完了したタスクがあり移動されたら True になる
    answer = [] # 完了タスクの uri を入れるリスト ("name","permalink_url") のタプルを一つの要素として入れる

    a = asana_functions.AsanaFunctions()
    task_gid_list = a.get_all_tasks()
    if not task_gid_list["ok"]:
        # 通知
        exit (1)

    for task_gid in task_gid_list["tasks"]:
        # タスクが完了しているか調べる
        res = a.get_task_is_completed(task_gid)

        if res["completed"]: # タスクが完了済み
            r = a.move_task_section_to_completed(task_gid)
            if not r["ok"]:
                # 通知
                exit (1)

            task_is_moved = True
            answer.append((res["response"]["name"], res["response"]["permalink_url"]))

    if task_is_moved:
        message = "以下のタスクが完了しました。お疲れ様でした！\n\n"
        message += "\n\n".join(f"{x}\n{y}" for x, y in answer)
        discord_post.post(message)
        print ("move_task_section completed")
        exit (0)
    else:
        print ("no task completed, exit script.")
        exit (0)


if __name__ == '__main__':
    main()
