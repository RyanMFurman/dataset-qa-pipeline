from datasetqa.utils import map_det_type

def test_map_det_type():
    assert map_det_type("BB") == "broken_bone"
    assert map_det_type("NB") == "non_broken"
    assert map_det_type("EX") == "excluded"
