"Tests for the data cleaning methods used to clean excel data"

#FOR ALL THE FILE PATHS, FOLLOW MY EXAMPLE ON LINES 485-487
import pytest
from data.data_cleaner import DataCleaner
import os

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

high_sodium_ingredients = [
    "BIOSALT",
    "BRINE",
    "PRAGUE POWDER",
    "SALT",
    "SLAT",
    "SODIUM CHLORIDE",
]

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


def test_remove_text_1():
    """Use case for remove_unwanted_text() and strip_spaces() on
    servingspercontainer column as String values."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "products.xlsx")
    cleaner: DataCleaner = DataCleaner(file_path)
    cleaner.remove_text("servingspercontainer", "About")
    cleaner.strip_spaces("servingspercontainer")
    expected: list[str] = [
        "32",
        "32",
        "40",
        "24",
        "24",
        "24",
        "2",
        "32",
        "2",
        "18",
        "6",
        "12",
        "10",
        "24",
        "12",
        "24",
        "18",
        "20",
        "24",
        "12",
    ]
    res = cleaner.preview(20)["servingspercontainer"].tolist()
    assert expected == res


def test_energykcal_1():
    """Use case for column energykcal"""
    expected: list[str] = [
        0.0,
        0.0,
        0.0,
        0.0,
        170.0,
        150.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        30.0,
        140.0,
        5.0,
        160.0,
        80.0,
        0.0,
        140.0,
        170.0,
    ]
    cleaner: DataCleaner = DataCleaner("./data/products.xlsx")
    cleaner.remove_text("energykcal", "cal")
    cleaner.strip_spaces("energykcal")
    cleaner.to_float("energykcal")
    res = cleaner.preview(20)["energykcal"].tolist()
    assert expected == res


def test_to_float_fat():
    """Use case for column fat"""
    expected: list[str] = [
        4.96,
        3.98,
        3.56,
        8.38,
        7.98,
        6.98,
        2.36,
        5.98,
        15.48,
        8.98,
        8.96,
        6.38,
        1.88,
        6.98,
        16.84,
        4.72,
        8.96,
        15.48,
        6.98,
        5.78,
    ]
    cleaner: DataCleaner = DataCleaner("./data/products.xlsx")
    cleaner.round("price", 2)
    res = cleaner.preview(20)["price"].tolist()
    assert expected == res


def test_strip_spaces_edge():
    """If strip_spaces() is called on a column containing no spaces, exception must be raised."""
    with pytest.raises(Exception):
        cleaner: DataCleaner = DataCleaner("./data/products.xlsx")
        cleaner.strip_spaces("price")


def test_round_use():
    expected_1: list[str] = [
        5.0,
        4.0,
        3.6,
        8.4,
        8.0,
        7.0,
        2.4,
        6.0,
        15.5,
        9.0,
        9.0,
        6.4,
        1.9,
        7.0,
        16.8,
        4.7,
        9.0,
        15.5,
        7.0,
        5.8,
    ]
    expected_2: list[str] = [
        4.96,
        3.98,
        3.56,
        8.38,
        7.98,
        6.98,
        2.36,
        5.98,
        15.48,
        8.98,
        8.96,
        6.38,
        1.88,
        6.98,
        16.84,
        4.72,
        8.96,
        15.48,
        6.98,
        5.78,
    ]
    cleaner1: DataCleaner = DataCleaner("./data/products.xlsx")
    cleaner1.round("price", 1)
    res1 = cleaner1.preview(20)["price"].tolist()
    assert res1 == expected_1

    cleaner2: DataCleaner = DataCleaner("./data/products.xlsx")
    cleaner2.round("price", 2)
    res2 = cleaner2.preview(20)["price"].tolist()
    assert res2 == expected_2


def test_strip_spaces():
    dc: DataCleaner = DataCleaner("./data/testing_subset.xlsx")
    dc.remove_text("energykcal", "cal")
    energy_expected_space = [
        "282.0 ",
        "230.0 ",
        "450.0 ",
        "230.0 ",
        "440.0 ",
        "470.0 ",
        "450.0 ",
        "450.0 ",
        "370.0 ",
        "180.0 ",
        "430.0 ",
        "210.0 ",
        "180.0 ",
        "180.0 ",
        "180.0 ",
        "300.0 ",
        "330.0 ",
        "350.0 ",
        "320.0 ",
        "   380.0 ",
    ]
    assert dc.to_list("energykcal") == energy_expected_space

    dc.strip_spaces("energykcal")
    energy_expected = [
        "282.0",
        "230.0",
        "450.0",
        "230.0",
        "440.0",
        "470.0",
        "450.0",
        "450.0",
        "370.0",
        "180.0",
        "430.0",
        "210.0",
        "180.0",
        "180.0",
        "180.0",
        "300.0",
        "330.0",
        "350.0",
        "320.0",
        "380.0",
    ]
    assert dc.to_list("energykcal") == energy_expected


def test_drop():
    dc: DataCleaner = DataCleaner("./data/testing_subset.xlsx")
    assert "aisle" in dc.df.columns
    assert "product" in dc.df.columns
    prev_cols = dc.num_cols()
    dc.drop("aisle")
    dc.drop("product")
    assert "aisle" not in dc.df.columns
    assert "product" not in dc.df.columns
    assert prev_cols - 2 == dc.num_cols()


def test_cols_rows():
    dc: DataCleaner = DataCleaner("./data/testing_subset.xlsx")
    assert dc.num_cols() == 23
    assert dc.num_rows() == 20
    dc.drop("aisle")
    dc.drop("product")
    assert dc.num_cols() == 21


def test_count_unique():
    dc: DataCleaner = DataCleaner("./data/testing_subset.xlsx")
    assert dc.count_unique_entries("aisle") == 4
    assert dc.count_unique_entries("updated") == 0


def test_drop_blanks():
    dc: DataCleaner = DataCleaner("./data/testing_subset.xlsx")
    assert dc.num_rows() == 20
    dc.drop_blank_rows()
    assert dc.num_rows() == 0


def test_m_to_g():
    dc: DataCleaner = DataCleaner("./data/testing_subset.xlsx")
    expected = [
        0.165,
        0.150,
        0.240,
        0.320,
        0.220,
        0.480,
        0.240,
        0.350,
        0.300,
        0.450,
        0.730,
        0.380,
        0.450,
        0.450,
        0.480,
        0.740,
        0.840,
        0.560,
        0.690,
        0.880,
    ]
    dc.convert_m_to_grams("salt")
    assert dc.to_list("salt") == expected


def test_standardize_serving_g():
    dc: DataCleaner = DataCleaner("./data/testing_subset.xlsx")
    expected = [
        118,
        81,
        136,
        83,
        119,
        113,
        136,
        119,
        125,
        56.699,
        416.738,
        70.8738,
        56,
        57.7621534,
        59,
        130,
        149,
        149.3074885,
        133,
        170.097,
    ]


def test_standardize_column():
    dc: DataCleaner = DataCleaner("./data/testing_subset.xlsx")
    fat_expected = [
        8.47,
        13.58,
        18.38,
        8.43,
        16.81,
        20.35,
        18.38,
        17.65,
        16.80,
        22.93,
        4.56,
        14.11,
        23.21,
        10.39,
        11.86,
        8.46,
        8.72,
        11.39,
        11.28,
        8.82,
    ]
    dc.strip_spaces("servingsize")
    dc.extract_bracketed_value("servingsize")
    dc.strip_spaces("servingsize")
    dc.convert_package_based_size("servingsize")
    dc.standardize_column("fat")
    res = dc.to_list("fat per 100")
    assert len(fat_expected) == len(res)
    for i in range(len(fat_expected)):
        assert abs(fat_expected[i] - res[i]) <= 1


def test_flag_ultraprocessed():
    dc: DataCleaner = DataCleaner("./data/testing_subset.xlsx")
    # assume that "fructose" will be flagged, but NOT high fructose corn syrup
    expected = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    ultraprocessed_subset = ["FRUCTOSE"]
    dc.flag_ultra_processed("ingredients", ultraprocessed_subset)
    print(dc.to_list("ultra_processed_flag"))
    assert len(expected) == len(dc.to_list("ultra_processed_flag"))
    assert expected == dc.to_list("ultra_processed_flag")


def test_flag_sugar():
    dc: DataCleaner = DataCleaner("./data/testing_subset.xlsx")
    expected = []
    high_sugar_subset = ["GLUCOSE"]
    dc.flag_high_sugar("ingredients", "sugar", "aisle", high_sugar_subset)
    assert len(expected) == len(dc.to_list("high_sugar_flag"))
    assert expected == dc.to_list("high_sugar_flag")


def test_extract_weight():
    dc: DataCleaner = DataCleaner("./data/testing_subset.xlsx")
    dc.extract_and_convert_weight()
    expected = []
    print(dc.to_list("weight_grams"))
    assert expected == dc.to_list("weight_grams")


def test_flag_sat_fat():
    dc: DataCleaner = DataCleaner("./data/testing_subset.xlsx")
    expected = []
    # TODO
    assert False


def test_flag_cals():
    dc: DataCleaner = DataCleaner("./data/testing_subset.xlsx")
    expected = []
    # TODO
    assert False


def test_flag_sodium():
    dc: DataCleaner = DataCleaner("./data/testing_subset.xlsx")
    expected = []
    # TODO
    assert False


def test_flag_NNS():
    dc: DataCleaner = DataCleaner("./data/testing_subset.xlsx")
    expected = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    dc.flag_nns("ingredients", nns_ingredients)
    print(dc.to_list("nns_flag"))
    assert len(expected) == len(dc.to_list("nns_flag"))
    assert expected == dc.to_list("nns_flag")
