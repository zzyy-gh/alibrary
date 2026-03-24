---
name: feedback_thorough_plans
description: User wants exhaustive verification of plans before approval — do final checks proactively
type: feedback
---

Always do a thorough final check before presenting plans for approval. The user will ask for verification if it's not done proactively. Read actual file contents to confirm references, don't rely on grep alone.

**Why:** User has been burned by incomplete audits (wrong UUIDs, missed file references). Trust but verify.

**How to apply:** Before calling ExitPlanMode, re-read critical files to confirm every reference is accounted for. Don't just list files — verify the actual content.
