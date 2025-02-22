from typing import TYPE_CHECKING, Generator

from .base import EXEC_NAMESPACE, EXPS_NAMESPACE, EXPS_STASH, ExpRefInfo

if TYPE_CHECKING:
    from dvc.scm.git import Git


def exp_refs(scm: "Git") -> Generator["ExpRefInfo", None, None]:
    """Iterate over all experiment refs."""
    for ref in scm.iter_refs(base=EXPS_NAMESPACE):
        if ref.startswith(EXEC_NAMESPACE) or ref == EXPS_STASH:
            continue
        yield ExpRefInfo.from_ref(ref)


def exp_refs_by_rev(
    scm: "Git", rev: str
) -> Generator["ExpRefInfo", None, None]:
    """Iterate over all experiment refs pointing to the specified revision."""
    for ref in scm.get_refs_containing(rev, EXPS_NAMESPACE):
        if not (ref.startswith(EXEC_NAMESPACE) or ref == EXPS_STASH):
            yield ExpRefInfo.from_ref(ref)


def exp_refs_by_name(
    scm: "Git", name: str
) -> Generator["ExpRefInfo", None, None]:
    """Iterate over all experiment refs matching the specified name."""
    for ref_info in exp_refs(scm):
        if ref_info.name == name:
            yield ref_info
