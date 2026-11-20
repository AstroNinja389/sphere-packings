"""Check rational contact-price and common-circle certificates on the previous frontier."""
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from flint import fmpq, fmpq_mat, fmpz_mat
from audit_cells import interval
from audit_cone import enumerate_min
from audit_mark_vectors import matrix, sql
from audit_cells import test as verify_earlier_cell
from audit_planes import check as verify_earlier_plane

BASE = Path(__file__).resolve().parent

def signed_triangle(rows):
    return (len(rows) == 3 and fmpz_mat(rows).rank() == 2 and
            any(all(x+a*y+b*z == 0 for x,y,z in zip(*rows)) for a in (-1,1) for b in (-1,1)))

def integral_direction(x):
    assert len(x) == 9 and any(x) and all(type(v) is int for v in x)

def verify_node(node, levels, contacts, area, near=()):
    if "split" in node:
        rows=node["split"]
        for x in rows: integral_direction(x)
        assert signed_triangle(rows) and len(node["children"]) == 3
        return sum(verify_node(c, levels, contacts, area, near+(v,)) for c,v in zip(node["children"],rows))
    u,t,cap,triple=levels
    S=fmpq_mat(fmpz_mat(node["S"]))/10**6
    assert S.nrows()==S.ncols()==9 and S==S.transpose() and all(x>0 for x in (-S).charpoly().coeffs())
    det=S.det()
    A=fmpq_mat(9,9)
    b=fmpq(0)
    for price, item in node["rows"]:
        assert type(price) is int and price>0
        mode=item[0]
        if mode in ("z","near"):
            rows=item[1] if mode=="z" else [item[1]]
            for x in rows: integral_direction(x)
            if mode=="near":
                assert rows[0] in near
                h=8*u/9
            elif len(rows)==1:h=t
            else:
                assert signed_triangle(rows)
                h=max(3*t,5*u/2,triple)
            Z=fmpq_mat(fmpz_mat(rows));K=Z.transpose()*Z
        elif mode=="area":
            for x in item[1]: integral_direction(x)
            Z=fmpq_mat(fmpz_mat(item[1]));H=fmpq_mat(fmpz_mat(item[2]))/10**6
            assert Z.nrows()==Z.rank()==2 and H.nrows()==H.ncols()==2 and H==H.transpose()
            assert H[0,0]>0 and H.det()>0 and type(item[3]) is int
            h=fmpq(item[3],10**7);assert h>0 and (h/2)**2<=H.det()*area
            K=Z.transpose()*H*Z
        else:
            assert mode in ("cof","det") and type(item[-1]) is int
            h=fmpq(item[-1],10**7)
            assert h>0
            if mode=="det":
                assert (h/9)**9*cap<=det
                K=S
            else:
                integral_direction(item[1])
                x=fmpq_mat(9,1,item[1]);y=S*x;value=(x.transpose()*y)[0,0]
                assert (h/8)**8*cap*value<=4*det
                K=S-y*y.transpose()/value
        A+=price*K;b+=price*h
    CA=contacts*A
    coeff=sorted((sum(CA[i,j]*contacts[i,j] for j in range(9)) for i in range(contacts.nrows())),reverse=True)
    assert sum(max(0,x) for x in coeff[:9]) < 4*b
    return 1

def check_prefix(key, kind, ref, contacts, P, cell_end, end, cell, plane):
    """Replay the part of the old interval cover needed by this marking."""
    head = Fraction(0)
    for item in cell["pieces"]:
        if head == cell_end:
            break
        lo, hi = Fraction(item["l"]), Fraction(item["r"])
        assert lo == head < hi <= cell_end
        levels = interval(kind, lo, hi, ref)
        if levels is None:
            assert item.get("empty")
        else:
            w = item["witness"]
            assert item["candidate"] and w["key"] == key
            assert verify_earlier_cell(w, kind, P, contacts, *levels)
        head = hi
    assert head == cell_end == Fraction(plane["old_prefix"])
    for lo, hi, witness in plane["pieces"]:
        if head == end:
            break
        lo, hi = Fraction(lo), Fraction(hi)
        assert lo == head < hi <= end
        levels = interval(kind, lo, hi, ref)
        if levels is None:
            assert witness == "empty"
        else:
            assert verify_earlier_plane(witness, contacts, P, levels, kind, hi, P.det())
        head = hi
    assert head == end

