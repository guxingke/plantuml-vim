#!/usr/bin/env python3
import vim
import sys
import subprocess
import shlex


def _vimerr(errmsg):
    sys.stderr.write(errmsg)

def _fetchCodeBlock():
    buf = vim.current.buffer
    r, c = vim.current.window.cursor

    beginCapture = False
    finishCapture = False
    graphCodeBuf = ""

    start = -1
    end = -1

    # Find @plantuml xxx upwords
    toggle = True
    savebuf = buf[:r]
    for idx, line in enumerate(savebuf[::-1]):
        if line.rstrip() == "@enduml":
            _vimerr("Please locate cursor INSIDE the plantuml code block")
            return None
        if line.rstrip().startswith("@startuml"):
            start = r - idx - 2
            break

    if start == -1:
        _vimerr("Can't find plantuml block")
        return None

    #print("plantuml start at {}".format(start))

    for idx, line in enumerate(buf[start:]):
        #print("DBG:" + line)
        if line.rstrip().startswith("@startuml") and not beginCapture:
            beginCapture = True
            continue
        if line.rstrip() == "@enduml" and beginCapture:
            finishCapture = True
            end = start + idx + 2
            break
        if beginCapture:
            graphCodeBuf = graphCodeBuf + "\n" + line

    #print("plantuml end at {}".format(end))

    #print(graphCodeBuf)

    eb = buf[end:]
    if eb:
        ne = end
        for el in eb:
            if el == "": # blank line
                ne = ne + 1
                continue
            if el.strip() == "</div>":
                toggle = False
                ne = ne + 1
                continue
            if el == "": # blank line
                ne = ne+ 1
                continue
            if "plantuml" in el:
                ne = ne + 1
                break

    if not toggle:
        end = ne;

        while buf[start - 1] == "": # blank line
            start = start -1
        if buf[start-1].strip() == "<div hidden>":
            start = start - 1
        else: # bad case
            _vimerr("Can't find toggle start tag {}".format("<div hidden>"))
            return

    if not finishCapture:
        _vimerr("Can't find End Of Block {}".format("@enduml"))
        return

    return (toggle, start, end)


def Toggle():
    ret = _fetchCodeBlock()
    if ret is None:
        return
    t, s, e = ret
    codeb = "\n".join(vim.current.buffer[s+2:e-2])

    #print("T = {},  S = {},E = {}".format(t, s, e))
    #print("Code Block is\n{}\n".format(codeb))

    if codeb is None:
        _vimerr("Can't find graph")
        return

    if t:
        # Clear the range and append the graph
        r = vim.current.buffer.range(s+1, e)
        offset=0

        uc = "\n".join(r[1:-1])
        #print("Code Block is\n{}\n".format(uc))

        ret = _callExternal(uc)
        if not ret:
            _vimerr("Can't gen graph")
            return;


        t = []
        t.append("<div hidden>")
        t.append("")
        for line in r:
            t.append(line)
        t.append("</div>")
        t.append("")
        t.append("![](https://www.plantuml.com/plantuml/svg/{})".format(ret))

        #print("Code Block is\n{}\n".format(t))

        r[:] = None

        for line in t:
            offset = offset + 1
            r.append(line)
        vim.command("normal! " + str(offset) + "j")
    else:
        r = vim.current.buffer.range(s+1, e)
        t = []
        t.append("```plantuml")
        sb = False
        for line in r:
            if sb:
                t.append(line)
                if line.startswith("@enduml"):
                    break
            elif line.startswith("```plantuml"):
                sb = True
        t.append("```")

        r[:] = None

        offset=0
        for line in t:
            offset = offset + 1
            r.append(line)
        vim.command("normal! " + str(offset) + "j")


def _callExternal(buf):
    cmdarg = shlex.split("/usr/local/bin/plantuml -p -encodeurl ")
    proc = subprocess.Popen(
            cmdarg,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    try:
        proc.stdin.write(bytes(buf, "UTF-8"));

        out, err = proc.communicate(timeout=20)
        if proc.returncode != 0:
            if not out:
                errmsg = "call error, {}".format(err.decode("UTF-8"))
                _vimerr(errmsg)
            proc.stdin.close()
            proc.wait()
            return str(out, "UTF-8").strip()
        proc.stdin.close()
    except subprocess.TimeoutExpired:
        proc.kill()
        _vimerr("call time out")
        return None
    proc.wait()
    return str(out, "UTF-8")
