import os
import asana_api
from dotenv import load_dotenv
load_dotenv()

class AsanaFunctions:

    def __init__(self):
        self.a = asana_api.AsanaAPI()
        self.tag_bot_checkd = "1209970150654968"
        self.asana_ws_gid = os.getenv("ASANA_WS_ID")
        self.asana_pj_gid = os.getenv("ASANA_PJ_ID") # hstn-famliy-project
        self.asana_section_todo = os.getenv("ASANA_SECTION_TODO")
        self.asana_section_inprogress = os.getenv("ASANA_SECTION_INPROGRESS")
        self.asana_section_completed = os.getenv("ASANA_SECTION_COMPLETED")
        self.asana_section_archive2025 = os.getenv("ASANA_SECTION_ARCHIVED_2025")


    def get_all_tasks(self):
        """
        すべての todo と 進行中 セクションにあるタスクを取得し、その gid をリストにして返す
        """
        ret = {"ok": False}
        answer = []

        res = self.a.get_multiple_tasks(self.asana_section_todo)
        if not res["ok"]:
            print (res)
            exit (1)

        tasks_todo = res["response"]

        res = self.a.get_multiple_tasks(self.asana_section_inprogress)
        if not res["ok"]:
            print (res)
            exit (1)

        tasks_inpr = res["response"]

        for task in tasks_todo:
            answer.append(task["gid"])

        for task in tasks_inpr:
            answer.append(task["gid"])

        ret = {"ok": True, "tasks": answer}
        return ret

    def get_task_deadline(self, task_gid:str = None):
        """
        タスクの締め切り due_on を調べて返す
        """
        ret = {"ok": False}

        if task_gid is None:
            ret = {"ok": False, "response": "task_gid required"}
            return ret
        
        res = self.a.get_a_task(task_gid)
        due_date = res["response"]["due_on"]
        ret = {"ok": True, "due_on": due_date, "response": res}

        return ret
    
    def get_task_modified_at(self, task_gid:str = None):
        """
        タスクが最後に更新された日付 modified_at を調べて返す
        """
        ret = {"ok": False}

        if task_gid is None:
            ret = {"ok": False, "response": "task_gid required"}
            return ret
        
        res = self.a.get_a_task(task_gid)
        modified_at = res["response"]["modified_at"]
        ret = {"ok": True, "modified_at": modified_at, "response": res}

        return ret
    
    def get_task_is_botchecked(self, task_gid:str = None):
        """
        タスクにタグ bot-checked が付与されているかを調べて返す
        """
        ret = {"ok": False}

        if task_gid is None:
            ret = {"ok": False, "response": "task_gid required"}
            return ret
        
        res = self.a.get_a_task(task_gid)
        # tag フィールドがない場合
        if not "tags" in res["response"]:
            ret = {"ok": True, "is_botchecked": False, "response": res}

        else: # tag フィールドがある場合
            tags = res["response"]["tags"]
            if 1 <= len(tags): # この Asana プロジェクトで使われてる tag は bot-checkd の一つだけ
                ret = {"ok": True, "is_botchecked": True, "response": res}
            else:
                ret = {"ok": True, "is_botchecked": False, "response": res}
        
        return ret

    def get_last_story_from_a_task(self, task_gid:str = None):
        """
        タスクの最後の history を返す
        """
        ret = {"ok": False}
        if task_gid is None:
            ret = {"ok": False, "response": "task_gid required"}
            return ret
        
        res = self.a.get_stories_from_a_task(task_gid=task_gid)
        stories = list(res["response"])
        last = stories[len(stories)-1]
        last_type = last["type"]
        last_created_at = last["created_at"]

        ret = {"ok": True, "last_type": last_type, "last_created_at": last_created_at, "last_story": last}
        return ret

    def get_task_is_completed(self, task_gid:str = None):
        """
        タスクが完了しているかどうか調べる
        """
        ret = {"ok": False}
        if task_gid is None:
            ret = {"ok": False, "response": "task_gid required"}
            return ret

        res = self.a.get_a_task(task_gid)
        completed = res["response"]["completed"]
        ret = {"ok": True, "completed": completed, "response": res["response"]}

        return ret


    def check_task_is_botchecked(self, task_gid):
        """
        タスクにタグ bot-checkd を付与する
        """
        ret = {"ok": False}

        if task_gid is None:
            ret = {"ok": False, "response": "task_gid required"}
            return ret

        res = self.a.add_a_tag_to_a_task(task_gid) # tags を指定しない場合、 bot-checked がつくようになっている
        return res


    def create_a_task(self, task_name:str = None, task_notes:str = None, due_on:str = None):
        """
        タスクを作る
        """
        ret = {"ok": False}

        if task_name is None or task_notes is None:
            ret = {"ok": False, "response": "task_gid and task_notes required"}
            return ret
        
        res = self.a.create_a_task(task_name, task_notes, self.tag_bot_checkd, due_on)
        if res["ok"]:
            ret = {"ok": True, "response": res}
        else:
            ret = {"ok": False, "response": res}

        return ret

    def move_task_section_to_completed(self, task_gid:str = None):
        """
        タスクのセクションを completed へ移動する
        """
        ret = {"ok": False}
        if task_gid is None:
            ret = {"ok": False, "response": "task_gid required"}
            return ret

        res = self.a.add_a_task_to_section(task_gid=task_gid, section_gid=self.asana_section_completed)
        if res["ok"]:
            ret = {"ok": True, "response": res["response"]}
        else:
            ret = {"ok": False, "response": res["response"]}

        return ret
