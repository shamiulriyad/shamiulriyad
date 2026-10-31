# Text of the assignment. Inline **bold** and *italic* are supported.
# Figures and data are rounded values compiled from the sources listed under each figure/table.

ABSTRACT = [
    "Gross Domestic Product (GDP) is the most widely quoted number in economics. Governments set growth targets "
    "around it, the media report it every quarter, and international bodies use it to rank countries. Yet GDP was "
    "designed to measure the market value of production, not the quality of people's lives. This assignment asks "
    "whether GDP growth is an adequate measure of economic well-being.",
    "The study uses secondary data from the World Bank, UNDP, the World Inequality Lab, the World Happiness Report, "
    "the Bangladesh Bureau of Statistics (BBS) and peer-reviewed literature. It first explains how GDP is measured "
    "and what economists mean by well-being. It then sets out the case for GDP, followed by its main limitations: "
    "it ignores distribution, unpaid and informal work, environmental damage, defensive spending, leisure and "
    "subjective life satisfaction. Five worked demonstrations and seventeen charts show these points with numbers. "
    "Alternative measures, including the Human Development Index (HDI) and the Genuine Progress Indicator (GPI), "
    "are compared, and Bangladesh is used as a case study.",
    "The evidence shows that GDP growth is closely linked to falling poverty and better health in low-income "
    "countries, so it remains a necessary indicator. However, the link weakens at higher income levels, and GDP "
    "can rise while inequality, environmental loss and stress also rise. The study concludes that GDP growth is "
    "**necessary but not sufficient**: it is a good measure of economic activity but an inadequate measure of "
    "economic well-being on its own. A dashboard approach that reports GDP alongside distribution, human "
    "development and sustainability indicators is recommended, especially for Bangladesh.",
]

ABBREVIATIONS = [
    ("BBS", "Bangladesh Bureau of Statistics"),
    ("CO₂", "Carbon dioxide"),
    ("GDP", "Gross Domestic Product"),
    ("GNH", "Gross National Happiness (Bhutan)"),
    ("GNI", "Gross National Income"),
    ("GPI", "Genuine Progress Indicator"),
    ("HDI", "Human Development Index"),
    ("HIES", "Household Income and Expenditure Survey"),
    ("ILO", "International Labour Organization"),
    ("IHDI", "Inequality-adjusted Human Development Index"),
    ("LFS", "Labour Force Survey"),
    ("MPI", "Multidimensional Poverty Index"),
    ("OECD", "Organisation for Economic Co-operation and Development"),
    ("PPP", "Purchasing Power Parity"),
    ("SDG", "Sustainable Development Goals"),
    ("SEEA", "System of Environmental-Economic Accounting"),
    ("SNA", "System of National Accounts"),
    ("UNDP", "United Nations Development Programme"),
    ("WHR", "World Happiness Report"),
    ("WIR", "World Inequality Report"),
]

T_DATA_SOURCES = dict(
    title="Main data sources used in the study",
    headers=["Source", "Data used", "Period"],
    rows=[
        ["World Bank, World Development Indicators", "GDP per capita, life expectancy, Gini index, health spending", "2010-2023"],
        ["UNDP Human Development Report 2023/24", "HDI values and components", "1990-2022"],
        ["Bangladesh Bureau of Statistics (BBS)", "GDP growth, HIES poverty rates, Labour Force Survey", "2000-2024"],
        ["World Inequality Report 2022", "Global income and wealth shares", "2021"],
        ["World Happiness Report 2024", "Life evaluation scores", "2021-2023"],
        ["Global Carbon Project; World Bank", "CO₂ emissions and world real GDP", "1990-2022"],
        ["Academic literature", "GPI, Easterlin paradox, Stiglitz-Sen-Fitoussi report", "1934-2024"],
    ],
    widths=[58, 72, 30],
    src="Compiled by the author.",
)

T_APPROACHES = dict(
    title="The three approaches to measuring GDP",
    headers=["Approach", "What is added up", "Formula / example"],
    rows=[
        ["Expenditure approach", "Spending on final goods and services", "GDP = C + I + G + (X − M)"],
        ["Income approach", "Incomes earned in production", "Wages + rent + interest + profit + (taxes − subsidies) + depreciation"],
        ["Production (value-added) approach", "Value added at each stage of production", "GDP = Value of output − Value of intermediate inputs"],
    ],
    widths=[40, 52, 68],
    src="Adapted from Mankiw (2021) and the System of National Accounts 2008.",
)

T_DEMO1 = dict(
    title="Hypothetical economy: nominal and real GDP",
    headers=["Item", "Year 1 (base)", "Year 2"],
    rows=[
        ["Quantity of rice (million tonnes)", "100", "106"],
        ["Price of rice (Tk per tonne)", "40,000", "44,000"],
        ["Nominal GDP (Tk billion)", "4,000", "4,664"],
        ["Real GDP at Year 1 prices (Tk billion)", "4,000", "4,240"],
        ["Population (million)", "170", "172"],
        ["Real GDP per capita (Tk)", "23,529", "24,651"],
    ],
    widths=[80, 40, 40],
    src="Author's hypothetical example.",
)

T_DIMENSIONS = dict(
    title="Dimensions of economic well-being and example indicators",
    headers=["Dimension", "What it means", "Example indicator"],
    rows=[
        ["Material living standards", "Income, consumption and wealth of households", "Median household disposable income"],
        ["Distribution", "How income and wealth are shared", "Gini index, top 10% income share"],
        ["Health", "Length and quality of life", "Life expectancy, child mortality"],
        ["Education and skills", "Knowledge and capabilities", "Mean years of schooling"],
        ["Work and leisure", "Job quality, working hours, free time", "Share working over 48 hours a week"],
        ["Security", "Economic and physical safety", "Unemployment rate, crime rate"],
        ["Environment", "Quality and stock of natural resources", "Air quality (PM2.5), forest cover"],
        ["Subjective well-being", "How people evaluate their own lives", "Life satisfaction score (0-10)"],
    ],
    widths=[40, 64, 56],
    src="Based on Stiglitz, Sen and Fitoussi (2009) and the OECD Better Life Index.",
)

T_DEMO2 = dict(
    title="Same GDP, different well-being: Country A and Country B",
    headers=["Indicator", "Country A", "Country B"],
    rows=[
        ["GDP per capita (US$)", "5,000", "5,000"],
        ["Annual GDP growth", "6%", "6%"],
        ["Income share of poorest 20%", "6%", "9%"],
        ["Income share of richest 20%", "47%", "36%"],
        ["Average income of poorest 20% (US$)", "1,500", "2,250"],
        ["Ratio richest 20% : poorest 20%", "7.8 times", "4.0 times"],
        ["Approximate Gini index", "0.38", "0.25"],
    ],
    widths=[80, 40, 40],
    src="Author's hypothetical example.",
)

