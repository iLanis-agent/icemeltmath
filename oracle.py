import json, math

def jsnum(x):
    return int(x) if isinstance(x, float) and x == int(x) else x
def plural(n, word, form=None): return str(jsnum(n)) + " " + (word if n == 1 else (form or word + "s"))
def fmt(x): return str(jsnum(x))
def round1(x): return jsnum(math.floor(x * 10 + 0.5) / 10)

BAG_KG = 10

def melt_rate(thickMm):
    if thickMm <= 1: return 40
    if thickMm <= 3: return 80
    return 140

def melt_grams(areaM2, thickMm):
    return jsnum(areaM2 * melt_rate(thickMm))

def melt_verdict(thickMm):
    if thickMm <= 1: return "a broom-and-sprinkle film"
    if thickMm <= 3: return "a thin-glaze scatter"
    if thickMm <= 6: return "a stubborn-sheet job"
    return "a shovel-first rescue"

def melt_plan(areaM2, thickMm):
    if not (areaM2 > 0) or not (thickMm > 0):
        return {"error": "the area and the ice must be positive"}
    return {"grams": melt_grams(areaM2, thickMm), "verdict": melt_verdict(thickMm)}

def bag_plan(areaM2, thickMm):
    if not (areaM2 > 0) or not (thickMm > 0):
        return {"error": "the area and the ice must be positive"}
    kg = jsnum(melt_grams(areaM2, thickMm) / 1000)
    bags = math.ceil(kg / BAG_KG)
    leftover = round1(bags * BAG_KG - kg)
    if bags <= 1: verdict = "a one-bag storm"
    elif bags <= 4: verdict = "a shelf stack"
    else: verdict = "pallet territory"
    return {"kg": kg, "bags": bags, "leftover": leftover, "verdict": verdict}

def chem_plan(coldestC, meltKg):
    if not (coldestC <= 0) or not (meltKg > 0):
        return {"error": "the night must be freezing and the melt must be positive"}
    if coldestC >= -9: product, verdict = "rock salt", "plain and cheap"
    elif coldestC >= -15: product, verdict = "magnesium chloride", "worth the upgrade"
    elif coldestC >= -29: product, verdict = "calcium chloride", "the cold-snap reserve"
    else: product, verdict = "sand", "a grip-not-melt week"
    return {"product": product, "verdict": verdict}

def render_melt(r, areaM2, thickMm):
    return ("Your " + fmt(areaM2) + " m2 walk under " + fmt(thickMm) + " mm of ice calls for " + fmt(r["grams"])
            + " g of melt - " + r["verdict"] + ".")

def render_bag(r, *args):
    return ("That " + fmt(r["kg"]) + " kg of melt at a labeled " + fmt(BAG_KG) + " kg bag is "
            + plural(r["bags"], "bag") + ", leaving " + fmt(r["leftover"]) + " kg for the next storm - " + r["verdict"] + ".")

def render_chem(r, coldestC, meltKg):
    if r["product"] == "sand":
        return ("At " + fmt(coldestC) + " C no melt chemistry keeps working; spread sand for grip instead - " + r["verdict"] + ".")
    return ("At " + fmt(coldestC) + " C your " + fmt(meltKg) + " kg job is a " + r["product"] + " job - " + r["verdict"] + ".")

cases = []
def add(fn, f, rf, args):
    r = f(*args)
    c = {"fn": fn, "args": args, "result": r}
    if "error" not in r: c["render"] = rf(r, *args)
    cases.append(c)

for a in [[20,3],[10,1],[50,6],[30,2],[15,4],[40,10],[25,5],[35,3],[0,3],[20,0]]:
    add("meltPlan", melt_plan, render_melt, a)
for a in [[20,3],[10,1],[50,6],[80,10],[30,2],[15,4],[40,8],[25,5],[0,2],[30,0]]:
    add("bagPlan", bag_plan, render_bag, a)
for a in [[-5,2],[-12,5],[-20,8],[-32,3],[-9,1],[-15,2],[-29,4],[-10,6],[3,2],[-5,0]]:
    add("chemPlan", chem_plan, render_chem, a)
json.dump(cases, open("expected.json", "w"), separators=(",", ":"))
print(len(cases), "cases")
