#encoding=utf8

import sqlite3
import webbrowser
from wox import Wox,WoxAPI

_clipboard_exit=True
try:
    import clipboard
except ImportError:
    _clipboard_exit=False
    

class Wubi(Wox):
    def is_all_chinese(self,strs):
        for _char in strs:
            if not '\u4e00' <= _char <= '\u9fa5':
                return False
            return True

    def findChar(self,codes):
        ret={}
        if 0 < len(codes) <= 4:
            conn = sqlite3.connect('wubi-haifeng86.db')
            c = conn.cursor()
            cursor = c.execute("SELECT * from goucima WHERE goucima like '" + codes + "%'")
            for row in cursor:
                ret[row[0]]=row[1]
            conn.close()
            return ret
        else:
            return ret

    def findCode(self,strs):
        ret={}
        conn = sqlite3.connect('wubi-haifeng86.db')
        c = conn.cursor()
        for _char in strs:
            cursor = c.execute("SELECT goucima from goucima WHERE zi='" + _char + "'")
            for row in cursor:
                ret[_char]=row[0]
        conn.close()
        return ret


    def query(self,key):
        results = []
        title = "输入汉字或者五笔编码"

        if self.is_all_chinese(key):
            ret = self.findCode(key)
        else:
            ret = self.findChar(key)

        cnt = 1
        for _itr in ret:
            if cnt <= 20:
                results.append({"Title": _itr+" - "+ret[_itr] ,"IcoPath":"Images/app.png","JsonRPCAction":{"method": "copyContent","parameters":[_itr+" - "+ret[_itr]],"dontHideAfterAction":False}})
                cnt += 1
            else:
                break
        return results

    def copyContent(self,content):
        if _clipboard_exit:
            clipboard.copy(content)
        #webbrowser.open("https://baidu.com/s?word="+content)
        #todo:doesn't work when move this line up 
        #WoxAPI.change_query(url)

if __name__ == "__main__":
    Wubi()
