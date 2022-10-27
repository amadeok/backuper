import os

src = "E:\\amadeo\\SwordKing\\"
dst = "C:\\Users\\amade\\Documents\\Unreal Projects\\SwordKing503\\"

def listfiles(path):
    files = []
    for dirName, subdirList, fileList in os.walk(path):
        dir = dirName.replace(path, '')
        for fname in fileList:
            files.append(os.path.join(dir, fname))
    return files

x = listfiles(src)
y = listfiles(dst)