T_BROKEN = dict(
    title="GDP and well-being after a flood (hypothetical)",
    headers=["Item (US$ billion)", "Scenario 1: no flood", "Scenario 2: flood"],
    rows=[
        ["Normal output", "1,000", "900"],
        ["Reconstruction spending", "0", "150"],
        ["**Measured GDP**", "**1,000**", "**1,050**"],
        ["Houses, roads and crops destroyed", "0", "300"],
        ["National wealth at year end", "5,000", "4,700"],
        ["Household well-being index (100 = normal)", "100", "88"],
    ],
    widths=[80, 40, 40],
    src="Author's hypothetical example.",
)

T_LIMITS = dict(
    title="Summary of the main limitations of GDP",
    headers=["Limitation", "Example", "Effect on GDP as a well-being measure"],
    rows=[
        ["Ignores distribution", "Growth captured by the top 10%", "Average rises while most people gain little"],
        ["Excludes unpaid work", "Cooking, childcare, caring for elders", "Undervalues women's contribution"],
        ["Misses informal output", "Street vendors, small farms", "Understates real activity in poor countries"],
        ["Ignores environmental loss", "Air pollution, river damage, deforestation", "Counts depletion as income"],
        ["Counts defensive spending", "Flood repair, security guards, pollution illness", "GDP rises when life gets worse"],
        ["Ignores leisure", "Longer working hours", "More output, less free time"],
        ["Weak link to happiness", "Easterlin paradox", "Rising income, flat life satisfaction"],
        ["Quality and free goods", "Free apps, better medicines", "Under-records real gains"],
    ],
    widths=[40, 58, 62],
    src="Compiled by the author from the discussion in Chapter 5.",
)

T_HDI_CALC = dict(
    title="Calculation of Bangladesh's HDI, 2022",
    headers=["Component", "Actual value", "Min / Max (goalposts)", "Index"],
    rows=[
        ["Life expectancy at birth (years)", "73.7", "20 / 85", "0.826"],
        ["Expected years of schooling", "11.9", "0 / 18", "0.661"],
        ["Mean years of schooling", "7.4", "0 / 15", "0.493"],
        ["Education index (average of the two)", "-", "-", "0.577"],
        ["GNI per capita (2017 PPP $)", "6,511", "100 / 75,000", "0.631"],
        ["**HDI = (0.826 × 0.577 × 0.631)^(1/3)**", "-", "-", "**0.670**"],
    ],
    widths=[62, 30, 38, 30],
    src="Author's calculation using UNDP (2024) data and method.",
)

T_MEASURES = dict(
    title="Comparison of GDP with alternative well-being measures",
    headers=["Measure", "Developed by", "What it captures", "Main weakness"],
    rows=[
        ["GDP", "Kuznets; UN SNA", "Market production", "Ignores distribution, environment, unpaid work"],
        ["HDI", "UNDP (1990)", "Income, health, education", "Only three dimensions; no environment"],
        ["IHDI", "UNDP (2010)", "HDI adjusted for inequality", "Data gaps in many countries"],
        ["GPI", "Cobb, Daly and others (1989/95)", "Consumption adjusted for social and environmental costs", "Valuation choices are subjective"],
        ["Better Life Index", "OECD (2011)", "11 dimensions of well-being", "Mainly OECD countries"],
        ["Gross National Happiness", "Bhutan (2008 index)", "9 domains, 33 indicators", "Hard to compare across countries"],
        ["Life evaluation (WHR)", "Gallup / WHR (2012)", "Self-reported life satisfaction", "Cultural and survey bias"],
        ["Inclusive Wealth / SEEA", "UNEP; UN Statistics", "Produced, human and natural capital", "Complex to compile"],
    ],
    widths=[30, 36, 46, 48],
    size=9.5,
    src="Compiled by the author from UNDP (2024), OECD (2011), Kubiszewski et al. (2013) and UN (2021).",
)

T_BD = dict(
    title="Bangladesh: growth versus broader well-being indicators",
    headers=["Indicator", "Value", "Year", "What it tells us"],
    rows=[
        ["Average real GDP growth", "6.4%", "FY11-FY24", "Strong and stable growth"],
        ["GDP per capita (current US$)", "about 2,690", "2022", "Lower-middle-income status"],
        ["Upper poverty rate", "18.7%", "2022", "Poverty fell sharply"],
        ["Income Gini coefficient", "0.499", "2022", "Income inequality is high and rising"],
        ["Informal employment", "84.9%", "2022", "Most jobs lack protection"],
        ["Female labour force participation", "about 43%", "2022", "Large unpaid work burden"],
        ["Life expectancy at birth", "about 72-74 years", "2022", "Better than income level predicts"],
        ["HDI value", "0.670", "2022", "Medium human development"],
        ["Life evaluation (WHR)", "3.89 / 10", "2021-23", "Low reported life satisfaction"],
    ],
    widths=[48, 28, 24, 60],
    size=9.5,
    src="BBS (2023a, 2023b), UNDP (2024), World Bank (2024), Helliwell et al. (2024).",
)

T_COUNTRIES = dict(
    title="Selected countries: GDP per capita compared with well-being indicators",
    headers=["Country", "GDP per capita (US$)", "Life expectancy", "HDI", "Life evaluation (0-10)"],
    rows=[
        ["Norway", "108,700", "83.1", "0.966", "7.30"],
        ["United States", "76,300", "77.5", "0.927", "6.73"],
        ["Finland", "50,900", "81.2", "0.942", "7.74"],
        ["Japan", "34,000", "84.0", "0.920", "6.06"],
        ["Costa Rica", "13,200", "77.0", "0.806", "6.96"],
        ["China", "12,700", "78.6", "0.788", "5.97"],
        ["South Africa", "6,700", "62.3", "0.717", "5.42"],
        ["Vietnam", "4,200", "74.6", "0.726", "6.04"],
        ["Sri Lanka", "3,350", "76.4", "0.780", "3.90"],
        ["Bangladesh", "2,690", "73.4", "0.670", "3.89"],
        ["Nigeria", "2,160", "53.6", "0.548", "4.88"],
    ],
    widths=[34, 34, 30, 26, 36],
    src="World Bank (2024), UNDP (2024), Helliwell et al. (2024); values rounded, 2022 or latest year.",
)

T_DASH = dict(
    title="Dashboard scores for two hypothetical countries (0-100)",
    headers=["Dimension", "Country X", "Country Y"],
    rows=[
        ["GDP per capita", "80", "60"],
        ["Income equality", "40", "75"],
        ["Health", "60", "80"],
        ["Education", "65", "75"],
        ["Environment", "35", "70"],
        ["Life satisfaction", "50", "72"],
        ["Leisure and work balance", "45", "70"],
        ["**Average of all seven dimensions**", "**53.6**", "**71.7**"],
    ],
    widths=[80, 40, 40],
    src="Author's hypothetical example.",
)

