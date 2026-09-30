# Tasks: Tokenizer Application

**Input**: Design documents from `/specs/001-tokenizer-app/`

**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Organization**: Tasks are grouped by user story to enable independent implementation, testing, and delivery.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the backend and frontend structure required by the approved plan.

- [ ] T001 Create the project directories and initial repo structure for `backend/` and `frontend/` per the implementation plan.
- [ ] T002 Initialize the FastAPI backend with Python dependencies: `fastapi`, `uvicorn`, `pydantic`, `pytest`, `tiktoken`, and `PyMuPDF`.
- [ ] T003 Initialize the React + TypeScript frontend with Vite and install required client dependencies: `react`, `typescript`, `vite`, `@types/react`, and `axios`.
- [ ] T004 [P] Configure backend linting and test tooling for `pytest` and import hygiene.
- [ ] T005 [P] Configure frontend linting and formatting tooling for TypeScript and React.
- [ ] T006 Create the shared API contract documentation and establish the expected request/response shape across backend and frontend.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build the foundational architecture that all user stories depend on.

**Critical requirement**: No user story implementation may begin until this phase is complete.

- [ ] T007 Create the backend application scaffold: `backend/app/main.py`, `api/`, `schemas/`, `services/`, `core/`, and `utils/` directories.
- [ ] T008 Implement the FastAPI app entrypoint and application configuration for ports, environment handling, and request lifecycle.
- [ ] T009 [P] Implement common backend exception handling and consistent validation/error response patterns in `backend/app/core/exceptions.py` and related modules.
- [ ] T010 [P] Define Pydantic request and response models for tokenizer requests, file processing, validation errors, and token statistics in `backend/app/schemas/`.
- [ ] T011 Implement the REST router structure for tokenize, file processing, health, and custom vocabulary reset in `backend/app/api/routes/`.
- [ ] T012 Implement backend configuration and in-memory app state for the custom vocabulary baseline and runtime state in `backend/app/core/config.py` and related state modules.
- [ ] T013 Create the shared validation utilities for empty input, invalid encodings, unsupported files, oversized uploads, and PDF extraction failures in `backend/app/utils/validation.py`.
- [ ] T014 [P] Configure the backend test suite structure under `backend/tests/` for service, API, and validation scenarios.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - Enter text or upload supported files and tokenize output (Priority: P1) 🎯 MVP

**Goal**: Deliver the main end-to-end flow for direct text input and file-based input processing.

**Independent Test**: A user can paste text or upload a valid `.txt`/text-based PDF, click tokenize, and receive token summary and token details.

### Tests for User Story 1

- [ ] T015 [P] [US1] Add a backend API contract test for `POST /api/v1/tokenize` with valid text input in `backend/tests/test_tokenize_api.py`.
- [ ] T016 [P] [US1] Add a backend API contract test for `POST /api/v1/process-file` with a valid `.txt` file in `backend/tests/test_file_validation.py`.
- [ ] T017 [P] [US1] Add a backend API test for a valid text-based PDF extraction path in `backend/tests/test_pdf_service.py`.

### Implementation for User Story 1

- [ ] T018 [US1] Implement the file processing service for upload validation, `.txt` handling, and PDF intake in `backend/app/services/file_service.py`.
- [ ] T019 [US1] Implement PDF extraction logic with PyMuPDF for valid text-based PDFs in `backend/app/services/pdf_service.py`.
- [ ] T020 [US1] Implement text normalization and token source handling utilities in `backend/app/utils/text_processing.py`.
- [ ] T021 [US1] Implement the token statistics calculator in `backend/app/services/stats_service.py` for character count, word count, token count, tokens per word, and tokens per character.
- [ ] T022 [US1] Implement the tokenize route in `backend/app/api/routes/tokenize.py` to validate request payloads and call the service layer.
- [ ] T023 [US1] Add the `process-file` route in `backend/app/api/routes/tokenize.py` or file-processing route to validate file type and return extracted text.
- [ ] T024 [US1] Add a health endpoint in `backend/app/api/routes/health.py` to confirm the backend is operational.
- [ ] T025 [US1] Implement the frontend input panel, file upload controls, and mode/encoding selectors in `frontend/src/components/tokenizer/`.
- [ ] T026 [US1] Implement the React app shell and top-level state orchestration in `frontend/src/app/App.tsx` and the relevant hooks.
- [ ] T027 [US1] Implement the HTTP client and REST request layer in `frontend/src/services/api.ts` and `frontend/src/services/tokenizerClient.ts`.
- [ ] T028 [US1] Implement the statistics panel and token table rendering in `frontend/src/components/tokenizer/StatisticsPanel.tsx` and `TokenTable.tsx`.

