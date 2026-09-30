# Implementation Plan: Tokenizer Application

**Branch**: `001-tokenizer-app` | **Date**: 2026-09-29 | **Spec**: `specs/001-tokenizer-app/spec.md`

**Input**: Feature specification from `/specs/001-tokenizer-app/spec.md`

## Summary

This feature delivers a small, focused tokenizer application that lets a user paste text or upload `.txt` or text-based PDF files, choose between Tiktoken and a custom regex-based tokenizer, inspect tokenized output, and review custom vocabulary state without persistent storage. The implementation will use a React + TypeScript frontend for the user experience and a FastAPI + Python backend for REST APIs, file processing, validation, and tokenization services. The backend will keep Tiktoken and Custom Tokenizer logic fully independent, will never modify Tiktoken vocabulary, and will keep all business logic in services rather than in API routes.

## Technical Context

**Language/Version**: Python 3.11, TypeScript 5.x, React 18+

**Primary Dependencies**: FastAPI, Pydantic, pytest, tiktoken, PyMuPDF, React, Vite, TypeScript, Axios

**Storage**: In-memory only; no database or persistent storage used for vocabulary or user data

**Testing**: pytest for backend tests; frontend testing only for critical UI states if required by project standards; no database integration test layer required

**Target Platform**: Browser-based web application served locally or in a lightweight deployment target

**Project Type**: Web application with frontend + backend services

**Performance Goals**: Process typical document inputs under expected browser-safe size limits without blocking the UI; maintain responsive tokenization for text inputs and text-based PDFs up to the defined upload cap

**Constraints**: Must remain client-side for local session state; must not persist data; must keep Tiktoken and custom tokenizer implementations independent; must support accessible UI, clear validation, and deterministic custom vocabulary behavior

## Constitution Check

The implementation plan is governed by the TOkenizer constitution and must satisfy the following constraints:

- Clean, modular architecture: backend services, schemas, and UI state are kept separated by responsibility.
- Separation of responsibilities: API layer handles HTTP concerns only; business logic remains in backend services; React state remains view logic and not tokenization logic.
- Readable, production-quality code: use explicit service boundaries, typed contracts, and clear naming.
- Secure handling of secrets and configuration: no secrets or credentials are required; environment variables only for non-sensitive app config if needed.
- Meaningful testing: backend tests cover validation, tokenizer mode isolation, PDF extraction edge cases, and custom vocabulary behavior.
- Proper error handling and validation: validation must be explicit for empty input, unsupported files, oversized uploads, invalid PDFs, and unsupported encodings.
- Minimal dependencies: no extra frameworks beyond the project-approved stack.
- Performance, reliability, security: no unnecessary network or persistence; all processing stays in-memory and deterministic.
- Reproducible environments: pinned or documented dependencies and simple startup steps.

## Project Structure

### Repository Structure

```text
backend/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── tokenize.py
│   │       └── health.py
│   ├── core/
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   └── logging.py
│   ├── models/
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── tokenizer.py
│   │   ├── files.py
│   │   └── responses.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── tiktoken_service.py
│   │   ├── custom_tokenizer_service.py
│   │   ├── file_service.py
│   │   ├── stats_service.py
│   │   └── pdf_service.py
│   ├── utils/
│   │   ├── validation.py
│   │   └── text_processing.py
│   └── main.py
├── tests/
│   ├── test_tokenize_api.py
│   ├── test_tiktoken_service.py
│   ├── test_custom_tokenizer_service.py
│   ├── test_file_validation.py
│   └── test_pdf_service.py
└── requirements.txt

frontend/
├── src/
│   ├── app/
│   │   ├── App.tsx
│   │   └── routes.tsx
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   └── Layout.tsx
│   │   ├── tokenizer/
│   │   │   ├── InputPanel.tsx
│   │   │   ├── ModeSelector.tsx
│   │   │   ├── EncodingSelector.tsx
│   │   │   ├── TokenizeButton.tsx
│   │   │   ├── StatisticsPanel.tsx
│   │   │   ├── TokenTable.tsx
│   │   │   ├── VocabularyPanel.tsx
│   │   │   ├── ExtractedTextPanel.tsx
│   │   │   └── ErrorBanner.tsx
│   │   └── shared/
│   │       ├── LoadingState.tsx
│   │       ├── EmptyState.tsx
│   │       └── StatusBadge.tsx
│   ├── hooks/
│   │   ├── useTokenizer.ts
│   │   └── useCustomVocabulary.ts
│   ├── services/
│   │   ├── api.ts
│   │   └── tokenizerClient.ts
│   ├── styles/
│   │   ├── theme.ts
│   │   ├── globals.css
│   │   └── neon.css
│   ├── types/
│   │   ├── tokenizer.ts
│   │   └── api.ts
│   └── main.tsx
├── public/
│   └── assets/
├── package.json
├── tsconfig.json
├── vite.config.ts
└── index.html
```

