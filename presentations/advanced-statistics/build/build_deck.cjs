// Builds Advanced_Statistics_Presentation.pptx with pptxgenjs.
//
//   NODE_PATH=<node_modules with pptxgenjs, react-icons, react, react-dom, sharp> \
//     node build_deck.cjs <path to pptx skill apply_theme.js>
//
// Shapes whose objectName ends in " #n" are revealed on click n by add_animations.py.
const path = require("path");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");

const HERE = __dirname;
const ASSETS = path.join(HERE, "assets");
const OUT = path.join(HERE, "..", "Advanced_Statistics_Presentation.pptx");
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
pres.subject = "University presentation on advanced statistics";
pres.author = "[Team Name]";

const C = pres.SchemeColor;
const INK = C.text1, NAVY = C.text2, WHITE = C.background1, MIST = C.background2;
const TEAL = C.accent1, AMBER = C.accent2, STEEL = C.accent3, CORAL = C.accent4, SLATE = C.accent5, ICE = C.accent6;
const HEAD = "+mj-lt"; // theme heading font

const M = 0.6, CW = 12.133, RIGHT = M + CW;
const FOOTER = "Implications of Advanced Statistics in Business and Research";

// ---------- layouts ----------
const kickerPh = (color) => ({ placeholder: { options: { name: "kicker", type: "body", x: M, y: 0.4, w: 8.2, h: 0.32, fontSize: 12, bold: true, color, charSpacing: 2, margin: 0, valign: "middle" }, text: "" } });
const titlePh = (color) => ({ placeholder: { options: { name: "title", type: "title", x: M, y: 0.72, w: CW, h: 0.78, fontFace: HEAD, fontSize: 34, bold: true, color, margin: 0, valign: "middle", align: "left" }, text: "" } });

pres.defineSlideMaster({
	title: "TITLE_DARK",
	background: { color: NAVY },
	objects: [
		{ placeholder: { options: { name: "title", type: "title", x: M, y: 0.98, w: 6.3, h: 1.85, fontFace: HEAD, fontSize: 36, bold: true, color: WHITE, margin: 0, valign: "top", align: "left" }, text: "" } },
	],
});
pres.defineSlideMaster({
	title: "CONTENT",
	background: { color: WHITE },
	objects: [
		kickerPh(TEAL),
		titlePh(NAVY),
		{ text: { text: FOOTER, options: { x: M, y: 7.05, w: 8, h: 0.28, fontSize: 9, color: SLATE, margin: 0, valign: "middle" } } },
	],
	slideNumber: { x: RIGHT - 0.6, y: 7.05, w: 0.6, h: 0.28, fontSize: 9, color: SLATE, align: "right", margin: 0 },
});
pres.defineSlideMaster({
	title: "CLOSING_DARK",
	background: { color: NAVY },
	objects: [
		kickerPh(AMBER),
		titlePh(WHITE),
		{ text: { text: FOOTER, options: { x: M, y: 7.05, w: 8, h: 0.28, fontSize: 9, color: ICE, margin: 0, valign: "middle" } } },
	],
	slideNumber: { x: RIGHT - 0.6, y: 7.05, w: 0.6, h: 0.28, fontSize: 9, color: ICE, align: "right", margin: 0 },
});

// ---------- helpers ----------
function text(slide, content, opts) {
	slide.addText(content, { isTextBox: true, margin: 0, valign: "top", color: INK, fontSize: 14, ...opts });
}
function box(slide, opts) {
	const { radius, ...rest } = opts;
	slide.addShape(radius ? pres.ShapeType.roundRect : pres.ShapeType.rect, { line: { type: "none" }, ...(radius ? { rectRadius: radius } : {}), ...rest });
}
function chevron(slide, x, y, name, color = SLATE) {
	slide.addShape(pres.ShapeType.chevron, { x, y, w: 0.13, h: 0.26, fill: { color }, line: { type: "none" }, objectName: name });
}
async function icon(Comp, color = "#FFFFFF", size = 256) {
	const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color, size: String(size) }));
	const buf = await sharp(Buffer.from(svg)).png().toBuffer();
	return "image/png;base64," + buf.toString("base64");
}
const shadow = () => ({ type: "outer", color: "0B1F33", opacity: 0.12, blur: 6, offset: 1.5, angle: 90 });

// ---------- slide 1: title ----------
function slideTitle() {
	pres.addSection({ title: "Opening" });
	const s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: "Opening" });
	s.addImage({ path: path.join(ASSETS, "hero.png"), x: 7.283, y: 0, w: 6.05, h: 7.5, altText: "Illustrative graphic built from simulated data: raw observations, a fitted trend with its uncertainty band, a widening forecast interval, and the predictive distribution used for a decision.", objectName: "Hero visual (simulated data)" });
	const stages = [["Data", 0.98, "center"], ["Model + uncertainty", 3.0, "center"], ["Forecast → decision", 4.45, "right"]];
	stages.forEach(([label, dx, align]) => text(s, label, { x: 7.283 + dx - 0.75, y: 6.98, w: 1.5, h: 0.26, fontSize: 10, color: ICE, align, objectName: `Hero label: ${label}` }));
	text(s, "Illustrative visual · simulated data", { x: 10.9, y: 0.25, w: 2.2, h: 0.24, fontSize: 9, color: SLATE, align: "right", italic: true, objectName: "Hero caption" });

	text(s, "ADVANCED STATISTICS IN PRACTICE", { x: M, y: 0.55, w: 6.3, h: 0.3, fontSize: 12, bold: true, color: ICE, charSpacing: 3, objectName: "Kicker" });
	s.addText("Implications of Advanced Statistics in Business and Research", { placeholder: "title" });
	text(s, "Turning data into evidence, decisions, and discovery", { x: M, y: 2.92, w: 6.4, h: 0.42, fontSize: 19, italic: true, color: ICE, objectName: "Subtitle" });

	// Team block: a borderless table, so members can be added (Tab in last cell) or removed (delete row).
	text(s, [{ text: "PRESENTED BY  ", options: { bold: true, color: AMBER, charSpacing: 2 } }, { text: "[Team Name]", options: { bold: true, color: WHITE } }], { x: M, y: 3.66, w: 6.3, h: 0.28, fontSize: 11.5, objectName: "Team name" });
	const none = { type: "none" };
	const memberRows = [1, 2, 3, 4, 5].map((i) => [
		{ text: `[Member ${i} Full Name]`, options: { color: WHITE } },
		{ text: "[Student ID]", options: { color: ICE } },
	]);
	s.addTable(memberRows, { x: M, y: 3.98, w: 5.4, colW: [3.3, 2.1], rowH: 0.27, fontSize: 13, margin: [0, 0, 0, 0], valign: "middle", border: [none, none, none, none], fill: { color: NAVY }, objectName: "Team members table" });

	const detail = (label, value, x, y, w, name) =>
		text(s, [{ text: label, options: { fontSize: 9.5, bold: true, color: AMBER, charSpacing: 2, breakLine: true } }, { text: value, options: { fontSize: 12.5, color: WHITE } }], { x, y, w, h: 0.46, objectName: name });
	detail("COURSE", "[Course Title] ([Course Code])", M, 5.5, 3.3, "Course title and code");
	detail("INSTRUCTOR", "[Instructor Name], [Designation]", 4.05, 5.5, 3.0, "Instructor");
	detail("DEPARTMENT", "[Department]", M, 6.05, 3.3, "Department");
	detail("UNIVERSITY", "[University Name]", 4.05, 6.05, 3.0, "University");
	detail("DATE", "[Presentation Date]", M, 6.6, 3.3, "Presentation date");

	s.addNotes(
		"OPENING (about 1 minute)\n" +
			"Introduce the team and the question this presentation answers: what changes when organizations and researchers move beyond simple summaries to advanced statistical methods?\n\n" +
			"The visual on the right is the story of the talk in one picture (simulated data, for illustration only): raw observations (white points), a fitted model with an uncertainty band (teal), a forecast whose interval widens with the horizon (amber), and the predictive distribution that a decision-maker compares with a threshold (the horizontal line).\n\n" +
			"Roadmap: why it matters, the key methods, business implications, research implications, a worked A/B-test case, risks and ethics, and the takeaways.\n\n" +
			"Editing: team member names and IDs are in a borderless table. Click the last cell and press Tab to add a member; right-click a row and choose Delete Rows to remove one."
	);
}

