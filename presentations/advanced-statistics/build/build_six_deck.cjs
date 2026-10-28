// Builds Advanced_Statistics_Presentation_6_Slides.pptx: the full deck's topics on six
// uncluttered slides (title, why & methods, implications, case study, challenges, conclusion).
//
//   NODE_PATH=<node_modules with pptxgenjs, react-icons, react, react-dom, sharp> \
//     node build_six_deck.cjs <path to pptx skill apply_theme.js>
const path = require("path");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");

const HERE = __dirname;
const ASSETS = path.join(HERE, "assets");
const OUT = path.join(HERE, "..", "Advanced_Statistics_Presentation_6_Slides.pptx");
const { applyTheme } = require(process.argv[2]);

const THEME = {
	name: "Evidence Navy",
	headFontFace: "Cambria",
	bodyFontFace: "Calibri",
	colors: {
		dk1: "1B2633", lt1: "FFFFFF", dk2: "0B1F33", lt2: "EEF2F6",
		accent1: "0F8B8D", accent2: "E3A43B", accent3: "2F5D8A",
		accent4: "B8462F", accent5: "5E6B7A", accent6: "CFE9E7",
		hlink: "2F5D8A", folHlink: "5E6B7A",
	},
};
const HEX = THEME.colors;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "Implications of Advanced Statistics in Business and Research";
pres.subject = "Six-slide university presentation on advanced statistics";
pres.author = "[Team Name]";

const C = pres.SchemeColor;
const INK = C.text1, NAVY = C.text2, WHITE = C.background1, MIST = C.background2;
const TEAL = C.accent1, AMBER = C.accent2, STEEL = C.accent3, CORAL = C.accent4, SLATE = C.accent5, ICE = C.accent6;
const HEAD = "+mj-lt";

const M = 0.6, CW = 12.133, RIGHT = M + CW;
const FOOTER = "Implications of Advanced Statistics in Business and Research";

// ---------- layouts ----------
const kickerPh = (color) => ({ placeholder: { options: { name: "kicker", type: "body", x: M, y: 0.4, w: 8.2, h: 0.32, fontSize: 12, bold: true, color, charSpacing: 2, margin: 0, valign: "middle" }, text: "" } });
const titlePh = (color) => ({ placeholder: { options: { name: "title", type: "title", x: M, y: 0.72, w: CW, h: 0.78, fontFace: HEAD, fontSize: 34, bold: true, color, margin: 0, valign: "middle", align: "left" }, text: "" } });
const footer = (color) => ({ text: { text: FOOTER, options: { x: M, y: 7.05, w: 8, h: 0.28, fontSize: 9, color, margin: 0, valign: "middle" } } });
const slideNo = (color) => ({ x: RIGHT - 0.6, y: 7.05, w: 0.6, h: 0.28, fontSize: 9, color, align: "right", margin: 0 });

pres.defineSlideMaster({
	title: "TITLE_DARK",
	background: { color: NAVY },
	objects: [{ placeholder: { options: { name: "title", type: "title", x: M, y: 0.98, w: 6.3, h: 1.85, fontFace: HEAD, fontSize: 36, bold: true, color: WHITE, margin: 0, valign: "top", align: "left" }, text: "" } }],
});
pres.defineSlideMaster({ title: "CONTENT", background: { color: WHITE }, objects: [kickerPh(TEAL), titlePh(NAVY), footer(SLATE)], slideNumber: slideNo(SLATE) });
pres.defineSlideMaster({ title: "CLOSING_DARK", background: { color: NAVY }, objects: [kickerPh(AMBER), titlePh(WHITE), footer(ICE)], slideNumber: slideNo(ICE) });

// ---------- helpers ----------
function text(slide, content, opts) {
	slide.addText(content, { isTextBox: true, margin: 0, valign: "top", color: INK, fontSize: 15, ...opts });
}
function box(slide, opts) {
	const { radius, ...rest } = opts;
	slide.addShape(radius ? pres.ShapeType.roundRect : pres.ShapeType.rect, { line: { type: "none" }, ...(radius ? { rectRadius: radius } : {}), ...rest });
}
function chevron(slide, x, y, name) {
	slide.addShape(pres.ShapeType.chevron, { x, y, w: 0.15, h: 0.3, fill: { color: SLATE }, line: { type: "none" }, objectName: name });
}
async function icon(Comp, color = "#FFFFFF", size = 256) {
	const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color, size: String(size) }));
	const buf = await sharp(Buffer.from(svg)).png().toBuffer();
	return "image/png;base64," + buf.toString("base64");
}

