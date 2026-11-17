import json, subprocess, sys
ds=[(a.split(':')[0], int(a.split(':')[1])) for a in sys.argv[1:]]
def tts(b,n): return subprocess.run(['python3','/home/claude/video2d/tao_video.py',b,str(n),'--tts'],capture_output=True,text=True).stdout.strip()
t="\n".join(tts(b,n) for b,n in ds)
nk=json.load(open('/home/claude/video2d/elio/nhat_ky.json'))
print("const t = "+json.dumps(t,ensure_ascii=False)+";\nconst el = document.querySelector('textarea[aria-label=\"Speech block text\"]');\nel.focus(); el.select(); document.execCommand('insertText', false, t);\n[el.value.length, el.value.split('\\n').length]")
