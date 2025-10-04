import types


class DummyFile:
    def __init__(self, name, data=b""):
        self.name = name
        self._data = data
    def read(self):
        return self._data


def install_fake_pandas(monkeypatch):
    import importlib
    sys_modules = importlib.import_module('sys').modules
    for k in list(sys_modules.keys()):
        if k == 'pandas' or k.startswith('pandas.'):
            sys_modules.pop(k, None)
    import types as _types
    fake_pd = _types.ModuleType('pandas')

    class _DF:
        def __init__(self, data):
            self.data = data
    def read_csv(file, nrows=100):
        return _DF({"src": "csv", "name": getattr(file, 'name', '')})
    def read_excel(file, nrows=100):
        return _DF({"src": "xlsx", "name": getattr(file, 'name', '')})

    fake_pd.read_csv = read_csv
    fake_pd.read_excel = read_excel
    sys_modules['pandas'] = fake_pd


def test_load_data_csv(monkeypatch):
    install_fake_pandas(monkeypatch)
    from App.services.upload_service import load_data
    f = DummyFile('file.csv', b'a,b\n1,2\n')
    df = load_data(f, nrows=10)
    assert df.data['src'] == 'csv'


def test_load_data_xlsx(monkeypatch):
    install_fake_pandas(monkeypatch)
    from App.services.upload_service import load_data
    f = DummyFile('file.xlsx', b'...')
    df = load_data(f, nrows=5)
    assert df.data['src'] == 'xlsx'


def test_load_data_unsupported(monkeypatch):
    install_fake_pandas(monkeypatch)
    from App.services.upload_service import load_data
    f = DummyFile('file.txt', b'')
    assert load_data(f) is None
    assert load_data(None) is None


def test_perform_upload(monkeypatch, capsys):
    from App.services.upload_service import perform_upload

    class DummyStorage:
        def from_(self, name):
            return self
        def upload(self, *a, **k):
            print('uploaded')
            return types.SimpleNamespace(data={})

    class DummyClient:
        def __init__(self):
            self.storage = DummyStorage()

    conn = types.SimpleNamespace(supabase=DummyClient())

    f = DummyFile('data.csv', b'x,y\n')
    perform_upload(conn, 'data', f)
    out = capsys.readouterr().out
    assert 'uploaded' in out