def audit(records, prior=BASE):
    front=dict(row.split() for row in (prior/"FINAL-OPEN-MARKS.txt").read_text().splitlines())
    assert len(front)==32
    prefix={};cell_prefix={};history={}
    keys = {record["key"] for record in records}
    for stem in ("cells","planes"):
        hits={}
        for label in "ab":
            with (prior/f"{stem}-{label}.jsonl").open() as source:
                for line in source:
                    row=json.loads(line)
                    if row["key"] in keys:
                        assert row["key"] not in hits
                        hits[row["key"]]=row
        assert set(hits)==keys
        history[stem]=hits
    for tag in "ab":
        for k,p in json.loads((prior/f"cells-{tag}-audit.json").read_bytes())["partial_prefixes"].items():
            prefix[k]=Fraction(p[-1])
            cell_prefix[k]=Fraction(p[-1])
        for k,p in json.loads((prior/f"planes-{tag}-audit.json").read_bytes())["partial"].items():
            prefix[k]=max(prefix.get(k,Fraction(0)),Fraction(p))
    found={}; leaves=0
    for record in records:
        k=record["key"]
        assert k in front and k not in found
        kind,scale,blob=sql.execute("select kind,scale,gram from form where key=?",(k,)).fetchone()
        assert (kind if kind!="trace" else "reverse_trace_open")==front[k]
        G=matrix(blob);contacts=fmpq_mat(enumerate_min(G,scale))
        ref=Fraction(4,scale)**9*int(G.det())
        head=prefix.get(k,Fraction(0)); assert head==Fraction(record["prefix"])
        check_prefix(k,kind,ref,contacts,4*fmpq_mat(G)/scale,cell_prefix.get(k,Fraction(0)),head,
                     history["cells"][k],history["planes"][k])
        spans=[]
        for l,r,node in record["pieces"]:
            l,r=Fraction(l),Fraction(r)
            assert l==head<r
            head=r
            if node is None:continue
            levels=interval(kind,l,r,ref)
            if levels is None:assert node=={"empty":True}
            else:
                u=levels[0];area=u**2/2
                if r<=Fraction(9799,10000):
                    area=max(area,4*max(fmpq(str(ref)),u*(768 if kind=="virtual" else 1113))/(9*fmpq(99331,100)))
                leaves+=verify_node(node,levels,contacts,area)
            spans.append((l,r))
        # The range above the final endpoint is impossible using d >= 768.
        assert head**5*768>1024
        found[k]=spans
    return front,prefix,found,leaves

def fully_covered(prefix,spans):
    end=prefix
    for l,r in sorted(spans):
        if l>end:break
        end=max(end,r)
    return end**5*768>1024

if __name__=="__main__":
    import sys
    if not __debug__:raise RuntimeError("Use assertions.")
    f=Path(sys.argv[1]) if len(sys.argv)>1 else BASE/"contact-prices.jsonl"
    prior=Path(sys.argv[2]) if len(sys.argv)>2 else BASE
    records=[json.loads(l) for l in f.read_text().splitlines()]
    front,prefix,spans,leaves=audit(records,prior)
    closed=sorted(k for k,ss in spans.items() if fully_covered(prefix.get(k,Fraction(0)),ss))
    print(json.dumps({"source_sha256":hashlib.sha256(f.read_bytes()).hexdigest(),"rational_price_leaves":leaves,
                      "certified_intervals":sum(map(len,spans.values())),"whole_markings":closed}))
