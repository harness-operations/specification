import tempfile
from pathlib import Path
import unittest

from handoff import (
    Action,
    Approval,
    Artifact,
    AuthorityRegistry,
    AuthorizationError,
    DecisionUnavailable,
    EvidenceLog,
    HandoffExecutor,
    OutcomeUncertain,
    Review,
    ValidationError,
)


def accepted_review(artifact: Artifact, action: Action) -> Review:
    return Review(
        review_id="review-1",
        reviewer="reviewer@example",
        artifact_digest=artifact.digest,
        action_digest=action.digest,
        decision="accept",
    )


def allowed_approval(artifact: Artifact, action: Action, *, expires_at: int = 100) -> Approval:
    return Approval(
        approval_id="approval-1",
        principal="operator@example",
        artifact_digest=artifact.digest,
        action_digest=action.digest,
        decision="allow",
        expires_at=expires_at,
    )


class HandoffTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp.name)
        self.evidence = EvidenceLog()
        self.authority = AuthorityRegistry()
        self.executor = HandoffExecutor(self.workspace, self.evidence, self.authority)
        self.artifact = Artifact.create("artifact-1", "reviewed patch contents")
        self.action = Action.write_text("action-1", "target/output.txt", "approved output")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_happy_path(self) -> None:
        result = self.executor.execute(
            self.artifact,
            self.action,
            accepted_review(self.artifact, self.action),
            allowed_approval(self.artifact, self.action),
            now=10,
        )
        self.assertEqual(result.status, "completed")
        self.assertEqual((self.workspace / "target/output.txt").read_text(), "approved output")
        self.assertEqual(self.evidence.events[-1]["type"], "execution.completed")

    def test_artifact_mutation_after_review_is_rejected(self) -> None:
        review = accepted_review(self.artifact, self.action)
        mutated = Artifact.create("artifact-1", "mutated after review")
        with self.assertRaisesRegex(ValidationError, "artifact changed"):
            self.executor.execute(
                mutated,
                self.action,
                review,
                allowed_approval(mutated, self.action),
                now=10,
            )
        self.assertFalse((self.workspace / "target/output.txt").exists())

    def test_action_mutation_after_review_is_rejected(self) -> None:
        review = accepted_review(self.artifact, self.action)
        changed_action = Action.write_text("action-1", "target/other.txt", "different")
        with self.assertRaisesRegex(ValidationError, "action changed"):
            self.executor.execute(
                self.artifact,
                changed_action,
                review,
                allowed_approval(self.artifact, changed_action),
                now=10,
            )

    def test_missing_or_malformed_decision_fails_closed(self) -> None:
        approval = allowed_approval(self.artifact, self.action)
        for invalid in (None, {"decision": "accept"}):
            with self.subTest(invalid=invalid):
                with self.assertRaises(DecisionUnavailable):
                    self.executor.execute(
                        self.artifact,
                        self.action,
                        invalid,
                        approval,
                        now=10,
                    )

    def test_denied_and_expired_approval_fail_closed(self) -> None:
        review = accepted_review(self.artifact, self.action)
        denied = Approval(
            approval_id="approval-denied",
            principal="operator@example",
            artifact_digest=self.artifact.digest,
            action_digest=self.action.digest,
            decision="deny",
            expires_at=100,
        )
        with self.assertRaisesRegex(AuthorizationError, "denied"):
            self.executor.execute(self.artifact, self.action, review, denied, now=10)

        expired = allowed_approval(self.artifact, self.action, expires_at=10)
        with self.assertRaisesRegex(AuthorizationError, "expired"):
            self.executor.execute(self.artifact, self.action, review, expired, now=10)

    def test_revocation_between_preflight_and_side_effect_is_enforced(self) -> None:
        review = accepted_review(self.artifact, self.action)
        approval = allowed_approval(self.artifact, self.action)

        with self.assertRaisesRegex(AuthorizationError, "revoked"):
            self.executor.execute(
                self.artifact,
                self.action,
                review,
                approval,
                now=10,
                before_apply=lambda: self.authority.revoke(approval.approval_id),
            )

        self.assertFalse((self.workspace / "target/output.txt").exists())

    def test_disconnect_after_side_effect_is_uncertain_until_reconciled(self) -> None:
        review = accepted_review(self.artifact, self.action)
        approval = allowed_approval(self.artifact, self.action)

        with self.assertRaises(OutcomeUncertain) as context:
            self.executor.execute(
                self.artifact,
                self.action,
                review,
                approval,
                now=10,
                simulate_disconnect_after_apply=True,
            )

        operation_id = context.exception.operation_id
        self.assertEqual(self.evidence.events[-1]["type"], "execution.outcome_uncertain")

        reconciled = self.executor.reconcile(operation_id)
        self.assertEqual(reconciled.status, "completed")
        self.assertEqual(self.evidence.events[-1]["type"], "execution.reconciled")

        retry = self.executor.execute(
            self.artifact,
            self.action,
            review,
            approval,
            now=10,
        )
        self.assertEqual(retry.status, "already_applied")

    def test_target_cannot_escape_disposable_workspace(self) -> None:
        action = Action.write_text("action-escape", "../outside.txt", "no")
        review = accepted_review(self.artifact, action)
        approval = allowed_approval(self.artifact, action)
        with self.assertRaisesRegex(ValidationError, "escapes"):
            self.executor.execute(self.artifact, action, review, approval, now=10)


if __name__ == "__main__":
    unittest.main()
