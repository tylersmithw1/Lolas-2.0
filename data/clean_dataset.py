"""Script to sub sample data."""

from data_cleaner import DataCleaner

dc: DataCleaner = DataCleaner("products_updated.xlsx")

dc.drop("updated")


# convert units in columns
dc.convert_m_to_grams("fat")
dc.convert_m_to_grams("transfat")
dc.convert_m_to_grams("saturatedfat")
dc.convert_m_to_grams("carbohydrates")
dc.convert_m_to_grams("sugar")
dc.convert_m_to_grams("salt")
dc.convert_m_to_grams("fibre")
dc.convert_m_to_grams("protein")


# standardising 'energykcal' column
dc.remove_text("energykcal", "cal")
dc.strip_spaces("energykcal")
dc.to_float("energykcal")


# remove text from servings per container column
dc.remove_text("servingspercontainer", "About")
dc.strip_spaces("servingspercontainer")
dc.remove_text("servingspercontainer", "ABOUT")
dc.strip_spaces("servingspercontainer")
dc.remove_text("servingspercontainer", "servings")
dc.strip_spaces("servingspercontainer")


# standardising 'servingsize' column
dc.convert_fl_oz_to_ml("servingsize")
dc.strip_spaces("servingsize")
dc.convert_oz_to_g("servingsize")
dc.clean_bracketed_values("servingsize")
dc.extract_bracketed_value("servingsize")
dc.strip_spaces("servingsize")
dc.convert_package_based_size("servingsize")
dc.strip_spaces("servingsize")
dc.convert_cups_to_ml("servingsize")
dc.strip_spaces("servingsize")
dc.convert_tbsp_to_g("servingsize")
dc.strip_spaces("servingsize")


# standardise columns to per 100g or 100ml
dc.standardize_column("energykcal")
dc.standardize_column("fat")
dc.standardize_column("saturatedfat")
dc.standardize_column("transfat")
dc.standardize_column("carbohydrates")
dc.standardize_column("sugar")
dc.standardize_column("salt")
dc.standardize_column("fibre")
dc.standardize_column("protein")


