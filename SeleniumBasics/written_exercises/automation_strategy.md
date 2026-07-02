# Hands-On 3 – Test Automation Process, Lifecycle & Framework Types

## Task 1

### 1. Criteria for Deciding What to Automate

There isn't a rule that says "automate everything," so a few things usually decide whether a test case is worth automating.

The first is how often the test gets repeated. If a test case is going to be run over and over, like a regression check that runs after every code change, automating it saves a huge amount of time compared to a person doing it manually each time. For example, the test case "POST /api/courses/ returns 201 with the correct data for valid input" is exactly this kind of case — it will be run on basically every build, so it's a strong candidate.

The second is how stable the feature is. If the feature keeps changing shape every sprint, an automated test for it will keep breaking and needing rewrites, which can actually cost more time than it saves. The course creation endpoint is fairly stable once it's built, so this works in favor of automating it.

The third is how much risk is involved if it breaks. High-risk areas, like core CRUD operations that the whole application depends on, are worth automating because a failure there affects everything downstream. Course creation is a core piece of functionality, so this is another point in favor.

The fourth is whether the test needs human judgment. Something visual or subjective, like "does this page look good," is hard to automate meaningfully and is usually better left to a person. Checking a 201 status code and comparing returned JSON fields, on the other hand, is a purely objective check, which automation handles well.

The fifth is the return on time invested. If writing the automated version takes far longer than just running it manually a handful of times, it might not be worth it yet. For the course creation test, since it will run constantly across every future build, the investment pays off quickly.

### 2. Automate or Manual — Course Management API Test Cases

(a) Regression test for all CRUD endpoints after every code change — **Automate**. This runs constantly and checks the same thing every time, which is exactly what automation is good at.

(b) Exploratory testing of a new search feature — **Manual**. Exploratory testing is about a human poking around and using intuition to find unexpected issues, which automation can't really replicate.

(c) Performance test with 100 concurrent users hitting GET /api/courses/ — **Automate**, but using a dedicated performance tool rather than Selenium, since simulating concurrent load isn't something a browser-driven test is built for.

(d) UI test for the login form — **Automate**. It's a fixed, repeatable flow (enter credentials, click login, check result), which is a textbook case for Selenium.

(e) Verifying the Swagger documentation is accurate — **Manual**. This needs a person to actually read the docs and compare them against how the API behaves, which isn't something a script can judge well.

(f) Smoke test to verify the API is reachable after deployment — **Automate**. It's simple, fast, and needs to run after every single deployment, so automating it means the team gets an instant signal instead of waiting on someone to check manually.

### 3. Automation ROI

Automation ROI is basically asking: after all the time spent building and maintaining an automated test, does it end up saving more time than it cost?

For this scenario, building the automated version takes 4 hours, and running the test manually takes 30 minutes each time.

Without factoring in maintenance, the automated version pays for itself once the time saved from not running it manually catches up to that initial 4-hour investment. That works out to 4 hours divided by 30 minutes per run, which is 8 runs.

But there's also a 20% maintenance overhead added after the 10th run, so after run 10, every run effectively costs 30 minutes times 1.2, which is 36 minutes of manual-equivalent time being saved instead of the full 30. Since the break-even point of 8 runs happens before that 10-run mark, the maintenance overhead doesn't actually change the answer here — the automation still pays for itself by the 8th run, and after that every additional run is pure time saved, even accounting for the extra maintenance cost that kicks in later.

### 4. Flaky Tests

A flaky test is one that sometimes passes and sometimes fails without the actual code changing in between, which makes it unreliable as a signal.

A common example in a Selenium suite is a test that clicks a button and immediately checks for a result, without waiting for the page to actually finish loading or for an element to become visible. On a fast machine or fast network it passes, but on a slower run it fails, even though nothing about the application actually broke.

A few ways to prevent or fix this:

First, replace any fixed sleep() calls with explicit waits, so the test waits for the actual condition (like an element becoming visible) instead of guessing a fixed amount of time.

Second, make sure each test starts from a clean, predictable state, like a fresh browser session or a reset database, so tests aren't accidentally affected by leftover data from a previous test run.

Third, avoid relying on timing-sensitive or animation-heavy UI elements where possible, and if that's not avoidable, wait specifically for the animation or transition to finish before interacting with the element.

---

## Task 2

### 5. Comparing the Five Framework Types

**Linear Framework** — this is the simplest approach, where each test script is written from start to finish with the steps hardcoded directly into the script, with no reuse between tests. It's quick to get started with, which is its main advantage, but the downside is that if a step like the login process changes, it has to be manually updated in every single script that uses it. It would only really make sense for a one-off, throwaway check on the Course Management system, not for anything that needs to be maintained long-term.

**Modular Framework** — this breaks the application into separate reusable functions, like a `login()` function or a `create_course()` function, and test scripts call these functions instead of repeating the same steps everywhere. The advantage is that if something changes, it only needs to be fixed in one function. The disadvantage is it still requires someone who can write code to build and use these modules. This would suit the Course Management frontend well, since login and course-creation steps are reused constantly across many tests.

**Data-Driven Framework** — this separates the test logic from the actual test data, so the same script runs multiple times with different input values pulled from a file or spreadsheet. The advantage is being able to test many combinations of input without duplicating the script itself. The disadvantage is that it adds complexity in managing the external data files and keeping them in sync with the tests. This fits well for something like testing course creation with dozens of different valid and invalid input combinations.

**Keyword-Driven Framework** — here, test steps are represented as keywords, like "Login" or "ClickSubmit," often stored in a spreadsheet, and the framework translates each keyword into the actual code that performs it. The advantage is that non-technical team members can write or modify tests just by arranging keywords, without touching code. The disadvantage is that building the underlying keyword engine takes considerable upfront effort. This could work well if the Course Management project has QA members who aren't strong coders but still need to contribute test cases.

**Hybrid Framework** — this combines pieces of the other approaches, usually taking the reusability of Modular, the parameterization of Data-Driven, and sometimes the accessibility of Keyword-Driven. The advantage is flexibility, since it can be shaped around what the team actually needs. The disadvantage is that it takes more planning and effort to set up properly compared to picking just one simple approach. For a growing project like the Course Management frontend, this is generally the most practical long-term choice.

### 6. Recommended Framework for the Given Scenario

The team needs to test login with 50 different user and password combinations, reuse login steps across 20 different test cases, and let both technical and non-technical team members write tests.

A pure Data-Driven approach handles the 50 login combinations well, and a pure Modular approach handles reusing the login steps across 20 tests, but neither one alone covers the third requirement about non-technical members writing tests.

Because of that, a Hybrid Framework makes the most sense here — specifically one that combines Modular (so the login flow is written once and reused everywhere), Data-Driven (so the 50 combinations are just rows in a data file rather than 50 separate scripts), and Keyword-Driven elements on top (so non-technical members can put together new test cases from existing keywords without writing code directly).

### 7. Hybrid Framework Folder Structure

For the Course Management frontend tests, a Hybrid framework folder structure would look roughly like this:

A `test_data` folder holding files like `login_credentials.csv` or `course_data.json`, which store all the different input combinations used by the data-driven parts of the suite.

A `pages` folder holding the page object files, like `login_page.py` and `course_page.py`, each containing the locators and actions for that specific page.

A `utils` folder holding shared helper code, like a custom wait helper, a config reader, or a report generator, that multiple tests rely on.

A `tests` folder holding the actual test files, like `test_login.py` and `test_course_creation.py`, which call into the page objects and read from the test data files, but don't contain any raw locators themselves.

A `config` folder or file, like `config.yaml`, holding environment-specific settings such as the base URL, browser type, and timeout values, so these don't get hardcoded inside the tests.
