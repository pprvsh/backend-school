
### The Reason for the Error

In `school_core/settings.py`, your backend has:

<pre><div node="[object Object]" class="relative whitespace-pre-wrap word-break-all my-2 rounded-xl bg-muted border"><div class="min-h-7 relative box-border flex flex-row items-center justify-between rounded-t border-b border-border px-2 py-0.5"><div class="font-sans text-sm text-muted-foreground">python</div><div class="flex flex-row gap-2 justify-end"></div></div><div class="p-3"><div class="code-block w-full text-xs cursor-text  "><div class="flex flex-col w-full"><div data-index="0" data-line-number="1" data-line-start="1" data-line-end="1" class="code-line "><div class="line-content"><span class="mtk1">REST_FRAMEWORK </span><span class="mtk3">=</span><span class="mtk1"> {</span></div></div><div data-index="1" data-line-number="2" data-line-start="2" data-line-end="2" class="code-line "><div class="line-content"><span class="mtk1"></span><span class="mtk12">"DEFAULT_PERMISSION_CLASSES"</span><span class="mtk1">: [</span></div></div><div data-index="2" data-line-number="3" data-line-start="3" data-line-end="3" class="code-line "><div class="line-content"><span class="mtk1"></span><span class="mtk12">"rest_framework.permissions.IsAuthenticated"</span><span class="mtk1">,</span></div></div><div data-index="3" data-line-number="4" data-line-start="4" data-line-end="4" class="code-line "><div class="line-content"><span class="mtk1">    ],</span></div></div><div data-index="4" data-line-number="5" data-line-start="5" data-line-end="5" class="code-line "><div class="line-content"><span class="mtk1">}</span></div></div><div data-index="5" data-line-number="6" data-line-start="6" data-line-end="6" class="code-line "><div class="line-content"><span class="mtk1"></span></div></div></div></div></div></div></pre>

This forces **all** endpoints to require a logged-in user with a JWT token unless a ViewSet explicitly defines its own `permission_classes`.

While you added the `import` statements at the top of the files, `permission_classes = ...` was  **not assigned inside the ViewSet class body** . Without that attribute, Django fell back to `IsAuthenticated` and rejected the public form submission with:

<pre><div node="[object Object]" class="relative whitespace-pre-wrap word-break-all my-2 rounded-xl bg-muted border"><div class="min-h-7 relative box-border flex flex-row items-center justify-between rounded-t border-b border-border px-2 py-0.5"><div class="font-sans text-sm text-muted-foreground">text</div><div class="flex flex-row gap-2 justify-end"></div></div><div class="p-3"><div class="code-block w-full text-xs cursor-text  "><div class="flex flex-col w-full"><div data-index="0" data-line-number="1" data-line-start="1" data-line-end="1" class="code-line "><div class="line-content"><span class="mtk1">detail: Authentication credentials were not provided.</span></div></div><div data-index="1" data-line-number="2" data-line-start="2" data-line-end="2" class="code-line "><div class="line-content"><span class="mtk1"></span></div></div></div></div></div></div></pre>

---

### ✅ What I Fixed:

1. In  **`admissions/views.py`** , added `permission_classes = [AdmissionsPermission]` to `AdmissionInquiryViewSet`:

   <pre><div node="[object Object]" class="relative whitespace-pre-wrap word-break-all my-2 rounded-xl bg-muted border"><div class="min-h-7 relative box-border flex flex-row items-center justify-between rounded-t border-b border-border px-2 py-0.5"><div class="font-sans text-sm text-muted-foreground">python</div><div class="flex flex-row gap-2 justify-end"></div></div><div class="p-3"><div class="code-block w-full text-xs cursor-text  "><div class="flex flex-col w-full"><div data-index="0" data-line-number="1" data-line-start="1" data-line-end="1" class="code-line "><div class="line-content"><span class="mtk6">class</span><span class="mtk1"></span><span class="mtk17">AdmissionInquiryViewSet</span><span class="mtk1">(</span><span class="mtk17">viewsets</span><span class="mtk1">.</span><span class="mtk17">ModelViewSet</span><span class="mtk1">):</span></div></div><div data-index="1" data-line-number="2" data-line-start="2" data-line-end="2" class="code-line "><div class="line-content"><span class="mtk1">    serializer_class </span><span class="mtk3">=</span><span class="mtk1"> AdmissionInquirySerializer</span></div></div><div data-index="2" data-line-number="3" data-line-start="3" data-line-end="3" class="code-line "><div class="line-content"><span class="mtk1">    permission_classes </span><span class="mtk3">=</span><span class="mtk1"> [AdmissionsPermission]  </span><span class="mtk5"># <-- Added</span></div></div><div data-index="3" data-line-number="4" data-line-start="4" data-line-end="4" class="code-line "><div class="line-content"><span class="mtk1"></span></div></div></div></div></div></div></pre>

   *(Allows public users to `POST` inquiries, while restricting viewing/modifying to staff).*
2. In  **`faculty/views.py`** , added `permission_classes = [IsAdminUserOrReadOnly]` to `FacultyViewSet`:

   <pre><div node="[object Object]" class="relative whitespace-pre-wrap word-break-all my-2 rounded-xl bg-muted border"><div class="min-h-7 relative box-border flex flex-row items-center justify-between rounded-t border-b border-border px-2 py-0.5"><div class="font-sans text-sm text-muted-foreground">python</div><div class="flex flex-row gap-2 justify-end"></div></div><div class="p-3"><div class="code-block w-full text-xs cursor-text  "><div class="flex flex-col w-full"><div data-index="0" data-line-number="1" data-line-start="1" data-line-end="1" class="code-line "><div class="line-content"><span class="mtk6">class</span><span class="mtk1"></span><span class="mtk17">FacultyViewSet</span><span class="mtk1">(</span><span class="mtk17">viewsets</span><span class="mtk1">.</span><span class="mtk17">ModelViewSet</span><span class="mtk1">):</span></div></div><div data-index="1" data-line-number="2" data-line-start="2" data-line-end="2" class="code-line "><div class="line-content"><span class="mtk1">    serializer_class </span><span class="mtk3">=</span><span class="mtk1"> FacultySerializer</span></div></div><div data-index="2" data-line-number="3" data-line-start="3" data-line-end="3" class="code-line "><div class="line-content"><span class="mtk1">    permission_classes </span><span class="mtk3">=</span><span class="mtk1"> [IsAdminUserOrReadOnly]  </span><span class="mtk5"># <-- Added</span></div></div><div data-index="3" data-line-number="4" data-line-start="4" data-line-end="4" class="code-line "><div class="line-content"><span class="mtk1"></span></div></div></div></div></div></div></pre>

   *(Allows public users to `GET` the faculty list, while restricting edits to staff).*

---

### 🧪 Verified:

We sent a test request to the running server:

* `POST /api/admissions/` returned **HTTP 201 Created** ✅
* `GET /api/faculty/` returned **HTTP 200 OK** ✅

You can now refresh your frontend page (`http://localhost:3000/admissions`) and click **"Submit Inquiry"** — it will succeed immediately!




### Test via Web Browser

You can also log in directly through the Django Admin interface:

1. Open **`http://127.0.0.1:8000/admin/`**
2. Log in with your staff username and password.
3. Click in the admission inquiry
4. navigate to **`http://127.0.0.1:8000/admin/admissions/admissioninquiry/`** to view and manage all inquiries.
