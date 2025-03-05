import pytest
from data import DataCleaner


def test_remove_text_1():
    """Use case for remove_unwanted_text() and strip_spaces() on
    servingspercontainer column as String values."""
    cleaner: DataCleaner = DataCleaner("products.xlsx")
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
    cleaner: DataCleaner = DataCleaner("products.xlsx")
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
    cleaner: DataCleaner = DataCleaner("products.xlsx")
    cleaner.round("price", 2)
    res = cleaner.preview(20)["price"].tolist()
    assert expected == res


def test_strip_spaces_edge():
    """If strip_spaces() is called on a column containing no spaces, exception must be raised."""
    with pytest.raises(Exception):
        cleaner: DataCleaner = DataCleaner("products.xlsx")
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
    cleaner1: DataCleaner = DataCleaner("products.xlsx")
    cleaner1.round("price", 1)
    res1 = cleaner1.preview(20)["price"].tolist()
    assert res1 == expected_1

    cleaner2: DataCleaner = DataCleaner("products.xlsx")
    cleaner2.round("price", 2)
    res2 = cleaner2.preview(20)["price"].tolist()
    assert res2 == expected_2


def test_strip_spaces():
    dc: DataCleaner = DataCleaner("testing_subset.xlsx")
    shelf_expected = [
        "Pies&Tarts",
        "Pies&Tarts",
        "Pies&Tarts",
        "Pies&Tarts",
        "Pies&Tarts",
        "Pies&Tarts",
        "Pies&Tarts",
        "Pies&Tarts",
        "Pies&Tarts",
        "KidsLunch&SnackPacks",
        "KidsLunch&SnackPacks",
        "KidsLunch&SnackPacks",
        "KidsLunch&SnackPacks",
        "Biscuits,Cookies&CookieDoughs",
        "Biscuits,Cookies&CookieDoughs",
        "FrozenPizza",
        "FrozenPizza",
        "FrozenPizza",
        "FrozenPizza",
        "FrozenPizza",
    ]
    dc.strip_spaces("shelf")
    assert dc.tolist("shelf") == shelf_expected

    dc.strip_spaces("energykcal")
    energy_expected = [
        "282.0cal",
        "230.0cal",
        "450.0cal",
        "230.0cal",
        "440.0cal",
        "470.0cal",
        "450.0cal",
        "450.0cal",
        "370.0cal",
        "180.0cal",
        "430.0cal",
        "210.0cal",
        "180.0cal",
        "180.0cal",
        "180.0cal",
        "300.0cal",
        "330.0cal",
        "350.0cal",
        "320.0cal",
        "380.0cal",
    ]
    assert dc.tolist("energykcal") == energy_expected


def test_drop():
    dc: DataCleaner = DataCleaner("testing_subset.xlsx")
    assert "aisle" in dc.df.columns
    assert "product" in dc.df.columns
    prev_cols = dc.num_cols()
    dc.drop("aisle")
    dc.drop("product")
    assert "aisle" not in dc.df.columns
    assert "product" not in dc.df.columns
    assert prev_cols - 2 == dc.num_cols()


def test_cols_rows():
    dc: DataCleaner = DataCleaner("testing_subset.xlsx")
    assert dc.num_cols() == 23
    assert dc.num_rows() == 20
    dc.drop("aisle")
    dc.drop("product")
    assert dc.num_cols() == 21


def test_count_unique():
    # TODO
    assert False


def test_drop_blanks():
    # TODO
    assert False


def test_m_to_g():
    # TODO
    assert False


def test_standardize_column():
    # TODO
    assert False


def test_flag_ultraprocessed():
    # TODO
    assert False


def test_flag_sugar():
    # TODO
    assert False


def test_flag_sat_fat():
    # TODO
    assert False


def test_flag_cals():
    # TODO
    assert False


def test_flag_sodium():
    # TODO
    assert False