// ---------- slide 1: title ----------
function slideTitle() {
	pres.addSection({ title: "Opening" });
	const s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: "Opening" });
	s.addImage({ path: path.join(ASSETS, "hero.png"), x: 7.283, y: 0, w: 6.05, h: 7.5, altText: "Illustrative graphic built from simulated data: data points, a fitted trend with its uncertainty band, and a forecast range used for a decision.", objectName: "Hero visual (simulated data)" });
	[["Data", 0.98, "center"], ["Model + uncertainty", 3.0, "center"], ["Forecast → decision", 4.45, "right"]].forEach(([label, dx, align]) =>
		text(s, label, { x: 7.283 + dx - 0.75, y: 6.98, w: 1.5, h: 0.26, fontSize: 10, color: ICE, align, objectName: `Hero label: ${label}` }));
	text(s, "Illustrative visual · simulated data", { x: 10.9, y: 0.25, w: 2.2, h: 0.24, fontSize: 9, color: SLATE, align: "right", italic: true, objectName: "Hero caption" });

	text(s, "ADVANCED STATISTICS IN PRACTICE", { x: M, y: 0.55, w: 6.3, h: 0.3, fontSize: 12, bold: true, color: ICE, charSpacing: 3, objectName: "Kicker" });
	s.addText("Implications of Advanced Statistics in Business and Research", { placeholder: "title" });
	text(s, "Turning data into evidence, decisions, and discovery", { x: M, y: 2.92, w: 6.4, h: 0.42, fontSize: 19, italic: true, color: ICE, objectName: "Subtitle" });

	text(s, [{ text: "PRESENTED BY  ", options: { bold: true, color: AMBER, charSpacing: 2 } }, { text: "[Team Name]", options: { bold: true, color: WHITE } }], { x: M, y: 3.66, w: 6.3, h: 0.28, fontSize: 11.5, objectName: "Team name" });
	const none = { type: "none" };
	const rows = [1, 2, 3, 4, 5].map((i) => [{ text: `[Member ${i} Full Name]`, options: { color: WHITE } }, { text: "[Student ID]", options: { color: ICE } }]);
	s.addTable(rows, { x: M, y: 3.98, w: 5.4, colW: [3.3, 2.1], rowH: 0.27, fontSize: 13, margin: [0, 0, 0, 0], valign: "middle", border: [none, none, none, none], fill: { color: NAVY }, objectName: "Team members table" });

	const detail = (label, value, x, y, w, name) =>
		text(s, [{ text: label, options: { fontSize: 9.5, bold: true, color: AMBER, charSpacing: 2, breakLine: true } }, { text: value, options: { fontSize: 12.5, color: WHITE } }], { x, y, w, h: 0.46, objectName: name });
	detail("COURSE", "[Course Title] ([Course Code])", M, 5.5, 3.3, "Course title and code");
	detail("INSTRUCTOR", "[Instructor Name], [Designation]", 4.05, 5.5, 3.0, "Instructor");
	detail("DEPARTMENT", "[Department]", M, 6.05, 3.3, "Department");
	detail("UNIVERSITY", "[University Name]", 4.05, 6.05, 3.0, "University");
	detail("DATE", "[Presentation Date]", M, 6.6, 3.3, "Presentation date");

	s.addNotes(
		"Good morning. Our topic is the implications of advanced statistics in business and research. " +
			"In simple words: how companies and researchers use statistics to turn data into reliable decisions. " +
			"The picture on the right shows the idea: we start with data, fit a model with its uncertainty, and use a forecast to make a decision. " +
			"We will cover why statistics matters, where it is used, one A/B-test example, and the main cautions."
	);
}


