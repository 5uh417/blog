Title: Node.js Performance Optimization: From Slow to Lightning Fast
Date: 2025-06-25 13:15
Tags: nodejs, performance, optimization, javascript, backend
Author: Suhail
Summary: Practical techniques for optimizing Node.js applications, covering everything from event loop management to database queries and memory optimization.

Node.js performance can make or break your application. Here are the techniques that took my API from 2-second response times to sub-100ms.

## Understanding the Event Loop

### The Foundation of Node.js Performance
```javascript
// Blocking operation - NEVER do this
const fs = require('fs');
const data = fs.readFileSync('large-file.txt'); // Blocks entire thread
console.log('This waits for file read');

// Non-blocking operation - The Node.js way
fs.readFile('large-file.txt', (err, data) => {
  if (err) throw err;
  console.log('File read complete');
});
console.log('This executes immediately');
```

### Event Loop Phases
```javascript
// Understanding the order of execution
console.log('1. Synchronous');

setImmediate(() => console.log('2. setImmediate'));

process.nextTick(() => console.log('3. nextTick'));

setTimeout(() => console.log('4. setTimeout'), 0);

Promise.resolve().then(() => console.log('5. Promise'));

console.log('6. Synchronous');

// Output: 1, 6, 3, 5, 4, 2
```

## Profiling and Monitoring

### Built-in Node.js Profiler
```bash
# Start your app with profiling
node --prof app.js

# Generate human-readable output
node --prof-process isolate-*.log > processed.txt
```

### Using clinic.js for Comprehensive Analysis
```bash
npm install -g clinic

# CPU profiling
clinic doctor -- node app.js

# Event loop monitoring
clinic bubbleprof -- node app.js

# Memory heap profiling
clinic heapprofiler -- node app.js
```

### Performance Monitoring Code
```javascript
const performanceHooks = require('perf_hooks');

// Measure function execution time
function measureTime(fn, name) {
  return async (...args) => {
    const start = performanceHooks.performance.now();
    const result = await fn(...args);
    const end = performanceHooks.performance.now();
    
    console.log(`${name} took ${(end - start).toFixed(2)}ms`);
    return result;
  };
}

// Usage
const optimizedFunction = measureTime(originalFunction, 'Database Query');
```

## Database Optimization

### Connection Pooling
```javascript
// Bad: Creating new connections
const mysql = require('mysql2');

app.get('/users', async (req, res) => {
  const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'password',
    database: 'mydb'
  });
  
  const users = await connection.execute('SELECT * FROM users');
  connection.end(); // Expensive operation
  res.json(users);
});

// Good: Using connection pool
const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'password',
  database: 'mydb',
  connectionLimit: 10,
  acquireTimeout: 60000,
  timeout: 60000
});

app.get('/users', async (req, res) => {
  const [users] = await pool.execute('SELECT * FROM users');
  res.json(users);
});
```

### Query Optimization
```javascript
// Bad: N+1 query problem
async function getUsersWithPosts() {
  const users = await User.findAll();
  
  for (let user of users) {
    user.posts = await Post.findAll({ where: { userId: user.id } });
  }
  
  return users;
}

// Good: Single query with joins
async function getUsersWithPostsOptimized() {
  return await User.findAll({
    include: [{
      model: Post,
      as: 'posts'
    }]
  });
}

// Better: Pagination for large datasets
async function getUsersWithPostsPaginated(page = 1, limit = 20) {
  const offset = (page - 1) * limit;
  
  return await User.findAndCountAll({
    include: [{ model: Post, as: 'posts' }],
    limit,
    offset,
    order: [['createdAt', 'DESC']]
  });
}
```

## Caching Strategies

### Memory Caching with Node-Cache
```javascript
const NodeCache = require('node-cache');
const cache = new NodeCache({ stdTTL: 600 }); // 10 minutes TTL

async function getCachedUser(userId) {
  const cacheKey = `user:${userId}`;
  
  // Try cache first
  let user = cache.get(cacheKey);
  if (user) {
    console.log('Cache hit');
    return user;
  }
  
  // Fetch from database
  user = await User.findById(userId);
  
  // Store in cache
  cache.set(cacheKey, user);
  console.log('Cache miss - stored in cache');
  
  return user;
}
```

### Redis for Distributed Caching
```javascript
const redis = require('redis');
const client = redis.createClient();

class CacheService {
  static async get(key) {
    try {
      const data = await client.get(key);
      return data ? JSON.parse(data) : null;
    } catch (error) {
      console.error('Cache get error:', error);
      return null;
    }
  }
  
  static async set(key, data, expiration = 3600) {
    try {
      await client.setEx(key, expiration, JSON.stringify(data));
    } catch (error) {
      console.error('Cache set error:', error);
    }
  }
  
  static async invalidate(pattern) {
    try {
      const keys = await client.keys(pattern);
      if (keys.length > 0) {
        await client.del(keys);
      }
    } catch (error) {
      console.error('Cache invalidation error:', error);
    }
  }
}

// Usage in route handler
app.get('/products/:category', async (req, res) => {
  const cacheKey = `products:${req.params.category}`;
  
  let products = await CacheService.get(cacheKey);
  if (!products) {
    products = await Product.findByCategory(req.params.category);
    await CacheService.set(cacheKey, products, 1800); // 30 minutes
  }
  
  res.json(products);
});
```

