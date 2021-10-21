import os
import os.path as osp
import xml.dom.minidom
import random
import shutil

class XMLTools:

    def __init__(self, xmlFilesRoot, txtFilesRoot):
        self.xmlFilesRoot = xmlFilesRoot
        self.txtFilesRoot = txtFilesRoot

    def xmlToTxt(self, postName):

        class_map = {}
        id = 1
        if not osp.exists(osp.join(self.txtFilesRoot, "train")):
            os.makedirs(osp.join(self.txtFilesRoot, "train"))
        if not osp.exists(osp.join(self.txtFilesRoot, "test")):
            os.makedirs(osp.join(self.txtFilesRoot, "test"))

        out1, out2 = open(osp.join(self.txtFilesRoot, "train_" + postName + ".txt"), "w"), open(osp.join(self.txtFilesRoot, "train_" + postName + ".txt"), "w")
        dst1, dst2 = osp.join(self.txtFilesRoot, "train"), osp.join(self.txtFilesRoot, "test")

        for roots, dirs, files in os.walk(self.xmlFilesRoot):
            for f in files:
                if not f.endswith('.xml'):
                    continue
                (out, dst) = (out2, dst2) if random.randint(0, 9) == 0 else (out1, dst1)
                filename = osp.splitext(f)[0] + ".jpg"
                shutil.copyfile(osp.join(roots, filename), osp.join(dst, filename))

                out.write("#\n")
                DOMTree = xml.dom.minidom.parse(osp.join(roots, f))
                ano = DOMTree.documentElement
                out.write(filename + "\n")
                w = ano.getElementsByTagName("size")[0].getElementsByTagName("width")[0].childNodes[0].nodeValue
                h = ano.getElementsByTagName("size")[0].getElementsByTagName("height")[0].childNodes[0].nodeValue
                out.write(w + " " + h + "\n")
                objs = ano.getElementsByTagName("object")
                objs_cnt = len(objs)
                out.write(str(objs_cnt) + "\n")

                for obj in objs:
                    class_name = obj.getElementsByTagName("name")[0].childNodes[0].nodeValue
                    if class_name not in class_map:
                        class_map[class_name] = id
                        id += 1
                    class_id = class_map[class_name]
                    bbox = obj.getElementsByTagName("bndbox")[0]
                    xmin = bbox.getElementsByTagName("xmin")[0].childNodes[0].nodeValue
                    ymin = bbox.getElementsByTagName("ymin")[0].childNodes[0].nodeValue
                    xmax = bbox.getElementsByTagName("xmax")[0].childNodes[0].nodeValue
                    ymax = bbox.getElementsByTagName("ymax")[0].childNodes[0].nodeValue
                    ostr = xmin + " " + ymin + " " + xmax + " " + ymax + " " + str(class_id) + "\n"
                    out.write(ostr)
        out1.close()
        out2.close()

m_tools = XMLTools(r'D:\work\Code\feather\data\xml\tianchi', r'D:\work\Code\feather\data\txt\tianchi')
m_tools.xmlToTxt("tianchi")




