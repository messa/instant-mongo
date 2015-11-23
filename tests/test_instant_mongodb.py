from pathlib import Path
import py.path

from instant_mongo import InstantMongoDB


def test_run(tmpdir):
    dd = tmpdir / 'data'
    assert isinstance(dd, py._path.local.LocalPath), type(dd)
    for data_dir in [dd, str(dd), Path(str(dd))]:
        print()
        print('data_dir: {!r}'.format(data_dir))
        im = InstantMongoDB(data_dir=data_dir)
        with im:
            im.testdb.testcoll.insert({'foo': 'bar'})
            doc, = im.testdb.testcoll.find()
            assert doc['foo'] == 'bar'
            im.testdb.testcoll.drop()


def test_drop_everything(tmpdir):
    im = InstantMongoDB(data_dir=tmpdir / 'data')
    with im:
        im.testdb.testcoll.insert({'foo': 'bar'})
        assert im.testdb.testcoll.count() == 1
        im.drop_everything()
        assert im.testdb.testcoll.count() == 0

