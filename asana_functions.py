import asana_api
from dotenv import load_dotenv
load_dotenv()

class AsanaFunctions:

    def __init__(self):
        self.a = asana_api.AsanaAPI()
        self.tag_bot_checkd = "1209970150654968"

    def get_task_deadline(self, task_gid:str = None):
        ret = {"ok": False}

        if task_gid is None:
            ret = {"ok": False, "response": "task_gid required"}
            return ret
        
        res = self.a.get_a_task(task_gid)
        due_date = res["response"]["due_on"]
        ret = {"ok": True, "due_on": due_date, "response": res}

    def create_a_task(self, task_name:str = None, task_notes:str = None, due_on:str = None):
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
