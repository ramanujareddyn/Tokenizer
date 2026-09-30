# Feature Specification: Tokenizer Application

**Feature Branch**: `001-tokenizer-app`

**Created**: 2026-09-29

**Status**: Draft

**Input**: User description: "Define the functional requirements for the Tokenizer Application. The application must: ..."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Enter or upload text for tokenization (Priority: P1)

A user wants to analyze a short message or a document by pasting text or uploading a supported file and seeing how it is tokenized. The app must make the process obvious and immediate, while clearly surfacing any validation failures.

**Why this priority**: This is the primary value of the product: turning input text into understandable token information with visible metrics and error handling.

**Independent Test**: A user can paste text, choose a tokenizer mode and encoding, click tokenization, and immediately see token details and summary statistics.

**Acceptance Scenarios**:

1. **Given** the application is open, **When** a user enters plain text and selects a supported tokenizer mode, **Then** the app tokenizes the content and shows token-level details, aggregate metrics, and the selected source type.
2. **Given** the application is open, **When** a user uploads a valid `.txt` file, **Then** the app extracts the file content and processes it the same as direct text input.
3. **Given** the application is open, **When** a user uploads a valid text-based PDF, **Then** the app extracts readable text and tokenizes the extracted content.

---

### User Story 2 - Use Tiktoken or Custom Tokenizer modes safely and independently (Priority: P1)

A user wants to compare tokenization results across two modes: real Tiktoken output and the application-owned custom vocabulary strategy. The app must keep the two modes separate and must prevent Tiktoken state from being mutated.

**Why this priority**: Comparison and correctness are core to the product; mode independence and correctness are critical to trust and usability.

**Independent Test**: A user switches between modes, selects encodings, and confirms that Tiktoken results are real and custom vocabulary behavior does not change Tiktoken state.

**Acceptance Scenarios**:

1. **Given** the app is configured for Tiktoken mode, **When** a user selects a supported encoding, **Then** the app uses that exact encoding for tokenization and returns real token IDs and token metadata.
2. **Given** the app is configured for Custom Tokenizer mode, **When** the user tokenizes text with tokens not yet in the vocabulary, **Then** the app creates deterministic custom IDs and tracks token frequency.
3. **Given** Tiktoken mode is active, **When** custom tokenization is performed or the vocabulary is reset, **Then** the Tiktoken vocabulary remains unchanged.

---

### User Story 3 - Manage customizable vocabulary and track new tokens (Priority: P1)

A user wants to understand the custom tokenizer vocabulary and identify tokens created during the active tokenization operation. The app must show the vocabulary state and make newly created tokens clear.

**Why this priority**: This is the distinctive feature beyond raw tokenization and is central to the custom tokenizer workflow.

**Independent Test**: A user tokenizes text that contains both known and unseen tokens, then verifies that the vocabulary list updates immediately and new tokens are visually highlighted.

**Acceptance Scenarios**:

1. **Given** a custom vocabulary already contains some entries, **When** the user tokenizes text with known tokens, **Then** the app reuses the existing token IDs.
2. **Given** a custom vocabulary does not contain a token from the current input, **When** tokenization runs, **Then** the app creates a deterministic new ID and records the token frequency.
3. **Given** the app has newly created tokens in the current operation, **When** the results are rendered, **Then** the UI shows those tokens with a distinct visual state and flags them as newly created.
4. **Given** the user resets the vocabulary, **When** the reset action succeeds, **Then** the vocabulary returns to its initial state and no custom entries remain beyond the original baseline.

---

### User Story 4 - Understand and recover from invalid input and processing failures (Priority: P1)

A user may provide empty input, unsupported files, invalid PDF files, or cases where the app cannot extract text. The app must prevent confusion by providing clear validation and processing messages and by keeping the UI in a clear state.

**Why this priority**: Robust input validation and friendly error handling are required for trust and usability, especially for file handling and document processing.

**Independent Test**: A user submits invalid input, oversized files, PDFs without extractable text, and unsupported encodings and confirms that each case results in a clear, actionable error state.

**Acceptance Scenarios**:

1. **Given** the user submits empty text or an empty uploaded file, **When** tokenization is attempted, **Then** the app shows a validation error and does not continue processing.
2. **Given** a user uploads a file type that is not supported, **When** the upload is processed, **Then** the app displays a user-friendly error and keeps the UI in an error state.
3. **Given** a PDF file is corrupted or contains no extractable text, **When** the app attempts extraction, **Then** the app reports the issue clearly and surfaces the error state without crashing.
4. **Given** a user selects an unsupported encoding, **When** tokenization begins, **Then** the app shows a validation error and prevents execution.