// ---------- slide 2: why it matters & key methods ----------
async function slideWhy() {
	pres.addSection({ title: "Content" });
	const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Content" });
	s.addText("01 · WHY IT MATTERS & KEY METHODS", { placeholder: "kicker" });
	s.addText("From data to decisions", { placeholder: "title" });

	const stages = [["Raw data", "What was recorded?"], ["Description", "What happened?"], ["Prediction", "What is likely next?"], ["Inference", "Is it real? How sure?"], ["Decision", "What should we do?"]];
	const gap = 0.2, w = (CW - 4 * gap) / 5, y = 1.68, h = 1.05;
	stages.forEach(([name, q], i) => {
		const x = M + i * (w + gap), last = i === stages.length - 1;
		box(s, { x, y, w, h, radius: 0.08, fill: { color: last ? NAVY : MIST }, objectName: `Stage ${i + 1} card` });
		text(s, [{ text: name, options: { bold: true, fontSize: 16, color: last ? AMBER : NAVY, breakLine: true } }, { text: q, options: { fontSize: 13.5, color: last ? WHITE : SLATE } }], { x: x + 0.2, y, w: w - 0.4, h, valign: "middle", objectName: `Stage ${i + 1} text` });
		if (i > 0) chevron(s, x - gap / 2 - 0.075, y + h / 2 - 0.15, `Stage arrow ${i + 1}`);
	});

	text(s, "Key methods: each answers a different question", { x: M, y: 3.0, w: 8.2, h: 0.38, fontFace: HEAD, fontSize: 17, bold: true, color: NAVY, objectName: "Methods heading" });
	const methods = [
		["regression", "Regression", "How outcomes change with their drivers"],
		["hypothesis", "Hypothesis tests & CIs", "Is a difference real, and how big?"],
		["bayes", "Bayesian inference", "Update beliefs as new data arrives"],
		["timeseries", "Time-series forecasting", "Predict the future, with a range"],
		["experiment", "Experiments & causal inference", "What happens if we act?"],
		["cluster", "Clustering & multivariate", "Find groups in complex data"],
	];
	const cw = (8.2 - 0.4) / 3, ch = 1.57;
	methods.forEach(([g, name, line], i) => {
		const x = M + (i % 3) * (cw + 0.2), cy = 3.5 + Math.floor(i / 3) * (ch + 0.2);
		box(s, { x, y: cy, w: cw, h: ch, radius: 0.08, fill: { color: MIST }, objectName: `${name} card` });
		s.addImage({ path: path.join(ASSETS, `glyph_${g}.png`), x: x + 0.15, y: cy + 0.15, w: 0.62, h: 0.62, altText: `Diagram: ${name}`, objectName: `${name} diagram` });
		text(s, name, { x: x + 0.88, y: cy + 0.15, w: cw - 1.0, h: 0.62, fontFace: HEAD, fontSize: 14, bold: true, color: NAVY, valign: "middle", objectName: `${name} title` });
		text(s, line, { x: x + 0.18, y: cy + 0.88, w: cw - 0.36, h: 0.6, fontSize: 13.5, objectName: `${name} text` });
	});

	const px = 9.1, pw = RIGHT - px, py = 3.0, ph = 3.84;
	box(s, { x: px, y: py, w: pw, h: ph, radius: 0.08, fill: { color: NAVY }, objectName: "Evidence panel" });
	text(s, "EVIDENCE", { x: px + 0.3, y: py + 0.3, w: pw - 0.6, h: 0.26, fontSize: 11, bold: true, color: AMBER, charSpacing: 2, objectName: "Evidence tag" });
	text(s, "5–6%", { x: px + 0.3, y: py + 0.65, w: pw - 0.6, h: 0.9, fontFace: HEAD, fontSize: 50, bold: true, color: AMBER, valign: "middle", objectName: "Evidence statistic" });
	text(s, "higher productivity in firms that use data-driven decision-making", { x: px + 0.3, y: py + 1.65, w: pw - 0.6, h: 1.0, fontSize: 15, color: WHITE, objectName: "Evidence text" });
	text(s, "Brynjolfsson, Hitt & Kim (2011) · observational study of 179 large firms", { x: px + 0.3, y: py + 2.85, w: pw - 0.6, h: 0.6, fontSize: 10.5, color: ICE, objectName: "Evidence source" });

	s.addNotes(
		"Data alone does not give answers. Statistics moves us from raw data, to describing what happened, to predicting what comes next, to checking whether a pattern is real, and finally to a decision. " +
			"Different methods answer different questions: regression links outcomes to their drivers, hypothesis tests and confidence intervals check if a difference is real, Bayesian inference updates beliefs with new data, " +
			"forecasting predicts the future with a range, experiments show what happens when we act, and clustering finds groups. " +
			"Evidence: firms that use data-driven decision-making are about 5 to 6 percent more productive (Brynjolfsson, Hitt and Kim, 2011). This is an observational finding, not an experiment."
	);
}