**Checkpoint**: User Story 1 should be functional and independently testable.

---

## Phase 4: User Story 2 - Tiktoken and Custom Tokenizer mode behavior (Priority: P1)

**Goal**: Support real Tiktoken processing and deterministic custom tokenizer processing without cross-mode contamination.

**Independent Test**: A user can switch between modes and verify that Tiktoken uses the selected encoding while custom mode uses the app-owned vocabulary without mutating Tiktoken state.

### Tests for User Story 2

- [ ] T029 [P] [US2] Add backend tests for supported and unsupported Tiktoken encodings in `backend/tests/test_tiktoken_service.py`.
- [ ] T030 [P] [US2] Add backend tests for deterministic custom tokenization and ID reuse in `backend/tests/test_custom_tokenizer_service.py`.
- [ ] T031 [P] [US2] Add mode-isolation tests to ensure Tiktoken and custom tokenization remain independent.

### Implementation for User Story 2

- [ ] T032 [US2] Implement the Tiktoken service in `backend/app/services/tiktoken_service.py` to validate encodings and return real token IDs and metadata.
- [ ] T033 [US2] Implement the custom tokenizer service in `backend/app/services/custom_tokenizer_service.py` using a regex-based deterministic algorithm.
- [ ] T034 [US2] Implement deterministic ID generation and vocabulary lookup logic for unseen and repeated tokens in the custom tokenizer service.
- [ ] T035 [US2] Implement custom vocabulary frequency tracking, run-state markers, and a vocabulary snapshot response in the custom tokenizer service.
- [ ] T036 [US2] Add the reset-vocabulary endpoint and service behavior in `backend/app/api/routes/tokenize.py` for the in-memory baseline reset workflow.
- [ ] T037 [US2] Implement the frontend mode switch and encoding selector components in `frontend/src/components/tokenizer/ModeSelector.tsx` and `EncodingSelector.tsx`.
- [ ] T038 [US2] Implement the custom vocabulary UI in `frontend/src/components/tokenizer/VocabularyPanel.tsx` and related status badge components.
- [ ] T039 [US2] Ensure the frontend keeps Tiktoken and custom state logically independent and does not move tokenization logic into React.

**Checkpoint**: User Story 2 should be fully functional and independently testable.

---

## Phase 5: User Story 3 - Custom vocabulary lifecycle and new-token tracking (Priority: P1)

**Goal**: Maintain a user-resettable custom vocabulary that updates immediately after successful custom tokenization.

**Independent Test**: A user tokenizes text containing new and existing tokens and then resets the vocabulary back to the initial baseline.

### Tests for User Story 3

- [ ] T040 [P] [US3] Add a backend test for reused token IDs and frequency increment behavior.
- [ ] T041 [P] [US3] Add a backend test for new token creation and newly created token identification.
- [ ] T042 [P] [US3] Add a backend test for reset-to-baseline behavior in custom vocabulary state.

### Implementation for User Story 3

- [ ] T043 [US3] Create the baseline custom vocabulary initialization logic and in-memory reset mechanism in the backend service layer.
- [ ] T044 [US3] Implement the active-run tracking for newly created custom tokens and mark them in the response payload.
- [ ] T045 [US3] Add UI visual differentiation for new vs existing custom vocabulary entries in `frontend/src/components/tokenizer/VocabularyPanel.tsx` and `StatusBadge.tsx`.
- [ ] T046 [US3] Implement immediate vocabulary refresh after successful custom tokenization in the frontend state model and client call logic.
- [ ] T047 [US3] Add reset controls and reset action flow to the content panel and UI state model in `frontend/src/components/tokenizer/InputPanel.tsx`.

**Checkpoint**: Vocabulary lifecycle and custom runtime behavior are complete and independently testable.

---

## Phase 6: User Story 4 - Validation, error handling, and document processing resilience (Priority: P1)

**Goal**: Validate unsupported inputs and provide clear, user-friendly error states without crashing the app.

**Independent Test**: The app reports clear failures for empty input, unsupported file types, oversized files, invalid PDFs, unreadable PDFs, and unsupported encodings.

### Tests for User Story 4

- [ ] T048 [P] [US4] Add validation tests for empty input, malformed requests, and unsupported encodings in `backend/tests/test_file_validation.py`.
- [ ] T049 [P] [US4] Add backend tests for oversized file rejection.
- [ ] T050 [P] [US4] Add backend tests for invalid PDF files and no-extractable-text PDF cases.

