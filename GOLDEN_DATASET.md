# Golden Dataset for AI Prompt Validation

This dataset contains standardized code snippets used to validate the output quality of the AutoDoc Writer AI. 
Every time we modify the system prompts (in `backend/app/core/prompts.py`), we must run these snippets through the AI to ensure the output meets the acceptance criteria.

---

## Snippet 1: Python (Data Processing)
**Focus:** List comprehensions and sorting logic.
**Test Goal:** Ensure the "Plain English" persona explains the lambda function simply.

```python
def process_data(data):
    clean_data = [d.strip() for d in data if d]
    return sorted(clean_data, key=lambda x: len(x))
```

## Snippet 2: JavaScript (React Component)
**Focus:** UI rendering and destructuring.
**Test Goal:** Ensure the "Research" persona describes this formally as a "functional stateless component" without using "I" or "We".

```javascript
const UserCard = ({ user }) => {
  return (
    <div className="card">
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </div>
  );
};
```

## Snippet 3: C++ (Algorithm)
**Focus:** Recursion and binary search logic.
**Test Goal:**Ensure the "LaTeX" persona generates valid syntax that compiles in Overleaf without markdown errors.

```c++
int binarySearch(int arr[], int l, int r, int x) {
    if (r >= l) {
        int mid = l + (r - l) / 2;
        if (arr[mid] == x) return mid;
        if (arr[mid] > x) return binarySearch(arr, l, mid - 1, x);
        return binarySearch(arr, mid + 1, r, x);
    }
    return -1;
}
```