// ---------- slide 2: why it matters ----------
async function slideWhy() {
	pres.addSection({ title: "Foundations" });
	const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Foundations" });
	s.addText("02 · WHY ADVANCED STATISTICS MATTERS", { placeholder: "kicker" });
	s.addText("Statistics turns data into evidence you can act on", { placeholder: "title" });

	const stages = [
		["RAW DATA", "What was recorded?", "Transactions, sensors, surveys and trial records — noisy and incomplete.", SLATE],
		["DESCRIPTION · BI", "What happened?", "Dashboards and averages summarize the past but cannot separate signal from noise.", STEEL],
		["PREDICTIVE ANALYTICS", "What is likely next?", "Models learn patterns to forecast outcomes and score the risk of new cases.", STEEL],
		["STATISTICAL INFERENCE", "Is it real, why, and how sure are we?", "Tests, intervals and causal designs weigh competing explanations.", TEAL],
		["EVIDENCE-BASED DECISION", "What should we do?", "Act with the expected benefit and its uncertainty made explicit.", AMBER],
	];
	const w = 2.25, gap = 0.22, y = 1.72, h = 2.08;
	stages.forEach(([tag, q, d, col], i) => {
		const x = M + i * (w + gap);
		const last = i === stages.length - 1;
		const n = ` #${i + 1}`;
		box(s, { x, y, w, h, radius: 0.08, fill: { color: last ? NAVY : MIST }, objectName: `Stage ${i + 1} card${n}` });
		text(s, tag, { x: x + 0.15, y: y + 0.16, w: w - 0.3, h: 0.24, fontSize: 10, bold: true, color: last ? AMBER : col, charSpacing: 1, objectName: `Stage ${i + 1} tag${n}` });
		text(s, q, { x: x + 0.15, y: y + 0.44, w: w - 0.3, h: 0.6, fontFace: HEAD, fontSize: 15, bold: true, color: last ? WHITE : NAVY, objectName: `Stage ${i + 1} question${n}` });
		text(s, d, { x: x + 0.15, y: y + 1.1, w: w - 0.3, h: 0.9, fontSize: 12, color: last ? ICE : INK, objectName: `Stage ${i + 1} description${n}` });
		if (i > 0) chevron(s, x - gap / 2 - 0.065, y + h / 2 - 0.13, `Arrow into stage ${i + 1}${n}`);
	});

	text(s, "Why intuition and simple summaries fall short", { x: M, y: 4.15, w: 7.7, h: 0.36, fontFace: HEAD, fontSize: 17, bold: true, color: NAVY, objectName: "Limits heading" });
	const limits = [
		[fa.FaLayerGroup, "Averages hide structure", "Combined data can show the opposite trend to every subgroup (Simpson’s paradox)."],
		[fa.FaWaveSquare, "Patterns can be noise", "Without a measure of sampling variability, chance fluctuations look like real signals."],
		[fa.FaProjectDiagram, "Correlation ≠ causation", "A hidden confounder can drive both variables; only design or explicit causal assumptions resolve it."],
	];
	const cw = 2.43, cg = 0.2;
	for (let i = 0; i < limits.length; i++) {
		const [Ic, head, body] = limits[i];
		const x = M + i * (cw + cg), y0 = 4.65;
		box(s, { x, y: y0, w: cw, h: 2.2, radius: 0.08, fill: { color: WHITE }, line: { color: MIST, width: 1.25 }, shadow: shadow(), objectName: `Limit ${i + 1} card` });
		s.addShape(pres.ShapeType.ellipse, { x: x + 0.18, y: y0 + 0.2, w: 0.5, h: 0.5, fill: { color: TEAL }, line: { type: "none" }, objectName: `Limit ${i + 1} icon circle` });
		s.addImage({ data: await icon(Ic), x: x + 0.3, y: y0 + 0.32, w: 0.26, h: 0.26, altText: head, objectName: `Limit ${i + 1} icon` });
		text(s, head, { x: x + 0.18, y: y0 + 0.82, w: cw - 0.36, h: 0.3, fontSize: 14, bold: true, color: NAVY, objectName: `Limit ${i + 1} heading` });
		text(s, body, { x: x + 0.18, y: y0 + 1.15, w: cw - 0.36, h: 0.95, fontSize: 12, objectName: `Limit ${i + 1} text` });
	}

	const px = 8.69, pw = RIGHT - px, py = 4.15;
	box(s, { x: px, y: py, w: pw, h: 2.7, radius: 0.08, fill: { color: NAVY }, objectName: "Evidence panel" });
	text(s, "EVIDENCE FROM BUSINESS RESEARCH", { x: px + 0.25, y: py + 0.2, w: pw - 0.5, h: 0.24, fontSize: 10, bold: true, color: AMBER, charSpacing: 1, objectName: "Evidence tag" });
	text(s, "5–6%", { x: px + 0.25, y: py + 0.45, w: pw - 0.5, h: 0.72, fontFace: HEAD, fontSize: 44, bold: true, color: AMBER, valign: "middle", objectName: "Evidence statistic" });
	text(s, "higher output and productivity in firms that use data-driven decision-making than their other investments and IT use would predict (179 large publicly traded U.S. firms).", { x: px + 0.25, y: py + 1.2, w: pw - 0.5, h: 0.92, fontSize: 12.5, color: WHITE, objectName: "Evidence text" });
	text(s, "Brynjolfsson, Hitt & Kim (2011). Observational study; instrumental variables used to address reverse causality.", { x: px + 0.25, y: py + 2.15, w: pw - 0.5, h: 0.45, fontSize: 10, color: ICE, objectName: "Evidence source" });

	s.addNotes(
		"WHY IT MATTERS (about 2 minutes)\n\n" +
			"Walk the five stages left to right (each appears on click).\n" +
			"- Business intelligence describes what happened: dashboards, KPIs, averages. Useful, but it cannot tell you whether a change is real or random.\n" +
			"- Predictive analytics answers 'what is likely next?' It can be very accurate without explaining why.\n" +
			"- Statistical inference asks whether a pattern is real, how large it is, how uncertain we are, and which explanation the evidence favors. Causal designs go one step further and ask what happens if we intervene.\n" +
			"Shmueli (2010), 'To explain or to predict?', makes this distinction: explanatory, predictive and descriptive models serve different goals and are judged by different criteria.\n\n" +
			"Limits of intuition: Simpson's paradox (aggregated data can reverse a subgroup trend); sampling variability (small samples produce striking but unstable patterns); confounding (a third factor drives both variables).\n\n" +
			"Evidence: Brynjolfsson, Hitt and Kim (2011) surveyed 179 large publicly traded firms and found that firms adopting data-driven decision-making had output and productivity about 5-6% higher than expected given their other investments and IT use. Be precise: this is an observational association; the authors use instrumental-variable methods to argue against reverse causality, but it is not a randomized experiment.\n\n" +
			"Source: Brynjolfsson, E., Hitt, L. M., & Kim, H. H. (2011). Strength in numbers: How does data-driven decisionmaking affect firm performance? https://doi.org/10.2139/ssrn.1819486"
	);
}