### Implementation for User Story 4

- [ ] T051 [US4] Implement centralized validation for empty input, unsupported file types, oversized files, and unsupported Tiktoken encodings in the backend validation utilities.
- [ ] T052 [US4] Implement backend error translation for invalid or corrupt PDF extraction results and no-text PDF extraction cases.
- [ ] T053 [US4] Add frontend error state rendering with actionable user guidance in `frontend/src/components/tokenizer/ErrorBanner.tsx`.
- [ ] T054 [US4] Add loading, empty, and success state components in `frontend/src/components/shared/` and connect them to the top-level app state.
- [ ] T055 [US4] Implement extracted text display for uploaded documents in `frontend/src/components/tokenizer/ExtractedTextPanel.tsx`.
- [ ] T056 [US4] Ensure error states are visually distinct and do not disrupt the overall layout or user flow.

**Checkpoint**: User Story 4 is complete and validation paths are reliable.

---

## Phase 7: User Story 5 - Responsive and accessible UI polish (Priority: P2)

**Goal**: Deliver a professional, responsive, accessible interface with the required sections and a cyberpunk neon aesthetic.

**Independent Test**: A user can navigate the app across desktop and tablet layouts and complete core flows with keyboard and screen-reader-friendly semantics.

### Tests for User Story 5

- [ ] T057 [P] [US5] Add frontend component tests for layout and state transitions for loading, empty, success, and error states.
- [ ] T058 [P] [US5] Add accessibility smoke tests for major controls and keyboard navigation with the app shell.

### Implementation for User Story 5

- [ ] T059 [US5] Implement the neon-gradient dark-theme styling and layout in `frontend/src/styles/globals.css` and `frontend/src/styles/neon.css`.
- [ ] T060 [US5] Create the shared layout shell and page header in `frontend/src/components/layout/`.
- [ ] T061 [US5] Ensure all required UI sections are present: application title, description, input mode and controls, encoding selector, tokenize button, statistics, token visualization, extracted text, and error panel.
- [ ] T062 [US5] Audit color contrast, focus states, and semantic structure for responsive and accessible usage.
- [ ] T063 [US5] Ensure the frontend remains readable and usable across supported viewport sizes and does not rely on hidden state for rendering.

**Checkpoint**: Accessibly styled interface is complete and ready for integration testing.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final verification, contract consistency, and quality checks across all stories.

- [ ] T064 [P] Run the full backend pytest suite for tokenizer service, API contract, validation, and PDF extraction coverage.
- [ ] T065 [P] Run frontend verification for the main state transitions, API response rendering, and custom vocabulary refresh flow.
- [ ] T066 Check that Tiktoken mode never modifies the app-owned custom vocabulary and that the custom tokenizer remains independent.
- [ ] T067 Validate that no database or persistent storage is introduced and that the app remains in scope without out-of-scope features.
- [ ] T068 Verify all API payload fields required for frontend rendering are present and consistent across the tokenization result endpoints.
- [ ] T069 Run a final UX review against the constitution and approved spec for maintainability, accessibility, and clear error handling.
- [ ] T070 [P] Document the startup/run instructions and feature summary for future contributors in the feature docs or project README as needed.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup**: No dependencies; starts immediately.
- **Foundational**: Depends on Setup completion; blocks all User Story work.
- **User Story 1**: Depends on Foundational completion.
- **User Story 2**: Depends on Foundational completion and can begin in parallel with US1 if needed.
- **User Story 3**: Depends on the custom tokenizer service and vocabulary foundation from US2.
- **User Story 4**: Depends on validation and API structure from earlier phases.
- **User Story 5**: Depends on the app shell and major data flow from earlier stories.
- **Polish**: Depends on all desired user story work being complete.

### Parallel Opportunities

- Tasks marked `[P]` can run in parallel when they are isolated to different files and do not share state.
- The backend service tests can be developed in parallel with frontend state implementation once foundational contracts are stable.
- UI component work can proceed in parallel after the API layer and response shapes are agreed.

---

## Notes

- [P] tasks are independent and can be executed in parallel.
- Each user story should be independently testable before moving to the next one.
- The implementation must respect the constitution: modular services, no database, no persistent storage, no tokenization logic in React, and no Tiktoken vocabulary mutation.
- No implementation code is included here; this file is an execution plan for conversion into implementation tasks.