**Structure Decision**: Separate backend and frontend repositories or top-level folders are recommended because the backend and frontend are intentionally independent but share a single feature scope. This preserves REST boundaries, keeps services dedicated, and avoids coupling tokenization logic into the UI.

## System Architecture and Component Boundaries

### Architecture Overview

The application is a layered, client-server architecture:

1. Frontend UI layer
   - Handles user interactions, input controls, and display of statistics and token data.
   - Calls REST APIs only; no tokenization logic in React components.
   - Owns visual states: loading, empty, success, and error.

2. API gateway layer
   - Exposes thin REST routes for tokenization requests and file upload validation.
   - Delegates work to backend services and returns typed response payloads.

3. Backend service layer
   - `tiktoken_service.py`: handles all Tiktoken mode logic and uses the actual selected encoding without mutating the library vocabulary.
   - `custom_tokenizer_service.py`: handles regex-based custom tokenization, vocabulary lifecycle, token frequency, and new-token identification.
   - `file_service.py`: validates file type, size, and upload content.
   - `pdf_service.py`: extracts textual content from valid text-based PDFs with PyMuPDF.
   - `stats_service.py`: computes token statistics and derived metrics.

4. In-memory state layer
   - The custom vocabulary is stored in process memory only and resettable by the user.
   - No database or persistent storage is used.

### Frontend and Backend Boundaries

- Frontend does not implement token logic, custom vocab updates, or file parsing.
- Backend owns all tokenizer logic and data transformation.
- The frontend may maintain UI state and local view model state, but not business logic or domain rules.

## API Contracts and Pydantic Schemas

### REST Endpoints

- `POST /api/v1/tokenize`
  - Accepts text or file metadata and tokenizer mode selection.
  - Returns token results, summary stats, selected encoding, source type, and a vocabulary snapshot when relevant.

- `POST /api/v1/process-file`
  - Accepts uploaded file content and validates file type, size, and PDF readability.
  - Returns extracted text and validation result for use before tokenization.

- `POST /api/v1/custom-vocabulary/reset`
  - Resets the in-memory custom vocabulary to its initial baseline state.

- `GET /api/v1/health`
  - Returns backend health and readiness status.

### Pydantic Schemas

- `TokenizerRequest`
  - `input_text: str | None`
  - `source_type: Literal["text", "txt", "pdf"]`
  - `tokenizer_mode: Literal["tiktoken", "custom"]`
  - `encoding: str | None`
  - `file_name: str | None`
  - `file_content: bytes | None`

- `TokenizerResponse`
  - `original_text: str`
  - `token_count: int`
  - `token_ids: list[int]`
  - `decoded_tokens: list[str]`
  - `character_count: int`
  - `word_count: int`
  - `tokens_per_word: float`
  - `tokens_per_character: float`
  - `selected_encoding: str | None`
  - `source_type: str`
  - `tokens: list[TokenDetail]`
  - `statistics: TokenStatistics`
  - `custom_vocabulary: list[CustomVocabularyEntry] | None`
  - `newly_created_tokens: list[str]`