// ---------- slide 3: business and research ----------
function pills(s, items, x0, y0, maxW, color, prefix) {
	let x = x0, y = y0;
	items.forEach((t, i) => {
		const w = 0.32 + t.length * 0.088;
		if (x + w > x0 + maxW) { x = x0; y += 0.55; }
		box(s, { x, y, w, h: 0.42, radius: 0.21, fill: { color: WHITE }, line: { color, width: 1.25 }, objectName: `${prefix} tag ${i + 1}` });
		text(s, t, { x, y, w, h: 0.42, fontSize: 13.5, bold: true, color: NAVY, align: "center", valign: "middle", objectName: `${prefix} tag ${i + 1} text` });
		x += w + 0.15;
	});
}

async function slideImplications() {
	const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Content" });
	s.addText("02 · IMPLICATIONS", { placeholder: "kicker" });
	s.addText("Better decisions in business and research", { placeholder: "title" });

	const w = (CW - 0.35) / 2, y = 1.7, h = 5.15;
	const panel = async (x, name, Ic, col, tags) => {
		box(s, { x, y, w, h, radius: 0.08, fill: { color: MIST }, objectName: `${name} panel` });
		s.addShape(pres.ShapeType.ellipse, { x: x + 0.3, y: y + 0.25, w: 0.56, h: 0.56, fill: { color: col }, line: { type: "none" }, objectName: `${name} icon circle` });
		s.addImage({ data: await icon(Ic), x: x + 0.44, y: y + 0.39, w: 0.28, h: 0.28, altText: name, objectName: `${name} icon` });
		text(s, name, { x: x + 1.05, y: y + 0.25, w: w - 1.3, h: 0.56, fontFace: HEAD, fontSize: 21, bold: true, color: NAVY, valign: "middle", objectName: `${name} heading` });
		pills(s, tags, x + 0.3, y + 1.05, w - 0.6, col, name);
		box(s, { x: x + 0.3, y: y + 2.35, w: w - 0.6, h: 2.5, radius: 0.06, fill: { color: NAVY }, objectName: `${name} case box` });
	};

	// Business: Bing experiment in three steps
	const bx = M;
	await panel(bx, "Business", fa.FaBriefcase, STEEL, ["Demand forecasting", "Customer segments", "Pricing", "Credit risk & fraud"]);
	const cx = bx + 0.5, cy = y + 2.35, cw = w - 1.0;
	text(s, "REAL CASE · BING SEARCH ADS", { x: cx, y: cy + 0.18, w: cw, h: 0.26, fontSize: 11, bold: true, color: AMBER, charSpacing: 2, objectName: "Business case tag" });
	const steps = [["IDEA", "Show longer ad titles"], ["METHOD", "Randomized A/B test"], ["RESULT", "+12% revenue", "≈ $100M a year in the U.S."]];
	const sw = (cw - 2 * 0.3) / 3;
	steps.forEach(([k, v, sub], i) => {
		const sx = cx + i * (sw + 0.3);
		box(s, { x: sx, y: cy + 0.58, w: sw, h: 1.35, radius: 0.06, fill: { color: i === 2 ? TEAL : STEEL }, objectName: `Bing step ${i + 1} box` });
		text(s, [{ text: k, options: { bold: true, fontSize: 10, color: i === 2 ? NAVY : AMBER, charSpacing: 1, breakLine: true } }, { text: v, options: { fontSize: 14, bold: i === 2, color: WHITE, breakLine: !!sub } }, ...(sub ? [{ text: sub, options: { fontSize: 12, color: WHITE } }] : [])], { x: sx + 0.13, y: cy + 0.68, w: sw - 0.26, h: 1.2, objectName: `Bing step ${i + 1} text` });
		if (i > 0) chevron(s, sx - 0.15 - 0.075, cy + 0.58 + 0.675 - 0.15, `Bing arrow ${i + 1}`);
	});
	text(s, "Kohavi & Thomke (2017), Harvard Business Review", { x: cx, y: cy + 2.08, w: cw, h: 0.26, fontSize: 10.5, italic: true, color: ICE, objectName: "Business case source" });

	// Research: RECOVERY trial bars
	const rx = M + w + 0.35;
	await panel(rx, "Research", fa.FaFlask, TEAL, ["Study design", "Power analysis", "Confidence intervals", "Reproducibility"]);
	const qx = rx + 0.5, qw = w - 1.0;
	text(s, "REAL CASE · RECOVERY TRIAL", { x: qx, y: cy + 0.18, w: qw, h: 0.26, fontSize: 11, bold: true, color: AMBER, charSpacing: 2, objectName: "Research case tag" });
	text(s, "28-day deaths in ventilated COVID-19 patients", { x: qx, y: cy + 0.5, w: qw, h: 0.3, fontSize: 13.5, color: ICE, objectName: "Research case subtitle" });
	const lw = 1.6, barX = qx + lw, barMax = qw - lw - 0.8;
	[["Usual care", 41.4, SLATE], ["Dexamethasone", 29.3, TEAL]].forEach(([lab, v, c], i) => {
		const by = cy + 0.98 + i * 0.5;
		text(s, lab, { x: qx, y: by, w: lw - 0.1, h: 0.36, fontSize: 14, color: WHITE, valign: "middle", objectName: `RECOVERY ${lab} label` });
		box(s, { x: barX, y: by + 0.03, w: barMax * (v / 50), h: 0.3, fill: { color: c }, objectName: `RECOVERY ${lab} bar` });
		text(s, `${v.toFixed(1)}%`, { x: barX + barMax * (v / 50) + 0.1, y: by, w: 0.75, h: 0.36, fontSize: 14, bold: true, color: WHITE, valign: "middle", objectName: `RECOVERY ${lab} value` });
	});
	text(s, "Randomized trial · RECOVERY Collaborative Group (2021), NEJM", { x: qx, y: cy + 2.08, w: qw, h: 0.26, fontSize: 10.5, italic: true, color: ICE, objectName: "Research case source" });

	s.addNotes(
		"In business, statistics drives demand forecasting, customer segmentation, pricing, and credit-risk and fraud checks. " +
			"Real case: Bing tested longer ad titles with a randomized A/B test. Revenue rose about 12 percent, worth more than 100 million dollars a year in the U.S. (Kohavi and Thomke, 2017). " +
			"In research, statistics makes results reliable through good study design, a power analysis to choose the sample size, confidence intervals, and reproducibility. " +
			"Real case: the RECOVERY randomized trial found that dexamethasone cut 28-day deaths in ventilated COVID-19 patients from 41.4 to 29.3 percent. " +
			"A warning from research: when 100 psychology studies were repeated, only 36 percent gave significant results again (Open Science Collaboration, 2015)."
	);
}