---

### User Story 5 - Use a responsive, accessible tokenizer interface (Priority: P2)

A user needs a clean, responsive interface that works across supported screen sizes and remains accessible to keyboard and assistive technology users.

**Why this priority**: A usable interface is necessary for product adoption, especially when users are comparing tokenizer behavior and diagnostics.

**Independent Test**: A user can navigate the full tokenizer workflow using the interface on a typical desktop and smaller viewport without losing primary functionality.

**Acceptance Scenarios**:

1. **Given** the application is loaded on a desktop or tablet layout, **When** the user interacts with controls, **Then** the layout remains readable and components remain usable.
2. **Given** the interface is used in text-only or keyboard-only navigation, **When** the user reaches controls such as input mode, encoding, and action buttons, **Then** the controls are accessible and clear.

---

### Edge Cases

- What happens when the uploaded file is larger than the permitted size limit?
- How does the system handle a PDF that is structurally valid but contains no extractable text?
- What happens when the user switches from one input source to another without clearing previous output?
- How are token counts computed when input contains whitespace, punctuation, or mixed encodings?
- What happens when a user selects a custom tokenizer mode after a Tiktoken run?
- How is the vocabulary reset handled when there are active results or ongoing processing?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The application MUST provide an input experience that allows users to enter text directly and to upload `.txt` or text-based `.pdf` files. Acceptance: A user can paste text or choose a file and proceed without needing an account or additional setup.
- **FR-002**: The application MUST allow users to choose among input modes for direct text entry and file upload. Acceptance: The interface exposes a clear input mode selector and supports the allowed actions for each mode.
- **FR-003**: The application MUST allow users to choose between Tiktoken and Custom Tokenizer modes. Acceptance: Switching modes changes the processing path and the displayed results without affecting the other mode’s state.
- **FR-004**: The application MUST allow users to select a supported Tiktoken encoding from the available options. Acceptance: The selected encoding is applied to tokenization and is included in the response metadata.
- **FR-005**: The application MUST tokenize the current input using the selected tokenizer mode. Acceptance: The results include tokens and token metadata according to the chosen mode.
- **FR-006**: The application MUST display token index, token ID, token text, and relevant token details for each tokenized item. Acceptance: Each rendered token row includes identifiable values needed for analysis and comparison.
- **FR-007**: The application MUST display summary statistics including character count, word count, token count, tokens per word, and tokens per character. Acceptance: The statistics panel updates immediately after a successful tokenization run.
- **FR-008**: For Tiktoken mode, the application MUST use the actual selected encoding and return real token IDs and token metadata. Acceptance: The output reflects the chosen encoding rather than a mock or placeholder value.
- **FR-009**: For Custom Tokenizer mode, the application MUST use a deterministic token-splitting strategy. Acceptance: The same input and vocabulary state produce the same token sequence across repeated runs in the same environment.
- **FR-010**: The application MUST maintain an application-owned Custom Tokenizer vocabulary. Acceptance: The vocabulary is managed by the app itself and is not loaded from external storage.
- **FR-011**: The application MUST reuse existing custom vocabulary token IDs for repeated tokens. Acceptance: When a token already exists in the app-owned vocabulary, the same ID is reused instead of creating a duplicate.
- **FR-012**: The application MUST create new vocabulary entries for tokens that are not already present. Acceptance: Previously unseen tokens are added to the custom vocabulary and assigned deterministic IDs.
- **FR-013**: The application MUST assign deterministic IDs to newly created custom tokens. Acceptance: Re-running the same tokenization with the same initial vocabulary and input yields the same custom IDs.
- **FR-014**: The application MUST track token frequency for each vocabulary entry. Acceptance: The vocabulary display includes frequency values that update after tokenization runs.
- **FR-015**: The application MUST identify tokens created during the current tokenization operation. Acceptance: The UI clearly marks newly created custom tokens in the current run and distinguishes them from pre-existing entries.
- **FR-016**: The application MUST display the current custom vocabulary with ID, token, frequency, and status. Acceptance: The vocabulary panel shows all required fields and updates immediately after successful custom tokenization.
- **FR-017**: The application MUST visually distinguish newly created tokens from existing tokens in the vocabulary display. Acceptance: The new-vs-existing state is visible and not ambiguous from the user perspective.
- **FR-018**: The application MUST allow users to reset the custom vocabulary to its initial state. Acceptance: After reset, the vocabulary returns to its original baseline without persisting changes in a database.
- **FR-019**: The application MUST validate empty input, unsupported file types, oversized files, invalid or corrupted PDFs, PDFs with no extractable text, and unsupported encodings. Acceptance: Each invalid case triggers a user-friendly validation message and prevents the run from continuing.
- **FR-020**: The application MUST display clear, user-friendly validation and processing errors throughout the interface. Acceptance: Error states include a visible message that explains what went wrong and what the user can do next.
- **FR-021**: The application MUST provide loading, empty, error, and success states for the user experience. Acceptance: The UI avoids ambiguity by clearly indicating when processing is active, when no content exists, when an error occurred, and when results are ready.
- **FR-022**: The application MUST be responsive and accessible. Acceptance: Core controls and output remain usable and readable across supported viewport sizes and keyboard-navigation scenarios.
- **FR-023**: The application MUST ensure that the Tiktoken vocabulary and custom vocabulary are never modified by the wrong mode. Acceptance: Tiktoken data remains untouched by custom tokenization logic and vice versa.
- **FR-024**: The application MUST keep Tiktoken and Custom Tokenizer behaviors independent. Acceptance: The result set, vocabulary state, and error handling for each mode do not contaminate the other mode.
- **FR-025**: The application MUST not persist vocabulary or user data in a database. Acceptance: All processing state remains in the application runtime and is not stored in a database.
- **FR-026**: The application MUST include the required UI sections for title, description, input mode selection, text input/upload controls, encoding selector, tokenize action, statistics, token visualization, extracted text area, and error messages. Acceptance: The interface layout contains each of the required sections and they are visible in the default experience.
- **FR-027**: The application MUST return API response data suitable for frontend rendering, including original text, token count, token IDs, decoded tokens, character count, word count, tokens per word, tokens per character, selected encoding, and source type. Acceptance: The frontend can render all required data from a single response object without additional hidden state.
- **FR-028**: The application MUST not introduce authentication, user accounts, OCR, databases, cloud storage, LLM inference, billing, tokenizer training, or similar out-of-scope functionality. Acceptance: The feature remains limited to the described tokenizer and analysis workflow only.

