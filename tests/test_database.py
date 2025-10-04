import types
import importlib
from unittest import mock


def install_fake_pandas(monkeypatch):
    sys_modules = importlib.import_module('sys').modules
    for k in list(sys_modules.keys()):
        if k == 'pandas' or k.startswith('pandas.'):
            sys_modules.pop(k, None)
    import types as _types
    fake_pd = _types.ModuleType('pandas')
    # default read_csv returns minimal frame-like object used in tests
    class _DF:
        def __init__(self, data):
            self._data = data
        def __getitem__(self, key):
            return self._data[key]
    def read_csv(_path):
        return _DF({
            'NEXT_PUBLIC_SUPABASE_URL': ["http://example"],
            'NEXT_PUBLIC_SUPABASE_ANON_KEY': ["key"],
        })
    fake_pd.read_csv = read_csv
    monkeypatch.setitem(sys_modules, 'pandas', fake_pd)


def install_fake_supabase(monkeypatch, client_obj):
    sys_modules = importlib.import_module('sys').modules
    for k in list(sys_modules.keys()):
        if k == 'supabase' or k.startswith('supabase.'):
            sys_modules.pop(k, None)
    fake = types.SimpleNamespace()
    fake.create_client = lambda url, key: client_obj
    fake.Client = object
    monkeypatch.setitem(sys_modules, 'supabase', fake)


class DummyStorage:
    def __init__(self):
        self._items = []

    def from_(self, name):
        return self

    def list(self, folder, opts):
        return [{"name": "a.csv"}, {"name": "b.csv"}]

    def upload(self, path, file, file_options):
        return types.SimpleNamespace(data={"path": path})


class DummyClient:
    def __init__(self):
        self.storage = DummyStorage()


def test_start_conection_success(monkeypatch):
    client = DummyClient()
    install_fake_supabase(monkeypatch, client)
    install_fake_pandas(monkeypatch)

    install_fake_pandas(monkeypatch)
    install_fake_pandas(monkeypatch)
    install_fake_pandas(monkeypatch)
    install_fake_pandas(monkeypatch)
    from App.utils import database
    importlib.reload(database)
    start_conection = database.start_conection
    out = start_conection("http://x", "k")
    assert out is client


def test_start_conection_errors(monkeypatch, capsys):
    # Replace supabase with one that raises ValueError
    fake = types.SimpleNamespace()
    def raise_value(url, key):
        raise ValueError("bad")
    fake.create_client = raise_value
    fake.Client = object
    monkeypatch.setitem(importlib.import_module('sys').modules, 'supabase', fake)

    install_fake_pandas(monkeypatch)
    from App.utils import database
    importlib.reload(database)
    assert database.start_conection("u", "k") is None


def test_start_conection_module_not_found(monkeypatch, capsys):
    # Simulate missing dependency
    fake = types.SimpleNamespace()
    def raise_mod(url, key):
        raise ModuleNotFoundError("missing")
    fake.create_client = raise_mod
    fake.Client = object
    monkeypatch.setitem(importlib.import_module('sys').modules, 'supabase', fake)
    
    install_fake_pandas(monkeypatch)
    from App.utils import database
    importlib.reload(database)
    assert database.start_conection("u", "k") is None
    out = capsys.readouterr().out
    assert "Missing dependency" in out


def test_start_conection_generic_exception(monkeypatch, capsys):
    fake = types.SimpleNamespace()
    def raise_generic(url, key):
        raise RuntimeError("boom")
    fake.create_client = raise_generic
    fake.Client = object
    monkeypatch.setitem(importlib.import_module('sys').modules, 'supabase', fake)
    
    install_fake_pandas(monkeypatch)
    from App.utils import database
    importlib.reload(database)
    assert database.start_conection("u", "k") is None
    out = capsys.readouterr().out
    assert "Um erro não experado" in out


def test_contentIn_bucket(monkeypatch):
    # Ensure supabase exists so import doesn’t fail
    client = DummyClient()
    install_fake_supabase(monkeypatch, client)
    install_fake_pandas(monkeypatch)

    from App.utils import database
    importlib.reload(database)

    conn = types.SimpleNamespace(supabase=client)
    names = database.contentIn_bucket(conn, "folder")
    assert names == ["a.csv", "b.csv"]


def test_upload_content_success(monkeypatch, capsys):
    client = DummyClient()
    install_fake_supabase(monkeypatch, client)
    install_fake_pandas(monkeypatch)

    from App.utils import database
    importlib.reload(database)

    class DummyFile:
        name = "file.csv"
        def read(self):
            return b"x,y\n1,2\n"

    conn = types.SimpleNamespace(supabase=client)
    database.upload_content(conn, "data", DummyFile())
    out = capsys.readouterr().out
    assert "armazenado com sucesso" in out


def test_upload_content_exception(monkeypatch, capsys):
    class FailingStorage(DummyStorage):
        def upload(self, *a, **k):
            raise RuntimeError("fail")
    client = DummyClient()
    client.storage = FailingStorage()
    install_fake_supabase(monkeypatch, client)
    install_fake_pandas(monkeypatch)

    from App.utils import database
    importlib.reload(database)

    class DummyFile:
        name = "file.csv"
        def read(self):
            return b"" 

    conn = types.SimpleNamespace(supabase=client)
    database.upload_content(conn, "data", DummyFile())
    out = capsys.readouterr().out
    assert "Erro ao armazenar arquivo" in out


def test_conection_singleton_and_keys(monkeypatch):
    # Prepare supabase
    client = DummyClient()
    install_fake_supabase(monkeypatch, client)
    # Fake pandas module with read_csv override
    fake_pd = types.SimpleNamespace()
    def _read_csv(*a, **k):
        class Keys:
            def __getitem__(self, key):
                return {"NEXT_PUBLIC_SUPABASE_URL": ["http://local"],
                        "NEXT_PUBLIC_SUPABASE_ANON_KEY": ["devkey"]}[key]
        return Keys()
    fake_pd.read_csv = _read_csv
    monkeypatch.setitem(importlib.import_module('sys').modules, 'pandas', fake_pd)

    from App.utils import database
    importlib.reload(database)

    c1 = database.Conection()
    c2 = database.Conection()
    assert c1 is c2
    assert hasattr(c1, "supabase")
