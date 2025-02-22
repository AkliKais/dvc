import logging
import os
from functools import partial
from typing import Callable, Iterable, Optional, Tuple

from funcy import first

from dvc.progress import Tqdm
from dvc.scm.base import CloneError, RevError, SCMError
from dvc.tree.base import BaseTree
from dvc.utils import fix_env, is_binary

from .base import BaseGitBackend

logger = logging.getLogger(__name__)


class TqdmGit(Tqdm):
    def update_git(self, op_code, cur_count, max_count=None, message=""):
        op_code = self.code2desc(op_code)
        if op_code:
            message = (op_code + " | " + message) if message else op_code
        if message:
            self.postfix["info"] = f" {message} | "
        self.update_to(cur_count, max_count)

    @staticmethod
    def code2desc(op_code):
        from git import RootUpdateProgress as OP

        ops = {
            OP.COUNTING: "Counting",
            OP.COMPRESSING: "Compressing",
            OP.WRITING: "Writing",
            OP.RECEIVING: "Receiving",
            OP.RESOLVING: "Resolving",
            OP.FINDING_SOURCES: "Finding sources",
            OP.CHECKING_OUT: "Checking out",
            OP.CLONE: "Cloning",
            OP.FETCH: "Fetching",
            OP.UPDWKTREE: "Updating working tree",
            OP.REMOVE: "Removing",
            OP.PATHCHANGE: "Changing path",
            OP.URLCHANGE: "Changing URL",
            OP.BRANCHCHANGE: "Changing branch",
        }
        return ops.get(op_code & OP.OP_MASK, "")


