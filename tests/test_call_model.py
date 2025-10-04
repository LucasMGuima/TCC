import builtins
import os
from unittest import mock
import importlib
import types


def install_fake_pandas_and_sklearn(monkeypatch):
    # Minimal pandas-like fake
    class Series:
        def __init__(self, values):
            self._values = values

        def isnull(self):
            class _IsNull:
                def __init__(self, values):
                    self._values = values

                def sum(self):
                    return sum(1 for v in self._values if v is None)

            return _IsNull(self._values)

        # pandas alias
        def isna(self):
            return self.isnull()

    class DataFrame:
        def __init__(self, data):
            # data: dict of column -> list
            self._cols = list(data.keys())
            # Normalize rows as list of dicts
            self._rows = [
                {col: data[col][i] for col in self._cols}
                for i in range(len(next(iter(data.values()))))
            ]

        def __len__(self):
            return len(self._rows)

        def __getitem__(self, key):
            return Series([row.get(key) for row in self._rows])

        def copy(self):
            return DataFrame({col: [r[col] for r in self._rows] for col in self._cols})

        def dropna(self, subset=None, inplace=False):
            subset = subset or []
            def ok(row):
                return all(row.get(col) is not None for col in subset)
            new_rows = [r for r in self._rows if ok(r)]
            if inplace:
                self._rows = new_rows
                return None
            out = DataFrame({col: [r[col] for r in new_rows] for col in self._cols})
            return out

        def sample(self, frac, random_state=None):
            k = max(0, int(len(self._rows) * frac))
            rows = self._rows[:k]
            out = DataFrame({col: [r[col] for r in rows] for col in self._cols})
            # store indices of sampled rows in parent space for drop()
            out._sampled_positions = set(range(k))
            return out

        def drop(self, indexes):
            # indexes is expected to be a sequence of positions from sample()
            if isinstance(indexes, list):
                drop_set = set(indexes)
            else:
                try:
                    drop_set = set(indexes)
                except TypeError:
                    drop_set = {indexes}
            keep = [r for i, r in enumerate(self._rows) if i not in drop_set]
            out = DataFrame({col: [r[col] for r in keep] for col in self._cols})
            return out

        def to_csv(self):
            # Very simple CSV rendering
            header = ",".join(self._cols)
            lines = [header]
            for r in self._rows:
                lines.append(",".join(str(r[c]) for c in self._cols))
            return "\n".join(lines) + "\n"

        @property
        def index(self):
            return list(range(len(self._rows)))

    # Ensure no existing pandas remains
    sys_modules = importlib.import_module('sys').modules
    for k in list(sys_modules.keys()):
        if k == 'pandas' or k.startswith('pandas.'):
            sys_modules.pop(k, None)

    import types as _types
    fake_pd = _types.ModuleType('pandas')
    fake_pd.DataFrame = DataFrame
    monkeypatch.setitem(sys_modules, 'pandas', fake_pd)

    # Minimal sklearn stub
    fake_sk_model_selection = types.SimpleNamespace(train_test_split=lambda *a, **k: None)
    fake_sklearn = types.SimpleNamespace(model_selection=fake_sk_model_selection)
    monkeypatch.setitem(importlib.import_module('sys').modules, 'sklearn', fake_sklearn)
    monkeypatch.setitem(importlib.import_module('sys').modules, 'sklearn.model_selection', fake_sk_model_selection)
    return DataFrame


def test_split_data_basic(tmp_path, monkeypatch):
    install_fake_pandas_and_sklearn(monkeypatch)
    from App.src.call_model import split_data

    DataFrame = install_fake_pandas_and_sklearn(monkeypatch)
    df = DataFrame({
        "y": [1, 2, 3, 4, 5],
        "x": [10, 20, 30, 40, 50],
    })

    test, train = split_data(40, df.copy(), "y")
    # Expect 40% test size (2 rows) and 60% train (3 rows)
    assert len(test) == 2
    assert len(train) == 3
    # Ensure no NaN in target column after split
    assert test["y"].isna().sum() == 0
    assert train["y"].isna().sum() == 0