// ---------- slide 4: A/B test case (illustrative data) ----------
function slideCase() {
	const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Content" });
	s.addText("03 · CASE STUDY", { placeholder: "kicker" });
	s.addText("A/B test: does a new product page sell more?", { placeholder: "title" });
	box(s, { x: 8.73, y: 0.38, w: 4.0, h: 0.36, radius: 0.18, fill: { color: AMBER }, objectName: "Illustrative data badge" });
	text(s, [{ text: "ILLUSTRATIVE DATA  ", options: { bold: true } }, { text: "hypothetical, not real company results" }], { x: 8.73, y: 0.38, w: 4.0, h: 0.36, fontSize: 11, color: NAVY, align: "center", valign: "middle", objectName: "Illustrative data badge text" });

	// Left: three steps
	const steps = [
		["Split", "40,000 visitors at random: 20,000 see the old page (A), 20,000 the new page (B)."],
		["Measure", "Conversion rate = orders ÷ visitors."],
		["Test", "Two-proportion z-test at the 5% level."],
	];
	steps.forEach(([k, v], i) => {
		const y = 1.75 + i * 1.12;
		s.addShape(pres.ShapeType.ellipse, { x: M, y, w: 0.5, h: 0.5, fill: { color: TEAL }, line: { type: "none" }, objectName: `Step ${i + 1} marker` });
		text(s, String(i + 1), { x: M, y, w: 0.5, h: 0.5, fontSize: 16, bold: true, color: WHITE, align: "center", valign: "middle", objectName: `Step ${i + 1} number` });
		text(s, [{ text: k, options: { bold: true, color: NAVY, fontSize: 16, breakLine: true } }, { text: v }], { x: M + 0.7, y: y - 0.02, w: 3.3, h: 1.0, fontSize: 14, objectName: `Step ${i + 1} text` });
	});
	text(s, "Visitors are assigned at random, so the only real difference between the groups is the page.", { x: M, y: 5.25, w: 4.0, h: 0.8, fontSize: 13, italic: true, color: SLATE, objectName: "Randomization note" });

	// Middle: native chart
	s.addChart(pres.ChartType.bar, [{ name: "Conversion rate (%)", labels: ["A · Old page", "B · New page"], values: [4.2, 4.8] }], {
		x: 4.85, y: 1.65, w: 3.9, h: 4.6, barDir: "col", barGapWidthPct: 70,
		chartColors: [HEX.accent3, HEX.accent1],
		showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: '0.00"%"', dataLabelFontSize: 14, dataLabelFontBold: true, dataLabelColor: HEX.dk2, dataLabelFontFace: "+mn-lt",
		valAxisMinVal: 0, valAxisMaxVal: 6, valAxisMajorUnit: 1, valAxisLabelFormatCode: '0"%"', valAxisLabelFontSize: 11, valAxisLabelColor: HEX.accent5, valAxisLabelFontFace: "+mn-lt",
		showValAxisTitle: true, valAxisTitle: "Conversion rate (%)", valAxisTitleFontSize: 11, valAxisTitleColor: HEX.accent5, valAxisTitleFontFace: "+mn-lt",
		catAxisLabelFontSize: 12, catAxisLabelColor: HEX.dk1, catAxisLabelFontFace: "+mn-lt",
		valGridLine: { color: "E2E7ED", size: 0.75 }, catGridLine: { style: "none" }, showLegend: false,
		altText: "Column chart of illustrative conversion rates: A 4.20 percent, B 4.80 percent; axis starts at zero.", objectName: "Conversion rate chart",
	});
	text(s, "A: 840 / 20,000   ·   B: 960 / 20,000 orders", { x: 4.85, y: 6.3, w: 3.9, h: 0.3, fontSize: 12, color: SLATE, align: "center", objectName: "Chart counts" });

	// Right: result and decision
	const rx = 9.05, rw = RIGHT - rx;
	const stats = [["+0.60 pp", "difference (B − A)"], ["+0.19 to +1.01 pp", "95% confidence interval"], ["p = 0.004", "very unlikely to be chance"]];
	stats.forEach(([v, l], i) => {
		const y = 1.7 + i * 0.95;
		box(s, { x: rx, y, w: rw, h: 0.82, radius: 0.06, fill: { color: MIST }, objectName: `Result ${i + 1} tile` });
		text(s, [{ text: v, options: { fontFace: HEAD, fontSize: 20, bold: true, color: NAVY, breakLine: true } }, { text: l, options: { fontSize: 12, color: SLATE } }], { x: rx + 0.2, y, w: rw - 0.4, h: 0.82, valign: "middle", objectName: `Result ${i + 1} text` });
	});
	text(s, [{ text: "Meaning  ", options: { bold: true, color: NAVY } }, { text: "The new page very likely works better, but the exact gain is uncertain." }], { x: rx, y: 4.6, w: rw, h: 0.8, fontSize: 14, objectName: "Interpretation" });
	box(s, { x: rx, y: 5.55, w: rw, h: 1.05, radius: 0.06, fill: { color: NAVY }, objectName: "Decision box" });
	text(s, [{ text: "DECISION", options: { bold: true, color: AMBER, charSpacing: 2, fontSize: 11, breakLine: true } }, { text: "Launch page B and keep monitoring results.", options: { color: WHITE } }], { x: rx + 0.2, y: 5.55, w: rw - 0.4, h: 1.05, fontSize: 14.5, valign: "middle", objectName: "Decision text" });

	s.addNotes(
		"This example uses made-up numbers to show the method. An online shop splits 40,000 visitors at random: half see the old page, half see the new page. " +
			"The old page converts 4.2 percent of visitors, the new page 4.8 percent, a difference of 0.6 percentage points. " +
			"The 95 percent confidence interval is 0.19 to 1.01 points and the p-value is 0.004, so the gain is very unlikely to be chance, although its exact size is uncertain. " +
			"Decision: launch the new page and keep monitoring."
	);
}