// ---------- slide 3: methods ----------
function slideMethods() {
	pres.addSection({ title: "Methods" });
	const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Methods" });
	s.addText("03 · KEY ADVANCED STATISTICAL METHODS", { placeholder: "kicker" });
	s.addText("Different methods answer different questions", { placeholder: "title" });

	const methods = [
		["regression", "Regression & predictive modeling", "How does an outcome move with its drivers, and what will it be for a new case?", "Price elasticity and sales drivers; wage and dose–response studies.", "Coefficients show association unless the design supports causation."],
		["hypothesis", "Hypothesis tests & confidence intervals", "Is a difference bigger than sampling noise, and how large could it plausibly be?", "Comparing campaigns or treatments; quality-control checks.", "p < 0.05 does not prove an important effect — report effect sizes."],
		["bayes", "Bayesian inference", "Given prior knowledge and new data, how probable is each explanation?", "Updating risk estimates; adaptive clinical trials; small-sample tests.", "Conclusions depend on the prior — state it and test its influence."],
		["timeseries", "Time-series forecasting", "What comes next, given trend, seasonality and autocorrelation?", "Demand, inventory and cash-flow planning; economic and disease series.", "Structural breaks can ruin forecasts; always show prediction intervals."],
		["experiment", "Experimental design & causal inference", "What happens if we intervene, rather than merely observe?", "A/B tests and pricing trials; randomized controlled trials; difference-in-differences.", "Needs randomization or strong, explicitly stated assumptions."],
		["cluster", "Multivariate analysis & clustering", "What structure exists across many variables at once?", "Customer segments; survey scales (PCA, factor analysis); gene groups.", "Clusters are descriptive and shift with variable scaling and the chosen k."],
	];
	const w = (CW - 0.4) / 3, h = 2.3, gap = 0.18;
	methods.forEach(([g, name, asks, applied, caveat], i) => {
		const x = M + (i % 3) * (w + gap), y = 1.68 + Math.floor(i / 3) * (h + gap);
		box(s, { x, y, w, h, radius: 0.08, fill: { color: MIST }, objectName: `${name} card` });
		s.addImage({ path: path.join(ASSETS, `glyph_${g}.png`), x: x + 0.14, y: y + 0.12, w: 0.72, h: 0.72, altText: `Diagram: ${name}`, objectName: `${name} diagram` });
		text(s, name, { x: x + 1.0, y: y + 0.12, w: w - 1.15, h: 0.72, fontFace: HEAD, fontSize: 15, bold: true, color: NAVY, valign: "middle", objectName: `${name} title` });
		text(s, [
			{ text: "Asks  ", options: { bold: true, color: TEAL } }, { text: asks, options: { breakLine: true } },
			{ text: "Applied  ", options: { bold: true, color: STEEL } }, { text: applied, options: { breakLine: true } },
			{ text: "Caveat  ", options: { bold: true, color: CORAL } }, { text: caveat },
		], { x: x + 0.15, y: y + 0.92, w: w - 0.3, h: 1.3, fontSize: 12, paraSpaceAfter: 3, objectName: `${name} summary` });
	});
	box(s, { x: M, y: 6.53, w: CW, h: 0.4, radius: 0.2, fill: { color: NAVY }, objectName: "Method selection note" });
	text(s, [
		{ text: "Choosing a method:  ", options: { bold: true, color: AMBER } },
		{ text: "research objective  →  data structure (scale, dependence, sample size)  →  assumptions  →  decision context", options: { color: WHITE } },
	], { x: M + 0.3, y: 6.53, w: CW - 0.6, h: 0.4, fontSize: 12.5, valign: "middle", align: "center", objectName: "Method selection text" });

	s.addNotes(
		"KEY METHODS (about 2 minutes). For each method: what it does, why it is useful, how it is applied, what it supports, and its limits.\n\n" +
			"1. Regression and predictive modeling. Models an outcome as a function of predictors and quantifies each association with uncertainty. Useful for explaining variation and predicting new cases. Business: price elasticity, sales-driver analysis. Research: wage equations, dose-response. Supports pricing, budgeting and targeting decisions. Limits: omitted variables, multicollinearity, overfitting; coefficients are associations unless the design is causal.\n\n" +
			"2. Hypothesis tests and confidence intervals. Ask whether an observed difference is larger than expected from sampling variation, and give a range of effect sizes compatible with the data. Supports go/no-go decisions and scientific claims. Limits: a p-value is not the probability that the hypothesis is true and does not measure effect size or importance (ASA statement, Wasserstein & Lazar, 2016). Always report the effect size and its interval.\n\n" +
			"3. Bayesian inference. Combines a prior distribution with the likelihood of the data to give a posterior distribution, so results can be stated as probabilities of hypotheses or parameter values. Useful with small samples, sequential decisions and when prior evidence exists. Applications: credit-risk updating, adaptive clinical trials, Bayesian A/B testing. Limits: sensitivity to the prior and computational cost; report the prior and run sensitivity analyses (Gelman et al., 2013).\n\n" +
			"4. Time-series forecasting. Models trend, seasonality and autocorrelation (exponential smoothing, ARIMA) to forecast future values with prediction intervals. Supports inventory, staffing and cash-flow planning. Limits: assumes the past pattern continues; structural breaks (for example, a pandemic) can invalidate a model (Hyndman & Athanasopoulos, 2021).\n\n" +
			"5. Experimental design and causal inference. Random assignment makes groups comparable on both measured and unmeasured factors, so differences in outcomes can be attributed to the intervention. Quasi-experimental methods (difference-in-differences, instrumental variables, regression discontinuity) estimate causal effects from observational data under explicit assumptions. Supports decisions about interventions. Limits: experiments are not always ethical or feasible; quasi-experiments rest on assumptions that must be defended (Hernan & Robins, 2020).\n\n" +
			"6. Multivariate analysis and clustering. Principal component and factor analysis reduce many correlated variables to a few dimensions; cluster analysis groups similar observations. Supports segmentation and measurement design. Limits: clusters are descriptive, depend on scaling and the number of clusters, and should be validated for stability.\n\n" +
			"Key message: the question, data structure and assumptions decide the method, not the software."
	);
}

// ---------- slide 4: business ----------
function slideBusiness() {
	pres.addSection({ title: "Implications" });
	const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Implications" });
	s.addText("04 · IMPLICATIONS IN BUSINESS DECISION-MAKING", { placeholder: "kicker" });
	s.addText("Statistics changes how firms decide", { placeholder: "title" });

	text(s, [
		{ text: "VERIFIED CASE  ", options: { bold: true, color: TEAL, charSpacing: 1 } },
		{ text: "Bing search ads: one online controlled experiment, from question to outcome (Kohavi & Thomke, 2017)", options: { color: INK } },
	], { x: M, y: 1.6, w: CW, h: 0.28, fontSize: 12.5, objectName: "Case label" });

	const chain = [
		["QUESTION", "Would longer ad titles raise revenue without hurting the user experience?"],
		["DATA", "Users randomly assigned to the old or new ad layout; revenue and user-experience metrics logged."],
		["METHOD", "Online controlled experiment (A/B test) with significance tests on each metric."],
		["INSIGHT", "Revenue up about 12% with no harm to key user-experience metrics; result replicated."],
		["DECISION", "Ship an idea that had sat in the backlog for more than six months."],
		["OUTCOME", "Estimated at more than $100 million a year in U.S. revenue at the time."],
	];
	const gap = 0.16, w = (CW - 5 * gap) / 6, y = 1.96, h = 1.68;
	chain.forEach(([tag, body], i) => {
		const x = M + i * (w + gap);
		const dark = i >= 4;
		const n = ` #${i + 1}`;
		box(s, { x, y, w, h, radius: 0.08, fill: { color: dark ? NAVY : MIST }, objectName: `Chain ${tag} card${n}` });
		text(s, `${i + 1} · ${tag}`, { x: x + 0.13, y: y + 0.14, w: w - 0.26, h: 0.24, fontSize: 10, bold: true, color: dark ? AMBER : TEAL, charSpacing: 1, objectName: `Chain ${tag} tag${n}` });
		text(s, body, { x: x + 0.13, y: y + 0.44, w: w - 0.26, h: h - 0.55, fontSize: 12, color: dark ? WHITE : INK, objectName: `Chain ${tag} text${n}` });
		if (i > 0) chevron(s, x - gap / 2 - 0.065, y + h / 2 - 0.13, `Chain arrow ${i + 1}${n}`);
	});

	text(s, "Across business functions: question, method, decision", { x: M, y: 3.86, w: CW, h: 0.34, fontFace: HEAD, fontSize: 17, bold: true, color: NAVY, objectName: "Functions heading" });
	const hdr = (t) => ({ text: t, options: { bold: true, color: WHITE, fill: { color: NAVY }, fontSize: 11.5 } });
	const rows = [
		["Demand & inventory", "How much will we sell next quarter, and how uncertain is that?", "Time-series models (ETS, ARIMA) with prediction intervals", "Set orders and safety stock from the interval, not a single point guess"],
		["Customer segmentation", "Which customers behave alike, and how do the groups differ?", "Cluster analysis; principal component analysis", "Tailor offers, channels and product design to each segment"],
		["Pricing & revenue", "How does demand respond to a price change?", "Price-elasticity regression; randomized price tests", "Change prices with an expected revenue effect and its uncertainty"],
		["Credit risk & fraud", "How likely is default or fraud for this application?", "Logistic-regression scorecards; anomaly detection", "Approve, price or flag — with error rates and fairness monitored"],
		["Churn & retention", "Who will leave, and does an offer change that?", "Survival or classification models plus uplift experiments", "Target customers the offer persuades, not just those most at risk"],
	];
	const thin = { type: "solid", color: HEX.lt2, pt: 1 };
	const body = rows.map((r, ri) => r.map((t, ci) => ({ text: t, options: { bold: ci === 0, color: ci === 0 ? NAVY : INK, fill: { color: ri % 2 ? MIST : WHITE } } })));
	s.addTable([["Function", "Key question", "Statistical method", "Decision supported"].map(hdr), ...body], {
		x: M, y: 4.26, w: CW, colW: [2.1, 3.75, 2.95, 3.333], rowH: [0.32, 0.42, 0.42, 0.42, 0.42, 0.42], fontSize: 11.5, valign: "middle", margin: [0.03, 0.1, 0.03, 0.1], border: [thin, thin, thin, thin], objectName: "Business functions table",
	});

	s.addNotes(
		"BUSINESS IMPLICATIONS (about 2 minutes)\n\n" +
			"Reveal the reasoning chain one step per click.\n" +
			"Case (Kohavi & Thomke, 2017, Harvard Business Review): a Bing employee proposed lengthening ad title lines by merging text from the line below the title. The idea was rated low priority and sat in the backlog for more than six months. When it was finally tested in an online controlled experiment, revenue rose about 12% with no significant harm to key user-experience metrics. The result was so large that it triggered a 'too good to be true' alert, so it was checked and replicated before shipping. The authors estimated the change was worth more than $100 million a year in U.S. revenue at the time. Note: these are the authors' published figures for Bing, not our estimates.\n\n" +
			"Why statistics mattered: expert judgment had ranked the idea low. Randomization isolated the causal effect of the change; guardrail metrics checked that revenue did not come at the cost of user experience; replication protected against a false positive.\n\n" +
			"Table: each business function pairs a question with an appropriate method. Two contrasts to highlight:\n" +
			"- Forecasting: planning from a prediction interval rather than a point forecast is what turns a forecast into an inventory policy (safety stock).\n" +
			"- Churn: a churn model predicts who will leave; it does not tell you who an offer will change. Uplift (treatment-effect) modeling with randomized offers estimates the causal effect, so budget goes where the offer actually works.\n\n" +
			"Sources: Kohavi, R., & Thomke, S. (2017). The surprising power of online experiments. Harvard Business Review, 95(5), 74-82. Kohavi, R., Tang, D., & Xu, Y. (2020). Trustworthy online controlled experiments. Cambridge University Press. Hyndman, R. J., & Athanasopoulos, G. (2021). Forecasting: Principles and practice (3rd ed.). OTexts."
	);
}