S_WB = "World Bank (2024), World Development Indicators; values for 2022, rounded."

BODY = [
    # ------------------------------------------------------------------ 1
    ("h1", "1. Introduction", False),
    ("h2", "1.1 Background of the Study"),
    ("p", "When a finance minister presents a budget, the first number most people hear is the expected GDP growth "
          "rate. A growth rate of 7 per cent is treated as good news and a rate of 3 per cent as a warning. Behind "
          "this habit lies an assumption that a bigger economy means a better life for the people who live in it. "
          "For much of the twentieth century this assumption was rarely questioned, because rising output usually "
          "brought more food, better housing, more schools and longer lives."),
    ("p", "Over the last few decades, however, economists, statisticians and policymakers have pointed out that GDP "
          "can rise while many people feel no better off. Inequality has widened in many countries, climate change "
          "and pollution impose costs that GDP does not subtract, and surveys of happiness show that life "
          "satisfaction does not always follow income. These concerns led to the influential Stiglitz-Sen-Fitoussi "
          "Commission (2009), the OECD Better Life Initiative and the United Nations' “Beyond GDP” work."),
    ("p", "Bangladesh is a useful example. The country grew at an average of more than 6 per cent a year for over a "
          "decade and moved into the lower-middle-income group in 2015. Poverty fell by more than half. At the same "
          "time, income inequality rose, most workers remain in informal jobs, and Dhaka regularly ranks among the "
          "most polluted cities in the world. These facts raise the question this assignment sets out to answer."),
    ("h2", "1.2 Statement of the Problem"),
    ("p", "GDP measures the market value of all final goods and services produced in a country in a given period. "
          "Economic well-being, in contrast, refers to how well people are able to live: their income and "
          "consumption, their security, their health, the time they have and the environment around them. The "
          "problem is that policy debates often treat the two as the same thing. If GDP is a weak guide to "
          "well-being, then policies designed to maximise growth may not maximise welfare, and some may even "
          "reduce it."),
    ("h2", "1.3 Objectives of the Study"),
    ("p", "The broad objective is to evaluate whether GDP growth is an adequate measure of economic well-being. "
          "The specific objectives are:"),
    ("ul", ["To explain how GDP is measured and what it is designed to capture.",
            "To define economic well-being and identify its main dimensions.",
            "To assess the evidence linking GDP growth with well-being outcomes.",
            "To identify and demonstrate the main limitations of GDP as a welfare measure.",
            "To compare GDP with alternative measures such as the HDI and GPI.",
            "To apply the analysis to Bangladesh and suggest practical recommendations."]),
    ("h2", "1.4 Research Questions"),
    ("ol", ["Does an increase in GDP reliably lead to an increase in people's economic well-being?",
            "What important aspects of well-being does GDP fail to capture?",
            "Which alternative or complementary measures give a fuller picture?",
            "What does the Bangladesh experience tell us about growth and well-being?"]),
    ("h2", "1.5 Methodology and Data Sources"),
    ("p", "This is a descriptive and analytical study based on **secondary data**. Quantitative data were collected "
          "from international and national sources and presented through tables and charts. Simple worked "
          "examples (called *demonstrations*) are used to show how GDP can move differently from well-being. The "
          "study follows the steps shown in Figure 1, and Table 1 lists the main data sources."),
    ("fig", "f00_framework", "Framework of the study", "Prepared by the author.", 158),
    ("table", T_DATA_SOURCES),
    ("h2", "1.6 Scope and Limitations"),
    ("p", "The study focuses on the conceptual adequacy of GDP growth as a welfare measure, using global comparisons "
          "and Bangladesh as a case study. It does not build an econometric model. Figures are rounded and some "
          "cross-country values refer to the latest available year, so small differences from the original "
          "databases are possible. Charts marked as *illustrative* or *stylised* are designed to explain a concept "
          "rather than report exact statistics."),

    # ------------------------------------------------------------------ 2
    ("h1", "2. Understanding Gross Domestic Product", True),
    ("h2", "2.1 Definition of GDP"),
    ("p", "Gross Domestic Product is **the total market value of all final goods and services produced within a "
          "country's borders during a specific period**, usually a quarter or a year (Mankiw, 2021). Each part of "
          "the definition matters. *Market value* means goods are weighted by their prices. *Final* goods exclude "
          "intermediate inputs to avoid double counting. *Within a country* means production by foreign firms "
          "located in Bangladesh counts in Bangladesh's GDP, while income earned by Bangladeshi workers abroad does "
          "not (it is part of Gross National Income instead)."),
    ("h2", "2.2 Three Approaches to Measuring GDP"),
    ("p", "Because every taka spent by a buyer is a taka of income for a seller, GDP can be measured in three ways "
          "that should, in principle, give the same answer (Table 2). The most familiar is the expenditure "
          "identity:"),
    ("eq", "GDP = C + I + G + (X − M)"),
    ("p", "where C is household consumption, I is investment, G is government purchases, X is exports and M is "
          "imports. Each of these items is a flow of spending in the market. Nothing in the formula asks whether "
          "the spending made anyone happier, healthier or more secure."),
    ("table", T_APPROACHES),
    ("h2", "2.3 Nominal GDP, Real GDP and GDP per Capita"),
    ("p", "Nominal GDP values output at current prices, so it rises with inflation. **Real GDP** values output at "
          "constant base-year prices and therefore measures changes in quantity. The **GDP growth rate** is the "
          "percentage change in real GDP. **GDP per capita** divides GDP by population and is the version most "
          "often used as a rough indicator of average living standards."),
    ("demo", "Separating price rises from real growth", [
        "Consider a simple economy that produces only rice. Table 3 shows its data for two years.",
        "Nominal GDP growth = (4,664 − 4,000) / 4,000 × 100 = **16.6%**",
        "Real GDP growth (Year 1 prices) = (4,240 − 4,000) / 4,000 × 100 = **6.0%**",
        "Real GDP per capita growth = (24,651 − 23,529) / 23,529 × 100 = **4.8%**",
        "**Lesson:** the headline nominal figure (16.6%) mostly reflects inflation. Even real growth (6%) "
        "overstates the gain per person (4.8%) because population also grew. And none of these numbers tells us "
        "whether the extra rice reached poor families.",
    ]),
    ("table", T_DEMO1),
    ("h2", "2.4 How GDP Became the Headline Number"),
    ("p", "Modern national accounts were developed in the 1930s by Simon Kuznets for the United States government, "
          "which needed to understand the collapse of output during the Great Depression. During the Second World "
          "War, GDP proved useful for planning production, and after the Bretton Woods conference in 1944 it became "
          "the standard yardstick for international comparison. The United Nations' System of National Accounts "
          "(SNA), first issued in 1953 and last revised in 2008, now provides common rules for all countries."),
    ("p", "Interestingly, the creator of the measure warned against using it as a welfare index. In his 1934 "
          "report to the US Congress, Kuznets wrote:"),
    ("quote", "The welfare of a nation can scarcely be inferred from a measurement of national income.",
     "Simon Kuznets (1934)"),
    ("p", "Robert F. Kennedy made a similar point in 1968 when he said that the gross national product “measures "
          "everything in short, except that which makes life worthwhile.” These warnings form the starting "
          "point for the critique developed in this assignment."),

    # ------------------------------------------------------------------ 3
    ("h1", "3. The Concept of Economic Well-Being", True),
    ("h2", "3.1 Defining Economic Well-Being"),
    ("p", "Economic well-being refers to people's command over the resources they need to live a good life, both "
          "now and in the future. The Canadian economists Osberg and Sharpe (2002) describe it through four "
          "components: consumption flows, accumulation of wealth for future generations, equality of income, and "
          "economic security against risks such as unemployment, illness and old age. Amartya Sen's capability "
          "approach goes further and argues that what finally matters is what people are able to *do and be*, "
          "such as being well nourished, educated and able to take part in community life (Sen, 1999)."),
    ("p", "Two features separate well-being from GDP. First, well-being is about **people**, not production: it "
          "asks how households fare, not how much is made. Second, well-being has a **time dimension**: a country "
          "that grows today by running down its forests or groundwater may reduce the well-being of tomorrow's "
          "citizens."),
    ("h2", "3.2 Dimensions of Well-Being"),
    ("p", "Most modern frameworks treat well-being as multi-dimensional. Table 4 brings together the dimensions "
          "used by the Stiglitz-Sen-Fitoussi Commission and the OECD Better Life Index, with an example indicator "
          "for each."),
    ("table", T_DIMENSIONS),
    ("h2", "3.3 The Stiglitz-Sen-Fitoussi Commission"),
    ("p", "In 2008 the French government asked Joseph Stiglitz, Amartya Sen and Jean-Paul Fitoussi to examine the "
          "limits of GDP. Their report (2009) made twelve recommendations. The most important for this "
          "assignment are:"),
    ("ul", ["Look at **income and consumption** rather than production.",
            "Consider income and consumption together with **wealth**.",
            "Emphasise the **household perspective** and give more prominence to the **distribution** of income.",
            "Broaden income measures to **non-market activities** such as household work.",
            "Measure **quality of life** (health, education, security, social connections) and **subjective well-being**.",
            "Assess **sustainability** separately, through stocks of natural, physical and human capital."]),
    ("h2", "3.4 GDP and Well-Being: A Conceptual Comparison"),
    ("p", "Figure 2 summarises the gap. The left panel shows items that GDP counts, including some that reflect "
          "harm rather than benefit. The right panel shows items that matter for well-being but are missing or "
          "mis-valued in GDP. The rest of this assignment examines both panels with evidence."),
    ("fig", "f01_concept", "What GDP counts and what it misses", "Prepared by the author, based on Stiglitz et al. (2009).", 150),

    # ------------------------------------------------------------------ 4
    ("h1", "4. The Case for GDP: Why Growth Still Matters", True),
    ("p", "A fair evaluation must begin with what GDP does well. Critics of GDP do not argue that growth is "
          "useless; rather, they argue that it is incomplete. The evidence shows that, especially for poorer "
          "countries, GDP growth is strongly connected with improvements in people's lives."),
    ("h2", "4.1 Growth and Living Standards"),
    ("p", "Figure 3 plots life expectancy against GDP per capita for a range of countries. This relationship, "
          "known as the **Preston curve** (Preston, 1975), is steep at low incomes and flattens at higher incomes. "
          "Moving from US$1,000 to US$10,000 per person is associated with about ten extra years of life, but "
          "moving from US$50,000 to US$100,000 adds very little. Higher income pays for food, clean water, "
          "vaccines and hospitals, so in poor countries growth and health tend to move together."),
    ("fig", "f03_preston", "GDP per capita and life expectancy (the Preston curve)", S_WB, 148),
    ("p", "The chart also shows that income is not the whole story. Bangladesh and Sri Lanka have higher life "
          "expectancy than their income would predict, while South Africa, Equatorial Guinea and Nigeria fall "
          "well below the trend line. The United States, one of the richest countries, has lower life expectancy "
          "than Costa Rica or China. Points far from the line show that *how* income is used matters as much "
          "as *how much* is produced."),
    ("h2", "4.2 Growth and Poverty Reduction: Evidence from Bangladesh"),
    ("p", "Bangladesh offers strong evidence that sustained growth can reduce poverty. Figure 4 shows real GDP "
          "growth from FY2011 to FY2024. Apart from the COVID-19 shock in FY2020, growth stayed between 6 and 8 "
          "per cent for most of the period, before slowing in FY2023 and FY2024."),
    ("fig", "f02_bd_growth", "Real GDP growth in Bangladesh, FY2011-FY2024 (%)",
     "Bangladesh Bureau of Statistics; FY2024 is provisional. Light bars mark growth below 5%.", 148),
    ("p", "Over roughly the same period, poverty fell sharply. According to the Household Income and Expenditure "
          "Survey (HIES), the share of people below the upper poverty line dropped from 48.9 per cent in 2000 to "
          "18.7 per cent in 2022, and extreme poverty fell from 34.3 per cent to 5.6 per cent (Figure 5). Growth "
          "in garment exports, remittances and agricultural productivity created jobs and raised incomes for "
          "millions of households."),
    ("fig", "f04_bd_poverty", "Poverty headcount rates in Bangladesh, 2000-2022", "BBS, Household Income and Expenditure Survey (2000-2022).", 148),
    ("h2", "4.3 Practical Advantages of GDP"),
    ("p", "Beyond its link with poverty and health, GDP has several practical strengths that explain why it remains "
          "the headline indicator:"),
    ("ul", ["**Standardised:** all countries follow the same SNA rules, so figures can be compared.",
            "**Timely and frequent:** many countries publish quarterly estimates, which helps short-term policy.",
            "**Objective:** it is based on market prices rather than opinions or arbitrary weights.",
            "**Linked to jobs:** changes in output are closely connected to employment (Okun's law).",
            "**Linked to public finance:** tax revenue, debt sustainability and budget planning depend on GDP.",
            "**Single number:** it is easy to communicate to the public and to track over time."]),
    ("p", "These advantages make GDP an excellent measure of **economic activity**. The question is whether they "
          "make it a good measure of **economic well-being**, which is the subject of the next chapter."),

    # ------------------------------------------------------------------ 5
    ("h1", "5. Limitations of GDP as a Measure of Well-Being", True),
    ("h2", "5.1 GDP Ignores the Distribution of Income"),
    ("p", "GDP and GDP per capita are totals and averages. If all the gains from growth go to a small group, "
          "average income rises even though most people are no better off. Figure 6 compares the Gini index, the "
          "standard measure of inequality, across countries. Brazil and South Africa have similar or higher GDP "
          "per capita than many Asian countries, but far higher inequality, which helps explain their weaker "
          "health and social outcomes."),
    ("fig", "f05_gini", "Income inequality across selected countries (Gini index)",
     "World Bank (2024), Poverty and Inequality Platform; latest available year. Mid-tone bars mark Gini of 40 or more.", 140),
    ("p", "At the global level, inequality is even more striking. According to the World Inequality Report 2022, "
          "the richest 10 per cent of the world's population receive 52 per cent of global income and own 76 per "
          "cent of global wealth, while the poorest half receive only 8.5 per cent of income and own just 2 per "
          "cent of wealth (Figure 7). A rise in world GDP tells us nothing about which of these groups gains."),
    ("fig", "f06_wir", "Global distribution of income and wealth, 2021", "Chancel, Piketty, Saez and Zucman (2022), World Inequality Report 2022.", 145),
    ("demo", "Two countries with the same GDP", [
        "Country A and Country B both have GDP per capita of US$5,000 and both grow at 6 per cent a year. A "
        "statistician looking only at GDP would say they are equally well off. Table 5 and Figure 8 show what "
        "the averages hide.",
        "Average income of a quintile = (income share ÷ 20%) × mean income",
        "= Poorest 20% in Country A: (6% ÷ 20%) × 5,000 = US$1,500",
        "= Poorest 20% in Country B: (9% ÷ 20%) × 5,000 = US$2,250",
        "**Lesson:** the poorest fifth in Country B earns 50 per cent more than in Country A, even though GDP is "
        "identical. Because an extra dollar adds more to the welfare of a poor family than a rich one (diminishing "
        "marginal utility), Country B has higher economic well-being.",
    ]),
    ("table", T_DEMO2),
    ("fig", "f07_demo_distribution", "Average income by quintile in Country A and Country B", "Author's hypothetical example (Demonstration 2).", 145),
    ("h2", "5.2 Non-Market and Unpaid Work"),
    ("p", "GDP counts only work that is bought and sold. When a family hires a cook, the cook's wage is part of "
          "GDP; when a mother cooks the same meal at home, nothing is recorded. The International Labour "
          "Organization estimates that people spend about 16.4 billion hours every day on unpaid care work, "
          "which would be worth around 9 per cent of global GDP if paid at the minimum wage (ILO, 2018). Most of "
          "this work is done by women."),
    ("p", "In Bangladesh, a study by the Centre for Policy Dialogue estimated that the value of women's unpaid "
          "household work was equivalent to roughly three-quarters of GDP or more, depending on the valuation "
          "method used (CPD, 2015). Leaving this work out does two things: it undervalues women's contribution, "
          "and it can make GDP rise simply because work moves from the home into the market, for example when "
          "families buy ready-made food instead of cooking, even if total work and welfare do not change."),
    ("h2", "5.3 The Informal Economy"),
    ("p", "In developing countries a large share of production takes place in the informal sector: small farms, "
          "street vendors, rickshaw pullers and home-based workers. Statistical offices try to estimate this "
          "activity, but it is often under-recorded. According to the Labour Force Survey 2022, about **84.9 per "
          "cent** of employed people in Bangladesh work informally (BBS, 2023b). Informal workers usually have no "
          "contract, pension or sick leave. So even where their output is counted, GDP says nothing about their "
          "insecurity, which is a core part of economic well-being."),
    ("h2", "5.4 Environmental Degradation and Resource Depletion"),
    ("p", "GDP treats the extraction of natural resources as income, without subtracting the loss of the resource "
          "itself. A country that cuts down its forests and sells the timber records higher GDP, even though its "
          "natural wealth has fallen. Pollution is also ignored, unless it creates spending on clean-up or "
          "medical treatment, which actually *adds* to GDP."),
    ("p", "Figure 9 shows that world real GDP more than doubled between 1990 and 2022, while global CO₂ "
          "emissions from fossil fuels rose by about 64 per cent. Growth has become somewhat less carbon-intensive, "
          "but emissions are still rising, and the damage from climate change does not appear in GDP. For "
          "Bangladesh, the World Bank (2018) estimated that environmental degradation, mainly air and water "
          "pollution in urban areas, cost the country about US$6.5 billion a year, equal to roughly 3.4 per cent "
          "of GDP in 2015."),
    ("fig", "f08_gdp_co2", "World real GDP and global CO₂ emissions, 1990-2022 (index, 1990 = 100)",
     "World Bank (2024) for real GDP; Global Carbon Project (2023) for emissions. Values rounded.", 145),
    ("h2", "5.5 Defensive Expenditure and the Broken-Window Problem"),
    ("p", "Some spending does not make people better off; it only protects them from something bad or repairs "
          "damage. Examples include security guards, air purifiers, flood repairs and treatment for illnesses "
          "caused by pollution. These **defensive** or *regrettable* expenditures raise GDP. The French economist "
          "Frédéric Bastiat illustrated a related error with the story of the broken window: replacing "
          "the glass creates work for the glazier, but society is not richer, because the money would otherwise "
          "have been spent on something new."),
    ("demo", "A flood that raises GDP", [
        "Imagine an economy with normal output of US$1,000 billion and national wealth of US$5,000 billion. A "
        "severe flood destroys houses, roads and crops worth US$300 billion and disrupts output by US$100 "
        "billion. The government and households then spend US$150 billion on reconstruction (Table 6).",
        "= Measured GDP = 900 + 150 = US$1,050 billion (+5%)",
        "= National wealth = 5,000 − 300 = US$4,700 billion (−6%)",
        "**Lesson:** GDP rises by 5 per cent in the year of a disaster, while the stock of wealth falls and "
        "households suffer losses, injury and displacement (Figure 10). For a flood-prone country such as "
        "Bangladesh, this is a practical warning against reading a post-disaster growth figure as good news.",
    ]),
    ("table", T_BROKEN),
    ("fig", "f16_broken_window", "GDP, wealth and well-being after a flood (hypothetical)", "Author's hypothetical example (Demonstration 3).", 140),
    ("h2", "5.6 Spending More Does Not Always Mean Living Better"),
    ("p", "Health care shows clearly that more spending, and therefore more GDP, does not automatically produce "
          "better outcomes. The United States spends about 17 per cent of its GDP on health, far more than any "
          "other country, yet its life expectancy is lower than in Japan, France or Canada, which spend much less "
          "(Figure 11). Sri Lanka and Costa Rica achieve life expectancy close to that of rich countries at a "
          "fraction of the cost. GDP records the spending, but it cannot tell whether that spending is efficient "
          "or whether it reflects worse underlying health."),
    ("fig", "f11_health", "Health spending and life expectancy in selected countries, 2021",
     "World Bank (2024) and WHO Global Health Expenditure Database; values rounded.", 150),
    ("h2", "5.7 Happiness and the Easterlin Paradox"),
    ("p", "If GDP measured well-being, we would expect people in countries with rising GDP to report rising "
          "satisfaction with life. Richard Easterlin (1974) found that this did not happen. In the United States, "
          "real GDP per capita roughly doubled between 1972 and 2018, but the share of people describing "
          "themselves as “very happy” in the General Social Survey stayed at around 30 per cent "
          "(Figure 12). This is known as the **Easterlin paradox**."),
    ("fig", "f09_easterlin", "United States: GDP per capita and reported happiness, 1972-2018",
     "US Bureau of Economic Analysis and NORC General Social Survey; illustrative, values rounded.", 145),
    ("p", "Across countries the picture is more nuanced. Figure 13 shows that richer countries do, on average, "
          "report higher life evaluations, so income clearly matters (Stevenson and Wolfers, 2008). But there "
          "are large differences at similar income levels. Costa Rica reports much higher life satisfaction "
          "than Russia or China at a similar GDP per capita, and Vietnam reports more than countries twice as "
          "rich. Social support, trust, freedom and good governance explain much of this gap (Helliwell et al., "
          "2024)."),
    ("fig", "f10_happiness", "GDP per capita and life evaluation across countries",
     "Helliwell et al. (2024), World Happiness Report; World Bank (2024) for GDP per capita.", 148),
    ("h2", "5.8 Quality Change, Free Digital Goods and Leisure"),
    ("p", "GDP also struggles with changes in quality. A smartphone today is far more powerful than a computer of "
          "twenty years ago, yet may cost less. Many digital services, such as search engines, maps and online "
          "learning, are free to users and hardly appear in GDP even though they add real value. In the other "
          "direction, GDP gives no value to **leisure**. If people work longer hours, GDP rises, even if the extra "
          "work leaves them exhausted and with less time for family. A country where people work 60 hours a week "
          "could have the same GDP as one where they work 40 hours with higher productivity, but the second "
          "clearly enjoys higher well-being."),
    ("p", "Table 7 summarises the limitations discussed in this chapter."),
    ("table", T_LIMITS),

    # ------------------------------------------------------------------ 6
    ("h1", "6. Alternative and Complementary Measures", True),
    ("p", "The limitations of GDP have encouraged the development of several alternative measures. Some replace "
          "GDP with a different single number, while others use a group of indicators (a *dashboard*). This "
          "chapter reviews the most important ones."),
    ("h2", "6.1 The Human Development Index (HDI)"),
    ("p", "The HDI was introduced by the United Nations Development Programme in 1990, based on the ideas of "
          "Mahbub ul Haq and Amartya Sen. It combines three dimensions: a long and healthy life (life expectancy), "
          "knowledge (expected and mean years of schooling) and a decent standard of living (GNI per capita in "
          "PPP terms, on a log scale). Each component is turned into an index between 0 and 1 using fixed "
          "minimum and maximum values (goalposts), and the HDI is their geometric mean:"),
    ("eq", "Dimension index = (Actual value − Minimum) / (Maximum − Minimum)"),
    ("eq", "HDI = (Health index × Education index × Income index)^(1/3)"),
    ("demo", "Calculating Bangladesh's HDI", [
        "Using UNDP data for 2022, the steps are:",
        "= Health index = (73.7 − 20) / (85 − 20) = 0.826",
        "= Education index = [(11.9 / 18) + (7.4 / 15)] / 2 = (0.661 + 0.493) / 2 = 0.577",
        "= Income index = [ln(6,511) − ln(100)] / [ln(75,000) − ln(100)] = 4.176 / 6.620 = 0.631",
        "= HDI = (0.826 × 0.577 × 0.631)^(1/3) = 0.670",
        "**Lesson:** Bangladesh's health index (0.826) is much stronger than its income index (0.631). Judged by "
        "GDP alone, the country's progress in health would be understated, while its weaker education outcomes "
        "would be invisible. Table 8 shows the full calculation.",
    ]),
    ("table", T_HDI_CALC),
    ("p", "Figure 14 shows that the HDI is strongly related to GDP per capita, as expected, since income is one of "
          "its components. Still, some countries perform much better on the HDI than their income would suggest "
          "(Sri Lanka, Vietnam), while others perform worse (Equatorial Guinea, Qatar, Nigeria). The ranking of a "
          "country can change considerably depending on whether GDP or HDI is used."),
    ("fig", "f13_hdi", "GDP per capita and Human Development Index, 2022", "UNDP (2024), Human Development Report 2023/24; World Bank (2024).", 148),
    ("h2", "6.2 The Genuine Progress Indicator (GPI)"),
    ("p", "The GPI starts with personal consumption, adjusts it for income inequality, adds the value of household "
          "and volunteer work, and subtracts costs such as crime, pollution, commuting, loss of leisure, "
          "depletion of resources and long-term environmental damage. Studies for the United States and for the "
          "world as a whole find that GPI per capita rose with GDP until the late 1970s and then stopped growing, "
          "even as GDP continued to rise (Kubiszewski et al., 2013). Figure 15 shows this pattern in stylised "
          "form. The widening gap suggests that, after a certain point, the costs of growth began to cancel out "
          "its benefits."),
    ("fig", "f12_gpi", "GDP per capita compared with the Genuine Progress Indicator (stylised)",
     "Stylised representation of the findings of Kubiszewski et al. (2013) and Talberth, Cobb and Slattery (2007).", 145),
    ("h2", "6.3 Other Measures"),
    ("ul", ["**Inequality-adjusted HDI (IHDI):** reduces the HDI according to how unequally health, education and "
            "income are shared. The difference between HDI and IHDI shows the loss due to inequality.",
            "**Multidimensional Poverty Index (MPI):** counts people who are deprived in several areas at once, "
            "such as nutrition, schooling, cooking fuel and sanitation.",
            "**OECD Better Life Index:** lets users compare countries across 11 dimensions, including housing, "
            "jobs, community, environment, civic engagement and work-life balance.",
            "**Gross National Happiness (Bhutan):** a national index of 9 domains and 33 indicators that guides "
            "public policy in Bhutan.",
            "**Green GDP and SEEA:** the UN System of Environmental-Economic Accounting adjusts national accounts "
            "for the use and depletion of natural resources.",
            "**Inclusive Wealth Index:** measures the stock of produced, human and natural capital, which "
            "indicates whether development is sustainable."]),
    ("p", "Table 9 compares these measures with GDP. Each alternative has its own weaknesses, mainly data "
          "requirements and value judgements in choosing weights. This is why most experts now recommend using "
          "them **alongside** GDP rather than as a complete replacement."),
    ("table", T_MEASURES),

    # ------------------------------------------------------------------ 7
    ("h1", "7. Case Study: Bangladesh", True),
    ("h2", "7.1 Growth Performance"),
    ("p", "Bangladesh is often described as a development success story. Its average real GDP growth of about 6.4 "
          "per cent between FY2011 and FY2024 (Figure 4) was among the fastest in the world, and GDP per capita "
          "rose above that of several neighbouring countries. The country is scheduled to graduate from the "
          "United Nations' Least Developed Country list in 2026. On a GDP basis, the story is very positive."),
    ("h2", "7.2 Human Development Progress"),
    ("p", "Human development has also improved. Bangladesh's HDI rose from about 0.394 in 1990 to 0.670 in 2022 "
          "(Figure 16), taking it into the medium human development group. Gains in life expectancy, child "
          "survival, girls' schooling and access to sanitation were achieved partly through growth, but also "
          "through low-cost public health programmes, NGO activity and community health workers. This shows that "
          "policy choices, and not only the growth rate, shape well-being."),
    ("fig", "f14_bd_hdi", "Human Development Index of Bangladesh, 1990-2022", "UNDP (2024), Human Development Report 2023/24.", 145),
    ("h2", "7.3 What GDP Growth Does Not Show"),
    ("p", "Table 10 places Bangladesh's growth record next to broader indicators. Several important issues are "
          "hidden by the headline growth figure:"),
    ("ul", ["**Rising inequality:** the income Gini coefficient rose to 0.499 in 2022, one of the highest levels "
            "recorded by HIES. The richest 10 per cent received about 41 per cent of total income (BBS, 2023a).",
            "**Informal and insecure work:** about 85 per cent of workers are informal, with little social "
            "protection.",
            "**Environmental pressure:** air pollution in Dhaka, river pollution from industry, and climate risks "
            "such as floods, cyclones and salinity impose large costs that GDP does not subtract.",
            "**Unpaid work:** women carry most unpaid household and care work, which is not counted.",
            "**Low reported life satisfaction:** Bangladesh scores 3.89 out of 10 on the World Happiness Report "
            "life evaluation, well below countries with similar income such as Vietnam.",
            "**Data reliability:** in 2024 a government-appointed white paper committee raised concerns that "
            "official growth figures in earlier years may have been overstated, which further weakens reliance on "
            "a single number."]),
    ("table", T_BD),
    ("p", "The Bangladesh case therefore supports both sides of the debate. Growth has clearly helped to reduce "
          "poverty and improve health, but the GDP figure alone would give a misleadingly positive picture of how "
          "evenly the benefits were shared and how sustainable they are."),

    # ------------------------------------------------------------------ 8
    ("h1", "8. Comparative Analysis: A Dashboard Approach", True),
    ("p", "Table 11 compares eleven countries across GDP per capita and three well-being indicators. Ranking by "
          "GDP and ranking by well-being give different results. The United States has more than twice Japan's "
          "GDP per capita but lower life expectancy. Finland, with less than half of Norway's GDP per capita, "
          "reports the highest life evaluation in the world. Costa Rica, Vietnam and Sri Lanka achieve much more "
          "health than their income suggests, while South Africa and Nigeria achieve much less."),
    ("table", T_COUNTRIES),
    ("p", "One practical way to look beyond GDP is to use a **dashboard**, which shows several indicators side by "
          "side instead of combining them into one number. The next demonstration shows how a dashboard can "
          "change a judgement based on GDP alone."),
    ("demo", "Reading a well-being dashboard", [
        "Country X has followed a high-growth strategy and scores 80 out of 100 on GDP per capita. Country Y has "
        "grown more slowly (score 60) but invested in health, education and environmental protection. Table 12 "
        "and Figure 17 show both countries on seven dimensions.",
        "= Average score: Country X = 375 / 7 = 53.6;  Country Y = 502 / 7 = 71.7",
        "**Lesson:** judged by GDP, Country X is ahead. Judged by the full dashboard, Country Y offers its people "
        "a better life on six of seven dimensions. A dashboard makes such trade-offs visible to policymakers and "
        "voters.",
    ]),
    ("table", T_DASH),
    ("fig", "f15_radar", "Well-being dashboard for two hypothetical countries", "Author's hypothetical example (Demonstration 5).", 118),

    # ------------------------------------------------------------------ 9
    ("h1", "9. Findings and Discussion", True),
    ("h2", "9.1 Key Findings"),
    ("ol", ["**GDP growth matters most where incomes are low.** The Preston curve and Bangladesh's poverty record "
            "show that growth is strongly linked to better health and lower poverty in poor countries.",
            "**The link weakens as countries get richer.** Above a certain income level, extra GDP adds little to "
            "life expectancy or happiness (Figures 3, 12 and 13).",
            "**GDP hides distribution.** Two countries with the same GDP can have very different living standards "
            "for the poor (Demonstration 2). Inequality in Bangladesh has risen even during rapid growth.",
            "**GDP counts some harms as gains.** Disasters, pollution-related illness and defensive spending can "
            "raise GDP while lowering well-being (Demonstration 3).",
            "**GDP ignores sustainability.** It counts the depletion of natural resources as income and does not "
            "subtract environmental damage (Figure 9).",
            "**GDP excludes unpaid and under-records informal work,** which is especially large in Bangladesh and "
            "falls mainly on women.",
            "**Alternative measures change the picture.** The HDI, GPI and life-evaluation data rank countries "
            "differently from GDP, and the GPI suggests that well-being stopped rising decades before GDP did."]),
    ("h2", "9.2 Discussion"),
    ("p", "The findings show that the answer to the research question depends on what we expect from GDP. As a "
          "measure of **market production**, GDP does exactly what it was designed to do, and it does so in a "
          "consistent and comparable way. Problems arise when GDP growth is used as a measure of **well-being** "
          "and becomes the main goal of policy. In that role, it gives an incomplete and sometimes misleading "
          "signal."),
    ("p", "It is also important not to swing to the opposite extreme. For a country like Bangladesh, where millions "
          "of people still live close to the poverty line, faster growth remains essential. The more useful "
          "question is not “growth or well-being?” but “what kind of growth?” Growth that creates "
          "decent jobs, is shared widely, invests in people and protects the environment will raise well-being. "
          "Growth that is concentrated, polluting or based on running down natural capital may raise GDP without "
          "improving lives, or may borrow well-being from the future."),

    # ------------------------------------------------------------------ 10
    ("h1", "10. Conclusion and Recommendations", True),
    ("h2", "10.1 Conclusion"),
    ("p", "This assignment asked whether GDP growth is an adequate measure of economic well-being. The evidence "
          "reviewed shows that GDP growth is **a necessary but not a sufficient** indicator. It captures the "
          "expansion of market production, which in poorer countries is closely tied to falling poverty and better "
          "health. But it does not show who benefits from growth, it leaves out unpaid and much informal work, it "
          "ignores environmental damage and the loss of leisure, it can rise because of disasters and defensive "
          "spending, and it is only weakly related to how satisfied people are with their lives in richer "
          "countries."),
    ("p", "Therefore, GDP growth is **not an adequate measure of economic well-being on its own**. It should be "
          "kept as one important indicator in a wider set that includes measures of distribution, human "
          "development, sustainability and subjective well-being. As Kuznets warned almost a century ago, the "
          "welfare of a nation cannot be read from national income alone."),
    ("h2", "10.2 Recommendations"),
    ("p", "Based on the findings, the following recommendations are made, with special reference to Bangladesh:"),
    ("ol", ["**Adopt a well-being dashboard.** The government should report GDP growth together with median "
            "household income, the Gini coefficient, poverty, HDI, informal employment and environmental "
            "indicators in the annual budget and the Bangladesh Economic Review.",
            "**Focus on median, not only average, income.** Median household income and the income of the bottom "
            "40 per cent better reflect what typical families experience.",
            "**Develop environmental accounts.** BBS should expand work under the UN SEEA framework to estimate "
            "the depletion of natural resources and the cost of pollution.",
            "**Value unpaid work.** Regular time-use surveys and satellite accounts for household work would make "
            "women's contribution visible in policy.",
            "**Strengthen data quality and independence.** Transparent methods and independent review of national "
            "accounts would increase trust in official statistics.",
            "**Link the dashboard to the SDGs.** Bangladesh already reports on the Sustainable Development Goals; "
            "these indicators can form the basis of a national well-being framework.",
            "**Teach beyond GDP.** Universities and the media should present GDP as a measure of economic "
            "activity, not as a scorecard of national success."]),
]

