// Builds Advanced_Statistics_Short_Presentation.pptx: a short-text version of the deck
// (a title slide plus five content slides).
//
//   NODE_PATH=<node_modules with pptxgenjs, react-icons, react, react-dom, sharp> \
//     node build_short_deck.cjs <path to pptx skill apply_theme.js>
const path = require("path");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");

const HERE = __dirname;
const ASSETS = path.join(HERE, "assets");
const OUT = path.join(HERE, "..", "Advanced_Statistics_Short_Presentation.pptx");
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
pres.subject = "Short university presentation on advanced statistics (title + five slides)";
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

// ---------- slide 2: what & why ----------
async function slideWhy() {
	pres.addSection({ title: "Content" });
	const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Content" });
	s.addText("01 · WHAT & WHY", { placeholder: "kicker" });
	s.addText("Statistics turns data into decisions", { placeholder: "title" });
	text(s, "Advanced statistics helps us find real patterns, measure how sure we are, and choose with evidence instead of guesswork.", { x: M, y: 1.6, w: CW, h: 0.5, fontSize: 16, color: SLATE, objectName: "Slide description" });

	const flow = ["Collect data", "Find patterns", "Measure uncertainty", "Make decisions"];
	const w = 2.8, gap = (CW - 4 * w) / 3, y = 2.35, h = 0.7;
	flow.forEach((t, i) => {
		const x = M + i * (w + gap), last = i === flow.length - 1;
		box(s, { x, y, w, h, radius: 0.35, fill: { color: last ? NAVY : MIST }, objectName: `Flow step ${i + 1}` });
		text(s, [{ text: `${i + 1}  `, options: { bold: true, color: last ? AMBER : TEAL } }, { text: t, options: { bold: true, color: last ? WHITE : NAVY } }], { x, y, w, h, fontSize: 16, align: "center", valign: "middle", objectName: `Flow step ${i + 1} text` });
		if (i > 0) chevron(s, x - gap / 2 - 0.075, y + h / 2 - 0.15, `Flow arrow ${i + 1}`);
	});

	text(s, "Four key methods", { x: M, y: 3.35, w: CW, h: 0.38, fontFace: HEAD, fontSize: 18, bold: true, color: NAVY, objectName: "Methods heading" });
	const methods = [
		["regression", "Regression", "Shows how one factor affects another, e.g. price → sales."],
		["hypothesis", "Hypothesis testing", "Checks whether a difference is real or just chance."],
		["timeseries", "Forecasting", "Predicts future values, such as demand, with a range."],
		["experiment", "A/B testing", "Compares two options fairly using random groups."],
	];
	const cw = (CW - 3 * 0.25) / 4, cy = 3.85, ch = 2.95;
	methods.forEach(([g, name, body], i) => {
		const x = M + i * (cw + 0.25);
		box(s, { x, y: cy, w: cw, h: ch, radius: 0.08, fill: { color: MIST }, objectName: `${name} card` });
		s.addImage({ path: path.join(ASSETS, `glyph_${g}.png`), x: x + 0.22, y: cy + 0.22, w: 1.0, h: 1.0, altText: `Diagram: ${name}`, objectName: `${name} diagram` });
		text(s, name, { x: x + 0.22, y: cy + 1.38, w: cw - 0.44, h: 0.4, fontFace: HEAD, fontSize: 17, bold: true, color: NAVY, objectName: `${name} title` });
		text(s, body, { x: x + 0.22, y: cy + 1.84, w: cw - 0.44, h: 0.95, fontSize: 14, objectName: `${name} text` });
	});

	s.addNotes(
		"Data alone does not give answers. Statistics takes us from collecting data, to finding patterns, to measuring how sure we are, and finally to a decision. " +
			"Four methods do most of this work: regression shows how one factor affects another; hypothesis testing checks whether a difference is real or just chance; " +
			"forecasting predicts the future with a range; and A/B testing compares two options fairly by splitting people into random groups."
	);
}