# flag UPF
ultraprocessed_ingredients = [
    "AGAVE",
    "FRUCTOSE",
    "NULOMOLINE",
    "BARLEY MALT SYRUP",
    "GALACTOSE",
    "ORGANIC BARLEY MALT SYRUP",
    "CANE JUICE",
    "GLUCOSE",
    "PALATINOSE",
    "CANEJUICE",
    "GOMME",
    "PANELA",
    "CANE SWEETENER",
    "HONEY",
    "PILONCILLO",
    "CLINTOSE",
    "HONI-BAKE",
    "SACCHAROSE",
    "COCONUT NECTAR",
    "HONI BAKE",
    "SORBOSE",
    "HONI FLAKE",
    "SUCROVERT",
    "CORN SWEET",
    "HONIFLAKE",
    "SUGAR",
    "CORN SWEETENER",
    "ISOGLUCOSE",
    "SUGARS",
    "CORNSWEETENER",
    "ISOMALTULOSE",
    "SWEET’N’NEAT",
    "DEMERARA",
    "JAGGERY",
    "SWEETNNEAT",
    "DEXTROSE",
    "KONA-AME",
    "SWEETN NEAT",
    "DISACCHARIDE",
    "KONA AME",
    "SWEET NNEAT",
    "DISACCHARIDES",
    "KONAAME",
    "SWEET N NEAT",
    "DRI-MOL",
    "LACTOSE",
    "SYRUP",
    "DRI MOL",
    "MALTOSE",
    "TAGATOSE",
    "DRIMOL",
    "MIZU-AME",
    "TREACLE",
    "DRI-SWEET",
    "MIZU AME",
    "TREHALOSE",
    "DRI SWEET",
    "MIZUAME",
    "TRUSWEET",
    "DRISWEET",
    "MOLASSES",
    "TRU SWEET",
    "FLO-MALT",
    "MONOSACCHARIDE",
    "TURBINADO",
    "FLO MALT",
    "MONOSACCHARIDES",
    "VERSATOSE",
    "FLOMALT",
    "MUSCOVADO",
    "YACON",
    "MALT",
    "BARLEY MALT",
    "POLYGLYCITOL SYRUP",
    "BARLEY MALT EXTRACT",
    "REDUCED LACTOSE WHEY",
    "BARLEY MALT FLOUR",
    "SORBITOL SYRUP",
    "D-GLUCITOL SYRUP",
    "SUGAR ALCOHOL",
    "HYDROGENATED GLUCOSE SYRUP",
    "SUGAR LEAF",
    "HYDROGENATED ISOMALTULOSE",
    "SUGAR SUBSTITUTE",
    "MALT EXTRACT",
    "SUGAR TWIN",
    "MALT EXTRACTS",
    "SUCROSE ACETATE ISOBUTYRATE",
    "MALTITOL SYRUP",
    "LACTOSE ENZYME",
    "NO SUGAR ADDED",
    "LACTOSE FREE",
    "ORGANIC BARLEY MALT",
    "LACTOSE-FREE",
    "ORGANIC BARLEY MALT EXTRACT",
    "SUGARCANE FIBER",
    "ORGANIC SPROUTED BARLEY",
    "MALTO",
    "MALTITOL",
    "ISOMALT",
    "BIOSALT",
    "BRINE",
    "PRAGUE POWDER",
    "SALT",
    "SLAT",
    "SODIUM CHLORIDE",
    "AMMONIUM CARBONATE",
    "PYROPHOSPHATE SODIUM ACID",
    "SODIUM HYDROXIDE",
    "ANTIOXIDANT ERYTHORBIC ACID",
    "SODIUM ACETATE",
    "SODIUM LACTATE",
    "ASCORBIC ACID",
    "SODIUM ALGINATE",
    "SODIUM NITRITE",
    "CITRATE OF SODIUM",
    "SODIUM ASCORBATE",
    "SODIUM METABISULPHITE",
    "CITRUS ACID",
    "SODIUM BENZOATE",
    "SODIUM MONO GLUTAMATE",
    "DISODIUM PHOSPHATE",
    "SODIUM BICARBONATE",
    "SODIUM MONOGLUTAMATE",
    "EDTA DISODIUM OF CALCIUM",
    "SODIUM BISULFITE",
    "SODIUM PHOSPHATE",
    "EMULSIFYNG SALTS",
    "SODIUM CARBONATE",
    "SODIUM PROPIONATE",
    "MONOSODIUM GLUTAMATE",
    "SODIUM CARBOXYMETHYLCELLULOSE",
    "SODIUM PYROPHOSPHATE",
    "POLYPHOSPHATES OF SODIUM",
    "SODIUM CITRATE",
    "SODIUM SELENATE",
    "POTASSIUM LACTATE",
    "SODIUM DIACETATE",
    "SODIUM SILICOALUMINATE",
    "POTASSIUM NITRATE",
    "SODIUM HEXAMETAPHOSPHATE",
    "SODIUM TRIPOLYPHOSPHATE",
    "TRISODIUM PHOSPHATE",
    "ANIMAL FAT",
    "LAMB FAT",
    "BEEF FAT",
    "LARD",
    "BUTTER",
    "OIL",
    "CHICKEN FAT",
    "OILS",
    "DRIPPING",
    "PALM FAT",
    "DUCK FAT",
    "PASTRY FAT",
    "FATS",
    "PORK FAT",
    "FATTY ACIDS",
    "SHORTENING",
    "FATTY MATERIAL",
    "STEARIC ACID",
    "GHEE",
    "TALLOW",
    "MARGARINE",
    "VEGETABLE FAT",
    "MEDIUM CHAIN TRIGLYCERIDES",
    "ACESULFAME",
    "OSLADIN",
    "E 954",
    "ADVANTAME",
    "OUBLI",
    "E 955",
    "ALITAME",
    "PENTADIN",
    "E 957",
    "ALTERN",
    "PUREVIA",
    "E 959",
    "ASPARTAME",
    "REB A",
    "E 960",
    "ASPARTIME",
    "REBAUDIOSIDE A",
    "E 961",
    "BRAZZEIN",
    "REBIANA",
    "E 962",
    "CANDY LEAF",
    "SACCHARIN",
    "E 969",
    "CURCULIN",
    "SPLENDA",
    "ERYTHRITOL",
    "CWEET",
    "STEVIA",
    "GALACTITOL",
    "CYCLAMATE",
    "STEVIOL",
    "GLUCITOL",
    "CYCLAMIC ACID",
    "STEVIOL GLYCOSIDES",
    "HYDROGENATED ISOMALTULOSE",
    "ENLITEN",
    "SUCRALOSE",
    "ISOMALT",
    "EQUAL",
    "SUGAR LEAF",
    "LACTITOL",
    "INSTA SWEET",
    "SUGAR TWIN",
    "MALTITOL",
    "KALTAME",
    "SUNETT",
    "MANNITOL",
    "LUMBAH",
    "SWEETLEAF",
    "POLYGLYCITOL",
    "LUO HAN GUO",
    "SWEET’N LOW",
    "SORBITOL",
    "MABINLIN",
    "SWEET ONE",
    "XYLITOL",
    "MONATIN",
    "SYCLAMATE",
    "E 420",
    "MONELLIN",
    "TRICHLOROGALACTOSUCROSE",
    "E 421",
    "MONK FRUIT EXTRACT",
    "TWIN SWEET",
    "E 953",
    "MONK FRUIT",
    "TRUVIA",
    "E 964",
    "NATRA TASTE",
    "THAUMATIN",
    "E 965",
    "NECTA SWEET",
    "E 950",
    "E 966",
    "NEOHESPERIDINE DIHYDROCHALCONE",
    "E 951",
    "E 967",
    "NEOTAME",
    "E 952",
    "E 968",
    "NUTRA SWEET",
    "HYDROLYZED PROTEIN",
    "SOYA/SOY PROTEIN ISOLATE",
    "CASEIN",
    "WHEY PROTEIN",
    "MECHANICALLY SEPARATED MEAT",
    "INVERT SUGAR",
    "INVERT SUGAR SYRUP",
    "MALTODEXTRIN",
    "SOLUBLE FIBER",
    "INSOLUBLE FIBER",
    "HYDROGENATED OIL",
    "INTERESTERIFIED OIL",
    "GLUTEN",
    "FRUIT JUICE CONCENTRATE",
    "ANTI-FOAMING AGENT",
    "STABILIZERS AND THICKENERS",
    "THICKENER",
    "COLOR",
    "FLAVOR",
    "SWEETENER",
]
dc.flag_ultra_processed("ingredients", ultraprocessed_ingredients)


