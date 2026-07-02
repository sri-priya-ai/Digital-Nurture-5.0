# Hands-On 1 – QA Concepts, Functional Testing & Defect Lifecycle

## Task 1

### 1. Testing Types for Course Management API

#### Unit Testing

**Test Case:** Check whether the `validate_course_code()` function correctly rejects an invalid course code like `cs101` (should be something like `CS-101`).

* **Description:** Test only this one function directly, with no database or API call involved — just call it with different inputs and check the return value.
* **Type:** Functional Testing

---

#### Integration Testing

**Test Case:** Test the **POST /api/courses/** endpoint together with the database.

* **Description:** Send a request to create a course, then query the database directly to confirm a row was actually inserted with the correct values — not just that the API responded with success.
* **Type:** Functional Testing

---

#### System Testing

**Test Case:** Create a course through the API, then immediately fetch it back using the GET API.

* **Description:** Covers the full flow end-to-end — request goes in, hits validation, gets saved to the database, and comes back out correctly — with nothing mocked or skipped. Also confirms server-generated fields like `id` and `created_at` are correct.
* **Type:** Functional Testing

---

#### User Acceptance Testing (UAT)

**Test Case:** A college admin logs in and adds a new course through the portal.

* **Description:** Checks whether the admin can complete this task smoothly using the actual UI, without any confusing errors or unexpected behavior — this is about whether the feature is genuinely usable, not whether the code is technically correct.
* **Type:** Functional Testing

---

### Non-Functional Testing Example

**Performance Testing**

Check whether **GET /api/courses/** still responds within 2 seconds when 100 users are hitting it at the same time with 50,000 courses already in the database.

This is a **Non-Functional Test** because it checks how well the system performs under load, not whether a feature works correctly.

---

### 2. Black-Box Testing vs White-Box Testing

**Black-Box Testing**

The tester doesn't know how the code is written internally. They only give an input and check whether the output matches what's expected, based purely on requirements.

**White-Box Testing**

The tester knows the code, and designs test cases around the internal logic, conditions, and different code paths — for example, deliberately writing a test to hit a specific `if/else` branch they know exists in the source.

**Who Performs It?**

* QA Tester → Mostly does **Black-Box Testing**
* Developer → Mostly does **White-Box Testing**

---

### 3. Formal Test Cases for POST /api/courses/

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|
| TC001 | Create a course with valid details | API is running, user is authenticated | 1. Send POST request with valid course details (name, code, credits, instructor). | Course is created successfully with status code 201, and the response includes the new course's ID. | | |
| TC002 | Create a course without course name | API is running, user is authenticated | 1. Send POST request with the `name` field missing. | Validation error with status code 400, and no course is created in the database. | | |
| TC003 | Create a duplicate course | A course with the same course code already exists | 1. Send POST request using a course code that's already in use. | Error response (409 or 400) saying the course code already exists; no duplicate record is created. | | |

---

## Task 2

### 4. Defect Lifecycle

The defect lifecycle starts the moment a tester finds a bug.

**New → Assigned → Open → Fixed → Retest → Verified → Closed**

* **New** – Tester finds the bug and logs it.
* **Assigned** – A lead reviews it and assigns it to a developer.
* **Open** – Developer starts working on it.
* **Fixed** – Developer fixes the issue and pushes the code.
* **Retest** – Tester runs the same test again to check if it's actually fixed.
* **Verified** – Tester confirms the fix works and nothing else broke because of it.
* **Closed** – The defect is closed.

**Other Paths**

**Rejected** – The developer or lead decides it's not really a bug (maybe it's working as intended, or it's a duplicate of an existing report), so it's rejected instead of moving to Fixed. It can be reopened if the tester disagrees and provides more evidence.

**Deferred** – The defect is valid, but the team decides not to fix it in the current release since it's low-impact or not urgent — it gets picked up in a future release instead.

---

### 5. Severity and Priority Classification

**a) POST /api/courses/ returns 500 Internal Server Error**

* **Severity:** Critical
* **Priority:** P1
* **Reason:** Nobody can create a course at all — the core feature is completely broken for every user, so this needs to be fixed immediately.

**b) Course names longer than 150 characters get cut off without showing an error**

* **Severity:** Medium
* **Priority:** P3
* **Reason:** The system doesn't crash and this probably affects a small number of cases, but it silently corrupts data — the user has no idea their input got truncated. Bad, but not urgent enough to stop everything.

**c) Swagger page has a spelling mistake**

* **Severity:** Low
* **Priority:** P4
* **Reason:** Purely cosmetic — doesn't affect functionality or data in any way. Can be fixed whenever there's spare time.

**d) Login sometimes returns 401 even with correct credentials**

* **Severity:** High
* **Priority:** P1
* **Reason:** Users get randomly locked out of accounts that should work — and because it's intermittent, it's hard to reproduce and usually points to a deeper issue (like a race condition or token timing bug), which makes it more concerning than a bug that fails consistently and predictably.

---

### 6. Defect Report

**Defect ID:** BUG-001

**Title:** POST /api/courses/ returns 500 Internal Server Error

**Environment:** Windows 11, Python 3.12, FastAPI, Chrome Browser

**Build Version:** v1.0

**Severity:** Critical

**Priority:** P1

**Steps to Reproduce:**
1. Start the API server.
2. Open Swagger UI.
3. Select POST /api/courses/.
4. Enter valid course details.
5. Click Execute.

**Expected Result:** The course should be created successfully with status code **201**, and the response should include the created course's data.

**Actual Result:** The API returns **500 Internal Server Error** for every request, regardless of the input provided.

**Attachments:** Screenshot of 500 error.

---

### 7. Difference Between Severity and Priority

**Severity** tells how badly the defect affects the system — the actual technical impact.

**Priority** tells how quickly the defect needs to be fixed — driven by business or scheduling reasons, not just how broken it is.

**Example:**

Suppose the company logo goes missing from the home page right before an important client demo.

* **Severity:** Low — the application still works perfectly fine, nothing is actually broken or lost.
* **Priority:** High — it needs to be fixed immediately anyway, because the client is about to see it and it looks unprofessional.

A second example, going the other way: a rarely-used "export to legacy XML" feature that crashes completely would be **High Severity** (it fully breaks when used), but if only one client uses it and they're being migrated off it next month, it could still be **Low Priority** — because fixing it isn't worth the effort right now.

This shows Severity and Priority don't always move together — one is about how bad the bug is, the other is about how soon it needs attention.
