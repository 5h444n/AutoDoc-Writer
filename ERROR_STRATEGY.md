# API Error Handling & Rate Limit Strategy

**Status:** Drafted
**Related Issue:** #22
**Model:** Google Gemini 1.5 Flash (Free Tier)

## 1. Gemini Free Tier Limits (The Constraints)
We are currently operating under the "Pay-as-you-go" (Free Tier) constraints.
* **RPM (Requests Per Minute):** 15 RPM
* **TPM (Tokens Per Minute):** 1,000,000 TPM
* **RPD (Requests Per Day):** 1,500 RPD

**Impact:**
If a user tries to generate documentation for 20 files at once, the API will fail after the 15th file. We *must* queue these requests or handle the 429 error gracefully.

---

## 2. Retry Strategy: Exponential Backoff
When the Frontend receives a **429 (Too Many Requests)** or **503 (Service Unavailable)**, it should **NOT** alert the user immediately. It should attempt to retry silently using "Exponential Backoff".

**Algorithm:**
1.  **Request Fails** (Status 429).
2.  **Wait 1 second** -> Retry.
3.  **Request Fails again**.
4.  **Wait 2 seconds** -> Retry.
5.  **Request Fails again**.
6.  **Wait 4 seconds** -> Retry.
7.  **Request Fails again** -> **STOP**. Show UI Error Message to user.

**Total Wait Time:** ~7 seconds before bothering the user.

---

## 3. Error Code Matrix & UI Copy
When the retry strategy fails (or for non-retriable errors), display these "Toast" messages to the user.

| HTTP Code | Error Type | Internal Cause | User-Facing Message (UI Copy) | Action |
| :--- | :--- | :--- | :--- | :--- |
| **400** | Bad Request | Missing fields / Invalid JSON | "We couldn't understand that request. Please check your inputs." | Manual Retry |
| **401** | Unauthorized | Invalid/Expired Token | "Your session has expired. Please log in again." | Redirect to Login |
| **403** | Forbidden | User doesn't own the repo | "You don't have permission to view this repository." | Back to Dashboard |
| **404** | Not Found | Repo/File missing | "We couldn't find the documentation you're looking for." | Back to Dashboard |
| **422** | Validation | Pydantic Schema Error | "Data format error. Please contact support." | Manual Retry |
| **429** | **Rate Limit** | **Hit Gemini 15 RPM limit** | **" The AI is cooling down. Please wait 30 seconds and try again."** | **Auto-Retry or Timer** |
| **500** | Server Error | Backend Crash | "Our servers hit a snag. We've been notified." | Manual Retry |
| **503** | Service Unavail | Gemini API Down | "The AI service is currently unavailable. Try again later." | Manual Retry |

---

## 4. Implementation Guidelines
* **Frontend:** Use an interceptor (Axios/Fetch) to catch 429 errors globally.
* **Backend:** Ensure the `500` error handler does not expose raw Python stack traces to the frontend.