# high sugar
high_sugar_ingredients = [
    "AGAVE",
    "FRUCTOSE",
    "NULOMOLINE",
    "BARLEY MALT SYRUP",
    "GALACTOSE",
    "ORGANIC BARLEY MALT SYRUP",
    "CANE JUICE",
    "GLUCOSE",
    "PALATINOSE",
    "CANEJUICE",
    "GOMME",
    "PANELA",
    "CANE SWEETENER",
    "HONEY",
    "PILONCILLO",
    "CLINTOSE",
    "HONI-BAKE",
    "SACCHAROSE",
    "COCONUT NECTAR",
    "HONI BAKE",
    "SORBOSE",
    "COCONUT BLOSSOM NECTAR",
    "HONIBAKE",
    "SUCANAT",
    "COCONUT SAP",
    "HONI-FLAKE",
    "SUCROSE",
    "CORNSWEET",
    "HONI FLAKE",
    "SUCROVERT",
    "CORN SWEET",
    "HONIFLAKE",
    "SUGAR",
    "CORN SWEETENER",
    "ISOGLUCOSE",
    "SUGARS",
    "CORNSWEETENER",
    "ISOMALTULOSE",
    "SWEET’N’NEAT",
    "DEMERARA",
    "JAGGERY",
    "SWEETNNEAT",
    "DEXTROSE",
    "KONA-AME",
    "SWEETN NEAT",
    "DISACCHARIDE",
    "KONA AME",
    "SWEET NNEAT",
    "DISACCHARIDES",
    "KONAAME",
    "SWEET N NEAT",
    "DRI-MOL",
    "LACTOSE",
    "SYRUP",
    "DRI MOL",
    "MALTOSE",
    "TAGATOSE",
    "DRIMOL",
    "MIZU-AME",
    "TREACLE",
    "DRI-SWEET",
    "MIZU AME",
    "TREHALOSE",
    "DRI SWEET",
    "MIZUAME",
    "TRUSWEET",
    "DRISWEET",
    "MOLASSES",
    "TRU SWEET",
    "FLO-MALT",
    "MONOSACCHARIDE",
    "TURBINADO",
    "FLO MALT",
    "MONOSACCHARIDES",
    "VERSATOSE",
    "FLOMALT",
    "MUSCOVADO",
    "YACON",
    "MALT",
]
dc.flag_high_sugar("ingredients", "sugar", "aisle", high_sugar_ingredients)