### Key Entities *(include if feature involves data)*

- **TextSource**: The raw user input or uploaded file content used as input for tokenization, including the source type (direct text, `.txt`, or PDF).
- **TokenRecord**: A single tokenized unit containing token index, token ID, token text, decoded form, and relevant metadata needed for the UI.
- **TokenizationResult**: The complete output for a single run, including the original text, token list, summary statistics, selected encoding, and source metadata.
- **CustomVocabularyEntry**: A vocabulary record containing token text, deterministic ID, frequency, and status such as existing or newly created in the active run.
- **DocumentExtract**: The extracted textual content from a valid uploaded PDF, if any readable text is available.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can complete a basic tokenization flow from text entry or supported file upload in under 2 seconds for typical inputs under the configured size thresholds.
- **SC-002**: At least 95% of valid direct-text and supported-file scenarios produce a successful tokenization result with all required display fields rendered in the UI.
- **SC-003**: The app reliably identifies and reports invalid input conditions without crashing or silently accepting unsupported content.
- **SC-004**: A user can compare Tiktoken and Custom Tokenizer behaviors in the same interface and confirm that the modes remain independent.
- **SC-005**: The custom vocabulary updates immediately after successful custom tokenization, and newly created tokens are clearly distinguishable from existing entries.
- **SC-006**: The application remains usable, readable, and accessible across supported desktop and tablet viewport sizes without blocking essential functionality.
- **SC-007**: No user or vocabulary data is persisted to a database, and no out-of-scope functionality is introduced into the product.

## Assumptions

- The application runs as a small client-side tokenizer utility focused on understanding token conversion behavior rather than production-scale text processing.
- Supported PDF handling is limited to normal text-based PDFs that can be extracted without OCR.
- Uploaded files are constrained by a reasonable size threshold defined by the application and reported clearly when exceeded.
- Tiktoken uses the actual encoding chosen by the user and never stores or mutates custom vocabulary state.
- The custom vocabulary is application-owned and resettable, but not persisted beyond the in-memory session.
- The app does not include authentication, multi-user accounts, cloud storage, or remote model inference.