// ---------- slide 5: research ----------
function slideResearch() {
	const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Implications" });
	s.addText("05 · IMPLICATIONS IN SCIENTIFIC & ACADEMIC RESEARCH", { placeholder: "kicker" });
	s.addText("Rigor lives in the design, not just the analysis", { placeholder: "title" });

	const steps = [
		["Research question", "Testable hypothesis; primary outcome fixed in advance"],
		["Study design", "Randomized or observational? Plan for confounding"],
		["Data collection", "Sample size from a power analysis; valid measures"],
		["Statistical analysis", "Model matched to the data and its assumptions"],
		["Interpretation", "Effect sizes, confidence intervals, robustness checks"],
		["Conclusion", "Claims proportional to evidence; reproducible code and data"],
	];
	const sw = CW / 6, cy = 1.95;
	s.addShape(pres.ShapeType.line, { x: M + sw / 2, y: cy, w: CW - sw, h: 0, line: { color: SLATE, width: 1.25 }, objectName: "Workflow connector" });
	steps.forEach(([name, body], i) => {
		const cx = M + sw * (i + 0.5);
		const n = ` #${i + 1}`;
		s.addShape(pres.ShapeType.ellipse, { x: cx - 0.25, y: cy - 0.25, w: 0.5, h: 0.5, fill: { color: i === 5 ? AMBER : TEAL }, line: { color: WHITE, width: 2 }, objectName: `Step ${i + 1} marker${n}` });
		text(s, String(i + 1), { x: cx - 0.25, y: cy - 0.25, w: 0.5, h: 0.5, fontSize: 15, bold: true, color: i === 5 ? NAVY : WHITE, align: "center", valign: "middle", objectName: `Step ${i + 1} number${n}` });
		text(s, name, { x: cx - sw / 2 + 0.06, y: 2.3, w: sw - 0.12, h: 0.3, fontFace: HEAD, fontSize: 14, bold: true, color: NAVY, align: "center", objectName: `Step ${i + 1} name${n}` });
		text(s, body, { x: cx - sw / 2 + 0.1, y: 2.62, w: sw - 0.2, h: 0.75, fontSize: 12, align: "center", objectName: `Step ${i + 1} text${n}` });
	});

	// Forest plot redrawn from published RECOVERY results (NEJM 2021;384:693-704)
	const px = M, py = 3.6, pw = 7.95, ph = 3.28;
	box(s, { x: px, y: py, w: pw, h: ph, radius: 0.06, fill: { color: MIST }, objectName: "RECOVERY panel" });
	text(s, [
		{ text: "EVIDENCE EXAMPLE  ", options: { bold: true, color: TEAL, charSpacing: 1 } },
		{ text: "RECOVERY randomized trial: dexamethasone vs. usual care", options: { bold: true, color: NAVY } },
	], { x: px + 0.2, y: py + 0.14, w: pw - 0.4, h: 0.26, fontSize: 12.5, objectName: "RECOVERY title" });
	text(s, "28-day mortality, hospitalized COVID-19 patients · 6,425 randomized (2,104 vs. 4,321) · age-adjusted rate ratios", { x: px + 0.2, y: py + 0.42, w: pw - 0.4, h: 0.24, fontSize: 10.5, color: SLATE, objectName: "RECOVERY subtitle" });

	const col = { g: px + 0.2, d: px + 2.45, u: px + 3.2, p: px + 4.15, r: px + 6.4 };
	const cw = { g: 2.2, d: 0.72, u: 0.85, p: 2.15, r: 1.45 };
	const hy = py + 0.76;
	const hd = (t, x, w, align = "left") => text(s, t, { x, y: hy, w, h: 0.24, fontSize: 10.5, bold: true, color: SLATE, align, objectName: `Forest header: ${t}` });
	hd("Respiratory support", col.g, cw.g); hd("Dexa.", col.d, cw.d, "right"); hd("Usual care", col.u, cw.u, "right"); hd("Rate ratio (95% CI)", col.r, cw.r, "right");

	const lo = Math.log(0.4), hi = Math.log(1.8);
	const X = (v) => col.p + cw.p * ((Math.log(v) - lo) / (hi - lo));
	const rows = [
		["Invasive ventilation", "29.3%", "41.4%", 0.64, 0.51, 0.81],
		["Oxygen only", "23.3%", "26.2%", 0.82, 0.72, 0.94],
		["No respiratory support", "17.8%", "14.0%", 1.19, 0.92, 1.55],
		["All patients", "22.9%", "25.7%", 0.83, 0.75, 0.93],
	];
	const r0 = py + 1.08, rh = 0.38;
	s.addShape(pres.ShapeType.line, { x: X(1), y: r0 - 0.04, w: 0, h: rh * 4 + 0.06, line: { color: SLATE, width: 1, dashType: "dash" }, objectName: "Forest no-effect line" });
	rows.forEach(([g, d, u, rr, l, h], i) => {
		const y = r0 + i * rh, mid = y + rh / 2, all = i === 3;
		const f = { fontSize: 12, bold: all, color: all ? NAVY : INK, valign: "middle" };
		text(s, g, { x: col.g, y, w: cw.g, h: rh, ...f, objectName: `Forest row: ${g}` });
		text(s, d, { x: col.d, y, w: cw.d, h: rh, align: "right", ...f, objectName: `Forest ${g} dexamethasone` });
		text(s, u, { x: col.u, y, w: cw.u, h: rh, align: "right", ...f, objectName: `Forest ${g} usual care` });
		text(s, `${rr.toFixed(2)} (${l.toFixed(2)}–${h.toFixed(2)})`, { x: col.r, y, w: cw.r, h: rh, align: "right", ...f, objectName: `Forest ${g} estimate` });
		s.addShape(pres.ShapeType.line, { x: X(l), y: mid, w: X(h) - X(l), h: 0, line: { color: NAVY, width: 1.75 }, objectName: `Forest ${g} interval` });
		const m = all ? 0.24 : 0.16;
		s.addShape(all ? pres.ShapeType.diamond : pres.ShapeType.rect, { x: X(rr) - m / 2, y: mid - m / 2, w: m, h: m, fill: { color: all ? NAVY : TEAL }, line: { type: "none" }, objectName: `Forest ${g} point` });
	});
	const ay = r0 + rh * 4 + 0.08;
	s.addShape(pres.ShapeType.line, { x: col.p, y: ay, w: cw.p, h: 0, line: { color: SLATE, width: 1 }, objectName: "Forest axis" });
	[0.5, 0.75, 1, 1.5].forEach((v) => text(s, String(v), { x: X(v) - 0.25, y: ay + 0.03, w: 0.5, h: 0.2, fontSize: 10, color: SLATE, align: "center", objectName: `Forest tick ${v}` }));
	text(s, "← favors dexamethasone", { x: col.p - 0.6, y: ay + 0.24, w: X(1) - col.p + 0.55, h: 0.22, fontSize: 10, color: SLATE, align: "right", objectName: "Forest label left" });
	text(s, "favors usual care →", { x: X(1) + 0.08, y: ay + 0.24, w: 1.6, h: 0.22, fontSize: 10, color: SLATE, objectName: "Forest label right" });
	text(s, "Log scale. Redrawn from RECOVERY, NEJM 2021.", { x: px + 0.2, y: ay + 0.26, w: 3.45, h: 0.22, fontSize: 9, italic: true, color: SLATE, objectName: "Forest source" });

	const qx = 8.8, qw = RIGHT - qx;
	box(s, { x: qx, y: py, w: qw, h: ph, radius: 0.06, fill: { color: NAVY }, objectName: "Reproducibility panel" });
	text(s, "REPRODUCIBILITY CHECK", { x: qx + 0.25, y: py + 0.18, w: qw - 0.5, h: 0.24, fontSize: 10, bold: true, color: AMBER, charSpacing: 1, objectName: "Reproducibility tag" });
	text(s, [{ text: "97%", options: { color: WHITE } }, { text: " → ", options: { color: ICE, fontFace: "+mn-lt" } }, { text: "36%", options: { color: AMBER } }], { x: qx + 0.25, y: py + 0.45, w: qw - 0.5, h: 0.65, fontFace: HEAD, fontSize: 36, bold: true, valign: "middle", objectName: "Reproducibility statistic" });
	text(s, "of 100 published psychology studies reported significant results; only 36% of their high-powered replications did. Replication effects were about half as large.", { x: qx + 0.25, y: py + 1.15, w: qw - 0.5, h: 0.95, fontSize: 12, color: WHITE, objectName: "Reproducibility text" });
	text(s, "Open Science Collaboration (2015), Science", { x: qx + 0.25, y: py + 2.12, w: qw - 0.5, h: 0.22, fontSize: 10, color: ICE, objectName: "Reproducibility source" });
	text(s, "Low power, flexible analysis and selective publication inflate findings; pre-registration and open data counter them.", { x: qx + 0.25, y: py + 2.4, w: qw - 0.5, h: 0.75, fontSize: 11.5, italic: true, color: ICE, objectName: "Reproducibility lesson" });

	s.addNotes(
		"RESEARCH IMPLICATIONS (about 2 minutes)\n\n" +
			"Reveal the six workflow steps on click. Statistical thinking enters at every step, not only at 'analysis':\n" +
			"- Question: a falsifiable hypothesis and a pre-specified primary outcome prevent outcome-switching.\n" +
			"- Design: randomization balances measured and unmeasured confounders; observational designs need explicit adjustment and causal assumptions.\n" +
			"- Data collection: a power analysis sets the sample size. Underpowered studies miss real effects and exaggerate the ones they find (Button et al., 2013).\n" +
			"- Analysis: the model must fit the data type and assumptions (independence, distribution, missing-data mechanism).\n" +
			"- Interpretation: report effect sizes with confidence intervals, and run robustness and sensitivity analyses.\n" +
			"- Conclusion: claims should match the strength of evidence; share code and data so others can reproduce them.\n\n" +
			"Evidence example: RECOVERY trial (RECOVERY Collaborative Group, NEJM 2021). 2,104 patients were randomized to dexamethasone and 4,321 to usual care. 28-day mortality: 22.9% vs 25.7%, age-adjusted rate ratio 0.83 (95% CI 0.75 to 0.93; P<0.001). Ventilated patients: 29.3% vs 41.4%, RR 0.64 (0.51 to 0.81). Oxygen only: 23.3% vs 26.2%, RR 0.82 (0.72 to 0.94). No respiratory support: 17.8% vs 14.0%, RR 1.19 (0.92 to 1.55), so no benefit was shown in that group.\n" +
			"What statistics contributed: randomization made the comparison causal; confidence intervals show both size and precision; the subgroup pattern informed who should receive the drug. Subgroup results should be read with caution, since many subgroups increase the chance of spurious differences.\n\n" +
			"Reproducibility: the Open Science Collaboration (2015) replicated 100 studies from three psychology journals. 97% of originals had p < .05; 36% of replications did, and mean replication effect sizes were about half the original. This is a warning about weak designs and selective reporting, not a reason to distrust statistics.\n\n" +
			"Sources: RECOVERY Collaborative Group (2021), NEJM 384(8), 693-704, https://doi.org/10.1056/NEJMoa2021436. Open Science Collaboration (2015), Science 349(6251), aac4716, https://doi.org/10.1126/science.aac4716. Button et al. (2013), Nature Reviews Neuroscience 14, 365-376."
	);
}

