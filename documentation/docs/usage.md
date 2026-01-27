# User Guide: Workflow & Features

Once the application is running, follow this step-by-step workflow to generate and manage your documentation.

## 1. Login & Connection
* **Authentication:** Click **"Login with GitHub"** to securely authorize the app using OAuth. Your password is never stored by the application.
* **Dashboard:** After logging in, you will see a list of all your repositories.
* **Status Indicators:** Check the visual indicators to see which repos are "Active" or "Inactive".
* **Select Projects:** Toggle the switch to **"Active"** for any repository you want the AI to monitor.

## 2. Generating Documentation
There are two distinct ways to trigger documentation generation:

* **Automatic (Real-Time):** Simply push code to GitHub (`git push`). The app detects the new commit immediately and starts generating the text.
* **Manual History:** Navigate to the **"Commit Activity"** tab. Here you can see a log of recent pushes. Select any past commit and click **"Generate Docs"** to create documentation for that specific version.

## 3. Viewing Results
Navigate to the **Documentation Viewer** to see the AI-generated output in three specific formats:

1.  **Plain Text:** A simple, plain English explanation of the code changes.
2.  **Research Style:** Formal, academic paragraphs describing the logic (ideal for thesis reports).
3.  **LaTeX:** A ready-to-use LaTeX code block that you can copy directly into Overleaf.

## 4. Exporting & Offline Access
You can extract your documentation for external use:

* **One-Click Copy:** Use the copy button to instantly paste text into your report.
* **Export File:** Save your documentation locally as **Markdown (`.md`)**, **PDF**, or **LaTeX (`.tex`)** files.
* **Offline Access:** All generated documentation is cached locally, so you can view your past write-ups even without an internet connection.