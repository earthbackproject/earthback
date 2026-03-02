-- SCHEMA_V10_seed.sql
-- INSERT statements for 30 construction methods
-- Auto-generated from methods.json
-- Date: 2026-03-02

TRUNCATE TABLE member_skills, construction_methods CASCADE;

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    1,
    'cob',
    'Cob Construction',
    'Monolithic sculpted earth — clay, sand, straw',
    'green',
    'moderate',
    '["Earth-Based", "Zero Waste"]'::JSONB,
    'Cob is one of humanity''s oldest and most enduring building traditions, with structures still standing after 500+ years in the UK, Yemen, and Morocco. The word "cob" comes from Old English meaning "lump" or "rounded mass." Walls are built by hand, sculpting a wet mixture of subsoil (rich in clay), coarse sand, and long-strand straw into a monolithic, load-bearing mass — no forms, no molds, no bricks.',
    '["Clay-rich subsoil (20\u201330% clay content)", "Coarse sharp sand", "Long-strand straw (wheat, rice, or barley)", "Water", "Lime or earthen plaster (finish)", "Stone or rubble trench foundation"]'::JSONB,
    '["Semi-arid and Mediterranean climates (ideal)", "Temperate climates with dry summers", "Avoid: high-rainfall zones without excellent roof protection", "Avoid: freeze-thaw cycles without lime stabilization", "Traditional use: Yemen, Morocco, UK, SW USA, New Zealand"]'::JSONB,
    '["Extremely low embodied energy \u2014 materials are local", "Excellent thermal mass for temperature regulation", "Fully biodegradable and non-toxic", "Sculpted into any organic shape \u2014 no formwork", "Pest-resistant (no voids or cavities)", "Fire-resistant", "Essentially zero material cost"]'::JSONB,
    '["Very labor-intensive and slow to build", "Not suitable for cold/wet climates without modification", "Low tensile strength \u2014 seismic design requires care", "Must cure before adding loads (weeks to months)", "Permitting can be difficult in some jurisdictions", "Requires ongoing plaster maintenance"]'::JSONB,
    '["Ianto Evans", "Michael Smith", "The Cob Research Institute", "Sasha Rabin & Lydia Doleman", "Kevin McCabe", "Natural Building Network"]'::JSONB,
    '01-cob'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    2,
    'adobe',
    'Adobe Construction',
    'Sun-dried earthen bricks — ancient &amp; proven worldwide',
    'green',
    'easy',
    '["Earth-Based", "Brick System"]'::JSONB,
    'Adobe is one of the most widespread building materials in human history, used continuously for over 10,000 years on every inhabited continent. The word "adobe" derives from Arabic/Egyptian roots meaning "the brick." Unlike fired brick, adobe bricks are simply formed from a wet clay-sand-straw mixture and left to dry in the sun — no kiln required, no fuel consumed.',
    '["Clay-rich subsoil (20\u201335% clay)", "Sand and/or gravel aggregate", "Straw, grass, or manure as binder fiber", "Water", "Optional: Portland cement or bitumen stabilizer (5\u201310%)", "Earthen or lime mortar for laying"]'::JSONB,
    '["Arid and semi-arid (classic \u2014 SW USA, N. Africa, Middle East)", "Hot-dry climates with significant day/night temperature swings", "Avoid: wet tropical climates without cement stabilization", "Avoid: prolonged freeze-thaw without protective plaster"]'::JSONB,
    '["Incredibly low cost \u2014 soil is essentially free", "No kiln firing \u2014 minimal embodied energy", "Superior thermal mass for desert climates", "Can be made on-site by unskilled labor", "Fully recyclable \u2014 bricks dissolve back to soil", "Excellent acoustic insulation", "Recognized in building codes (NM, AZ, CA)"]'::JSONB,
    '["Very susceptible to water erosion without protection", "Drying takes weeks \u2014 weather dependent", "Low tensile strength (seismic reinforcement required)", "Heavy \u2014 requires substantial foundation", "Not suitable for high-rainfall regions"]'::JSONB,
    '["Southwest Solaradobe School", "Paul G. McHenry Jr.", "Quentin Branch", "Adobe in Action", "Earth Architecture", "CRAterre (France)"]'::JSONB,
    '02-adobe'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    3,
    'rammed-earth',
    'Rammed Earth (Pisé de Terre)',
    'Compressed monolithic earth walls of extraordinary density and beauty',
    'green',
    'hard',
    '["Earth-Based", "High Strength"]'::JSONB,
    'Modern rammed earth often incorporates 5–10% Portland cement (Stabilized Rammed Earth or STRE) for improved water resistance and compressive strength, achieving 300–900 psi. Traditional (unstabilized) rammed earth achieves 150–400 psi — still stronger than most adobe.',
    '["Subsoil: 70% non-expansive gravel/sand, 30% clay-silt", "Optimal moisture content: 8\u201312%", "Portland cement (5\u201310% for STRE stabilization)", "Timber or steel formwork (reusable)", "Pneumatic or manual tamping equipment", "Rebar reinforcement for seismic zones"]'::JSONB,
    '["Arid, semi-arid, and Mediterranean (ideal)", "Temperate climates with good drainage", "Used extensively in Australia, SW USA, S. Africa, Spain", "Unstabilized: avoid heavy rainfall without protection", "STRE handles moderate-rainfall climates well"]'::JSONB,
    '["Spectacular layered aesthetic \u2014 high design value", "Exceptional thermal mass and acoustic performance", "Very high compressive strength (STRE)", "Low embodied energy (mostly local soil)", "Pest-proof, fire-resistant, non-toxic", "Lifespan measured in centuries", "Increasingly mainstream in architecture"]'::JSONB,
    '["Requires specialized formwork and equipment", "Labor-intensive \u2014 skilled operators needed", "Not all soils are suitable (testing required)", "Heavy \u2014 substantial foundation required", "Cement addition reduces \"pure\" sustainability", "Cold climates require insulated ISRE systems"]'::JSONB,
    '["Rammed Earth Works", "Earth Structures", "Paulhaus", "SIREWALL", "Walker Wingsore Architects", "CRAterre"]'::JSONB,
    '03-rammed-earth'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    4,
    'ceb',
    'Compressed Earth Blocks (CEB / CSEB)',
    'Machine-pressed stabilized earth bricks — precision earthen masonry',
    'green',
    'moderate',
    '["Earth-Based", "Scalable"]'::JSONB,
    'Compressed Earth Blocks (CEBs), also called Compressed Stabilized Earth Blocks (CSEBs), are produced by mechanically pressing a slightly moist mixture of soil (and often a small percentage of cement or lime) into precise, uniform blocks using a hand-operated or motorized hydraulic press. The blocks achieve compressive strengths of 300–1,200 psi without firing — far stronger than sun-dried adobe — making them suitable for multi-story load-bearing construction.',
    '["Subsoil with 10\u201330% clay content", "Sand/gravel aggregate", "Portland cement or lime (5\u201312% stabilization)", "Water (optimal moisture ~10\u201312%)", "CEB hydraulic press (hand or motorized)", "Optional: lime or earthen mortar for laying"]'::JSONB,
    '["Tropical, semi-arid, and temperate climates", "Widely used across sub-Saharan Africa, India, Latin America", "Cement stabilization allows use in wetter climates", "With lime render: suitable for moderate rainfall regions"]'::JSONB,
    '["Uniform, precise blocks \u2014 easy to build with", "No kiln firing \u2014 extremely low embodied energy", "Higher compressive strength than adobe", "On-site production eliminates transport costs", "Interlocking varieties need no mortar", "Suitable for multi-story construction", "Widely documented for building codes"]'::JSONB,
    '["Requires CEB press (capital investment or rental)", "Soil testing required for optimal mix", "Cement addition increases cost and carbon", "Lower insulation value than straw bale or hempcrete", "Heavy \u2014 strong foundation needed"]'::JSONB,
    '["AECT (Alternative Earth Construction Technology)", "Earth Block International", "Build Simple", "Auroville Earth Institute", "Dwell Earth", "CRAterre / ENSAG"]'::JSONB,
    '04-compressed-earth-blocks'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    5,
    'earthship',
    'Earthship',
    'Radically sustainable homes from tires, bottles &amp; recycled materials',
    'green',
    'hard',
    '["Recycled Materials", "Off-Grid Ready"]'::JSONB,
    'Earthships are a radical approach to sustainable architecture developed by American architect Michael Reynolds beginning in the 1970s in Taos, New Mexico. The defining structural element is used automobile tires packed tightly with rammed earth using sledgehammers, creating massive thermal mass "bricks" that weigh 300–400 lbs each.',
    '["Used automobile tires (primary structural element)", "Rammed earth (to fill tires)", "Recycled glass bottles and aluminum cans (infill walls)", "Adobe/earthen plaster", "Reclaimed lumber and metal roofing", "Solar panels, wind turbines, water cisterns"]'::JSONB,
    '["Semi-arid with cold nights (Taos, NM is ideal)", "Passive solar design requires southern sun exposure", "Adaptable to many climates with design modifications", "Cold/cloudy climates: supplemental heating needed", "Tropical models: modified cross-ventilation designs"]'::JSONB,
    '["Uses massive amounts of waste materials (tires, bottles)", "Designed for complete off-grid self-sufficiency", "Extraordinary thermal mass \u2014 naturally regulated temps", "Integrated food growing, water, and energy systems", "Unique aesthetic unlike any other architecture", "Can be owner-built with guidance"]'::JSONB,
    '["Packing tires is extremely labor-intensive", "Tire off-gassing concerns (debated; plastered walls minimize)", "Difficult to permit in many jurisdictions", "Passive solar works poorly in north-facing or cloudy sites", "Complex systems integration requires expertise", "Not well-suited to urban or suburban contexts"]'::JSONB,
    '["Earthship Biotecture", "Earthship Academy", "Earthship Europe", "Biotecture Planet Earth", "Documentary: \"Garbage Warrior\" (2007)", "Global Model Earthship"]'::JSONB,
    '05-earthship'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    6,
    'underground',
    'Earth-Sheltered &amp; Underground Construction',
    'Homes built into hillsides or bermed with earth for thermal stability',
    'green',
    'hard',
    '["Earth-Integrated", "Thermal Stability"]'::JSONB,
    'At a depth of just 4–8 feet below grade, soil temperature stabilizes at the local annual mean temperature (typically 50–60°F in temperate regions) year-round. This means earth-sheltered homes maintain comfortable temperatures with minimal energy input.',
    '["Reinforced concrete (most common structural system)", "Waterproofing membrane (critical)", "Drainage board and gravel backfill", "Structural timber or masonry (alternative systems)", "Earth backfill (on-site)", "Green roof growing medium + plants"]'::JSONB,
    '["All climates benefit from ground tempering", "Especially valuable in extreme cold or hot climates", "Requires good site drainage to avoid water issues", "Passive solar glazing orientation is critical", "Most used in North America, Europe, Australia"]'::JSONB,
    '["60\u201380% reduction in heating/cooling energy", "Natural disaster resistance (tornado, hurricane)", "Soundproofing from above-grade noise", "Minimal visual impact on landscape", "Green roof provides stormwater management", "Can combine with any structural system"]'::JSONB,
    '["Waterproofing is critical and costly if done incorrectly", "Limited natural light without careful design", "Significant earthwork and excavation costs", "Requires well-draining site", "Humidity management can be challenging", "High structural engineering requirements"]'::JSONB,
    '["Malcolm Wells", "Earth Shelter Technology", "Terracycle Homes", "Green Magic Homes", "Hobbit Houses", "Underground Space Center"]'::JSONB,
    '06-earth-sheltered-underground'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    7,
    'straw-bale',
    'Straw Bale Construction',
    'Agricultural waste as super-insulating wall systems',
    'green',
    'moderate',
    '["Agricultural Waste", "Super-Insulating"]'::JSONB,
    'Straw bale construction uses compressed bales of agricultural straw (wheat, rice, rye, barley, or oat — not hay, which retains seeds and nutrients) as either load-bearing structural walls (the "Nebraska style," developed on the Great Plains in the 1880s) or as infill insulation within a post-and-beam frame (the more modern approach, which is easier to engineer and permit). The bales are stacked like oversized bricks, tied together with pins (hazel rods, rebar, or bamboo), and then rendered inside and out with lime or earthen plaster to provide weather protection and fire resistance.',
    '["Straw bales (wheat, rice, rye \u2014 dry, tightly bound)", "Post-and-beam frame (timber, steel, or bamboo)", "Hazel or bamboo pins for bale connection", "Lime plaster (2\u20133 coats, inside and out)", "Earthen plaster (interior option)", "Rubble trench or concrete stem wall foundation"]'::JSONB,
    '["Cold and very cold climates (exceptional insulation)", "Temperate and semi-arid climates", "Used successfully in Montana, Canada, UK, Germany, Australia", "Hot-arid: less ideal (poor thermal mass) but works", "Avoid: high-humidity tropics without careful moisture management"]'::JSONB,
    '["Exceptional insulation (R-30 to R-45)", "Uses agricultural waste \u2014 very low cost material", "Carbon-sequestering \u2014 stores atmospheric carbon", "Excellent fire resistance when plastered", "Highly accessible DIY technique with workshops", "Beautiful thick-wall aesthetic", "Good acoustic insulation"]'::JSONB,
    '["Moisture is the critical risk \u2014 must stay dry", "Plaster application requires skill", "Not suitable without good roof overhangs", "Pest management required (mice love straw)", "Sourcing dry bales can be regional/seasonal", "Wall thickness reduces interior square footage"]'::JSONB,
    '["California Straw Building Association (CASBA)", "Amazon Nails", "The Last Straw Journal", "Strawbale.com", "Endeavour Centre", "Australian Straw Bale Association"]'::JSONB,
    '07-straw-bale'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    8,
    'hempcrete',
    'Hempcrete (Hemp-Lime)',
    'Carbon-negative biocomposite of hemp hurds and hydraulic lime',
    'green',
    'moderate',
    '["Hemp", "Carbon Negative"]'::JSONB,
    'Hempcrete walls are typically 12–16 inches thick and achieve insulation values of R-2.5 to R-3.7 per inch. More significantly, hemp-lime''s hygroscopic nature allows it to absorb and release moisture, acting as a humidity buffer and preventing condensation — a critical performance characteristic lacking in most conventional insulation systems.',
    '["Hemp hurds/shivs (woody hemp stem core)", "Hydraulic lime binder (NHL 3.5 or 5)", "Water", "Structural timber frame (carries all loads)", "Lime render/plaster (2\u20133 coats finish)", "Optional: hemp fabric insulation for roof/floor"]'::JSONB,
    '["Temperate, oceanic, and cool climates (ideal)", "Excellent in cold-humid climates where vapor management is critical", "UK, France, N. Europe \u2014 most developed market", "Canada, NE USA \u2014 growing adoption", "Can work in hot climates with design modifications"]'::JSONB,
    '["Certified carbon-negative (net CO2 storage)", "Excellent vapor management \u2014 breathable walls", "Natural humidity buffering (reduces indoor RH swings)", "Pest-resistant and mold-resistant", "Fire resistant (tested to BS EN standards)", "Lightweight \u2014 reduced foundation requirements", "30+ year track record in France"]'::JSONB,
    '["Not structural \u2014 requires separate load-bearing frame", "Hemp hurds not yet universally available", "Hydraulic lime can be tricky to work with", "Long cure time (lime continues hardening for months)", "Requires vapor-permeable finishes only (no vapor barriers)", "Building codes still limited in many US states"]'::JSONB,
    '["HempStone", "Lime Technology", "Hemp Technologies Global", "American Lime Technology", "Hemp Building Association", "Steve Allin", "Klara Marosszeky"]'::JSONB,
    '08-hempcrete-hemp-lime'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    9,
    'bamboo',
    'Bamboo Construction',
    'The world''s fastest-growing structural material — stronger than steel by weight',
    'green',
    'hard',
    '["Renewable", "High Strength"]'::JSONB,
    'Structural bamboo construction ranges from traditional vernacular forms in South and Southeast Asia (where over 1 billion people live in bamboo structures) to extraordinarily sophisticated contemporary architecture. Colombian architect Simón Vélez has pioneered engineering-grade bamboo construction, treating culms with borax solution (for pest resistance) and using concrete-filled connections at joints.',
    '["Structural bamboo culms (Guadua, Moso, Phyllostachys)", "Borax/boric acid treatment solution", "Concrete or steel connection nodes", "Engineered bamboo products (LBL, strand, CLB)", "Traditional: rope lashing (jute, rattan)", "Epoxy for modern joinery"]'::JSONB,
    '["Tropical and subtropical (native habitat)", "Used traditionally across SE Asia, India, C./S. America", "Engineered bamboo products suitable for temperate climates", "Moisture management critical in all climates", "Not ideal for prolonged below-freezing temperatures"]'::JSONB,
    '["Extraordinary tensile strength-to-weight ratio", "Fastest-growing renewable building material", "Carbon sequestration during growth", "Abundant and low-cost in tropical regions", "Naturally flexible \u2014 excellent seismic resistance", "Beautiful natural aesthetic", "Engineered products expanding applicability"]'::JSONB,
    '["Requires treatment to prevent insect and fungal attack", "Natural culms: non-standard sizing complicates engineering", "Connection design is the critical engineering challenge", "Not widely available in all regions (shipping adds embodied energy)", "Building codes limited outside tropical countries", "Engineered products: processing reduces green credentials"]'::JSONB,
    '["IBUKU", "Sim\u00f3n V\u00e9lez", "Bamboo Living", "International Bamboo and Rattan Organization (INBAR)", "ZERI Foundation", "ISO 22156", "BambooU"]'::JSONB,
    '09-bamboo'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    10,
    'cordwood',
    'Cordwood / Stackwall / Stackwood',
    'Log-ends stacked crosswise in mortar — ancient northern European tradition',
    'green',
    'easy',
    '["Wood-Based", "Low Waste"]'::JSONB,
    'Cordwood walls have excellent thermal performance, combining the insulating properties of the wood itself (end-grain is a poor conductor) with the thermal mass of the mortar matrix. A 16-inch cordwood wall achieves approximately R-20, with some builders claiming higher values.',
    '["Dry, debarked log sections (cedar, pine, poplar are favorites)", "Lime putty or hydraulic lime", "Sawdust (insulating mortar component)", "Sand and Portland cement (outer mortar)", "Post-and-beam frame (for larger structures)", "Glass bottles (optional decorative inserts)"]'::JSONB,
    '["Cold and subarctic climates (traditional range)", "Temperate continental climates", "Excellent in the Canadian Shield and upper Midwest", "Not recommended for hot-humid climates (moisture)", "Wood must be bone-dry before use (1\u20132 year seasoning)"]'::JSONB,
    '["Uses small-diameter \"waste\" wood efficiently", "No heavy equipment needed", "Excellent DIY-accessible technique", "Beautiful, unique aesthetic", "Good thermal performance (~R-20 at 16 inches)", "Locally sourced materials possible", "Can be built incrementally"]'::JSONB,
    '["Wood must be very dry \u2014 cracking if not seasoned", "Mortar cracking between wood and mortar is common", "Not suitable for seismically active zones without engineering", "Time-consuming \u2014 labor intensive for large walls", "High maintenance if moisture infiltrates", "Limited building code recognition in some areas"]'::JSONB,
    '["Robert Roy (RoyCroft)", "Cordwood Construction Council of North America", "Jack Henstridge", "Cliff Shockey", "Earthwood Building School"]'::JSONB,
    '10-cordwood-stackwall'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    11,
    'timber-frame',
    'Timber Frame / Post &amp; Beam',
    'Heavy structural timbers joined with traditional mortise &amp; tenon joinery',
    'green',
    'hard',
    '["Renewable Wood", "Centuries-Old"]'::JSONB,
    'Timber framing is a post-and-beam structural system using large, solid wood timbers (typically 6×6 inches or larger) connected with traditional woodworking joints — mortise and tenon, housed joints, and wooden pegs (trunnels) — rather than metal fasteners. This technique has been the dominant structural approach for large buildings across Europe, Japan, and North America for over 2,000 years.',
    '["Structural hardwood or softwood timbers (6\u00d76 and up)", "Wooden pegs (oak trunnels, traditionally)", "Infill of choice: SIPs, straw bale, hempcrete", "Engineered: glulam beams, CLT panels", "Hand tools: chisels, mallets, drawbore pins", "Crane or gin pole for raising"]'::JSONB,
    '["All climates \u2014 performance depends on infill choice", "Temperate and cold climates (historic heartland)", "Excellent in high-snow-load areas (strong roof structures)", "Tropical: wood selection critical for pest resistance", "Seismic: engineered connections required"]'::JSONB,
    '["Exceptional structural longevity (500+ year lifespan)", "Carbon stored in timber mass", "Infill flexibility \u2014 pair with any natural wall system", "Open floor plans \u2014 no load-bearing interior walls", "Stunning exposed interior aesthetic", "Repairable and adaptable over centuries", "FSC certification ensures sustainable sourcing"]'::JSONB,
    '["Highly skilled joinery \u2014 expensive labor", "High material cost vs. stick framing", "Frame raising requires crane or community effort", "Timber sourcing can be difficult in some regions", "Fire performance depends on timber size (large sections char slowly)"]'::JSONB,
    '["Timber Framers Guild", "New Energy Works", "Tedd Benson", "Jack Sobon", "Heartwood School", "Fox Maple School of Traditional Building"]'::JSONB,
    '11-timber-frame-post-and-beam'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    12,
    'log',
    'Log Construction',
    'Horizontal stacked logs forming solid, structural walls',
    'green',
    'hard',
    '["Solid Wood", "Mountain Heritage"]'::JSONB,
    'Log construction — the horizontal stacking of whole or milled logs to form solid, monolithic walls — is one of the oldest building traditions of forested northern regions. Unlike timber framing (where the structure and infill are separate), log walls are simultaneously structural, insulating, and the finished interior and exterior surface.',
    '["Whole logs: pine, spruce, cedar, fir, larch", "Chinking material (mortar, foam backer rod + sealant)", "Drift pins or lag screws for connection", "Chainsaw, drawknife, scribe for handcrafted", "Milled log systems: factory-processed", "Log stain/preservative for exterior protection"]'::JSONB,
    '["Cold and subarctic climates (traditional heartland)", "Dry mountain climates (ideal moisture conditions)", "Temperate continental climates", "Humid climates: require careful moisture management", "Most popular: Canada, Scandinavia, Alps, Rocky Mountains"]'::JSONB,
    '["Carbon stored in solid wood mass", "Walls are structural + finish in one (no cladding needed)", "Extraordinary aesthetic appeal \u2014 iconic character", "Excellent longevity when maintained (100\u2013500+ years)", "Good thermal mass performance", "Natural, non-toxic materials"]'::JSONB,
    '["Settling requires special design provisions", "Moderate insulation value only", "Requires significant log sourcing", "Handcrafted: highly skilled, expensive", "Requires regular exterior maintenance (staining)", "Fire risk higher than masonry systems"]'::JSONB,
    '["International Log Builders Association (ILBA)", "B. Allan Mackie", "Robert W. Chambers", "Pioneer Log Homes of BC", "Sitka Log Homes", "Log Home Living Magazine"]'::JSONB,
    '12-log-construction'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    13,
    'stone',
    'Natural Stone Masonry',
    'Fieldstone, rubble, and ashlar — the most ancient durable building material',
    'green',
    'hard',
    '["Natural Stone", "Timeless"]'::JSONB,
    'Stone walls have exceptional thermal mass (similar to rammed earth), high compressive strength (granite: 19,000–35,000 psi), and essentially indefinite lifespan when properly constructed. Traditional stone buildings found throughout the British Isles, Mediterranean, Middle East, and Himalayas have stood for hundreds of years.',
    '["Local fieldstone, granite, limestone, sandstone, slate", "Lime mortar (NHL 2 or 3.5 for traditional stone)", "Sand and aggregate for mortar", "Stone-cutting tools: hammer, cold chisel, angle grinder", "Rubble fill for wide walls", "Lintels: stone, timber, or steel over openings"]'::JSONB,
    '["All climates \u2014 stone is used worldwide", "Limestone and sandstone: avoid acid rain and freeze-thaw", "Granite: highly resistant to all weathering", "Dry stone especially suited to well-drained sites", "Traditional stone construction in every inhabited region"]'::JSONB,
    '["Potentially indefinite lifespan", "Zero manufacturing energy (for gathered fieldstone)", "Excellent thermal mass", "Non-toxic, natural, fully recyclable", "Extraordinary aesthetic character", "Pest-proof, fire-proof, rot-proof", "Can use entirely local materials"]'::JSONB,
    '["Very skilled labor required (expensive)", "Heavy \u2014 significant foundation required", "Low tensile strength \u2014 seismic reinforcement needed", "Transport of stone can have high carbon footprint", "Quarrying has environmental impacts", "Slow to build"]'::JSONB,
    '["Dry Stone Walling Association of Great Britain (DSWA)", "Stone Foundation", "Patrick McAfee", "Natural Building Collective", "Stonemason''s Yard", "Paul Webber"]'::JSONB,
    '13-natural-stone-masonry'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    14,
    'lime',
    'Lime-Based Construction',
    'Hydraulic lime as mortar, plaster, and binder — breathable and self-healing',
    'green',
    'moderate',
    '["Ancient Binder", "Breathable"]'::JSONB,
    'Limecrete (a lime-aggregate mixture) is used as an alternative to concrete for floor slabs in historic buildings and natural building. It is slower to develop strength but compatible with lime-built walls (unlike Portland cement, which creates incompatible moisture barriers).',
    '["Natural Hydraulic Lime (NHL 2, 3.5, or 5)", "Lime putty (non-hydraulic, for plasters)", "Sharp sand and aggregate", "Pozzolans (volcanic ash, brick dust \u2014 for ancient-style)", "Animal hair or plant fiber (plaster reinforcement)", "Hemp, flax, or jute fiber (for limecrete/hempcrete)"]'::JSONB,
    '["All climates \u2014 lime adapts to every situation", "Critical in humid/wet climates for vapor management", "Slow cure in cold (below 5\u00b0C) \u2014 protect from frost", "Ubiquitous in Mediterranean, European, and Asian traditions"]'::JSONB,
    '["Breathable \u2014 allows wall to dry and avoid trapped moisture", "Self-healing micro-cracks via carbonation", "Lower embodied energy than Portland cement", "Partial CO2 re-absorption during curing", "Compatible with all natural wall systems", "Flexible \u2014 less prone to cracking than cement", "Beautiful, tactile finish quality"]'::JSONB,
    '["Slow strength development", "Caustic \u2014 requires protective equipment", "Not suitable below 5\u00b0C without protection", "Less compressive strength than Portland cement", "Multi-coat plaster application requires skill", "Some hydraulic limes contain cement fractions"]'::JSONB,
    '["NHL Direct / Unilit", "Ty Mawr Lime", "The Lime Centre", "Holmes Lime", "Historic England / Historic Environment Scotland", "Roger Webb"]'::JSONB,
    '14-lime-based-construction'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    15,
    'earthbag',
    'Earthbag / Superadobe Construction',
    'Polypropylene bags or tubes filled with earth, stacked into arches and domes',
    'green',
    'easy',
    '["Earth-Based", "Disaster-Resilient"]'::JSONB,
    'Earthbag construction uses polypropylene grain sacks or long continuous tubes (Superadobe) filled with moist earth, stacked in courses and stabilized between rows with double strands of barbed wire (which acts as mortar and reinforcement). The concept was developed in the 1980s by Iranian-American architect Nader Khalili of Cal-Earth Institute, who envisioned it as emergency shelter and then refined it into permanent housing.',
    '["Polypropylene grain sacks or tube bags", "Local fill: earth, sand, gravel, or scoria", "Double-strand barbed wire (between courses)", "Lime or earthen plaster (exterior/interior finish)", "Tamping tool (manual)", "Optional: cement or lime stabilization of fill"]'::JSONB,
    '["Semi-arid and arid climates (ideal)", "All climates with appropriate fill and plaster", "Excellent in seismic zones (tested performance)", "Used in California, Middle East, Africa, Mexico", "Humid climates: requires cement-stabilized fill and lime plaster"]'::JSONB,
    '["Extremely low cost \u2014 fill material is free or cheap", "No specialized tools or equipment", "Suitable for dome and vault shapes (no formwork)", "Good seismic performance (tested)", "Owner-builder accessible", "Uses local materials", "Thermal mass performance"]'::JSONB,
    '["Polypropylene bags degrade in UV \u2014 must be plastered promptly", "Labor-intensive filling and tamping", "Barbed wire is hazardous during construction", "Not widely recognized in building codes", "Dome forms require careful geometry", "Scoria fill improves insulation but is region-specific"]'::JSONB,
    '["Cal-Earth Institute", "Owen Geiger", "Kelly Hart", "Patti Stouter", "Ecology of a Cracker Barrel", "UNHCR / Red Cross"]'::JSONB,
    '15-earthbag-superadobe'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    16,
    'papercrete',
    'Papercrete',
    'Recycled paper pulp + cement or lime — lightweight insulating panels and blocks',
    'green',
    'easy',
    '["Recycled", "Lightweight"]'::JSONB,
    'Papercrete is a composite building material made from recycled waste paper (newspaper, cardboard, or scrap paper) mixed with water, Portland cement (or lime), and sometimes sand. The paper is pulped in a tow mixer or tow-mixer contraption (a large cement mixer with slurry paddles), blended with binders, and cast into blocks or panels, or applied as an insulating plaster coat.',
    '["Waste paper (newspaper, cardboard, any paper)", "Water", "Portland cement or lime (binder)", "Sand (optional \u2014 for added density)", "Tow mixer or modified cement mixer", "Block molds or panel forms"]'::JSONB,
    '["Arid and semi-arid climates (best performance)", "Not suitable for wet or humid climates without excellent protection", "Most use in SW USA, New Mexico, Arizona, Mexico", "With lime plaster protection: moderate climates possible"]'::JSONB,
    '["Uses 100% waste paper \u2014 extremely low material cost", "Lightweight \u2014 easy to handle and cut", "Good insulation value", "Can be made with simple DIY equipment", "Nailable and workable like wood", "Excellent sound absorption"]'::JSONB,
    '["Highly moisture-absorbent \u2014 must be sealed", "Low compressive strength \u2014 not structural", "Requires cement or lime binder (embodied energy)", "Fire risk if not properly treated", "No building code recognition", "Pest attraction if wet"]'::JSONB,
    '["Gordon Solberg", "Mike McCain", "Papercrete.com", "The Last Straw Journal", "Natural Building Network"]'::JSONB,
    '16-papercrete'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    17,
    'ferro',
    'Ferro-Cement',
    'Thin cement mortar over wire mesh — for curved, shell structures',
    'green',
    'moderate',
    '["Shell Structures", "Minimal Material"]'::JSONB,
    'Ferro-cement (or ferrocement) is a composite building system consisting of a thin layer (3/4 to 1.5 inches) of cement mortar reinforced by multiple layers of closely-spaced wire mesh (chicken wire, welded wire mesh, or fine galvanized wire mesh). The technique was pioneered by French engineer Joseph-Louis Lambot in the 1840s for boat construction and was later promoted by Pier Luigi Nervi for thin-shell architectural structures in the 20th century.',
    '["Chicken wire or welded wire mesh (galvanized)", "Fine wire mesh (hardware cloth)", "Portland cement and sand mortar (1:2 to 1:1.5)", "Steel rod armature (for shaping structure)", "Water and admixtures", "Lime (optional partial replacement)"]'::JSONB,
    '["All climates \u2014 very versatile system", "Excellent in marine and coastal environments", "Hot and humid climates: popular in Africa, Asia, Latin America", "Cold climates: thin shell requires insulation layer"]'::JSONB,
    '["Extraordinary structural efficiency for thin shells", "Very low material cost", "Enables complex curved and organic forms", "Highly crack-resistant", "Durable in marine/humid environments", "No formwork needed for shell structures", "Low embodied energy relative to strength"]'::JSONB,
    '["Labor-intensive hand plastering", "Portland cement is primary material (embodied CO2)", "Low insulation value \u2014 requires separate insulation", "Corrosion of mesh if not fully encased", "Complex doubly-curved geometry requires skill", "Not recognized in most residential building codes"]'::JSONB,
    '["Pier Luigi Nervi", "Nader Khalili", "FAO (Food and Agriculture Organization, UN)", "Fernando Minke", "Cement and Concrete Research Journal"]'::JSONB,
    '17-ferro-cement'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    18,
    'mycelium',
    'Mycelium / Mushroom Construction',
    'Fungal mycelium grown into structural panels and blocks — fully compostable',
    'green',
    'hard',
    '["Biocomposite", "Fully Compostable"]'::JSONB,
    'Mycelium composites were commercialized by Ecovative Design (New York) beginning around 2010 for packaging and insulation. Their material — Myco Board, Hempcrete, and various panel systems — competes with EPS foam in insulation applications while being 100% compostable at end of life.',
    '["Agricultural waste substrate (hemp hurds, straw, sawdust)", "Fungal mycelium inoculant (Ganoderma, Pleurotus)", "Water and incubation environment", "Molds for block or panel shaping", "Heat for inactivation after growth", "Surface sealer (optional \u2014 beeswax, shellac)"]'::JSONB,
    '["Interior use currently most appropriate", "Exterior applications require protective cladding", "Not yet proven for direct weathering exposure", "Research ongoing for all-climate exterior applications"]'::JSONB,
    '["100% compostable and biodegradable", "Uses waste agricultural material as substrate", "Very low embodied energy (no high-temperature processing)", "Good insulation properties", "Fire-resistant (chars, does not sustain flame)", "Can be grown into any mold shape", "Rapidly advancing technology"]'::JSONB,
    '["Low compressive strength compared to conventional materials", "Moisture sensitivity \u2014 must be kept dry", "Production requires controlled incubation environment", "Not yet code-approved for structural applications", "Technology still maturing for full-scale construction", "Scale of production limited"]'::JSONB,
    '["Ecovative Design", "The Living Architecture", "WASP", "Arup / Biohm", "Mogu", "MIT Media Lab / Self-Assembly Lab"]'::JSONB,
    '18-mycelium-mushroom'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    19,
    'green-roofs',
    'Living / Green Roofs &amp; Walls',
    'Vegetated surfaces for insulation, stormwater, habitat, and thermal mass',
    'green',
    'moderate',
    '["Biodiverse", "Stormwater"]'::JSONB,
    'Green roofs provide insulation (R-value depends on substrate depth and saturation), reduce the urban heat island effect, manage stormwater (retaining 50–90% of rainfall), extend roof membrane life by protecting it from UV and thermal cycling, and provide habitat for pollinators and birds. The Norse tradition of turf roofs (Iceland, Norway, Faroe Islands) demonstrates the technology''s ancient roots — turf roofs on Icelandic farmhouses have been used for over 1,000 years.',
    '["Root-resistant waterproofing membrane", "Drainage board (egg-crate or dimple mat)", "Filter fabric (geotextile)", "Growing medium (extensive: 80% pumice/perlite; intensive: soil)", "Drought-tolerant plants (sedum, wildflowers, grasses)", "Irrigation system (intensive roofs)"]'::JSONB,
    '["Temperate, oceanic, and continental climates", "Well-suited to Northern Europe, Pacific NW, UK", "Hot-dry climates: higher irrigation demand", "Cold climates: sedum species highly frost-tolerant", "All climates benefit from storm water management"]'::JSONB,
    '["50\u201390% stormwater retention", "Extends roof membrane life 2\u20133\u00d7 (UV and thermal protection)", "Urban heat island reduction", "Habitat and biodiversity", "Additional insulation layer", "Qualifies for many green building certifications", "Psychological and aesthetic benefits"]'::JSONB,
    '["Added structural load \u2014 requires engineering", "Higher upfront cost than conventional roofing", "Access for maintenance", "Intensive: significant irrigation requirements", "Waterproofing failures are difficult to diagnose", "Limited DIY accessibility without experience"]'::JSONB,
    '["Green Roofs for Healthy Cities", "ZinCo", "Bauder", "American Society of Landscape Architects (ASLA)", "Dusty Gedge", "Ambius / Biotecture"]'::JSONB,
    '19-living-green-roofs-walls'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    20,
    'bottle',
    'Bottle / Glass Brick Construction',
    'Recycled glass bottles and cans mortared into translucent, colorful walls',
    'green',
    'easy',
    '["Recycled Glass", "Decorative"]'::JSONB,
    'Bottle construction — using whole glass bottles (wine bottles, beer bottles, liquor bottles) set horizontally in mortar as non-load-bearing wall infill — is one of the most visually spectacular natural building techniques. When sunlight passes through a bottle wall, the interior glows with rich colors from the glass.',
    '["Glass bottles (wine, beer, spirits \u2014 uniform size ideal)", "Mortar: lime, earthen, or Portland-based", "Tape (for joining bottle pairs)", "Structural frame (bottles are infill, not structural)", "Aluminum cans (alternative for smaller-scale walls)", "Lime plaster for surrounding structure"]'::JSONB,
    '["All climates (glass is non-degrading)", "Tropical: excellent durability", "Cold: thermal mass helps but bottles can crack at extreme freeze", "South-facing bottle walls harvest significant solar gain"]'::JSONB,
    '["Uses waste glass \u2014 zero cost material", "Extraordinary beauty and light effects", "High thermal mass", "Air-filled bottles add insulation", "No specialist skills required", "Excellent for community building projects", "Glass is inert, non-toxic, durable"]'::JSONB,
    '["Non-structural \u2014 infill only", "Significant material collection required", "Limited thermal insulation (unless bottles sealed with air)", "Challenging to achieve weather-tight mortar joints", "Not recognized in building codes", "Labor-intensive for large areas"]'::JSONB,
    '["Earthship Biotecture", "Daniel Phillips", "Global Bottle Village", "Grandma Prisbrey''s Bottle Village", "Natural Building Blog"]'::JSONB,
    '20-bottle-glass-brick'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    21,
    'recycled',
    'Recycled &amp; Upcycled Material Construction',
    'Shipping containers, reclaimed lumber, pallets, and salvaged materials',
    'green',
    'moderate',
    '["Circular Economy", "Diverse"]'::JSONB,
    'Shipping container architecture has become mainstream: ISO containers are dimensionally standardized, structurally robust (designed to stack 9 containers high loaded), and readily available globally. However, they require significant insulation (the steel shell is a thermal bridge), cutting and reinforcement for openings, and their apparent "sustainability" is debated — shipping vast steel boxes for housing may have higher embodied energy than locally sourced alternatives.',
    '["ISO shipping containers (20ft, 40ft, high-cube)", "Reclaimed lumber (barn wood, old-growth beams)", "Salvaged brick and stone", "Reclaimed windows, doors, hardware", "EUR/EPAL wooden pallets", "Salvaged steel, roofing, and piping"]'::JSONB,
    '["All climates \u2014 depends on materials used", "Containers: all climates with insulation strategy", "Reclaimed wood: temperate and dry climates best", "Coastal: check for paint/chemical history of containers"]'::JSONB,
    '["Diverts materials from landfill", "Near-zero embodied energy for salvaged materials", "Containers: structurally proven, fast to assemble", "Reclaimed lumber: superior quality and character", "Cost savings on materials (often free or cheap)", "Unique, one-of-a-kind aesthetic"]'::JSONB,
    '["Containers: poor insulation, thermal bridging, chemical residues", "Sourcing and quality assessment requires expertise", "Structural engineers needed for container modifications", "Pallets: not suitable as primary structure", "Lead paint and chemical treatment risks in old materials", "Permitting can be complex"]'::JSONB,
    '["Poteet Architects", "LOT-EK", "Container City", "Planet Reuse", "The Reuse People of America", "Salvage Style Magazine"]'::JSONB,
    '21-recycled-upcycled-materials'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    22,
    'wattle',
    'Wattle &amp; Daub',
    'Woven stick lattice daubed with clay, dung, and straw — 6,000 year-old tradition',
    'green',
    'easy',
    '["Ancient Tradition", "Earth-Based"]'::JSONB,
    'Wattle and daub is one of the oldest surviving building techniques, with evidence of use dating back 6,000+ years and examples found on every inhabited continent. The "wattle" is a woven lattice of flexible sticks, branches, or reeds (typically hazel, willow, oak lath, or bamboo) interwoven between upright posts or studs.',
    '["Wattle: hazel, willow, bamboo, or oak riven lath", "Clay subsoil", "Sand", "Animal dung (cow, horse, or donkey)", "Chopped straw or other fiber", "Lime wash or plaster (finish coat)"]'::JSONB,
    '["Temperate climates (traditional European heartland)", "Semi-arid and warm climates", "Requires good roof protection from driving rain", "Traditional across Europe, Africa, Asia, Americas", "Not suitable for high-moisture climates without lime plaster"]'::JSONB,
    '["Materials entirely free and local", "No tools required", "Low skill barrier to start", "Completely biodegradable", "Proven 6,000-year lifespan", "Historical restoration applications", "Excellent for teaching natural building"]'::JSONB,
    '["Non-structural \u2014 infill only", "Low thermal performance", "Requires ongoing maintenance", "Cracking common without fiber reinforcement", "Not suitable as primary wall in cold climates", "No code recognition as a contemporary method"]'::JSONB,
    '["Weald and Downland Living Museum", "SPAB (Society for the Protection of Ancient Buildings)", "Natural Building Network", "CRAterre", "Traditional Building Forum"]'::JSONB,
    '22-wattle-and-daub'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    23,
    'pumice',
    'Pumice &amp; Volcanic Stone Construction',
    'Lightweight volcanic aggregates for insulating masonry and concrete',
    'green',
    'moderate',
    '["Volcanic", "Insulating"]'::JSONB,
    'Pumice and volcanic scoria (also called "cinder" or "lava rock") are naturally occurring porous volcanic rocks with exceptionally low density and good insulating properties. Pumice — the extremely light, glassy volcanic foam — has a density of only 25–50% of regular rock, and its countless trapped air pockets give it an insulation value of approximately R-0.9 to R-1.3 per inch as masonry.',
    '["Pumice block (whole masonry units)", "Volcanic scoria/cinder aggregate", "Portland cement or lime binder", "Water", "Pozzolanic volcanic ash (for Roman-style concrete)", "Standard masonry mortar"]'::JSONB,
    '["All climates where volcanic material is locally available", "Cold climates: pumice fill in earthbags is excellent", "Mediterranean: traditional pumice block construction", "Iceland, Canary Islands, Pacific NW, Hawaii, E. Africa"]'::JSONB,
    '["Natural material requiring no manufacturing", "Lightweight \u2014 easy to handle and build with", "Good insulation value for a masonry material", "Free or very low cost where locally available", "Non-toxic, pest-proof, fire-proof", "Pozzolanic ash creates extraordinarily durable concrete"]'::JSONB,
    '["Highly regional \u2014 only available near volcanic areas", "Lower compressive strength than dense stone", "Porous \u2014 requires weather protection", "Transport from volcanic regions negates green benefits", "Inconsistent quality between deposits"]'::JSONB,
    '["Iceland Pumice Association", "Pumice Products Association", "Cal-Earth Institute", "Owen Geiger", "Roman Concrete Research (Marie Jackson, UC Berkeley)"]'::JSONB,
    '23-pumice-volcanic-stone'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    24,
    'stud-frame',
    'Wood Stud Frame (Platform / Stick Frame)',
    'The dominant North American residential construction method',
    'conventional',
    'moderate',
    '["Conventional", "Fast Build"]'::JSONB,
    'Platform (stick) framing is by far the most common residential construction method in North America, accounting for over 90% of new single-family homes. It uses dimensional lumber (2×4 or 2×6 studs) at 16 or 24 inches on center, sheathed with OSB or plywood for lateral stability, then clad in any exterior finish.',
    '[]'::JSONB,
    '[]'::JSONB,
    '["Universal code compliance \u2014 fastest permitting", "Fast construction timeline", "Familiar to all contractors \u2014 competitive pricing", "Easily modified and repaired", "Compatible with all insulation types", "Engineered lumber products improve sustainability"]'::JSONB,
    '["Relatively short design lifespan vs. masonry", "High embodied energy from lumber processing", "Thermal bridging through studs reduces R-value", "Poor air sealing without careful detailing", "Vulnerable to fire, moisture damage, and pests", "Relies on new-growth timber (old-growth long gone)"]'::JSONB,
    '[]'::JSONB,
    '24-wood-stud-frame'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    25,
    'cmu',
    'Concrete Masonry Units (CMU / Cinder Block)',
    'Hollow concrete block — universal commercial and residential masonry',
    'conventional',
    'moderate',
    '["Conventional", "High Strength"]'::JSONB,
    'Concrete Masonry Units (CMUs, commonly called "cinder blocks" or "breeze blocks") are hollow rectangular concrete blocks manufactured to precise dimensions (typically 8×8×16 inches nominal), stacked in courses with mortar, and often reinforced with vertical rebar through the hollow cores (which are then grouted). CMU is the most widely used masonry system in the Americas, Caribbean, Middle East, and parts of Africa — particularly popular in hot, humid, and hurricane-prone regions.',
    '[]'::JSONB,
    '[]'::JSONB,
    '["Universal availability and code compliance", "Excellent fire, pest, and rot resistance", "Hurricane and tornado resistant", "Long lifespan (100+ years)", "Lower thermal mass than poured concrete", "AAC variant: low density, high insulation"]'::JSONB,
    '["High Portland cement embodied energy", "Poor insulation (standard block ~R-2)", "Thermal bridging through mortar joints", "Heavy \u2014 significant foundation", "Not breathable \u2014 can trap moisture", "Cold to the touch \u2014 poor comfort without insulation"]'::JSONB,
    '[]'::JSONB,
    '25-concrete-masonry-cmu'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    26,
    'icf',
    'Insulated Concrete Forms (ICF)',
    'Foam block formwork filled with poured concrete — strong and insulating',
    'conventional',
    'moderate',
    '["Conventional", "Well-Insulated"]'::JSONB,
    'ICF (Insulated Concrete Forms) are hollow interlocking foam blocks (typically EPS — expanded polystyrene) that are stacked like Lego bricks, reinforced with rebar, and then filled with poured concrete. The foam forms stay in place permanently after the concrete cures, providing continuous insulation on both sides of a monolithic concrete wall.',
    '[]'::JSONB,
    '[]'::JSONB,
    '["Excellent insulation + thermal mass combination", "Extraordinary disaster resistance", "Faster than conventional poured concrete", "Good air sealing naturally achieved", "Code-compliant everywhere", "Quiet interior (excellent sound attenuation)"]'::JSONB,
    '["High Portland cement and EPS embodied energy", "EPS is petroleum-based and non-recyclable", "Heavy \u2014 requires good foundation", "More expensive than stick frame", "Prone to termite damage in foam (some species)", "Modifications after pour are difficult"]'::JSONB,
    '[]'::JSONB,
    '26-insulated-concrete-forms-icf'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    27,
    'sip',
    'Structural Insulated Panels (SIPs)',
    'Factory-made foam sandwich panels — fast, airtight, highly insulated',
    'conventional',
    'moderate',
    '["Conventional", "Engineered"]'::JSONB,
    'Structural Insulated Panels (SIPs) are factory-made composite panels consisting of a rigid foam insulation core (EPS, XPS, or polyurethane) sandwiched between two structural facing boards (typically OSB). They are manufactured in a range of thicknesses (typically 4–12 inches) and can be cut to order, then assembled on site like a giant 3D puzzle.',
    '[]'::JSONB,
    '[]'::JSONB,
    '["Very fast erection \u2014 1\u20133 days for shell", "Excellent insulation (R-14 to R-52)", "Superior air sealing vs. stick frame", "Consistent quality (factory-made)", "Straw-core SIPs available for green building", "Ideal for Passive House construction"]'::JSONB,
    '["EPS/XPS foam: petroleum-based, difficult to recycle", "Higher upfront cost than stick framing", "Requires crane for larger panels", "Joints between panels are critical air-sealing points", "Electrical and plumbing require pre-cut chases", "Modifications on site are difficult"]'::JSONB,
    '[]'::JSONB,
    '27-structural-insulated-panels-sip'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    28,
    'brick',
    'Fired Brick Masonry',
    'Kiln-fired clay bricks — the most universal durable building material',
    'conventional',
    'moderate',
    '["Conventional", "Durable"]'::JSONB,
    'Fired brick is the most widely used masonry material in the world, manufactured by shaping clay into rectangular units and firing them in a kiln at 900–1,200°C to achieve a ceramic hardness. Fired bricks have been used in construction since at least 3,000 BCE (Indus Valley civilization).',
    '[]'::JSONB,
    '[]'::JSONB,
    '["Extraordinary durability \u2014 200\u2013500+ year lifespan", "Waterproof and frost-resistant", "Fire-resistant", "Excellent thermal mass", "Reclaimed bricks: near-zero embodied energy", "Universal code compliance", "Timeless aesthetic appeal"]'::JSONB,
    '["Kiln firing: high energy and CO2 in production", "Heavy \u2014 substantial foundation required", "Low tensile strength \u2014 seismic reinforcement needed", "Poor insulation \u2014 must be combined with insulation layer", "Skilled bricklayers are expensive", "New brick production depletes clay deposits"]'::JSONB,
    '[]'::JSONB,
    '28-brick-masonry'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    29,
    'steel',
    'Steel Frame Construction',
    'Light gauge or structural steel framing — precise, non-combustible, recyclable',
    'conventional',
    'hard',
    '["Conventional", "Engineered"]'::JSONB,
    'The primary sustainability concern with new steel is its very high embodied energy — steel production accounts for approximately 7–9% of global CO2 emissions. However, structural steel made from recycled scrap (electric arc furnace — EAF) has approximately 1/4 the embodied carbon of virgin steel.',
    '[]'::JSONB,
    '[]'::JSONB,
    '["100% recyclable \u2014 circular material", "Non-combustible (will not burn)", "Dimensionally stable \u2014 no warping or settling", "Enables long spans and open floor plans", "Precise, factory-manufactured components", "EAF recycled steel: substantially lower carbon"]'::JSONB,
    '["Very high embodied energy (new steel)", "Severe thermal bridging in light gauge systems", "Corrosion requires protection in humid/coastal environments", "Steel loses strength rapidly in fire (1000\u00b0F)", "Specialized connections and engineering required", "Poor acoustics without isolation"]'::JSONB,
    '[]'::JSONB,
    '29-steel-frame'
);