REFERENCES = [
    "Bangladesh Bureau of Statistics. (2023a). *Household Income and Expenditure Survey (HIES) 2022: Final report*. BBS.",
    "Bangladesh Bureau of Statistics. (2023b). *Labour Force Survey 2022*. BBS.",
    "Centre for Policy Dialogue. (2015). *Estimating women's contribution to the economy: The case of Bangladesh*. CPD.",
    "Chancel, L., Piketty, T., Saez, E., & Zucman, G. (2022). *World inequality report 2022*. World Inequality Lab.",
    "Easterlin, R. A. (1974). Does economic growth improve the human lot? Some empirical evidence. In P. A. David & M. W. Reder (Eds.), *Nations and households in economic growth* (pp. 89-125). Academic Press.",
    "Global Carbon Project. (2023). *Global carbon budget 2023*. https://globalcarbonbudget.org",
    "Helliwell, J. F., Layard, R., Sachs, J. D., De Neve, J.-E., Aknin, L. B., & Wang, S. (Eds.). (2024). *World happiness report 2024*. Wellbeing Research Centre, University of Oxford.",
    "International Labour Organization. (2018). *Care work and care jobs for the future of decent work*. ILO.",
    "Kennedy, R. F. (1968, March 18). *Remarks at the University of Kansas* [Speech]. Lawrence, Kansas.",
    "Kubiszewski, I., Costanza, R., Franco, C., Lawn, P., Talberth, J., Jackson, T., & Aylmer, C. (2013). Beyond GDP: Measuring and achieving global genuine progress. *Ecological Economics, 93*, 57-68.",
    "Kuznets, S. (1934). *National income, 1929-1932* (Senate Document No. 124). US Government Printing Office.",
    "Mankiw, N. G. (2021). *Principles of economics* (9th ed.). Cengage Learning.",
    "OECD. (2011). *How's life? Measuring well-being*. OECD Publishing.",
    "Osberg, L., & Sharpe, A. (2002). An index of economic well-being for selected OECD countries. *Review of Income and Wealth, 48*(3), 291-316.",
    "Preston, S. H. (1975). The changing relation between mortality and level of economic development. *Population Studies, 29*(2), 231-248.",
    "Sen, A. (1999). *Development as freedom*. Oxford University Press.",
    "Stevenson, B., & Wolfers, J. (2008). Economic growth and subjective well-being: Reassessing the Easterlin paradox. *Brookings Papers on Economic Activity, 2008*(1), 1-87.",
    "Stiglitz, J. E., Sen, A., & Fitoussi, J.-P. (2009). *Report by the Commission on the Measurement of Economic Performance and Social Progress*. Paris.",
    "Talberth, J., Cobb, C., & Slattery, N. (2007). *The Genuine Progress Indicator 2006: A tool for sustainable development*. Redefining Progress.",
    "United Nations. (2021). *System of Environmental-Economic Accounting: Ecosystem accounting (SEEA EA)*. United Nations.",
    "United Nations Development Programme. (2024). *Human development report 2023/2024: Breaking the gridlock*. UNDP.",
    "World Bank. (2018). *Enhancing opportunities for clean and resilient growth in urban Bangladesh: Country environmental analysis 2018*. World Bank.",
    "World Bank. (2024). *World development indicators*. https://databank.worldbank.org",
]

GLOSSARY = [
    ["Defensive expenditure", "Spending that protects against or repairs harm (e.g. flood repair) rather than adding new welfare."],
    ["Easterlin paradox", "The finding that average happiness in a country may not rise as its income per person grows over time."],
    ["Economic well-being", "People's command over resources needed for a good life now and in the future, including income, security, equality and wealth."],
    ["GDP per capita", "GDP divided by population; a rough indicator of average income."],
    ["Gini coefficient", "A measure of inequality from 0 (everyone has the same income) to 1 or 100 (one person has everything)."],
    ["Informal sector", "Economic activity that is not registered or regulated and usually offers no social protection."],
    ["Natural capital", "The stock of natural resources (forests, water, soil, minerals, clean air) that supports the economy."],
    ["Nominal GDP", "GDP measured at current prices."],
    ["Preston curve", "The relationship between income per person and life expectancy, steep at low incomes and flat at high incomes."],
    ["Purchasing power parity", "An exchange rate that adjusts for differences in price levels between countries."],
    ["Real GDP", "GDP measured at constant prices, showing changes in quantity rather than prices."],
    ["Satellite account", "An extension of the national accounts that covers an area such as unpaid work or the environment."],
]