## Memory Management

### Identifying Memory Leaks
```javascript
// Monitor memory usage
function logMemoryUsage() {
  const used = process.memoryUsage();
  console.log({
    rss: `${Math.round(used.rss / 1024 / 1024 * 100) / 100} MB`,
    heapTotal: `${Math.round(used.heapTotal / 1024 / 1024 * 100) / 100} MB`,
    heapUsed: `${Math.round(used.heapUsed / 1024 / 1024 * 100) / 100} MB`,
    external: `${Math.round(used.external / 1024 / 1024 * 100) / 100} MB`
  });
}

// Run every 30 seconds
setInterval(logMemoryUsage, 30000);
```

### Common Memory Leak Patterns
```javascript
// Bad: Global variables that grow indefinitely
let globalCache = {};

function cacheData(key, data) {
  globalCache[key] = data; // Never cleaned up!
}

// Good: Bounded cache with TTL
const LRU = require('lru-cache');
const cache = new LRU({
  max: 1000, // Maximum 1000 items
  maxAge: 1000 * 60 * 10 // 10 minutes TTL
});

function cacheData(key, data) {
  cache.set(key, data);
}

// Bad: Event listeners not removed
class DataProcessor {
  constructor() {
    process.on('data', this.handleData); // Leak!
  }
  
  handleData(data) {
    // Process data
  }
}

// Good: Proper cleanup
class DataProcessor {
  constructor() {
    this.handleData = this.handleData.bind(this);
    process.on('data', this.handleData);
  }
  
  destroy() {
    process.removeListener('data', this.handleData);
  }
  
  handleData(data) {
    // Process data
  }
}
```

## Asynchronous Optimization

### Parallel Processing
```javascript
// Bad: Sequential processing
async function processUsersBad(userIds) {
  const results = [];
  
  for (const id of userIds) {
    const user = await fetchUser(id);
    const processed = await processUser(user);
    results.push(processed);
  }
  
  return results;
}

// Good: Parallel processing
async function processUsersGood(userIds) {
  const userPromises = userIds.map(id => fetchUser(id));
  const users = await Promise.all(userPromises);
  
  const processPromises = users.map(user => processUser(user));
  return await Promise.all(processPromises);
}

// Better: Controlled concurrency
const pLimit = require('p-limit');
const limit = pLimit(5); // Max 5 concurrent operations

async function processUsersControlled(userIds) {
  const promises = userIds.map(id => 
    limit(() => fetchAndProcessUser(id))
  );
  
  return await Promise.all(promises);
}
```

### Stream Processing for Large Data
```javascript
const fs = require('fs');
const { Transform } = require('stream');

// Bad: Loading entire file into memory
async function processLargeFileBad(filename) {
  const data = fs.readFileSync(filename, 'utf8'); // Loads entire file
  const lines = data.split('\n');
  
  const results = [];
  for (const line of lines) {
    results.push(processLine(line));
  }
  
  return results;
}

// Good: Stream processing
function processLargeFileGood(filename) {
  return new Promise((resolve, reject) => {
    const results = [];
    let lineBuffer = '';
    
    const processStream = new Transform({
      transform(chunk, encoding, callback) {
        lineBuffer += chunk.toString();
        const lines = lineBuffer.split('\n');
        
        // Process all complete lines
        for (let i = 0; i < lines.length - 1; i++) {
          const processed = processLine(lines[i]);
          results.push(processed);
        }
        
        // Keep incomplete line in buffer
        lineBuffer = lines[lines.length - 1];
        callback();
      },
      
      flush(callback) {
        if (lineBuffer) {
          results.push(processLine(lineBuffer));
        }
        callback();
      }
    });
    
    fs.createReadStream(filename)
      .pipe(processStream)
      .on('finish', () => resolve(results))
      .on('error', reject);
  });
}
```

## HTTP and API Optimization

### Response Compression
```javascript
const compression = require('compression');
const express = require('express');
const app = express();

// Enable gzip compression
app.use(compression({
  level: 6, // Compression level 1-9
  threshold: 1024, // Only compress responses > 1KB
  filter: (req, res) => {
    // Don't compress already compressed files
    if (req.headers['x-no-compression']) {
      return false;
    }
    return compression.filter(req, res);
  }
}));
```