// ---------- slide 6: case study (illustrative data) ----------
function slideCase() {
	pres.addSection({ title: "Case study" });
	const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Case study" });
	s.addText("06 · PRACTICAL CASE STUDY", { placeholder: "kicker" });
	s.addText("Does a redesigned product page lift conversion?", { placeholder: "title" });
	box(s, { x: 8.73, y: 0.38, w: 4.0, h: 0.36, radius: 0.18, fill: { color: AMBER }, objectName: "Illustrative data badge" });
	text(s, [{ text: "ILLUSTRATIVE DATA  ", options: { bold: true } }, { text: "hypothetical, not real company results" }], { x: 8.73, y: 0.38, w: 4.0, h: 0.36, fontSize: 11, color: NAVY, align: "center", valign: "middle", objectName: "Illustrative data badge text" });

	const cw = 3.85, x1 = M, x2 = 4.75, x3 = 8.9, w3 = RIGHT - x3, top = 1.66;
	const head = (n, t, x, w, name) => text(s, [{ text: `${n}  `, options: { color: TEAL } }, { text: t, options: { color: NAVY } }], { x, y: top, w, h: 0.34, fontFace: HEAD, fontSize: 16, bold: true, objectName: name });

	// Column 1: design
	head("1", "Design", x1, cw, "Design heading");
	box(s, { x: x1, y: 2.12, w: cw, h: 0.42, radius: 0.06, fill: { color: MIST }, objectName: "Visitors box" });
	text(s, "40,000 product-page visitors", { x: x1, y: 2.12, w: cw, h: 0.42, fontSize: 12.5, bold: true, color: NAVY, align: "center", valign: "middle", objectName: "Visitors text" });
	s.addShape(pres.ShapeType.line, { x: x1 + cw / 2, y: 2.54, w: 0, h: 0.2, line: { color: SLATE, width: 1.5, endArrowType: "triangle" }, objectName: "Arrow to randomization" });
	box(s, { x: x1 + 0.6, y: 2.76, w: cw - 1.2, h: 0.36, radius: 0.18, fill: { color: NAVY }, objectName: "Randomization pill" });
	text(s, "Random assignment, 50 / 50", { x: x1 + 0.6, y: 2.76, w: cw - 1.2, h: 0.36, fontSize: 11.5, bold: true, color: WHITE, align: "center", valign: "middle", objectName: "Randomization text" });
	const aw = (cw - 0.25) / 2;
	s.addShape(pres.ShapeType.line, { x: x1 + aw / 2, y: 3.12, w: cw / 2 - aw / 2, h: 0.22, flipH: true, line: { color: SLATE, width: 1.5, endArrowType: "triangle" }, objectName: "Arrow to control" });
	s.addShape(pres.ShapeType.line, { x: x1 + cw / 2, y: 3.12, w: cw / 2 - aw / 2, h: 0.22, line: { color: SLATE, width: 1.5, endArrowType: "triangle" }, objectName: "Arrow to treatment" });
	[["A · Control", "current page", STEEL, x1], ["B · Treatment", "redesigned page", TEAL, x1 + aw + 0.25]].forEach(([t, d, c, x]) => {
		box(s, { x, y: 3.36, w: aw, h: 0.78, radius: 0.06, fill: { color: c }, objectName: `${t} box` });
		text(s, [{ text: t, options: { bold: true, breakLine: true } }, { text: d, options: { fontSize: 11, breakLine: true } }, { text: "n = 20,000", options: { fontSize: 11 } }], { x: x + 0.1, y: 3.36, w: aw - 0.2, h: 0.78, fontSize: 12.5, color: WHITE, align: "center", valign: "middle", objectName: `${t} text` });
	});
	const lbl = (t) => ({ text: t, options: { bold: true, color: NAVY } });
	text(s, [
		lbl("Hypotheses  "), { text: "H" }, { text: "0", options: { subscript: true } }, { text: ": p" }, { text: "B", options: { subscript: true } }, { text: " = p" }, { text: "A", options: { subscript: true } },
		{ text: "    H" }, { text: "1", options: { subscript: true } }, { text: ": p" }, { text: "B", options: { subscript: true } }, { text: " ≠ p" }, { text: "A", options: { subscript: true } }, { text: "", options: { breakLine: true } },
		lbl("Test  "), { text: "two-sided, α = 0.05", options: { breakLine: true } },
		lbl("Primary metric  "), { text: "conversion rate = orders ÷ visitors", options: { breakLine: true } },
		lbl("Power  "), { text: "80% to detect +0.6 pp from a 4.2% baseline needs ≈ 18,740 visitors per arm → 20,000 planned", options: { breakLine: true } },
		lbl("Discipline  "), { text: "fixed test length set in advance; no stopping on interim peeks" },
	], { x: x1, y: 4.36, w: cw, h: 2.5, fontSize: 12, paraSpaceAfter: 6, objectName: "Design details" });

	// Column 2: results chart (native, editable)
	head("2", "Results", x2, cw, "Results heading");
	s.addChart(pres.ChartType.bar, [{ name: "Conversion rate (%)", labels: ["A · Current page", "B · Redesign"], values: [4.2, 4.8] }], {
		x: x2, y: 2.05, w: cw, h: 3.45, barDir: "col", barGapWidthPct: 70,
		chartColors: [HEX.accent3, HEX.accent1],
		showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: '0.00"%"', dataLabelFontSize: 13, dataLabelFontBold: true, dataLabelColor: HEX.dk2, dataLabelFontFace: "+mn-lt",
		valAxisMinVal: 0, valAxisMaxVal: 6, valAxisMajorUnit: 1, valAxisLabelFormatCode: '0"%"', valAxisLabelFontSize: 11, valAxisLabelColor: HEX.accent5, valAxisLabelFontFace: "+mn-lt",
		showValAxisTitle: true, valAxisTitle: "Conversion rate (%)", valAxisTitleFontSize: 11, valAxisTitleColor: HEX.accent5, valAxisTitleFontFace: "+mn-lt",
		catAxisLabelFontSize: 11.5, catAxisLabelColor: HEX.dk1, catAxisLabelFontFace: "+mn-lt", catAxisLineShow: true,
		valGridLine: { color: "E2E7ED", size: 0.75 }, catGridLine: { style: "none" }, showLegend: false,
		altText: "Column chart of illustrative conversion rates: A 4.20 percent, B 4.80 percent; axis starts at zero.", objectName: "Conversion rate chart #1",
	});
	text(s, [
		{ text: "A: 840 orders / 20,000 visitors = 4.20%", options: { breakLine: true } },
		{ text: "B: 960 orders / 20,000 visitors = 4.80%" },
	], { x: x2 + 0.1, y: 5.6, w: cw - 0.1, h: 0.5, fontSize: 12, color: INK, objectName: "Results counts #1" });
	text(s, [{ text: "Axis starts at zero. Separate 95% CIs:", options: { breakLine: true } }, { text: "A 3.92–4.48%  ·  B 4.50–5.10%" }], { x: x2 + 0.1, y: 6.2, w: cw - 0.1, h: 0.45, fontSize: 10.5, color: SLATE, objectName: "Results note #1" });

	// Column 3: inference and decision
	head("3", "Inference & decision", x3, w3, "Inference heading");
	text(s, [{ text: "Method  ", options: { bold: true, color: NAVY } }, { text: "two-proportion z-test (large samples, independent visitors, random assignment)" }], { x: x3, y: 2.08, w: w3, h: 0.5, fontSize: 12, objectName: "Method line #2" });
	const tiles = [["+0.60 pp", "difference (B − A)"], ["+14.3%", "relative lift"], ["p = 0.004", "z = 2.89, two-sided"]];
	const tw = (w3 - 0.2) / 3;
	tiles.forEach(([v, l], i) => {
		const x = x3 + i * (tw + 0.1);
		box(s, { x, y: 2.68, w: tw, h: 0.82, radius: 0.06, fill: { color: MIST }, objectName: `Stat tile ${i + 1} #2` });
		text(s, v, { x, y: 2.74, w: tw, h: 0.4, fontFace: HEAD, fontSize: 17, bold: true, color: NAVY, align: "center", valign: "middle", objectName: `Stat tile ${i + 1} value #2` });
		text(s, l, { x: x + 0.05, y: 3.14, w: tw - 0.1, h: 0.3, fontSize: 10, color: SLATE, align: "center", objectName: `Stat tile ${i + 1} label #2` });
	});
	text(s, "95% confidence interval for the difference", { x: x3, y: 3.66, w: w3, h: 0.26, fontSize: 11.5, bold: true, color: NAVY, objectName: "CI heading #2" });
	const X0 = x3 + 0.15, XW = w3 - 0.3, cx = (v) => X0 + XW * ((v + 0.5) / 2.0), ly = 4.42;
	s.addShape(pres.ShapeType.line, { x: X0, y: ly + 0.3, w: XW, h: 0, line: { color: SLATE, width: 1 }, objectName: "CI axis #2" });
	[-0.5, 0, 0.5, 1.0, 1.5].forEach((v) => text(s, (v > 0 ? "+" : "") + v.toFixed(1), { x: cx(v) - 0.25, y: ly + 0.34, w: 0.5, h: 0.2, fontSize: 10, color: SLATE, align: "center", objectName: `CI tick ${v} #2` }));
	text(s, "pp", { x: X0 + XW - 0.05, y: ly + 0.1, w: 0.3, h: 0.18, fontSize: 9.5, color: SLATE, objectName: "CI unit #2" });
	s.addShape(pres.ShapeType.line, { x: cx(0), y: ly - 0.32, w: 0, h: 0.62, line: { color: CORAL, width: 1.25, dashType: "dash" }, objectName: "CI zero line #2" });
	text(s, "no effect", { x: cx(0) - 0.45, y: ly - 0.5, w: 0.9, h: 0.18, fontSize: 9.5, color: CORAL, align: "center", objectName: "CI zero label #2" });
	s.addShape(pres.ShapeType.line, { x: cx(0.19), y: ly, w: cx(1.01) - cx(0.19), h: 0, line: { color: TEAL, width: 3 }, objectName: "CI whisker #2" });
	[0.19, 1.01].forEach((v) => s.addShape(pres.ShapeType.line, { x: cx(v), y: ly - 0.1, w: 0, h: 0.2, line: { color: TEAL, width: 2 }, objectName: `CI cap ${v} #2` }));
	s.addShape(pres.ShapeType.ellipse, { x: cx(0.6) - 0.09, y: ly - 0.09, w: 0.18, h: 0.18, fill: { color: NAVY }, line: { type: "none" }, objectName: "CI point #2" });
	text(s, "+0.19", { x: cx(0.19) - 0.3, y: ly - 0.32, w: 0.6, h: 0.18, fontSize: 10, color: TEAL, bold: true, align: "center", objectName: "CI lower label #2" });
	text(s, "+1.01", { x: cx(1.01) - 0.3, y: ly - 0.32, w: 0.6, h: 0.18, fontSize: 10, color: TEAL, bold: true, align: "center", objectName: "CI upper label #2" });

	text(s, "If the redesign had no effect, a gap this large would arise in only about 0.4% of repeated experiments. The true lift is plausibly anywhere from +0.19 to +1.01 pp: likely real, but its size is uncertain.", { x: x3, y: 5.04, w: w3, h: 1.0, fontSize: 12, objectName: "Interpretation #3" });
	box(s, { x: x3, y: 6.08, w: w3, h: 0.8, radius: 0.06, fill: { color: NAVY }, objectName: "Decision box #3" });
	text(s, [{ text: "DECISION  ", options: { bold: true, color: AMBER, charSpacing: 1 } }, { text: "Roll out B if guardrail metrics (returns, page speed) show no harm; keep monitoring for novelty effects.", options: { color: WHITE } }], { x: x3 + 0.15, y: 6.08, w: w3 - 0.3, h: 0.8, fontSize: 11.5, valign: "middle", objectName: "Decision text #3" });

	s.addNotes(
		"CASE STUDY (about 2 minutes). ALL NUMBERS ON THIS SLIDE ARE HYPOTHETICAL, created to illustrate the method. They are not results from any real company.\n\n" +
			"Design: 40,000 visitors are randomly assigned 50/50. Random assignment means the two groups differ only by chance and by the page they see, so a difference in conversion can be attributed to the redesign. Hypotheses: H0: pB = pA; H1: pB != pA, two-sided, alpha = 0.05. Primary metric fixed in advance: conversion rate = orders / visitors.\n" +
			"Power analysis (normal approximation): to detect 4.2% -> 4.8% with 80% power at alpha 0.05 two-sided, n per arm = [1.96*sqrt(2*0.045*0.955) + 0.8416*sqrt(0.042*0.958 + 0.048*0.952)]^2 / 0.006^2 = about 18,738. We plan 20,000 per arm. The test runs for a fixed period; stopping early when p first dips below 0.05 inflates the false-positive rate.\n\n" +
			"Results (click 1): A = 840/20,000 = 4.20%; B = 960/20,000 = 4.80%.\n\n" +
			"Inference (click 2): two-proportion z-test.\n" +
			"Pooled p = 1,800/40,000 = 0.045. SE under H0 = sqrt(0.045*0.955*(1/20,000 + 1/20,000)) = 0.002073.\n" +
			"z = 0.006 / 0.002073 = 2.89; two-sided p = 0.0038, about 0.004.\n" +
			"95% CI for the difference uses the unpooled SE = sqrt(0.042*0.958/20,000 + 0.048*0.952/20,000) = 0.002073; 0.006 +/- 1.96*0.002073 = +0.19 to +1.01 percentage points.\n" +
			"Relative lift = 0.60/4.20 = 14.3%.\n\n" +
			"Interpretation (click 3): the p-value is the probability of a difference at least this large if there were truly no effect; it is not the probability that the redesign works. The confidence interval matters more for the business: the effect could be as small as 0.19 pp or as large as 1.01 pp. Assumptions: independent visitors (one count per visitor), stable traffic mix, no interference between groups.\n" +
			"Decision: launch B, provided guardrail metrics such as return rate and page load time show no harm. Monitor after launch, because novelty effects can fade. If the minimum worthwhile lift were, say, 0.5 pp, the interval would not settle that question and a larger test would be justified.\n\n" +
			"Method reference: Kohavi, Tang & Xu (2020), Trustworthy Online Controlled Experiments; Montgomery (2017), Design and Analysis of Experiments."
	);
}

