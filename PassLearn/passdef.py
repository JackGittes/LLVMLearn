from typing import Dict, List
import json


def parse_pass(pass_file: str, passdef: str):
    dep_cnt: Dict[str, int] = dict()
    with open(pass_file, "r") as fp:
        passes = fp.read()
    pass1 = passes.split("\n")
    with open(passdef, "r") as fp:
        deppass = fp.read()
    pass2 = list()
    dep_dict: Dict[str, List[str]] = dict()
    for deps in deppass.split("\n"):
        pri_pass, sec_pass = deps.split(" ")
        pass2.append(pri_pass)
        pass2.append(sec_pass)
        if pri_pass not in dep_dict.keys():
            dep_dict[pri_pass] = [sec_pass]
        else:
            dep_dict[pri_pass].append(sec_pass)
        dep_cnt[sec_pass] = 1 + dep_cnt.get(sec_pass, 0)
    uni_pass2 = set(pass2)
    for p in uni_pass2:
        if p not in pass1:
            pass1.append(p)
    pass1 = sorted(set(pass1))
    with open("deps.json", "w") as fp:
        json.dump(dep_dict, fp)
    with open("fullpass.log", "w") as fp:
        for idx, p in enumerate(pass1):
            fp.write(p + ('\n' if idx != len(pass1) - 1 else ""))
    with open("depcnt.log", "w") as fp:
        sorted_keys = sorted(dep_cnt.keys())
        for idx, k in enumerate(sorted_keys):
            fp.write(k + ": " + str(dep_cnt[k]) + ('\n' if idx != len(dep_cnt) - 1 else ""))


def write_dot():
    with open("deps.json", "r") as fp:
        relations = json.load(fp)
    with open("passdep.dot", "w") as fp:
        fp.write("digraph passdep {\n")
        for item in relations.keys():
            fp.write("  " + item + ";\n")
        label = 0
        for pri, sec in relations.items():
            for sec_pass in sec:
                fp.write("  " + pri + " -> " + sec_pass +
                         ' [label="{}"];\n'.format(label))
                label += 1
        fp.write("}\n")



if __name__ == "__main__":
    parse_pass("/home/zhaomingxin/CodeBase/LLVM-learn/llvm-project/pass.log",
               "/home/zhaomingxin/CodeBase/LLVM-learn/llvm-project/depmiddle.log")
    write_dot()