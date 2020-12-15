" Plugin writing

py3 import vim, sys,os, importlib
py3 cwd = vim.eval('expand(\"<sfile>:p:h\")')
py3 sys.path.insert(0, os.path.join(cwd, "python"))
py3 import ge
py3 importlib.reload(ge)

function! Plantuml_Toggle()
    py3 ge.Toggle()
endfunction

nmap <Leader>gg :call Plantuml_Toggle()<CR>