// ---------- slide 7: challenges ----------
function slideChallenges() {
	pres.addSection({ title: "Risks and ethics" });
	const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Risks and ethics" });
	s.addText("07 · CHALLENGES, ETHICS & FUTURE IMPLICATIONS", { placeholder: "kicker" });
	s.addText("Sophistication without discipline misleads", { placeholder: "title" });

	const thin = { type: "solid", color: HEX.lt2, pt: 1 };
	const hdr = (t) => ({ text: t, options: { bold: true, color: WHITE, fill: { color: NAVY } } });
	const rows = [
		["Data quality & sampling bias", "Sample does not represent the population of interest", "Audit data provenance; reweight or redesign the sample"],
		["Violated model assumptions", "Biased estimates and wrong standard errors", "Residual diagnostics; robust or alternative models"],
		["Overfitting", "Model memorizes noise and fails on new data", "Hold-out data and cross-validation; simpler models"],
		["Multiple testing & p-hacking", "Testing many outcomes guarantees some false positives", "Pre-registration; Holm or false-discovery-rate correction"],
		["Confounding", "Spurious causal claims from observational data", "Randomize, or use explicit causal designs and diagrams"],
		["Misreading significance", "“Significant” read as “large” or “important”", "Report effect sizes with confidence intervals"],
		["Privacy & fairness", "Models harm individuals or disadvantage groups", "Consent, data minimization, bias audits across groups"],
		["Missing domain expertise", "Valid statistics answer the wrong question", "Involve domain experts; report methods transparently"],
	];
	const body = rows.map((r, ri) => r.map((t, ci) => ({ text: t, options: { bold: ci === 0, color: ci === 0 ? NAVY : INK, fill: { color: ri % 2 ? MIST : WHITE } } })));
	s.addTable([["Risk", "What goes wrong", "Safeguard"].map(hdr), ...body], {
		x: M, y: 1.68, w: 7.95, colW: [2.2, 2.7, 3.05], rowH: [0.34, ...rows.map(() => 0.6)], fontSize: 11.5, valign: "middle", margin: [0.03, 0.1, 0.03, 0.1], border: [thin, thin, thin, thin], objectName: "Risk and safeguard table",
	});

	const px = 8.8, pw = RIGHT - px, py = 1.68, ph = 5.17;
	box(s, { x: px, y: py, w: pw, h: ph, radius: 0.06, fill: { color: NAVY }, objectName: "Future panel" });
	text(s, "MACHINE LEARNING & AI", { x: px + 0.25, y: py + 0.2, w: pw - 0.5, h: 0.24, fontSize: 10, bold: true, color: AMBER, charSpacing: 1, objectName: "ML tag" });
	text(s, "ML excels at prediction from large, complex data and increasingly complements statistical modeling. But accurate prediction does not show what would happen under an intervention: prediction is not causation (Shmueli, 2010).", { x: px + 0.25, y: py + 0.5, w: pw - 0.5, h: 1.25, fontSize: 12, color: WHITE, objectName: "ML text" });
	text(s, "Example: a widely used U.S. health algorithm predicted cost as a proxy for need, and so understated the needs of Black patients (Obermeyer et al., 2019).", { x: px + 0.25, y: py + 1.8, w: pw - 0.5, h: 0.75, fontSize: 11, italic: true, color: ICE, objectName: "Fairness example" });
	text(s, "RESPONSIBLE PRACTICE", { x: px + 0.25, y: py + 2.68, w: pw - 0.5, h: 0.24, fontSize: 10, bold: true, color: AMBER, charSpacing: 1, objectName: "Framework tag" });
	const steps = [["Plan", "pre-specify question, outcome, analysis"], ["Check", "data quality and model assumptions"], ["Estimate", "effect sizes with their uncertainty"], ["Stress-test", "robustness and hold-out data"], ["Report", "transparently, limitations included"]];
	steps.forEach(([k, v], i) => {
		const y = py + 3.0 + i * 0.42;
		s.addShape(pres.ShapeType.ellipse, { x: px + 0.25, y: y + 0.04, w: 0.3, h: 0.3, fill: { color: TEAL }, line: { type: "none" }, objectName: `Framework ${k} marker` });
		text(s, String(i + 1), { x: px + 0.25, y: y + 0.04, w: 0.3, h: 0.3, fontSize: 11, bold: true, color: WHITE, align: "center", valign: "middle", objectName: `Framework ${k} number` });
		text(s, [{ text: `${k}  `, options: { bold: true, color: WHITE } }, { text: v, options: { color: ICE } }], { x: px + 0.67, y, w: pw - 0.85, h: 0.38, fontSize: 11.5, valign: "middle", objectName: `Framework ${k} text` });
	});

	s.addNotes(
		"CHALLENGES AND ETHICS (about 2 minutes)\n\n" +
			"Advanced methods amplify whatever goes into them. The table pairs each common failure with a practical safeguard.\n" +
			"- Sampling bias: a large biased sample is still biased; size does not fix representativeness.\n" +
			"- Assumptions: check residuals, independence, and missing-data mechanisms; use robust methods when assumptions fail.\n" +
			"- Overfitting: evaluate on data the model has not seen (hold-out sets, cross-validation) (Hastie et al., 2009).\n" +
			"- Multiple testing and p-hacking: with 20 independent tests at alpha 0.05, about one 'significant' result is expected by chance. Flexible analysis choices can push false-positive rates far above 5% (Simmons, Nelson & Simonsohn, 2011). Pre-register and correct for multiplicity.\n" +
			"- Confounding: causal claims need randomization or explicit causal assumptions (Hernan & Robins, 2020).\n" +
			"- Significance: the ASA statement (Wasserstein & Lazar, 2016) stresses that p-values do not measure effect size or importance; Amrhein, Greenland & McShane (2019) argue against dichotomizing results as significant or not.\n" +
			"- Privacy and fairness: Obermeyer et al. (2019, Science) showed that an algorithm using health-care cost as a proxy for health need assigned Black patients the same risk score as White patients who were less sick, because less money had been spent on their care. The statistical target, not just the model, created the bias.\n" +
			"- Domain expertise: statistics answers the question you asked; experts make sure it is the right question.\n\n" +
			"ML and AI: machine learning is increasingly used alongside classical statistics, especially for prediction with many variables. Statistical thinking remains essential for uncertainty, study design and causal questions.\n\n" +
			"Framework: Plan, Check, Estimate, Stress-test, Report."
	);
}