def test_run_model_writes_and_calls_R(tmp_path, monkeypatch):
    # Work from a temp directory
    cwd = tmp_path
    monkeypatch.chdir(cwd)
    (cwd / "data").mkdir()
    (cwd / "models").mkdir()

    # Prepare dataframe
    install_fake_pandas_and_sklearn(monkeypatch)
    import importlib as _importlib
    DataFrame = _importlib.import_module('pandas').DataFrame
    df = DataFrame({
        "resp": [1, 0, 1, 0, 1],
        "a": [1, 2, 3, 4, 5],
        "b": [5, 4, 3, 2, 1],
    })

    # Mock subprocess.run to simulate Rscript output
    mock_cp = mock.Mock()
    mock_cp.stdout = "OK"
    monkeypatch.setattr("subprocess.run", lambda *args, **kwargs: mock_cp)

    from App.src.call_model import run_model

    out = run_model(
        data_name="data\\mydata.csv",
        data=df,
        model="my_model.R",
        response="resp",
        predictors=["a", "b"],
    )

    # Output should be forwarded
    assert out == "OK"

    # Files should have been written to data/
    assert (cwd / "data" / "test_mydata.csv").exists()
    assert (cwd / "data" / "train_mydata.csv").exists()


def test_run_model_skips_write_when_files_exist(tmp_path, monkeypatch):
    cwd = tmp_path
    monkeypatch.chdir(cwd)
    (cwd / "data").mkdir()
    (cwd / "models").mkdir()
    # Pre-create files so branch is skipped
    (cwd / "data" / "test_data.csv").write_text("x\n1\n")
    (cwd / "data" / "train_data.csv").write_text("x\n2\n")

    DataFrame = install_fake_pandas_and_sklearn(monkeypatch)
    df = DataFrame({"resp": [1, 0], "a": [1, 2]})

    mock_cp = mock.Mock()
    mock_cp.stdout = "DONE"
    monkeypatch.setattr("subprocess.run", lambda *args, **kwargs: mock_cp)

    install_fake_pandas_and_sklearn(monkeypatch)
    from App.src.call_model import run_model

    out = run_model(
        data_name="data\\data.csv",
        data=df,
        model="m.R",
        response="resp",
        predictors=["a"],
    )
    assert out == "DONE"


def test_run_teste_calls_R_and_returns_stdout(monkeypatch):
    mock_cp = mock.Mock()
    mock_cp.stdout = "METRICS"
    monkeypatch.setattr("subprocess.run", lambda *args, **kwargs: mock_cp)

    from App.src.call_model import run_teste
    out = run_teste("{\"model\":\"m\"}")
    assert out == "METRICS"


def test_run_teste_handles_exception(monkeypatch, capsys):
    def raise_err(*args, **kwargs):
        import subprocess
        raise subprocess.CalledProcessError(1, "Rscript", stderr="fail")

    monkeypatch.setattr("subprocess.run", raise_err)

    from App.src.call_model import run_teste
    out = run_teste("{}")
    # Should not raise and should return None
    assert out is None
    captured = capsys.readouterr()
    assert "Erro ao executar" in captured.out


def test_run_model_handles_subprocess_error(tmp_path, monkeypatch, capsys):
    cwd = tmp_path
    monkeypatch.chdir(cwd)
    (cwd / "data").mkdir()
    (cwd / "models").mkdir()

    DataFrame = install_fake_pandas_and_sklearn(monkeypatch)
    df = DataFrame({"resp": [1, 0, 1, 0], "a": [1, 2, 3, 4]})

    def raise_err(*args, **kwargs):
        import subprocess
        raise subprocess.CalledProcessError(1, "Rscript", stderr="bad")

    monkeypatch.setattr("subprocess.run", raise_err)
    from App.src.call_model import run_model

    out = run_model(
        data_name="data\\file.csv",
        data=df,
        model="m.R",
        response="resp",
        predictors=["a"],
    )
    assert out is None
    assert "Erro ao executar o script R" in capsys.readouterr().out
