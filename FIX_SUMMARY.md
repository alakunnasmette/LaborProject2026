# Phase 2.0 Session Persistence Fix

## Issue
Phase 2.0 (Career Anchors) was not saving answers to the session file despite the auto-save code being implemented.

## Root Cause
In [phases/phase20.py](phases/phase20.py#L211-L219), the `auto_save_loopbaan()` function was attempting to serialize `StringVar` objects directly instead of extracting their values using `.get()`:

```python
# BROKEN - tries to save StringVar object, not its value
answers_to_save = {str(k): v for k, v in vraag_vars.items()}
```

This would create a dictionary with StringVar references instead of the actual string values, causing serialization to JSON to fail silently.

## Solution
Changed line 213 to call `.get()` on each StringVar to extract the actual string value:

```python
# FIXED - extracts the string value from each StringVar
answers_to_save = {str(k): v.get() for k, v in vraag_vars.items()}
```

## Verification
✅ All phases now save and load correctly:
- **Phase 2.0** (Career Anchors): 30 questions, radio button selections
- **Phase 2.1** (Career Clusters): Checkbox states (tuple keys with 3-value arrays)
- **Phase 2.2** (Culture): Likert scale ratings (1-5)
- **Phase 2.3** (Job Characteristics): Free-text responses

## Files Modified
- `phases/phase20.py` - Fixed auto_save_loopbaan() function (line 213)

## Testing
Run this command to verify all phases work:
```bash
python test_all_phases_comprehensive.py
```

Expected output: All phases return ✓ PASS
