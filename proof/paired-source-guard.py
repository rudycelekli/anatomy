import sys,subprocess,hashlib
from pathlib import Path
sources={"baseline":("e6600ffc4e8e6620eeb45bf49bcdbd5e4b84163f","e9e0827dbf5a388fd643221626bcd164d587d0a3"),"candidate":("d0fc75b3c07c44c0f0462b07dfa4cb89eac7010d","09b374a83f7236b87eedcbbc33f10b40a4597764")}
variant=sys.argv[3]
assert variant in sources
head,tree=sources[variant]
p=Path(sys.argv[1])
assert subprocess.check_output(["git","-C",str(p),"rev-parse","HEAD"],text=True).strip()==head
assert subprocess.check_output(["git","-C",str(p),"rev-parse","HEAD^{tree}"],text=True).strip()==tree
hashes={}
paths=subprocess.check_output(["git","-C",str(p),"ls-files","-z"]).decode().strip("\0").split("\0")
raw=subprocess.check_output(["git","-C",str(p),"cat-file","--batch"],input="".join(f"HEAD:{name}\n" for name in paths).encode())
offset=0
for name in paths:
    end=raw.index(b"\n",offset);size=int(raw[offset:end].split()[2]);blob=raw[end+1:end+1+size];offset=end+1+size+1
    hashes[name]=hashlib.sha256((p/name).read_bytes()).hexdigest()
    assert hashes[name]==hashlib.sha256(blob).hexdigest(),name
status=subprocess.check_output(["git","-C",str(p),"status","--porcelain","--untracked-files=all"],text=True).splitlines()
assert status == [],status
print(f"Frozen source verified: {len(paths)} tracked blob hashes and exact untracked fixture boundary")

if len(sys.argv)>2:
    import json
    Path(sys.argv[2]).write_text(json.dumps({"head":head, "tree":tree, "file_hashes":hashes,"status":status},indent=2))
