from unittest import mock


def test_plot_success(monkeypatch, capsys):
    mock_cp = mock.Mock()
    mock_cp.stdout = "PLOT"
    monkeypatch.setattr("subprocess.run", lambda *a, **k: mock_cp)

    from App.src.plot_model import plot
    plot("modelo.rds")
    captured = capsys.readouterr()
    assert "PLOT" in captured.out


def test_plot_error(monkeypatch, capsys):
    def raise_err(*args, **kwargs):
        import subprocess
        raise subprocess.CalledProcessError(1, "Rscript", stderr="boom")

    monkeypatch.setattr("subprocess.run", raise_err)

    from App.src.plot_model import plot
    plot("modelo.rds")
    captured = capsys.readouterr()
    assert "Erro ao executar o script R:" in captured.out
    assert "boom" in captured.out

