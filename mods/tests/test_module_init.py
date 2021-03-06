import libvis_mods
from libvis_mods import utils

def test_init_file(tmp_path):
    target_dir = tmp_path/'tmp_mods'
    target_dir.mkdir()
    libvis_mods.init_file('TestMod', output_dir=target_dir)
    ls = list(target_dir.iterdir())
    names = [x.name for x in ls]
    assert names == ['TestMod']
    utils.rm(target_dir)