# high sodium
high_sodium_ingredients = [
    "BIOSALT",
    "BRINE",
    "PRAGUE POWDER",
    "SALT",
    "SLAT",
    "SODIUM CHLORIDE",
]
dc.flag_high_sodium("ingredients", "salt", "aisle", high_sodium_ingredients)

# high saturated fat
high_saturated_fat_ingredients = [
    "ANIMAL FAT",
    "LAMB FAT",
    "BEEF FAT",
    "LARD",
    "BUTTER",
    "OIL",
    "CHICKEN FAT",
    "OILS",
    "DRIPPING",
    "PALM FAT",
    "DUCK FAT",
    "PASTRY FAT",
    "FATS",
    "PORK FAT",
    "FATTY ACIDS",
    "SHORTENING",
    "FATTY MATERIAL",
    "STEARIC ACID",
    "GHEE",
    "TALLOW",
    "MARGARINE",
    "VEGETABLE FAT",
    "MEDIUM CHAIN TRIGLYCERIDES",
]
dc.flag_high_saturated_fat(
    "ingredients", "saturatedfat", "aisle", high_saturated_fat_ingredients
)


# high calorie
dc.flag_high_calories("energykcal", "aisle")


# nns
nns_ingredients = [
    "ACESULFAME",
    "OSLADIN",
    "E 954",
    "ADVANTAME",
    "OUBLI",
    "E 955",
    "ALITAME",
    "PENTADIN",
    "E 957",
    "ALTERN",
    "PUREVIA",
    "E 959",
    "ASPARTAME",
    "REB A",
    "E 960",
    "ASPARTIME",
    "REBAUDIOSIDE A",
    "E 961",
    "BRAZZEIN",
    "REBIANA",
    "E 962",
    "CANDY LEAF",
    "SACCHARIN",
    "E 969",
    "CURCULIN",
    "SPLENDA",
    "ERYTHRITOL",
    "CWEET",
    "STEVIA",
    "GALACTITOL",
    "CYCLAMATE",
    "STEVIOL",
    "GLUCITOL",
    "CYCLAMIC ACID",
    "STEVIOL GLYCOSIDES",
    "HYDROGENATED ISOMALTULOSE",
    "ENLITEN",
    "SUCRALOSE",
    "ISOMALT",
    "EQUAL",
    "SUGAR LEAF",
    "LACTITOL",
    "INSTA SWEET",
    "SUGAR TWIN",
    "MALTITOL",
    "KALTAME",
    "SUNETT",
    "MANNITOL",
    "LUMBAH",
    "SWEETLEAF",
    "POLYGLYCITOL",
    "LUO HAN GUO",
    "SWEET’N LOW",
    "SORBITOL",
    "MABINLIN",
    "SWEET ONE",
    "XYLITOL",
    "MONATIN",
    "SYCLAMATE",
    "E 420",
    "MONELLIN",
    "TRICHLOROGALACTOSUCROSE",
    "E 421",
    "MONK FRUIT EXTRACT",
    "TWIN SWEET",
    "E 953",
    "MONK FRUIT",
    "TRUVIA",
    "E 964",
    "NATRA TASTE",
    "THAUMATIN",
    "E 965",
    "NECTA SWEET",
    "E 950",
    "E 966",
    "NEOHESPERIDINE DIHYDROCHALCONE",
    "E 951",
    "E 967",
    "NEOTAME",
    "E 952",
    "E 968",
    "NUTRA SWEET",
]
dc.flag_nns("ingredients", nns_ingredients)

