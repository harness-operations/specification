import json
import tempfile
from pathlib import Path

from handoff import Action, Approval, Artifact, AuthorityRegistry, EvidenceLog, HandoffExecutor, Review


def main() -> None:
    artifact = Artifact.create("artifact-demo", "reviewed patch contents")
    action = Action.write_text("action-demo", "target/output.txt", "approved output")
    review = Review(
        review_id="review-demo",
        reviewer="reviewer@example",
        artifact_digest=artifact.digest,
        action_digest=action.digest,
        decision="accept",
    )
    approval = Approval(
        approval_id="approval-demo",
        principal="operator@example",
        artifact_digest=artifact.digest,
        action_digest=action.digest,
        decision="allow",
        expires_at=100,
    )

    evidence = EvidenceLog()
    authority = AuthorityRegistry()

    with tempfile.TemporaryDirectory() as directory:
        executor = HandoffExecutor(Path(directory), evidence, authority)
        result = executor.execute(artifact, action, review, approval, now=10)
        print(json.dumps({"result": result.status, "operation_id": result.operation_id}, indent=2))
        print(json.dumps(evidence.events, indent=2))


if __name__ == "__main__":
    main()