// ---------- slide 8: conclusion ----------
function slideConclusion() {
	pres.addSection({ title: "Conclusion" });
	const s = pres.addSlide({ masterName: "CLOSING_DARK", sectionTitle: "Conclusion" });
	s.addText("08 · CONCLUSION & KEY TAKEAWAYS", { placeholder: "kicker" });
	s.addText("Reliable conclusions are where data creates value", { placeholder: "title" });

	const items = [
		["Advanced statistics turns raw data into structured evidence.", "Description, prediction and inference answer different questions."],
		["Businesses decide better by quantifying uncertainty and testing alternatives.", "Experiments and intervals replace opinion with measured risk."],
		["Researchers strengthen conclusions through design and rigorous inference.", "Power, randomization and robustness checks matter as much as models."],
		["Responsible interpretation matters as much as technical sophistication.", "Effect sizes, transparency and fairness keep results trustworthy."],
	];
	items.forEach(([h, d], i) => {
		const y = 1.78 + i * 0.93;
		text(s, `0${i + 1}`, { x: M, y, w: 0.75, h: 0.55, fontFace: HEAD, fontSize: 28, bold: true, color: AMBER, objectName: `Takeaway ${i + 1} number` });
		text(s, [{ text: h, options: { bold: true, color: WHITE, fontSize: 15, breakLine: true } }, { text: d, options: { color: ICE, fontSize: 12.5 } }], { x: M + 0.85, y: y + 0.02, w: 5.9, h: 0.85, objectName: `Takeaway ${i + 1} text` });
	});

	const qx = 7.75, qw = RIGHT - qx;
	text(s, "“", { x: qx, y: 1.6, w: 0.8, h: 0.9, fontFace: HEAD, fontSize: 72, bold: true, color: AMBER, objectName: "Quote mark" });
	text(s, "The value of data lies not merely in collecting it, but in drawing reliable conclusions from it.", { x: qx, y: 2.4, w: qw, h: 1.65, fontFace: HEAD, fontSize: 23, italic: true, color: WHITE, objectName: "Closing statement" });
	text(s, "Thank you · Questions and discussion", { x: qx, y: 4.2, w: qw, h: 0.35, fontSize: 15, bold: true, color: AMBER, objectName: "Thank you" });

	text(s, "KEY REFERENCES", { x: M, y: 5.62, w: 4, h: 0.24, fontSize: 10, bold: true, color: AMBER, charSpacing: 2, objectName: "References heading" });
	const refA = [
		"Brynjolfsson, Hitt & Kim (2011). Strength in numbers. SSRN 1819486.",
		"Kohavi & Thomke (2017). The surprising power of online experiments. HBR, 95(5).",
		"RECOVERY Collaborative Group (2021). NEJM, 384(8), 693–704.",
	];
	const refB = [
		"Open Science Collaboration (2015). Science, 349(6251), aac4716.",
		"Wasserstein & Lazar (2016). The ASA statement on p-values. Am. Stat., 70(2).",
		"Shmueli (2010). To explain or to predict? Statistical Science, 25(3).",
	];
	const refs = (arr) => arr.map((t, i) => ({ text: t, options: { breakLine: i < arr.length - 1 } }));
	text(s, refs(refA), { x: M, y: 5.9, w: 5.95, h: 0.8, fontSize: 10.5, color: ICE, paraSpaceAfter: 2, objectName: "Key references column 1" });
	text(s, refs(refB), { x: 6.75, y: 5.9, w: 5.98, h: 0.8, fontSize: 10.5, color: ICE, paraSpaceAfter: 2, objectName: "Key references column 2" });
	text(s, "Full reference list with DOIs and visual sources: Appendix A (supplementary slide).", { x: M, y: 6.72, w: CW, h: 0.24, fontSize: 10, italic: true, color: ICE, objectName: "Appendix pointer" });

	s.addNotes(
		"CONCLUSION (about 1 minute)\n\n" +
			"Four takeaways:\n" +
			"1. Advanced statistics turns raw data into structured evidence: description, prediction and inference answer different questions.\n" +
			"2. Businesses decide better when they quantify uncertainty and test alternatives, as the Bing experiment showed.\n" +
			"3. Researchers strengthen conclusions through design (power, randomization) and rigorous inference (effect sizes, intervals, robustness), as RECOVERY showed and the replication project warned.\n" +
			"4. Responsible interpretation matters as much as technical sophistication: significance is not importance, prediction is not causation, and fairness and transparency are part of good practice.\n\n" +
			"Closing line: 'The value of data lies not merely in collecting it, but in drawing reliable conclusions from it.'\n\n" +
			"Invite questions. Full references are on the appendix slide after this one."
	);
}