// ---------- slide 5: challenges & ethics ----------
async function slideChallenges() {
	const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Content" });
	s.addText("04 · CHALLENGES & ETHICS", { placeholder: "kicker" });
	s.addText("Use statistics carefully and honestly", { placeholder: "title" });

	const risks = [
		[fa.FaDatabase, "Biased data", "Wrong or one-sided data gives wrong answers."],
		[fa.FaChartLine, "Overfitting", "A model that memorizes noise fails on new data."],
		[fa.FaRedo, "P-hacking", "Running many tests guarantees some false “wins”."],
		[fa.FaProjectDiagram, "Correlation ≠ causation", "Even accurate AI predictions do not prove cause."],
		[fa.FaSearchPlus, "Significant ≠ important", "Always report how big the effect is."],
		[fa.FaUserShield, "Privacy & fairness", "Protect people and check models for bias."],
	];
	const w = (CW - 0.5) / 3, h = 1.55;
	for (let i = 0; i < risks.length; i++) {
		const [Ic, name, line] = risks[i];
		const x = M + (i % 3) * (w + 0.25), y = 1.7 + Math.floor(i / 3) * (h + 0.2);
		box(s, { x, y, w, h, radius: 0.08, fill: { color: MIST }, objectName: `${name} card` });
		s.addShape(pres.ShapeType.ellipse, { x: x + 0.22, y: y + 0.22, w: 0.55, h: 0.55, fill: { color: CORAL }, line: { type: "none" }, objectName: `${name} icon circle` });
		s.addImage({ data: await icon(Ic), x: x + 0.355, y: y + 0.355, w: 0.28, h: 0.28, altText: name, objectName: `${name} icon` });
		text(s, name, { x: x + 0.95, y: y + 0.22, w: w - 1.15, h: 0.55, fontFace: HEAD, fontSize: 16, bold: true, color: NAVY, valign: "middle", objectName: `${name} title` });
		text(s, line, { x: x + 0.22, y: y + 0.92, w: w - 0.44, h: 0.55, fontSize: 14, objectName: `${name} text` });
	}

	text(s, "RESPONSIBLE PRACTICE", { x: M, y: 5.3, w: CW, h: 0.28, fontSize: 11, bold: true, color: TEAL, charSpacing: 2, objectName: "Framework heading" });
	const steps = [["Plan", "set the question first"], ["Check", "data and assumptions"], ["Estimate", "effects with uncertainty"], ["Stress-test", "robustness checks"], ["Report", "honestly, with limits"]];
	const gap = 0.3, pw = (CW - 4 * gap) / 5;
	steps.forEach(([k, v], i) => {
		const x = M + i * (pw + gap);
		box(s, { x, y: 5.68, w: pw, h: 0.58, radius: 0.29, fill: { color: NAVY }, objectName: `Framework ${k} pill` });
		text(s, [{ text: `${i + 1}  `, options: { color: AMBER } }, { text: k, options: { color: WHITE } }], { x, y: 5.68, w: pw, h: 0.58, fontSize: 15.5, bold: true, align: "center", valign: "middle", objectName: `Framework ${k} text` });
		text(s, v, { x, y: 6.34, w: pw, h: 0.32, fontSize: 12.5, color: SLATE, align: "center", objectName: `Framework ${k} note` });
		if (i > 0) chevron(s, x - gap / 2 - 0.075, 5.68 + 0.29 - 0.15, `Framework arrow ${i + 1}`);
	});

	s.addNotes(
		"Statistics can mislead if we are careless. Six common problems: biased data, overfitting, p-hacking (running many tests until something looks significant), " +
			"confusing correlation with causation (even accurate AI predictions do not prove cause), treating 'significant' as 'important', and ignoring privacy and fairness. " +
			"Good practice follows five steps: plan the question first, check the data and assumptions, estimate effects with their uncertainty, stress-test the results, and report honestly with limitations."
	);
}