class GitPythonBackend(BaseGitBackend):  # pylint:disable=abstract-method
    """git-python Git backend."""

    def __init__(  # pylint:disable=W0231
        self, scm, root_dir=os.curdir, search_parent_directories=True
    ):
        import git
        from git.exc import InvalidGitRepositoryError

        self.scm = scm

        try:
            self.repo = git.Repo(
                root_dir, search_parent_directories=search_parent_directories
            )
        except InvalidGitRepositoryError:
            msg = "{} is not a git repository"
            raise SCMError(msg.format(root_dir))

        # NOTE: fixing LD_LIBRARY_PATH for binary built by PyInstaller.
        # http://pyinstaller.readthedocs.io/en/stable/runtime-information.html
        env = fix_env(None)
        libpath = env.get("LD_LIBRARY_PATH", None)
        self.repo.git.update_environment(LD_LIBRARY_PATH=libpath)

    def close(self):
        self.repo.close()

    @property
    def git(self):
        return self.repo.git

    def is_ignored(self, path):
        raise NotImplementedError

    @property
    def root_dir(self) -> str:
        return self.repo.working_tree_dir

    @staticmethod
    def clone(
        url: str,
        to_path: str,
        rev: Optional[str] = None,
        shallow_branch: Optional[str] = None,
    ):
        import git

        ld_key = "LD_LIBRARY_PATH"

        env = fix_env(None)
        if is_binary() and ld_key not in env.keys():
            # In fix_env, we delete LD_LIBRARY_PATH key if it was empty before
            # PyInstaller modified it. GitPython, in git.Repo.clone_from, uses
            # env to update its own internal state. When there is no key in
            # env, this value is not updated and GitPython re-uses
            # LD_LIBRARY_PATH that has been set by PyInstaller.
            # See [1] for more info.
            # [1] https://github.com/gitpython-developers/GitPython/issues/924
            env[ld_key] = ""

        try:
            if shallow_branch is not None and os.path.exists(url):
                # git disables --depth for local clones unless file:// url
                # scheme is used
                url = f"file://{url}"
            with TqdmGit(desc="Cloning", unit="obj") as pbar:
                clone_from = partial(
                    git.Repo.clone_from,
                    url,
                    to_path,
                    env=env,  # needed before we can fix it in __init__
                    no_single_branch=True,
                    progress=pbar.update_git,
                )
                if shallow_branch is None:
                    tmp_repo = clone_from()
                else:
                    tmp_repo = clone_from(branch=shallow_branch, depth=1)
            tmp_repo.close()
        except git.exc.GitCommandError as exc:  # pylint: disable=no-member
            raise CloneError(url, to_path) from exc

        # NOTE: using our wrapper to make sure that env is fixed in __init__
        repo = GitPythonBackend(None, to_path)

        if rev:
            try:
                repo.checkout(rev)
            except git.exc.GitCommandError as exc:  # pylint: disable=no-member
                raise RevError(
                    "failed to access revision '{}' for repo '{}'".format(
                        rev, url
                    )
                ) from exc

    @staticmethod
    def is_sha(rev):
        import git

        return rev and git.Repo.re_hexsha_shortened.search(rev)

    @property
    def dir(self) -> str:
        return self.repo.git_dir

    def add(self, paths: Iterable[str]):
        # NOTE: GitPython is not currently able to handle index version >= 3.
        # See https://github.com/iterative/dvc/issues/610 for more details.
        try:
            self.repo.index.add(paths)
        except AssertionError:
            msg = (
                "failed to add '{}' to git. You can add those files "
                "manually using `git add`. See "
                "https://github.com/iterative/dvc/issues/610 for more "
                "details.".format(str(paths))
            )

            logger.exception(msg)

    def commit(self, msg: str):
        self.repo.index.commit(msg)

    def checkout(
        self, branch: str, create_new: Optional[bool] = False, **kwargs
    ):
        if create_new:
            self.repo.git.checkout("HEAD", b=branch, **kwargs)
        else:
            self.repo.git.checkout(branch, **kwargs)

    def pull(self, **kwargs):
        infos = self.repo.remote().pull(**kwargs)
        for info in infos:
            if info.flags & info.ERROR:
                raise SCMError(f"pull failed: {info.note}")

    def push(self):
        infos = self.repo.remote().push()
        for info in infos:
            if info.flags & info.ERROR:
                raise SCMError(f"push failed: {info.summary}")

    def branch(self, branch):
        self.repo.git.branch(branch)

    def tag(self, tag):
        self.repo.git.tag(tag)

    def untracked_files(self):
        files = self.repo.untracked_files
        return [os.path.join(self.repo.working_dir, fname) for fname in files]

    def is_tracked(self, path):
        return bool(self.repo.git.ls_files(path))

    def is_dirty(self, **kwargs):
        return self.repo.is_dirty(**kwargs)

    def active_branch(self):
        return self.repo.active_branch.name

    def list_branches(self):
        return [h.name for h in self.repo.heads]

    def list_tags(self):
        return [t.name for t in self.repo.tags]

    def list_all_commits(self):
        return [c.hexsha for c in self.repo.iter_commits("--all")]

    def get_tree(self, rev: str, **kwargs) -> BaseTree:
        from dvc.tree.git import GitTree

        return GitTree(self.repo, self.resolve_rev(rev), **kwargs)

    def get_rev(self):
        return self.repo.rev_parse("HEAD").hexsha

    def resolve_rev(self, rev):
        from contextlib import suppress

        from git.exc import BadName, GitCommandError

        def _resolve_rev(name):
            with suppress(BadName, GitCommandError):
                try:
                    # Try python implementation of rev-parse first, it's faster
                    return self.repo.rev_parse(name).hexsha
                except NotImplementedError:
                    # Fall back to `git rev-parse` for advanced features
                    return self.repo.git.rev_parse(name)
                except ValueError:
                    raise RevError(f"unknown Git revision '{name}'")

        # Resolve across local names
        sha = _resolve_rev(rev)
        if sha:
            return sha

        # Try all the remotes and if it resolves unambiguously then take it
        if not self.is_sha(rev):
            shas = {
                _resolve_rev(f"{remote.name}/{rev}")
                for remote in self.repo.remotes
            } - {None}
            if len(shas) > 1:
                raise RevError(f"ambiguous Git revision '{rev}'")
            if len(shas) == 1:
                return shas.pop()

        raise RevError(f"unknown Git revision '{rev}'")

    def resolve_commit(self, rev):
        """Return Commit object for the specified revision."""
        from git.exc import BadName, GitCommandError
        from git.objects.tag import TagObject

        try:
            commit = self.repo.rev_parse(rev)
        except (BadName, GitCommandError):
            commit = None
        if isinstance(commit, TagObject):
            commit = commit.object
        return commit

    def branch_revs(
        self, branch: str, end_rev: Optional[str] = None
    ) -> Iterable[str]:
        """Iterate over revisions in a given branch (from newest to oldest).

        If end_rev is set, iterator will stop when the specified revision is
        reached.
        """
        commit = self.resolve_commit(branch)
        while commit is not None:
            yield commit.hexsha
            commit = first(commit.parents)
            if commit and commit.hexsha == end_rev:
                return

    def set_ref(
        self,
        name: str,
        new_ref: str,
        old_ref: Optional[str] = None,
        message: Optional[str] = None,
        symbolic: Optional[bool] = False,
    ):
        raise NotImplementedError

    def get_ref(self, name, follow: Optional[bool] = True) -> Optional[str]:
        raise NotImplementedError

    def remove_ref(self, name: str, old_ref: Optional[str] = None):
        raise NotImplementedError

    def iter_refs(self, base: Optional[str] = None):
        from git import Reference

        for ref in Reference.iter_items(self.repo, common_path=base):
            if base and base.endswith("/"):
                base = base[:-1]
            yield "/".join([base, ref.name])

    def get_refs_containing(self, rev: str, pattern: Optional[str] = None):
        from git.exc import GitCommandError

        try:
            if pattern:
                args = [pattern]
            else:
                args = []
            for line in self.git.for_each_ref(
                *args, contains=rev, format=r"%(refname)"
            ).splitlines():
                line = line.strip()
                if line:
                    yield line
        except GitCommandError:
            pass

    def push_refspec(self, url: str, src: Optional[str], dest: str):
        raise NotImplementedError

    def fetch_refspecs(
        self,
        url: str,
        refspecs: Iterable[str],
        force: Optional[bool] = False,
        on_diverged: Optional[Callable[[bytes, bytes], bool]] = None,
    ):
        raise NotImplementedError

    def _stash_iter(self, ref: str):
        raise NotImplementedError

    def _stash_push(
        self,
        ref: str,
        message: Optional[str] = None,
        include_untracked: Optional[bool] = False,
    ) -> Tuple[Optional[str], bool]:
        from dvc.scm.git import Stash

        args = ["push"]
        if message:
            args.extend(["-m", message])
        if include_untracked:
            args.append("--include-untracked")
        self.git.stash(*args)
        commit = self.resolve_commit("stash@{0}")
        if ref != Stash.DEFAULT_STASH:
            # `git stash` CLI doesn't support using custom refspecs,
            # so we push a commit onto refs/stash, make our refspec
            # point to the new commit, then pop it from refs/stash
            # `git stash create` is intended to be used for this kind of
            # behavior but it doesn't support --include-untracked so we need to
            # use push
            self.scm.dulwich.set_ref(
                ref, commit.hexsha, message=commit.message
            )
            self.git.stash("drop")
        return commit.hexsha, False

    def _stash_apply(self, rev: str):
        self.git.stash("apply", rev)

    def reflog_delete(self, ref: str, updateref: bool = False):
        args = ["delete"]
        if updateref:
            args.append("--updateref")
        args.append(ref)
        self.git.reflog(*args)

    def describe(
        self,
        rev: str,
        base: Optional[str] = None,
        match: Optional[str] = None,
        exclude: Optional[str] = None,
    ) -> Optional[str]:
        raise NotImplementedError

    def diff(self, rev_a: str, rev_b: str, binary=False) -> str:
        raise NotImplementedError

    def reset(self, hard: bool = False, paths: Iterable[str] = None):
        self.repo.head.reset(index=True, working_tree=hard, paths=paths)

    def checkout_paths(self, paths: Iterable[str], force: bool = False):
        """Checkout the specified paths from HEAD index."""
        if paths:
            self.repo.index.checkout(paths=paths, force=force)