### HTTP/2 and Keep-Alive
```javascript
const http2 = require('http2');
const fs = require('fs');

// HTTP/2 server with SSL
const server = http2.createSecureServer({
  key: fs.readFileSync('private-key.pem'),
  cert: fs.readFileSync('certificate.pem')
});

server.on('stream', (stream, headers) => {
  const path = headers[':path'];
  
  // Server push for critical resources
  if (path === '/') {
    stream.pushStream({ ':path': '/styles.css' }, (err, pushStream) => {
      if (!err) {
        pushStream.respondWithFile('public/styles.css');
      }
    });
  }
  
  stream.respond({ ':status': 200 });
  stream.end('<html>...</html>');
});
```

### Request Batching
```javascript
// API endpoint for batch operations
app.post('/api/batch', async (req, res) => {
  const { operations } = req.body;
  
  try {
    // Process operations in parallel with controlled concurrency
    const limit = pLimit(10);
    const results = await Promise.allSettled(
      operations.map(op => limit(() => processOperation(op)))
    );
    
    const response = results.map((result, index) => ({
      id: operations[index].id,
      success: result.status === 'fulfilled',
      data: result.status === 'fulfilled' ? result.value : null,
      error: result.status === 'rejected' ? result.reason.message : null
    }));
    
    res.json({ results: response });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

## Cluster and Worker Processes

### Using Node.js Cluster Module
```javascript
const cluster = require('cluster');
const numCPUs = require('os').cpus().length;

if (cluster.isMaster) {
  console.log(`Master ${process.pid} is running`);
  
  // Fork workers
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }
  
  cluster.on('exit', (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died`);
    cluster.fork(); // Restart dead workers
  });
  
} else {
  // Worker process
  require('./app.js');
  console.log(`Worker ${process.pid} started`);
}
```

### PM2 for Production
```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'api-server',
    script: 'app.js',
    instances: 'max', // Use all CPU cores
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'production',
      PORT: 3000
    },
    max_memory_restart: '1G',
    node_args: '--max-old-space-size=1024'
  }]
};
```

## Performance Testing

### Load Testing with Artillery
```yaml
# artillery-config.yml
config:
  target: 'http://localhost:3000'
  phases:
    - duration: 60
      arrivalRate: 10
    - duration: 120
      arrivalRate: 50
    - duration: 60
      arrivalRate: 100
  
scenarios:
    - name: "API Load Test"
      requests:
        - get:
            url: "/api/users"
        - get:
            url: "/api/products"
        - post:
            url: "/api/orders"
            json:
              userId: 123
              productId: 456
```

### Benchmarking Code
```javascript
const Benchmark = require('benchmark');

const suite = new Benchmark.Suite;

// Add tests
suite
  .add('Array.forEach', function() {
    const arr = [1, 2, 3, 4, 5];
    arr.forEach(x => x * 2);
  })
  .add('for loop', function() {
    const arr = [1, 2, 3, 4, 5];
    for (let i = 0; i < arr.length; i++) {
      arr[i] * 2;
    }
  })
  .add('for...of', function() {
    const arr = [1, 2, 3, 4, 5];
    for (const x of arr) {
      x * 2;
    }
  })
  .on('cycle', function(event) {
    console.log(String(event.target));
  })
  .on('complete', function() {
    console.log('Fastest is ' + this.filter('fastest').map('name'));
  })
  .run({ 'async': true });
```

## Production Optimization Checklist

### Environment Configuration
```javascript
// Production environment variables
process.env.NODE_ENV = 'production';
process.env.UV_THREADPOOL_SIZE = 16; // Increase thread pool

// Optimize V8 flags for production
node --max-old-space-size=4096 \
     --optimize-for-size \
     --gc-interval=100 \
     app.js
```

### Security and Performance Headers
```javascript
const helmet = require('helmet');

app.use(helmet({
  hsts: { maxAge: 31536000 },
  noCache: false // Allow caching for performance
}));

// Performance monitoring
app.use((req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(`${req.method} ${req.path} - ${duration}ms`);
  });
  
  next();
});
```

### Error Handling and Graceful Shutdown
```javascript
// Graceful shutdown
process.on('SIGTERM', gracefulShutdown);
process.on('SIGINT', gracefulShutdown);

async function gracefulShutdown(signal) {
  console.log(`Received ${signal}. Starting graceful shutdown...`);
  
  // Stop accepting new connections
  server.close(async () => {
    console.log('HTTP server closed');
    
    // Close database connections
    await db.close();
    
    // Close Redis connection
    await redis.quit();
    
    console.log('Graceful shutdown complete');
    process.exit(0);
  });
  
  // Force shutdown after 30 seconds
  setTimeout(() => {
    console.log('Forced shutdown');
    process.exit(1);
  }, 30000);
}
```

## Key Takeaways

1. **Profile first, optimize second** - Measure before making changes
2. **Database queries** are usually the biggest bottleneck
3. **Caching strategy** can provide massive performance gains
4. **Memory leaks** will kill your application over time
5. **Async patterns** properly used prevent blocking
6. **Monitoring** in production is essential for maintaining performance

Remember: Premature optimization is the root of all evil, but understanding these patterns will help you write performant code from the start.