- `TokenDetail`
  - `index: int`
  - `token_id: int`
  - `token_text: str`
  - `details: dict[str, Any]`

- `TokenStatistics`
  - `character_count: int`
  - `word_count: int`
  - `token_count: int`
  - `tokens_per_word: float`
  - `tokens_per_character: float`

- `CustomVocabularyEntry`
  - `id: int`
  - `token: str`
  - `frequency: int`
  - `status: Literal["existing", "new"]`

- `ValidationErrorResponse`
  - `error_code: str`
  - `message: str`
  - `field: str | None`
  - `details: dict[str, Any] | None`

## Tiktoken Service Design

The Tiktoken service is responsible for all logic tied to actual Tiktoken behavior and must remain isolated from custom vocabulary operations.

Key responsibilities:

- Validate selected encoding against supported Tiktoken encodings.
- Encode source text with `tiktoken.get_encoding()` for the actual chosen encoding.
- Return real token IDs and decoded token values from the selected encoding.
- Return raw token metadata needed by the UI, without mutating any vocabulary state.
- Ensure custom vocabulary or reset functions never touch Tiktoken state.

Design constraints:

- Use the actual selected encoding string from the request.
- Do not wrap the library in a way that changes semantics or content.
- Provide a clear error path for unsupported encodings and encoding failures.
- Keep Tiktoken mode isolated from custom mode even when both are visible in the same UI.

## Custom Tokenizer Service and Deterministic Tokenization Algorithm

The custom tokenizer service will use a deterministic algorithm based on regular expressions, as required by the specification. The implementation should define a clear tokenization rule for whitespace-delimited behavior that is repeatable and predictable across runs.

Recommended algorithm:

- Tokenization starts from the normalized original text.
- Use regex-based splitting to separate tokens according to whitespace-delimited boundaries while respecting punctuation handling in the selected rule set.
- Lower-level token extraction is deterministic and reproducible.
- For each token, check if it exists in the custom in-memory vocabulary.
- Reuse the existing token ID when already present; otherwise create a new deterministic ID.
- Update token frequency counts for all processed tokens.
- Mark tokens created during the active operation as `new` and distinguish them visually in the UI.

Determinism requirements:

- Same input and same initial vocabulary state must yield the same custom IDs and frequencies.
- The custom tokenization algorithm must not depend on runtime state beyond the in-memory vocabulary and the input text.
- The algorithm must not mutate the Tiktoken vocabulary or rely on external persistent state.

## Custom Vocabulary State and Lifecycle

The custom vocabulary will be stored in memory only and resettable by the user.

Lifecycle flow:

1. Initialize a baseline vocabulary at application startup or feature reset.
2. When custom tokenization runs, inspect each token against the current vocabulary.
3. Reuse existing IDs and increment frequencies.
4. Create new IDs for unseen tokens and mark them as “new” for the active run.
5. Return a vocabulary snapshot and newly created token list in the API response.
6. Allow a reset endpoint to restore the baseline state without a database.

State rules:

- Vocabulary is app-owned and not persisted.
- Only the custom tokenizer may change the custom vocabulary.
- Tiktoken vocabulary is read-only and never mutated.
- If the app is refreshed or reset, the vocabulary returns to the initial baseline unless explicitly reinitialized from a startup baseline.

## TXT and PDF Processing

### TXT Processing

- Accept uploaded `.txt` files or direct text input.
- Validate file extension and MIME type as needed.
- Normalize line endings to a consistent format before tokenization.
- Keep extracted content in an explicit `source_type` value such as `text` or `txt` for UI and API reporting.

### PDF Processing

- Accept `.pdf` files only.
- Validate file readability and corruption before extraction.
- Use PyMuPDF to extract text from normal text-based PDFs only.
- Reject or flag PDFs that are corrupted, invalid, or contain no extractable text.
- Return extracted text and source metadata to the client for display and tokenization.

