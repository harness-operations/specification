from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Callable, Optional


def digest_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def digest_object(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return digest_text(encoded)


@dataclass(frozen=True)
class Artifact:
    artifact_id: str
    content: str
    digest: str

    @classmethod
    def create(cls, artifact_id: str, content: str) -> "Artifact":
        return cls(artifact_id=artifact_id, content=content, digest=digest_text(content))


@dataclass(frozen=True)
class Action:
    action_id: str
    kind: str
    target: str
    content: str
    digest: str

    @classmethod
    def write_text(cls, action_id: str, target: str, content: str) -> "Action":
        body = {"action_id": action_id, "kind": "write_text", "target": target, "content": content}
        return cls(
            action_id=action_id,
            kind="write_text",
            target=target,
            content=content,
            digest=digest_object(body),
        )


@dataclass(frozen=True)
class Review:
    review_id: str
    reviewer: str
    artifact_digest: str
    action_digest: str
    decision: str


@dataclass(frozen=True)
class Approval:
    approval_id: str
    principal: str
    artifact_digest: str
    action_digest: str
    decision: str
    expires_at: int


@dataclass(frozen=True)
class ExecutionResult:
    operation_id: str
    status: str


class HandoffError(RuntimeError):
    pass


class DecisionUnavailable(HandoffError):
    pass


class ValidationError(HandoffError):
    pass


class AuthorizationError(HandoffError):
    pass


class OutcomeUncertain(HandoffError):
    def __init__(self, operation_id: str):
        super().__init__(f"execution outcome is uncertain for operation {operation_id}")
        self.operation_id = operation_id


class EvidenceLog:
    def __init__(self) -> None:
        self.events: list[dict[str, object]] = []

    def emit(self, event_type: str, **details: object) -> None:
        self.events.append(
            {
                "sequence": len(self.events) + 1,
                "type": event_type,
                **details,
            }
        )


class AuthorityRegistry:
    def __init__(self) -> None:
        self._revoked_approvals: set[str] = set()

    def revoke(self, approval_id: str) -> None:
        self._revoked_approvals.add(approval_id)

    def is_revoked(self, approval_id: str) -> bool:
        return approval_id in self._revoked_approvals


class ReceiptStore:
    def __init__(self, workspace: Path) -> None:
        self.path = workspace / ".handoff-receipts.json"

    def _load(self) -> dict[str, dict[str, str]]:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def get(self, operation_id: str) -> Optional[dict[str, str]]:
        return self._load().get(operation_id)

    def put(self, operation_id: str, receipt: dict[str, str]) -> None:
        receipts = self._load()
        receipts[operation_id] = receipt
        self.path.write_text(json.dumps(receipts, sort_keys=True, indent=2) + "\n", encoding="utf-8")


class HandoffExecutor:
    def __init__(
        self,
        workspace: Path,
        evidence: EvidenceLog,
        authority: AuthorityRegistry,
    ) -> None:
        self.workspace = workspace.resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.evidence = evidence
        self.authority = authority
        self.receipts = ReceiptStore(self.workspace)

    def _resolve_target(self, target: str) -> Path:
        requested = (self.workspace / target).resolve()
        if requested != self.workspace and self.workspace not in requested.parents:
            raise ValidationError("target escapes the disposable execution workspace")
        return requested

    def _validate_review(self, artifact: Artifact, action: Action, review: object) -> Review:
        if not isinstance(review, Review):
            raise DecisionUnavailable("review decision is unavailable or malformed")
        if review.decision != "accept":
            raise ValidationError("review did not accept the proposed operation")
        if review.artifact_digest != artifact.digest:
            raise ValidationError("artifact changed after review")
        if review.action_digest != action.digest:
            raise ValidationError("proposed action changed after review")
        return review

    def _validate_approval(
        self,
        artifact: Artifact,
        action: Action,
        approval: Approval,
        now: int,
    ) -> None:
        if approval.decision != "allow":
            raise AuthorizationError("approval is denied")
        if now >= approval.expires_at:
            raise AuthorizationError("approval is expired")
        if self.authority.is_revoked(approval.approval_id):
            raise AuthorizationError("approval authority has been revoked")
        if approval.artifact_digest != artifact.digest:
            raise AuthorizationError("approval is bound to a different artifact")
        if approval.action_digest != action.digest:
            raise AuthorizationError("approval is bound to a different action")

    def _operation_id(self, artifact: Artifact, action: Action, approval: Approval) -> str:
        return digest_object(
            {
                "artifact_digest": artifact.digest,
                "action_digest": action.digest,
                "approval_id": approval.approval_id,
            }
        )

    def execute(
        self,
        artifact: Artifact,
        action: Action,
        review: object,
        approval: Approval,
        *,
        now: int,
        before_apply: Optional[Callable[[], None]] = None,
        simulate_disconnect_after_apply: bool = False,
    ) -> ExecutionResult:
        self.evidence.emit(
            "execution.requested",
            artifact_id=artifact.artifact_id,
            artifact_digest=artifact.digest,
            action_id=action.action_id,
            action_digest=action.digest,
            approval_id=approval.approval_id,
        )

        validated_review = self._validate_review(artifact, action, review)
        self._validate_approval(artifact, action, approval, now)
        self.evidence.emit(
            "execution.validated",
            review_id=validated_review.review_id,
            reviewer=validated_review.reviewer,
            principal=approval.principal,
        )

        operation_id = self._operation_id(artifact, action, approval)
        prior_receipt = self.receipts.get(operation_id)
        if prior_receipt:
            self.evidence.emit("execution.already_applied", operation_id=operation_id)
            return ExecutionResult(operation_id=operation_id, status="already_applied")

        if before_apply is not None:
            before_apply()

        # Revalidate immediately before the protected side effect. This is the
        # fixture's documented enforcement boundary.
        self._validate_approval(artifact, action, approval, now)

        if action.kind != "write_text":
            raise ValidationError(f"unsupported fixture action: {action.kind}")

        target = self._resolve_target(action.target)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(action.content, encoding="utf-8")

        receipt = {
            "target": str(target.relative_to(self.workspace)),
            "target_digest": digest_text(action.content),
            "artifact_digest": artifact.digest,
            "action_digest": action.digest,
        }
        self.receipts.put(operation_id, receipt)
        self.evidence.emit(
            "execution.side_effect_applied",
            operation_id=operation_id,
            target=receipt["target"],
            target_digest=receipt["target_digest"],
        )

        if simulate_disconnect_after_apply:
            self.evidence.emit("execution.outcome_uncertain", operation_id=operation_id)
            raise OutcomeUncertain(operation_id)

        self.evidence.emit("execution.completed", operation_id=operation_id)
        return ExecutionResult(operation_id=operation_id, status="completed")

    def reconcile(self, operation_id: str) -> ExecutionResult:
        receipt = self.receipts.get(operation_id)
        if receipt is None:
            self.evidence.emit("execution.reconcile_unknown", operation_id=operation_id)
            return ExecutionResult(operation_id=operation_id, status="unknown")

        target = self._resolve_target(receipt["target"])
        if not target.exists() or digest_text(target.read_text(encoding="utf-8")) != receipt["target_digest"]:
            self.evidence.emit("execution.reconcile_unknown", operation_id=operation_id)
            return ExecutionResult(operation_id=operation_id, status="unknown")

        self.evidence.emit("execution.reconciled", operation_id=operation_id, status="completed")
        return ExecutionResult(operation_id=operation_id, status="completed")
