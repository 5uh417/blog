Title: Modern JavaScript Async Patterns: From Callbacks to Async/Await
Date: 2025-07-04 10:15
Tags: javascript, async, promises, programming
Author: Suhail
Summary: A comprehensive guide to handling asynchronous operations in JavaScript, covering the evolution from callback hell to modern async/await patterns.

Asynchronous programming in JavaScript has evolved dramatically. Let's explore the journey from callback hell to elegant async/await patterns.

## The Evolution of Async JavaScript

### 1. Callbacks (The Dark Ages)
```javascript
getUserData(userId, (user) => {
  getPostsForUser(user.id, (posts) => {
    getCommentsForPosts(posts, (comments) => {
      // Welcome to callback hell!
      renderData(user, posts, comments);
    });
  });
});
```

Problems with callbacks:
- Pyramid of doom
- Error handling nightmare
- Hard to reason about

### 2. Promises (The Enlightenment)
```javascript
getUserData(userId)
  .then(user => getPostsForUser(user.id))
  .then(posts => getCommentsForPosts(posts))
  .then(comments => renderData(comments))
  .catch(error => handleError(error));
```

### 3. Async/Await (The Modern Era)
```javascript
async function loadUserContent(userId) {
  try {
    const user = await getUserData(userId);
    const posts = await getPostsForUser(user.id);
    const comments = await getCommentsForPosts(posts);
    renderData(user, posts, comments);
  } catch (error) {
    handleError(error);
  }
}
```

## Advanced Async Patterns

### Parallel Execution
```javascript
async function loadData() {
  // Run requests in parallel
  const [users, posts, comments] = await Promise.all([
    fetchUsers(),
    fetchPosts(),
    fetchComments()
  ]);
  
  return { users, posts, comments };
}
```

### Race Conditions
```javascript
async function fetchWithTimeout(url, timeout = 5000) {
  const timeoutPromise = new Promise((_, reject) =>
    setTimeout(() => reject(new Error('Timeout')), timeout)
  );
  
  return Promise.race([
    fetch(url),
    timeoutPromise
  ]);
}
```

### Sequential Processing
```javascript
async function processItemsSequentially(items) {
  const results = [];
  
  for (const item of items) {
    const result = await processItem(item);
    results.push(result);
  }
  
  return results;
}
```

## Error Handling Best Practices

### Try-Catch with Async/Await
```javascript
async function robustAsyncFunction() {
  try {
    const data = await riskyOperation();
    return processData(data);
  } catch (error) {
    console.error('Operation failed:', error.message);
    return defaultValue;
  }
}
```

### Promise Error Handling
```javascript
function handleAsyncOperation() {
  return riskyOperation()
    .then(data => processData(data))
    .catch(error => {
      if (error.code === 'NETWORK_ERROR') {
        return retryOperation();
      }
      throw error; // Re-throw if can't handle
    });
}
```

## Real-World Examples

### API Data Fetching
```javascript
class ApiClient {
  async fetchUserProfile(userId) {
    try {
      const response = await fetch(`/api/users/${userId}`);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Failed to fetch user:', error);
      throw error;
    }
  }
}
```

### Async Iterators
```javascript
async function* fetchPagedData(endpoint) {
  let page = 1;
  let hasMore = true;
  
  while (hasMore) {
    const response = await fetch(`${endpoint}?page=${page}`);
    const data = await response.json();
    
    yield data.items;
    
    hasMore = data.hasNextPage;
    page++;
  }
}
```

## Performance Considerations

1. **Avoid await in loops** for parallel operations
2. **Use Promise.all()** for concurrent requests
3. **Implement proper caching** for repeated operations
4. **Handle timeouts** for network requests

The key to mastering async JavaScript is understanding when to use each pattern and how they compose together for complex applications.