// ---------- slide 6: conclusion ----------
function slideConclusion() {
	pres.addSection({ title: "Conclusion" });
	const s = pres.addSlide({ masterName: "CLOSING_DARK", sectionTitle: "Conclusion" });
	s.addText("05 · CONCLUSION", { placeholder: "kicker" });
	s.addText("Key takeaways", { placeholder: "title" });

	const takeaways = [
		["Data becomes evidence", "Statistics separates real patterns from noise."],
		["Test before you decide", "Experiments and intervals beat opinion."],
		["Design drives rigor", "Good design and sample size make research reliable."],
		["Interpret responsibly", "Effect size, transparency and fairness matter."],
	];
	const gap = 0.3, w = (CW - 3 * gap) / 4, y = 1.8, h = 2.35;
	takeaways.forEach(([head, body], i) => {
		const x = M + i * (w + gap);
		box(s, { x, y, w, h, radius: 0.08, fill: { color: STEEL }, objectName: `Takeaway ${i + 1} card` });
		text(s, `0${i + 1}`, { x: x + 0.25, y: y + 0.2, w: 1.0, h: 0.55, fontFace: HEAD, fontSize: 28, bold: true, color: AMBER, objectName: `Takeaway ${i + 1} number` });
		text(s, head, { x: x + 0.25, y: y + 0.85, w: w - 0.5, h: 0.4, fontSize: 16, bold: true, color: WHITE, objectName: `Takeaway ${i + 1} heading` });
		text(s, body, { x: x + 0.25, y: y + 1.32, w: w - 0.5, h: 0.9, fontSize: 14, color: ICE, objectName: `Takeaway ${i + 1} text` });
	});

	text(s, "“The value of data lies not merely in collecting it, but in drawing reliable conclusions from it.”", { x: M, y: 4.5, w: CW, h: 0.95, fontFace: HEAD, fontSize: 23, italic: true, color: WHITE, objectName: "Closing statement" });
	text(s, "Thank you · Questions?", { x: M, y: 5.5, w: CW, h: 0.4, fontSize: 17, bold: true, color: AMBER, objectName: "Thank you" });
	text(s, "References: Brynjolfsson, Hitt & Kim (2011), SSRN · Kohavi & Thomke (2017), Harvard Business Review 95(5) · RECOVERY Collaborative Group (2021), NEJM 384(8) · Open Science Collaboration (2015), Science 349 · Wasserstein & Lazar (2016), The American Statistician 70(2)", { x: M, y: 6.2, w: CW, h: 0.6, fontSize: 10, color: ICE, objectName: "References" });

	s.addNotes(
		"Four takeaways. One: statistics turns data into evidence by separating real patterns from noise. Two: testing ideas before deciding beats opinion. " +
			"Three: in research, good design and the right sample size make results reliable. Four: interpret results responsibly, with effect sizes, transparency and fairness. " +
			"The value of data lies not merely in collecting it, but in drawing reliable conclusions from it. Thank you. We are happy to take questions."
	);
}

(async () => {
	slideTitle();
	await slideWhy();
	await slideImplications();
	slideCase();
	await slideChallenges();
	slideConclusion();
	await pres.writeFile({ fileName: OUT });
	await applyTheme(OUT, THEME);
	console.log("wrote", OUT);
})();
