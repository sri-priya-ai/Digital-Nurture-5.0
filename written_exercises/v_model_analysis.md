# Hands-On 2 – SDLC vs TDLC, V-Model & Agile QA Integration

## Task 1

### 1. V-Model Explained

The V-Model basically takes the usual step-by-step development process and lines it up against a matching testing process, so instead of testing happening only at the very end, each development phase has its own testing counterpart planned right from the start.

On the development side, you start with Requirements, then move to System Design, then Architecture Design, then Module Design, and finally Coding, which sits at the very bottom of the V.

On the testing side, each of those phases has a matching test level:

* Requirements pairs up with Acceptance Testing
* System Design pairs up with System Testing
* Architecture Design pairs up with Integration Testing
* Module Design pairs up with Unit Testing

So as you go down the development side, you're getting more detailed (from big-picture requirements down to actual code), and as you go up the testing side, you're getting broader again (from testing one small unit, all the way up to testing whether the whole system satisfies the business need). Coding is the one point where both sides meet in the middle.

---

### 2. What Gets Prepared at Each Phase

One thing that makes the V-Model useful is that you don't wait until coding is done to start thinking about tests — each phase produces its own test artifact alongside the development work:

* While Requirements are being written, the Acceptance Test Plan is also being drafted, based on what the business actually needs.
* While System Design is happening, the System Test Plan gets written, covering how the whole system should behave.
* While Architecture Design is happening, the Integration Test Plan gets written, covering how the different components are expected to talk to each other.
* While Module Design is happening, the Unit Test Plan gets written for the individual functions and modules.
* Coding itself happens alongside writing the actual unit tests.

Basically, test planning runs in parallel with each design phase instead of trailing behind it.

---

### 3. Entry and Exit Criteria for Each Testing Level

**Unit Testing**
Entry: the module's code is written and compiles without errors.
Exit: all the planned unit tests pass, and code coverage hits the agreed target.

**Integration Testing**
Entry: the individual modules have already passed unit testing and are ready to be connected together.
Exit: the modules work correctly together, and there are no critical defects still open.

**System Testing**
Entry: all modules are integrated and the build is stable enough to test end-to-end.
Exit: every planned system test case has been run, and there's nothing critical or high severity left unresolved.

**Acceptance Testing**
Entry: system testing is finished, and the build has been deployed to a staging or UAT environment.
Exit: the business stakeholders confirm the system actually meets their requirements and sign off on it.

---

### 4. Two Places QA Should Get Involved Early

The first spot is right at the Requirements stage. QA should be reviewing the requirements document itself before any design or coding starts, just to catch things that are vague or impossible to test. For example, if a requirement just says "the system should be fast," QA should push back and ask for an actual number, like a response time target, otherwise there's no way to write a real test case for it later.

The second spot is during the Design phase, whether that's system design or architecture design. QA reviewing the design early can catch things like a service that can't really be tested on its own, or a lack of proper logging that would make debugging painful later. Catching that kind of issue at the design stage is a lot cheaper than discovering it once the whole system is already built.

---

## Task 2

### 5. What Goes Wrong When Testing Happens Only at the End (Waterfall)

If the Course Management API only gets tested after development is completely finished, a few things tend to go wrong.

First, bugs get discovered way too late. If there was a mistake in how a requirement was understood right at the start, that mistake might not surface until months of code has already been built on top of it, and by then it's a lot more expensive and painful to fix.

Second, there's usually no time buffer left. Testing gets squeezed into whatever time is left before the deadline, so if QA finds serious issues at that point, there often isn't enough time to properly fix and retest everything before the release actually has to go out.

Third, developers have usually moved on by the time a bug comes back to them. They might be deep into a completely different feature, so they have to stop, go back, and try to remember code they wrote weeks earlier, which is slower and more error-prone than fixing something while it's still fresh in their head.

---

### 6. QA's Role in Agile Ceremonies

During **Sprint Planning**, QA helps write out clear, testable acceptance criteria for each user story before the sprint even begins, so everyone on the team agrees upfront on what "done" actually means for that story.

During the **Daily Standup**, QA flags anything that's blocking progress, like a test environment being down or a dependency that isn't ready yet, so the team can sort it out quickly instead of losing an entire day to it.

During the **Sprint Review**, QA demos the functionality that's been tested so far and gives an honest picture to stakeholders of what's genuinely working versus what still has open issues.

During the **Retrospective**, QA brings up whatever testing problems came up that sprint, like flaky tests or last-minute requirement changes, so the team can improve the process going into the next sprint.

---

### 7. Shift-Left Practices for the Course Management API

One practice is reviewing requirements for testability before development even starts. So before coding begins, QA checks that something like "course code must be unique" is specific enough to actually be tested against, rather than something vague.

Another is writing test cases before the code itself, following a TDD or BDD style. For something like the "create course" feature, the Given-When-Then scenarios would get written first, so the expected behavior is locked down before anyone writes the actual implementation.

A third practice is running static code analysis automatically on every commit, using something like flake8 or pylint, so obvious code issues get caught before the code even reaches a human tester.

The fourth is API contract testing before integration actually begins. Before the frontend team starts building against the Course Management API, they test against the agreed request/response schema first, so mismatches between frontend and backend get caught early instead of after both sides are already fully built.

---

### 8. Acceptance Criteria for the User Story

User story: As a college admin, I want to create a new course, so that students can enroll in it.

**Happy path**
Given I'm logged in as a college admin, when I submit a new course with a unique course code and all the required fields filled in, then the course should be created successfully and show up in the course list.

**Duplicate course code**
Given a course with the code CS-101 already exists, when I try to create another course using that same code, then the system should show an error saying the course code is already taken, and no new course should be created.

**Missing required field**
Given I'm logged in as a college admin, when I submit a course without entering the course name, then the system should show a validation error and the course should not be created.