Requirements for PDF handling:

- No OCR support.
- No cloud-based extraction.
- Only text-based PDFs are in scope.
- PDF extraction errors must be user-friendly and non-technical when possible.

## File Validation and Error Handling

Validation must be centralized in the backend and triggered before tokenization occurs.

### Validation Cases

- Empty input: reject with a clear message and no processing.
- Unsupported file types: reject with a clear error and support guidance.
- Oversized files: reject when the file exceeds the defined cap.
- Invalid or corrupted PDFs: reject with message indicating extraction failure.
- PDFs with no extractable text: reject and provide a friendly explanation.
- Unsupported encodings: reject before invocation of Tiktoken encoding.

### Error Response Standards

- Use consistent response envelopes for validation failures.
- Include a stable error code and a human-readable message.
- Return the source context, field name, and any available detail where useful.
- Frontend should render a visible error state and keep the rest of the UI stable.

## Token Statistics Calculation

A dedicated stats service will compute all derived values required by the UI and API response.

Metrics to calculate:

- Character count
- Word count
- Token count
- Tokens per word
- Tokens per character
- Token index and per-token metadata

Rules:

- Character count is measured on the original text string after normalization.
- Word count is computed using the project’s agreed splitting logic, ensuring consistency with UI expectations.
- Token count reflects the actual output of the selected tokenizer mode.
- `tokens_per_word` and `tokens_per_character` are computed with consistent numeric formatting for the UI.
- The service must not mix Tiktoken and custom-token metrics in the same result object.

## React State and Component Structure with Neon-Gradient Aesthetic

### UI Design Goals

- Dark-mode cyberpunk aesthetic with neon gradients and high contrast.
- Professional visual polish without sacrificing clarity and accessibility.
- Clear separation between input controls, output panels, and status/error states.

### Recommended Theme Palette

- Background: deep charcoal-black / midnight
- Primary accent: electric cyan
- Secondary accent: purple/violet or neon magenta
- Success accent: green glow
- Warning accent: amber
- Error accent: red/pink

### State Model

Use React state management with a small set of top-level data structures:

- `inputMode`: `text` | `upload`
- `tokenizerMode`: `tiktoken` | `custom`
- `selectedEncoding`: `str | null`
- `sourceType`: `text` | `txt` | `pdf` | `none`
- `textInput`: current textual content
- `uploadFile`: selected file state
- `result`: tokenization output payload
- `error`: validation/processing error object
- `isLoading`: boolean
- `customVocabulary`: vocabulary snapshot
- `newlyCreatedTokens`: list of tokens created in the current run

### Component Responsibilities

- `App.tsx`: top-level composition and layout
- `InputPanel.tsx`: input mode selection, text area, file upload, and reset controls
- `ModeSelector.tsx`: Tiktoken/custom switching and state wiring
- `EncodingSelector.tsx`: supports the official Tiktoken encoding list
- `StatisticsPanel.tsx`: all summary values and statuses
- `TokenTable.tsx`: token index, ID, text, and metadata display
- `VocabularyPanel.tsx`: custom vocabulary table including status and frequency
- `ExtractedTextPanel.tsx`: text extracted from uploaded PDF or `.txt` files
- `ErrorBanner.tsx`: error messages and user guidance
- `LoadingState.tsx`, `EmptyState.tsx`: UI states for no data and processing states

## Frontend/Backend Communication

- The frontend will call a thin API layer using REST requests.
- Backend returns typed payloads with all required rendering fields.
- API response should contain enough data to render the UI without additional hidden client-side state lookups.
- The UI will handle loading, empty, success, and error states explicitly.
- No tokenization logic will be moved into React components.

### REST Communication Pattern

- Frontend triggers a request to `/api/v1/tokenize` after validation and user action.
- Backend validates input and returns structured responses.
- Frontend renders results into the statistics panel, token table, vocabulary view, and extracted document view.