// ---------- appendix: references ----------
function slideAppendix() {
	pres.addSection({ title: "Appendix" });
	const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Appendix" });
	s.addText("APPENDIX A · SUPPLEMENTARY, OUTSIDE THE EIGHT-SLIDE MAIN DECK", { placeholder: "kicker" });
	s.addText("References and visual sources", { placeholder: "title" });
	const A = [
		"Amrhein, V., Greenland, S., & McShane, B. (2019). Scientists rise up against statistical significance. Nature, 567, 305–307. doi:10.1038/d41586-019-00857-9",
		"Brynjolfsson, E., Hitt, L. M., & Kim, H. H. (2011). Strength in numbers: How does data-driven decisionmaking affect firm performance? SSRN. doi:10.2139/ssrn.1819486",
		"Button, K. S., et al. (2013). Power failure: Why small sample size undermines the reliability of neuroscience. Nature Reviews Neuroscience, 14(5), 365–376. doi:10.1038/nrn3475",
		"Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013). Bayesian data analysis (3rd ed.). CRC Press.",
		"Hastie, T., Tibshirani, R., & Friedman, J. (2009). The elements of statistical learning (2nd ed.). Springer.",
		"Hernán, M. A., & Robins, J. M. (2020). Causal inference: What if. Chapman & Hall/CRC.",
		"Hyndman, R. J., & Athanasopoulos, G. (2021). Forecasting: Principles and practice (3rd ed.). OTexts. otexts.com/fpp3",
		"Kohavi, R., Tang, D., & Xu, Y. (2020). Trustworthy online controlled experiments: A practical guide to A/B testing. Cambridge University Press. doi:10.1017/9781108653985",
	];
	const B = [
		"Kohavi, R., & Thomke, S. (2017). The surprising power of online experiments. Harvard Business Review, 95(5), 74–82.",
		"Montgomery, D. C. (2017). Design and analysis of experiments (9th ed.). Wiley.",
		"Obermeyer, Z., Powers, B., Vogeli, C., & Mullainathan, S. (2019). Dissecting racial bias in an algorithm used to manage the health of populations. Science, 366(6464), 447–453. doi:10.1126/science.aax2342",
		"Open Science Collaboration. (2015). Estimating the reproducibility of psychological science. Science, 349(6251), aac4716. doi:10.1126/science.aac4716",
		"RECOVERY Collaborative Group. (2021). Dexamethasone in hospitalized patients with Covid-19. NEJM, 384(8), 693–704. doi:10.1056/NEJMoa2021436",
		"Shmueli, G. (2010). To explain or to predict? Statistical Science, 25(3), 289–310. doi:10.1214/10-STS330",
		"Simmons, J. P., Nelson, L. D., & Simonsohn, U. (2011). False-positive psychology. Psychological Science, 22(11), 1359–1366. doi:10.1177/0956797611417632",
		"Wasserstein, R. L., & Lazar, N. A. (2016). The ASA statement on p-values: Context, process, and purpose. The American Statistician, 70(2), 129–133. doi:10.1080/00031305.2016.1154108",
	];
	const list = (arr) => arr.map((t, i) => ({ text: t, options: { breakLine: i < arr.length - 1 } }));
	const cw = (CW - 0.4) / 2;
	text(s, list(A), { x: M, y: 1.66, w: cw, h: 4.45, fontSize: 11.5, paraSpaceAfter: 6, objectName: "References column 1" });
	text(s, list(B), { x: M + cw + 0.4, y: 1.66, w: cw, h: 4.45, fontSize: 11.5, paraSpaceAfter: 6, objectName: "References column 2" });
	box(s, { x: M, y: 6.22, w: CW, h: 0.66, radius: 0.06, fill: { color: MIST }, objectName: "Visual sources box" });
	text(s, [
		{ text: "Visual sources  ", options: { bold: true, color: NAVY } },
		{ text: "All charts and diagrams are original to this presentation. Title visual and method diagrams use simulated data (illustrative). Slide 5 forest plot is redrawn from published RECOVERY values. Slide 6 data are hypothetical. No third-party images are used." },
	], { x: M + 0.2, y: 6.22, w: CW - 0.4, h: 0.66, fontSize: 10.5, valign: "middle", objectName: "Visual sources text" });
	s.addNotes("Supplementary reference slide. It sits outside the eight-slide main presentation; hide it (right-click > Hide Slide) if your course requires exactly eight slides in slideshow mode.");
}

(async () => {
	slideTitle();
	await slideWhy();
	slideMethods();
	slideBusiness();
	slideResearch();
	slideCase();
	slideChallenges();
	slideConclusion();
	slideAppendix();
	await pres.writeFile({ fileName: OUT });
	await applyTheme(OUT, THEME);
	console.log("wrote", OUT);
})();