// ---------- slide 3: business and research ----------
async function slideUses() {
	const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Content" });
	s.addText("02 · REAL-WORLD USES", { placeholder: "kicker" });
	s.addText("Better decisions in business and research", { placeholder: "title" });

	const cols = [
		{
			name: "Business", icon: fa.FaBriefcase, col: STEEL,
			rows: [["Sales forecasting", "plan the right stock level"], ["Customer segmentation", "target the right customers"], ["Pricing", "find the price that earns most"], ["Risk & fraud", "approve loans more safely"]],
			caseText: "Bing tested longer ad titles with an A/B test: revenue rose about 12% (≈ $100M a year in the U.S.).",
			source: "Kohavi & Thomke (2017), Harvard Business Review",
		},
		{
			name: "Research", icon: fa.FaFlask, col: TEAL,
			rows: [["Study design", "make comparisons fair"], ["Sample size", "get reliable results"], ["Confidence intervals", "show how sure we are"], ["Replication", "build results others trust"]],
			caseText: "RECOVERY trial: dexamethasone cut 28-day deaths in ventilated COVID-19 patients from 41.4% to 29.3%.",
			source: "RECOVERY Collaborative Group (2021), NEJM",
		},
	];
	const w = (CW - 0.35) / 2, y = 1.7, h = 5.15;
	for (let i = 0; i < cols.length; i++) {
		const c = cols[i], x = M + i * (w + 0.35);
		box(s, { x, y, w, h, radius: 0.08, fill: { color: MIST }, objectName: `${c.name} panel` });
		s.addShape(pres.ShapeType.ellipse, { x: x + 0.3, y: y + 0.25, w: 0.56, h: 0.56, fill: { color: c.col }, line: { type: "none" }, objectName: `${c.name} icon circle` });
		s.addImage({ data: await icon(c.icon), x: x + 0.44, y: y + 0.39, w: 0.28, h: 0.28, altText: c.name, objectName: `${c.name} icon` });
		text(s, c.name, { x: x + 1.05, y: y + 0.25, w: w - 1.3, h: 0.56, fontFace: HEAD, fontSize: 21, bold: true, color: NAVY, valign: "middle", objectName: `${c.name} heading` });
		c.rows.forEach(([k, v], r) => {
			const ry = y + 1.05 + r * 0.5;
			s.addShape(pres.ShapeType.ellipse, { x: x + 0.36, y: ry + 0.14, w: 0.13, h: 0.13, fill: { color: c.col }, line: { type: "none" }, objectName: `${c.name} point ${r + 1} marker` });
			text(s, [{ text: k, options: { bold: true, color: NAVY } }, { text: `  →  ${v}` }], { x: x + 0.65, y: ry, w: w - 0.9, h: 0.42, fontSize: 15, valign: "middle", objectName: `${c.name} point ${r + 1}` });
		});
		box(s, { x: x + 0.3, y: y + 3.25, w: w - 0.6, h: 1.62, radius: 0.06, fill: { color: NAVY }, objectName: `${c.name} case box` });
		text(s, "REAL CASE", { x: x + 0.5, y: y + 3.4, w: w - 1.0, h: 0.24, fontSize: 10.5, bold: true, color: AMBER, charSpacing: 2, objectName: `${c.name} case tag` });
		text(s, c.caseText, { x: x + 0.5, y: y + 3.68, w: w - 1.0, h: 0.8, fontSize: 14, color: WHITE, objectName: `${c.name} case text` });
		text(s, c.source, { x: x + 0.5, y: y + 4.5, w: w - 1.0, h: 0.24, fontSize: 10, italic: true, color: ICE, objectName: `${c.name} case source` });
	}

	s.addNotes(
		"In business, statistics helps companies forecast sales, group customers, set prices and spot risky loans or fraud. " +
			"A real example: Bing tested longer ad titles using an A/B test. Revenue went up about 12 percent, worth more than 100 million dollars a year in the U.S. " +
			"In research, statistics makes studies fair and reliable through good design, the right sample size, confidence intervals and replication. " +
			"Example: the RECOVERY trial showed that dexamethasone reduced deaths in ventilated COVID-19 patients from 41.4 to 29.3 percent."
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

// ---------- slide 5: challenges ----------
async function slideChallenges() {
	const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Content" });
	s.addText("04 · CHALLENGES", { placeholder: "kicker" });
	s.addText("Use statistics carefully and honestly", { placeholder: "title" });
	text(s, "Statistics is powerful, but careless use can lead to confident and wrong decisions.", { x: M, y: 1.6, w: CW, h: 0.5, fontSize: 16, color: SLATE, objectName: "Slide description" });

	const risks = [
		[fa.FaDatabase, "Bad or biased data", "If the data is wrong or one-sided, the answer will be wrong too."],
		[fa.FaProjectDiagram, "Correlation ≠ causation", "Two things moving together does not prove one causes the other."],
		[fa.FaSearchPlus, "“Significant” ≠ important", "A tiny effect can still be significant. Always check how big it is."],
		[fa.FaUserShield, "Privacy & fairness", "Protect personal data and check that models are fair to every group."],
	];
	const w = (CW - 3 * 0.25) / 4, y = 2.3, h = 3.0;
	for (let i = 0; i < risks.length; i++) {
		const [Ic, head, body] = risks[i];
		const x = M + i * (w + 0.25);
		box(s, { x, y, w, h, radius: 0.08, fill: { color: MIST }, objectName: `Risk ${i + 1} card` });
		s.addShape(pres.ShapeType.ellipse, { x: x + 0.25, y: y + 0.28, w: 0.66, h: 0.66, fill: { color: CORAL }, line: { type: "none" }, objectName: `Risk ${i + 1} icon circle` });
		s.addImage({ data: await icon(Ic), x: x + 0.42, y: y + 0.45, w: 0.32, h: 0.32, altText: head, objectName: `Risk ${i + 1} icon` });
		text(s, head, { x: x + 0.25, y: y + 1.12, w: w - 0.5, h: 0.72, fontFace: HEAD, fontSize: 17, bold: true, color: NAVY, objectName: `Risk ${i + 1} heading` });
		text(s, body, { x: x + 0.25, y: y + 1.9, w: w - 0.5, h: 1.0, fontSize: 14, objectName: `Risk ${i + 1} text` });
	}

	box(s, { x: M, y: 5.6, w: CW, h: 1.15, radius: 0.08, fill: { color: NAVY }, objectName: "AI note box" });
	s.addShape(pres.ShapeType.ellipse, { x: M + 0.3, y: 5.84, w: 0.66, h: 0.66, fill: { color: TEAL }, line: { type: "none" }, objectName: "AI icon circle" });
	s.addImage({ data: await icon(fa.FaRobot), x: M + 0.47, y: 6.01, w: 0.32, h: 0.32, altText: "Machine learning and AI", objectName: "AI icon" });
	text(s, [
		{ text: "WHAT ABOUT AI?", options: { bold: true, color: AMBER, charSpacing: 2, fontSize: 11, breakLine: true } },
		{ text: "Machine learning is great at prediction, but a good prediction does not prove cause. Good practice: plan first, check the data, report results honestly.", options: { color: WHITE } },
	], { x: M + 1.2, y: 5.6, w: CW - 1.5, h: 1.15, fontSize: 14.5, valign: "middle", objectName: "AI note text" });

	s.addNotes(
		"Statistics can mislead if we are careless. First, bad or biased data gives wrong answers. Second, correlation is not causation: two things moving together does not prove one causes the other. " +
			"Third, 'significant' does not mean important; a very small effect can still be significant, so we always check its size. Fourth, we must protect privacy and make sure models are fair. " +
			"Finally, AI and machine learning are very good at prediction, but prediction alone does not prove cause, so careful planning and honest reporting still matter."
	);
}

// ---------- slide 6: conclusion ----------
function slideConclusion() {
	pres.addSection({ title: "Conclusion" });
	const s = pres.addSlide({ masterName: "CLOSING_DARK", sectionTitle: "Conclusion" });
	s.addText("05 · CONCLUSION", { placeholder: "kicker" });
	s.addText("Key takeaways", { placeholder: "title" });

	const takeaways = [
		["Data becomes evidence", "Statistics turns raw data into results we can trust."],
		["Better decisions", "Testing ideas and measuring uncertainty beat guesswork."],
		["Careful interpretation", "How we read results matters as much as the method."],
	];
	const w = (CW - 2 * 0.35) / 3, y = 1.85, h = 2.3;
	takeaways.forEach(([head, body], i) => {
		const x = M + i * (w + 0.35);
		box(s, { x, y, w, h, radius: 0.08, fill: { color: STEEL }, objectName: `Takeaway ${i + 1} card` });
		text(s, `0${i + 1}`, { x: x + 0.3, y: y + 0.25, w: 1.0, h: 0.6, fontFace: HEAD, fontSize: 30, bold: true, color: AMBER, objectName: `Takeaway ${i + 1} number` });
		text(s, head, { x: x + 0.3, y: y + 0.95, w: w - 0.6, h: 0.4, fontSize: 18, bold: true, color: WHITE, objectName: `Takeaway ${i + 1} heading` });
		text(s, body, { x: x + 0.3, y: y + 1.4, w: w - 0.6, h: 0.75, fontSize: 14.5, color: ICE, objectName: `Takeaway ${i + 1} text` });
	});

	text(s, "“The value of data lies not merely in collecting it, but in drawing reliable conclusions from it.”", { x: M, y: 4.5, w: CW, h: 0.95, fontFace: HEAD, fontSize: 23, italic: true, color: WHITE, objectName: "Closing statement" });
	text(s, "Thank you · Questions?", { x: M, y: 5.55, w: CW, h: 0.4, fontSize: 17, bold: true, color: AMBER, objectName: "Thank you" });
	text(s, "References: Kohavi & Thomke (2017), Harvard Business Review 95(5) · RECOVERY Collaborative Group (2021), NEJM 384(8) · Wasserstein & Lazar (2016), The American Statistician 70(2) · Shmueli (2010), Statistical Science 25(3)", { x: M, y: 6.3, w: CW, h: 0.5, fontSize: 10, color: ICE, objectName: "References" });

	s.addNotes(
		"To conclude, three takeaways. One: statistics turns raw data into evidence we can trust. Two: testing ideas and measuring uncertainty lead to better decisions than guesswork. " +
			"Three: careful interpretation matters as much as the method. " +
			"The value of data lies not merely in collecting it, but in drawing reliable conclusions from it. Thank you. We are happy to take questions."
	);
}

(async () => {
	slideTitle();
	await slideWhy();
	await slideUses();
	slideCase();
	await slideChallenges();
	slideConclusion();
	await pres.writeFile({ fileName: OUT });
	await applyTheme(OUT, THEME);
	console.log("wrote", OUT);
})();
