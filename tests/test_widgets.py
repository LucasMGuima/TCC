import types
import os
from unittest import mock
import importlib


def _install_fake_streamlit(monkeypatch):
    fake = types.SimpleNamespace()

    def identity_decorator(func=None, **_kwargs):
        # Behaves as a no-op decorator
        def wrapper(f):
            return f
        return wrapper if func is None else func

    fake.cache_data = identity_decorator
    fake.selectbox = lambda label, lst: (label, tuple(lst))
    fake.multiselect = lambda label, lst: (label, tuple(lst))
    fake.title = lambda *a, **k: None
    fake.file_uploader = lambda *a, **k: None
    fake.button = lambda *a, **k: False

    monkeypatch.setitem(importlib.import_module('sys').modules, 'streamlit', fake)
    return fake


def test_contentIn_folder(tmp_path, monkeypatch):
    _install_fake_streamlit(monkeypatch)
    from App.utils.widgets import contentIn_folder

    d = tmp_path / "folder"
    d.mkdir()
    (d / "a.txt").write_text("x")
    (d / "b.txt").write_text("y")

    files = contentIn_folder(str(d))
    assert set(files) == {"a.txt", "b.txt"}

    assert contentIn_folder(str(d / "missing")) is None


def test_select_multiselect(monkeypatch):
    _install_fake_streamlit(monkeypatch)
    from App.utils.widgets import creat_selectbox, creat_multselect
    sel = creat_selectbox([1, 2], "L")
    mul = creat_multselect([3, 4], "M")
    assert sel == ("L", (1, 2))
    assert mul == ("M", (3, 4))
