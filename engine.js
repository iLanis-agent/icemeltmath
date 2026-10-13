(function (root) {
  "use strict";
  var BAG_KG = 10; // labeled bag of ice melt, kilograms

  function round1(x) { return Math.round(x * 10) / 10; }
  function plural(n, word, form) { return n + " " + (n === 1 ? word : (form || word + "s")); }

  function meltRate(thickMm) {
    if (thickMm <= 1) return 40;
    if (thickMm <= 3) return 80;
    return 140;
  }

  function meltGrams(areaM2, thickMm) {
    return areaM2 * meltRate(thickMm);
  }

  function meltVerdict(thickMm) {
    if (thickMm <= 1) return "a broom-and-sprinkle film";
    if (thickMm <= 3) return "a thin-glaze scatter";
    if (thickMm <= 6) return "a stubborn-sheet job";
    return "a shovel-first rescue";
  }

  function meltPlan(areaM2, thickMm) {
    if (!(areaM2 > 0) || !(thickMm > 0)) return { error: "the area and the ice must be positive" };
    return { grams: meltGrams(areaM2, thickMm), verdict: meltVerdict(thickMm) };
  }

  function bagPlan(areaM2, thickMm) {
    if (!(areaM2 > 0) || !(thickMm > 0)) return { error: "the area and the ice must be positive" };
    var kg = meltGrams(areaM2, thickMm) / 1000;
    var bags = Math.ceil(kg / BAG_KG);
    var leftover = round1(bags * BAG_KG - kg);
    var verdict;
    if (bags <= 1) verdict = "a one-bag storm";
    else if (bags <= 4) verdict = "a shelf stack";
    else verdict = "pallet territory";
    return { kg: kg, bags: bags, leftover: leftover, verdict: verdict };
  }

  function chemPlan(coldestC, meltKg) {
    if (!(coldestC <= 0) || !(meltKg > 0)) return { error: "the night must be freezing and the melt must be positive" };
    var product, verdict;
    if (coldestC >= -9) { product = "rock salt"; verdict = "plain and cheap"; }
    else if (coldestC >= -15) { product = "magnesium chloride"; verdict = "worth the upgrade"; }
    else if (coldestC >= -29) { product = "calcium chloride"; verdict = "the cold-snap reserve"; }
    else { product = "sand"; verdict = "a grip-not-melt week"; }
    return { product: product, verdict: verdict };
  }

  function renderMelt(r, areaM2, thickMm) {
    return "Your " + areaM2 + " m2 walk under " + thickMm + " mm of ice calls for " + r.grams
      + " g of melt - " + r.verdict + ".";
  }

  function renderBag(r) {
    return "That " + r.kg + " kg of melt at a labeled " + BAG_KG + " kg bag is "
      + plural(r.bags, "bag") + ", leaving " + r.leftover + " kg for the next storm - " + r.verdict + ".";
  }

  function renderChem(r, coldestC, meltKg) {
    if (r.product === "sand") {
      return "At " + coldestC + " C no melt chemistry keeps working; spread sand for grip instead - " + r.verdict + ".";
    }
    return "At " + coldestC + " C your " + meltKg + " kg job is a " + r.product + " job - " + r.verdict + ".";
  }

  var api = { meltPlan: meltPlan, bagPlan: bagPlan, chemPlan: chemPlan, renderMelt: renderMelt, renderBag: renderBag, renderChem: renderChem };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.IceMeltMath = api;
})(this);
