import sys,subprocess,hashlib
from pathlib import Path
p=Path(sys.argv[1])
assert subprocess.check_output(["git","-C",str(p),"rev-parse","HEAD"],text=True).strip()=="e6600ffc4e8e6620eeb45bf49bcdbd5e4b84163f"
assert subprocess.check_output(["git","-C",str(p),"rev-parse","HEAD^{tree}"],text=True).strip()=="e9e0827dbf5a388fd643221626bcd164d587d0a3"
paths=subprocess.check_output(["git","-C",str(p),"ls-files","-z"]).decode().strip("\0").split("\0")
raw=subprocess.check_output(["git","-C",str(p),"cat-file","--batch"],input="".join(f"HEAD:{name}\n" for name in paths).encode())
offset=0
for name in paths:
    end=raw.index(b"\n",offset);size=int(raw[offset:end].split()[2]);blob=raw[end+1:end+1+size];offset=end+1+size+1
    assert hashlib.sha256((p/name).read_bytes()).digest()==hashlib.sha256(blob).digest(),name
status=subprocess.check_output(["git","-C",str(p),"status","--porcelain","--untracked-files=all"],text=True).splitlines()
assert status in ([],["?? scripts/curve-density.test.mjs"]),status
print(f"Frozen source verified: {len(paths)} tracked blob hashes and exact untracked fixture boundary")
