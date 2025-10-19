from types import SimpleNamespace
import gpt_pr.gh as gh_module


def test_create_pr_success(mocker, capsys):
    fake_repo = mocker.Mock()
    pr = SimpleNamespace(html_url="http://fake.url")
    fake_repo.create_pull.return_value = pr

    fake_gh = SimpleNamespace()
    fake_gh.get_repo = lambda repo_name: fake_repo

    branch_info = SimpleNamespace(
        owner="owner", repo="repo", branch="feature-branch", base_branch="main"
    )
    pr_data = SimpleNamespace(
        title="Test PR", branch_info=branch_info, create_body=lambda: "My body"
    )

    gh_module.create_pr(pr_data, yield_confirmation=True, gh=fake_gh)

    fake_repo.create_pull.assert_called_once_with(
        title="Test PR", body="My body", head="feature-branch", base="main"
    )
    captured = capsys.readouterr()
    assert "Pull request created successfully" in captured.out
    assert "http://fake.url" in captured.out


def test_create_pr_cancel(mocker, capsys):
    fake_repo = mocker.Mock()
    fake_gh = SimpleNamespace()
    fake_gh.get_repo = lambda repo_name: fake_repo

    class FakePrompt:
        def __init__(self, *args, **kwargs):
            pass

        def execute(self):
            return False

    mocker.patch.object(
        gh_module.inquirer,
        "confirm",
        lambda *args, **kwargs: FakePrompt(*args, **kwargs),
    )

    branch_info = SimpleNamespace(
        owner="owner", repo="repo", branch="branch", base_branch="base"
    )
    pr_data = SimpleNamespace(
        title="Cancel PR", branch_info=branch_info, create_body=lambda: "Body"
    )

    gh_module.create_pr(pr_data, yield_confirmation=False, gh=fake_gh)

    fake_repo.create_pull.assert_not_called()
    captured = capsys.readouterr()

    assert "cancelling..." in captured.out