## Token and Vocabulary Visualization

The UI must present both raw token information and custom vocabulary data clearly.

### Token Visualization

- Table or scrollable list with columns for index, token ID, token text, and metadata.
- Each row is inspectable in a readable format.
- Rows should reflect the actual selected mode and the chosen encoding for Tiktoken.

### Custom Vocabulary Visualization

- Table with columns for ID, token, frequency, and status.
- Newly created tokens are visually distinct by highlighting or badge state.
- After successful custom tokenization, the vocabulary snapshot updates immediately.
- Reset action restores the baseline vocabulary state and clears newly created run markers.

## Testing Strategy

### Backend Testing

Use pytest to validate each service and endpoint boundary:

- Tiktoken mode returns real values for supported encodings and rejects unsupported ones.
- Custom tokenizer uses deterministic regex tokenization and consistent ID creation.
- Custom vocabulary reuse logic assigns repeated tokens to the same ID.
- New tokens are identified correctly and frequencies update as expected.
- File validation rejects empty inputs, unsupported types, oversized files, and invalid PDFs.
- PDF extraction returns readable text only for valid text-based PDFs and failing cases surface clear errors.
- API response contract matches the frontend rendering requirements.

### Frontend Testing

- Validate state transitions for loading, empty, success, and error states.
- Confirm UI reflects backend response fields correctly.
- Confirm custom vocabulary display updates immediately after tokenization.
- Confirm reset action restores baseline state and removes run-specific highlights.

## Security and Configuration

- No secrets, API keys, or database credentials are required by the application design.
- Environment configuration should remain limited to developer-local settings if needed for service ports or URLs.
- No cloud storage or remote persistence is allowed.
- Custom vocabulary state stays in memory only and is resettable.
- File uploads are validated before processing and the app does not parse or store user content beyond the active session.

## Implementation Sequence and Dependencies

### Phase 0: Project Foundation

- Confirm repo layout and toolchain.
- Initialize backend and frontend packages.
- Define shared API schema and response contracts.
- Configure environment and testing setup.

### Phase 1: Backend Contracts and File Validation

- Implement FastAPI app scaffold and open API routes.
- Add Pydantic request/response schemas.
- Build file validation and upload handling.
- Add error handling pipeline and validation middleware.

### Phase 2: PDF and Text Processing

- Implement `.txt` handling and text extraction normalization.
- Implement PDF extraction using PyMuPDF.
- Ensure extraction failures are converted to user-friendly errors.

### Phase 3: Tiktoken Service

- Add Tiktoken service with encoding validation.
- Return real IDs and token metadata for the selected encoding.
- Keep mode behavior independent from custom mode.

### Phase 4: Custom Tokenizer and Vocabulary State

- Implement regex-based custom tokenization.
- Build deterministic ID assignment and vocabulary frequency tracking.
- Identify newly created tokens and final vocabulary snapshot.
- Add reset endpoint and in-memory baseline restoration.

### Phase 5: Statistics and Response Building

- Implement calculation logic for all required metrics.
- Build response payloads for frontend rendering.
- Ensure source_type and selected_encoding are returned consistently.

### Phase 6: Frontend UI and Visualization

- Implement layout and neon cyberpunk styling.
- Add input panels, token table, statistics, vocabulary panel, and extracted-text panel.
- Wire to backend endpoints and handle loading, success, and error states.

### Phase 7: Quality Validation and Regression Coverage

- Run backend tests for validation, service logic, and API contracts.
- Validate UI states and accessibility basics.
- Confirm Tiktoken and custom mode independence and no persistent storage.

## Final Delivery Expectations

The implementation will satisfy the approved specification by delivering a small, clean tokenizer application that compares Tiktoken and custom tokenization in a professional UI while keeping the technical architecture disciplined, deterministic, and easy to test. The app will remain in scope, will avoid unrelated features, and will provide a strong foundation for downstream task generation.