# extract blanks
# dc.extract_blank_rows("servingsize")

dc.standardize_nutrient_columns()
dc.convert_tsp_to_g("servingsize")
dc.convert_l_to_ml("servingsize")
dc.convert_mg_to_g("servingsize")
dc.convert_weird_g("servingsize")

dc.convert_fl_oz_to_ml("servingsize")
dc.strip_spaces("servingsize")
dc.convert_oz_to_g("servingsize")
dc.strip_spaces("servingsize")
dc.convert_package_based_size("servingsize")
dc.strip_spaces("servingsize")
dc.convert_cups_to_ml("servingsize")
dc.strip_spaces("servingsize")
dc.convert_tbsp_to_g("servingsize")
dc.strip_spaces("servingsize")


dc.handle_missing("department", "drop")
dc.handle_missing("aisle", "drop")
dc.handle_missing("shelf", "drop")
dc.handle_missing("product", "drop")
dc.handle_missing("price", "drop")
dc.handle_missing("servingspercontainer", "drop")
dc.handle_missing("servingsize", "drop")
dc.handle_missing("energykcal", "drop")
dc.handle_missing("fat", "drop")
dc.handle_missing("saturatedfat", "drop")
dc.handle_missing("transfat", "drop")
dc.handle_missing("carbohydrates", "drop")
dc.handle_missing("sugar", "drop")
dc.handle_missing("salt", "drop")
dc.handle_missing("fibre", "drop")
dc.handle_missing("protein", "drop")
dc.handle_missing("ingredients", "drop")
dc.handle_missing("redmeat", "drop")
dc.handle_missing("shelfrank", "drop")
dc.handle_missing("packsize", "drop")
dc.handle_missing("packunit", "drop")
dc.handle_missing("image", "drop")
dc.handle_missing("energykcal per 100", "drop")
dc.handle_missing("fat per 100", "drop")
dc.handle_missing("saturatedfat per 100", "drop")
dc.handle_missing("transfat per 100", "drop")
dc.handle_missing("carbohydrates per 100", "drop")
dc.handle_missing("sugar per 100", "drop")
dc.handle_missing("salt per 100", "drop")
dc.handle_missing("fibre per 100", "drop")
dc.handle_missing("protein per 100", "drop")
dc.handle_missing("ultra_processed_flag", "drop")
dc.handle_missing("high_sugar_flag", "drop")
dc.handle_missing("high_sodium_flag", "drop")
dc.handle_missing("high_saturated_fat_flag", "drop")
dc.handle_missing("high_calories_flag", "drop")
dc.handle_missing("nns_flag", "drop")

dc.price_per_container()

# save file
dc.save_data("cleaned_data_3.xlsx")