INSERT INTO construction_methods (
    sort_order, slug, name, subtitle, category, difficulty,
    badges, description, materials, climates, pros, cons,
    practitioners, image_folder
) VALUES (
    30,
    'concrete',
    'Poured / Cast-in-Place Reinforced Concrete',
    'The structural backbone of the modern built environment',
    'conventional',
    'hard',
    '["Conventional", "Strongest"]'::JSONB,
    'Poured reinforced concrete (RC) — Portland cement mixed with sand and aggregate, poured into formwork around a steel rebar cage — is the most widely used structural material in the world. It combines concrete''s excellent compressive strength with steel rebar''s tensile strength to create a composite that can form virtually any shape and handle virtually any load.',
    '[]'::JSONB,
    '[]'::JSONB,
    '["Extraordinary structural versatility", "Can form any shape with appropriate formwork", "Excellent compressive strength", "Fire-resistant", "Pest-resistant, rot-resistant", "Geopolymer and SCM variants reduce carbon significantly", "Universal code compliance"]'::JSONB,
    '["Highest embodied carbon of any major material (cement)", "Near-zero insulation value", "Heavy \u2014 requires deep foundations", "Formwork is expensive and wasteful", "Cracks over time without proper detailing", "Difficult to recycle (downcycled to aggregate only)", "Cold and hard \u2014 poor biophilic quality"]'::JSONB,
    '["Carbon Cure Technologies", "Prometheus Materials", "CCAA (Cement Concrete & Aggregates Australia)", "Global Cement and Concrete Association (GCCA)", "Geopolymer Institute"]'::JSONB,
    '30-poured-cast-concrete'
);

