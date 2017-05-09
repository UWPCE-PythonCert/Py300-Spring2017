# tests of saving the objects and datbase in json format.

from mailroom import model


def test_donor_round_trip():
    # get an arbitrary
    donor = model.get_sample_data()[0]

    json_dict = donor.to_json_compat()

    donor2 = model.Donor.from_json_dict(json_dict)

    print(json_dict)

    assert donor2 == donor


def test_database_save():
    db = model.DonorDB(model.get_sample_data())

    json_dict = db.to_json_compat()

    db2 = model.DonorDB.from_json_dict(json_dict)

    print(db2)

    assert db2 == db

    assert False
