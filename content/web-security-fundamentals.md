Title: Web Security Fundamentals Every Developer Should Know
Date: 2025-06-22 11:20
Tags: security, web-development, cybersecurity, best-practices
Author: Suhail
Summary: Essential web security concepts and practical implementation techniques to protect your applications from common vulnerabilities.

Security isn't optional in 2025. Here are the fundamental concepts every web developer needs to understand and implement.

## The OWASP Top 10 Explained

### 1. Injection Attacks

#### SQL Injection
```javascript
// Vulnerable code
app.get('/users', (req, res) => {
  const query = `SELECT * FROM users WHERE id = ${req.query.id}`;
  db.query(query, (err, results) => {
    res.json(results);
  });
});

// Attack: /users?id=1 OR 1=1 -- (returns all users)
```

```javascript
// Secure implementation
app.get('/users', async (req, res) => {
  try {
    const query = 'SELECT * FROM users WHERE id = ?';
    const results = await db.query(query, [req.query.id]);
    res.json(results);
  } catch (error) {
    res.status(500).json({ error: 'Database error' });
  }
});
```

#### NoSQL Injection
```javascript
// Vulnerable MongoDB query
app.post('/login', (req, res) => {
  const { username, password } = req.body;
  
  // Attack payload: {"username": {"$ne": null}, "password": {"$ne": null}}
  User.findOne({ username, password }, (err, user) => {
    if (user) {
      res.json({ success: true });
    } else {
      res.json({ success: false });
    }
  });
});

// Secure implementation
app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  
  // Validate input types
  if (typeof username !== 'string' || typeof password !== 'string') {
    return res.status(400).json({ error: 'Invalid input' });
  }
  
  try {
    const user = await User.findOne({ 
      username: username,
      password: await hashPassword(password)
    });
    
    if (user) {
      const token = generateJWT(user.id);
      res.json({ success: true, token });
    } else {
      res.status(401).json({ error: 'Invalid credentials' });
    }
  } catch (error) {
    res.status(500).json({ error: 'Server error' });
  }
});
```

### 2. Cross-Site Scripting (XSS)

#### Reflected XSS
```html
<!-- Vulnerable search page -->
<p>You searched for: <%= request.query.search %></p>

<!-- Attack URL: /search?search=<script>alert('XSS')</script> -->
```

```html
<!-- Secure implementation with escaping -->
<p>You searched for: <%= escapeHtml(request.query.search) %></p>
```

#### Stored XSS
```javascript
// Vulnerable comment system
app.post('/comments', (req, res) => {
  const comment = {
    text: req.body.text, // Stored without sanitization
    userId: req.user.id,
    createdAt: new Date()
  };
  
  Comments.create(comment);
  res.json({ success: true });
});

// Secure implementation
const DOMPurify = require('dompurify');
const { JSDOM } = require('jsdom');

app.post('/comments', (req, res) => {
  const window = new JSDOM('').window;
  const purify = DOMPurify(window);
  
  const comment = {
    text: purify.sanitize(req.body.text), // Sanitized content
    userId: req.user.id,
    createdAt: new Date()
  };
  
  Comments.create(comment);
  res.json({ success: true });
});
```

#### Content Security Policy (CSP)
```javascript
// Implement CSP headers
app.use((req, res, next) => {
  res.setHeader('Content-Security-Policy', 
    "default-src 'self'; " +
    "script-src 'self' 'unsafe-inline' https://trusted-cdn.com; " +
    "style-src 'self' 'unsafe-inline'; " +
    "img-src 'self' data: https:; " +
    "font-src 'self' https://fonts.gstatic.com; " +
    "connect-src 'self' https://api.example.com"
  );
  next();
});
```

### 3. Cross-Site Request Forgery (CSRF)

```javascript
// Vulnerable endpoint
app.post('/transfer', authenticateUser, (req, res) => {
  const { amount, toAccount } = req.body;
  
  // Process transfer without CSRF protection
  bankService.transfer(req.user.id, toAccount, amount);
  res.json({ success: true });
});

// Attack: Hidden form on malicious site
// <form action="https://yourbank.com/transfer" method="POST">
//   <input type="hidden" name="amount" value="10000">
//   <input type="hidden" name="toAccount" value="attacker-account">
// </form>
```

```javascript
// Secure implementation with CSRF tokens
const csrf = require('csurf');
const csrfProtection = csrf({ cookie: true });

app.use(csrfProtection);

app.get('/transfer-form', (req, res) => {
  res.render('transfer', { csrfToken: req.csrfToken() });
});

app.post('/transfer', authenticateUser, (req, res) => {
  const { amount, toAccount } = req.body;
  
  // CSRF token automatically validated by middleware
  bankService.transfer(req.user.id, toAccount, amount);
  res.json({ success: true });
});
```

## Authentication and Authorization

### Secure Password Handling
```javascript
const bcrypt = require('bcrypt');
const saltRounds = 12;

// Registration
app.post('/register', async (req, res) => {
  const { email, password } = req.body;
  
  // Password strength validation
  if (!isStrongPassword(password)) {
    return res.status(400).json({
      error: 'Password must be at least 8 characters with uppercase, lowercase, number, and special character'
    });
  }
  
  try {
    const hashedPassword = await bcrypt.hash(password, saltRounds);
    const user = await User.create({ email, password: hashedPassword });
    res.json({ success: true, userId: user.id });
  } catch (error) {
    res.status(500).json({ error: 'Registration failed' });
  }
});

// Login with rate limiting
const rateLimit = require('express-rate-limit');

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // Limit each IP to 5 requests per windowMs
  message: 'Too many login attempts, please try again later',
  standardHeaders: true,
  legacyHeaders: false,
});

app.post('/login', loginLimiter, async (req, res) => {
  const { email, password } = req.body;
  
  try {
    const user = await User.findOne({ email });
    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    const validPassword = await bcrypt.compare(password, user.password);
    if (!validPassword) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    const token = generateJWT(user.id);
    res.json({ success: true, token });
  } catch (error) {
    res.status(500).json({ error: 'Login failed' });
  }
});

function isStrongPassword(password) {
  const minLength = 8;
  const hasUpperCase = /[A-Z]/.test(password);
  const hasLowerCase = /[a-z]/.test(password);
  const hasNumbers = /\d/.test(password);
  const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
  
  return password.length >= minLength && 
         hasUpperCase && 
         hasLowerCase && 
         hasNumbers && 
         hasSpecialChar;
}
```

### JWT Security Best Practices
```javascript
const jwt = require('jsonwebtoken');
const crypto = require('crypto');

// Secure JWT configuration
const JWT_SECRET = process.env.JWT_SECRET; // Strong, random secret
const JWT_REFRESH_SECRET = process.env.JWT_REFRESH_SECRET;

function generateTokens(userId) {
  const payload = { 
    userId, 
    type: 'access',
    iat: Math.floor(Date.now() / 1000)
  };
  
  const accessToken = jwt.sign(payload, JWT_SECRET, { 
    expiresIn: '15m',
    algorithm: 'HS256'
  });
  
  const refreshToken = jwt.sign(
    { userId, type: 'refresh' }, 
    JWT_REFRESH_SECRET, 
    { expiresIn: '7d' }
  );
  
  return { accessToken, refreshToken };
}

function verifyToken(token, secret = JWT_SECRET) {
  try {
    return jwt.verify(token, secret);
  } catch (error) {
    if (error.name === 'TokenExpiredError') {
      throw new Error('Token expired');
    } else if (error.name === 'JsonWebTokenError') {
      throw new Error('Invalid token');
    }
    throw error;
  }
}

// Token refresh endpoint
app.post('/refresh', async (req, res) => {
  const { refreshToken } = req.body;
  
  try {
    const decoded = verifyToken(refreshToken, JWT_REFRESH_SECRET);
    
    if (decoded.type !== 'refresh') {
      return res.status(401).json({ error: 'Invalid token type' });
    }
    
    // Check if refresh token is still valid in database
    const isValidRefreshToken = await TokenService.validateRefreshToken(
      decoded.userId, 
      refreshToken
    );
    
    if (!isValidRefreshToken) {
      return res.status(401).json({ error: 'Invalid refresh token' });
    }
    
    const tokens = generateTokens(decoded.userId);
    res.json(tokens);
  } catch (error) {
    res.status(401).json({ error: error.message });
  }
});
```

## Secure HTTP Headers

```javascript
const helmet = require('helmet');

app.use(helmet({
  // Prevent XSS attacks
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
      fontSrc: ["'self'", "https://fonts.gstatic.com"],
      imgSrc: ["'self'", "data:", "https:"],
      scriptSrc: ["'self'"],
    },
  },
  
  // Prevent clickjacking
  frameguard: { action: 'deny' },
  
  // Force HTTPS
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  },
  
  // Prevent MIME type sniffing
  noSniff: true,
  
  // Prevent XSS
  xssFilter: true,
  
  // Hide server information
  hidePoweredBy: true,
  
  // Referrer policy
  referrerPolicy: { policy: 'strict-origin-when-cross-origin' }
}));

// Additional security headers
app.use((req, res, next) => {
  // Prevent caching of sensitive data
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, private');
  
  // Feature policy
  res.setHeader('Permissions-Policy', 
    'geolocation=(), microphone=(), camera=()');
  
  next();
});
```

## Input Validation and Sanitization

```javascript
const Joi = require('joi');
const validator = require('validator');

// Comprehensive validation schema
const userRegistrationSchema = Joi.object({
  email: Joi.string()
    .email({ minDomainSegments: 2 })
    .required()
    .custom((value, helpers) => {
      if (!validator.isEmail(value)) {
        return helpers.error('any.invalid');
      }
      return value;
    }),
  
  password: Joi.string()
    .min(8)
    .max(128)
    .pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/)
    .required()
    .messages({
      'string.pattern.base': 'Password must contain uppercase, lowercase, number, and special character'
    }),
  
  firstName: Joi.string()
    .min(1)
    .max(50)
    .pattern(/^[a-zA-Z\s]+$/)
    .required(),
  
  lastName: Joi.string()
    .min(1)
    .max(50)
    .pattern(/^[a-zA-Z\s]+$/)
    .required(),
  
  age: Joi.number()
    .integer()
    .min(13)
    .max(120)
    .required(),
  
  phoneNumber: Joi.string()
    .pattern(/^\+?[\d\s\-\(\)]+$/)
    .optional()
});

// Validation middleware
function validateInput(schema) {
  return (req, res, next) => {
    const { error, value } = schema.validate(req.body, {
      abortEarly: false,
      stripUnknown: true
    });
    
    if (error) {
      const errors = error.details.map(detail => ({
        field: detail.path.join('.'),
        message: detail.message
      }));
      
      return res.status(400).json({
        error: 'Validation failed',
        details: errors
      });
    }
    
    req.validatedData = value;
    next();
  };
}

// Usage
app.post('/register', validateInput(userRegistrationSchema), async (req, res) => {
  const userData = req.validatedData;
  // userData is now validated and sanitized
  // Proceed with registration
});
```

## File Upload Security

```javascript
const multer = require('multer');
const path = require('path');
const crypto = require('crypto');

// Secure file upload configuration
const upload = multer({
  storage: multer.diskStorage({
    destination: (req, file, cb) => {
      cb(null, 'uploads/');
    },
    filename: (req, file, cb) => {
      // Generate secure filename
      const uniqueSuffix = crypto.randomBytes(16).toString('hex');
      const ext = path.extname(file.originalname);
      cb(null, `${uniqueSuffix}${ext}`);
    }
  }),
  
  fileFilter: (req, file, cb) => {
    // Whitelist allowed file types
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf'];
    
    if (allowedTypes.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error('Invalid file type'), false);
    }
  },
  
  limits: {
    fileSize: 5 * 1024 * 1024, // 5MB limit
    files: 1 // Single file upload
  }
});

app.post('/upload', upload.single('file'), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }
  
  try {
    // Additional file validation
    const fileInfo = await validateFile(req.file.path);
    
    if (!fileInfo.isValid) {
      // Delete invalid file
      fs.unlinkSync(req.file.path);
      return res.status(400).json({ error: 'Invalid file content' });
    }
    
    // Scan for malware (optional, using external service)
    const scanResult = await scanForMalware(req.file.path);
    if (!scanResult.clean) {
      fs.unlinkSync(req.file.path);
      return res.status(400).json({ error: 'File failed security scan' });
    }
    
    res.json({
      success: true,
      filename: req.file.filename,
      size: req.file.size
    });
  } catch (error) {
    res.status(500).json({ error: 'File processing failed' });
  }
});

async function validateFile(filePath) {
  // Check file headers match extension
  const fileType = await import('file-type');
  const type = await fileType.fileTypeFromFile(filePath);
  
  return {
    isValid: type !== undefined,
    detectedType: type?.mime
  };
}
```

## API Security

### Rate Limiting
```javascript
const rateLimit = require('express-rate-limit');
const RedisStore = require('rate-limit-redis');
const Redis = require('redis');

const redisClient = Redis.createClient();

// Different rate limits for different endpoints
const createApiLimiter = (windowMs, max, message) => {
  return rateLimit({
    store: new RedisStore({
      sendCommand: (...args) => redisClient.sendCommand(args),
    }),
    windowMs,
    max,
    message: { error: message },
    standardHeaders: true,
    legacyHeaders: false,
    keyGenerator: (req) => {
      // Use API key or IP address
      return req.headers['x-api-key'] || req.ip;
    }
  });
};

// Apply different limits
app.use('/api/auth', createApiLimiter(15 * 60 * 1000, 5, 'Too many auth attempts'));
app.use('/api/upload', createApiLimiter(60 * 60 * 1000, 10, 'Upload limit exceeded'));
app.use('/api/', createApiLimiter(15 * 60 * 1000, 100, 'API rate limit exceeded'));
```

### API Key Management
```javascript
const crypto = require('crypto');

class ApiKeyService {
  static generateApiKey() {
    return crypto.randomBytes(32).toString('hex');
  }
  
  static async hashApiKey(apiKey) {
    const salt = crypto.randomBytes(16).toString('hex');
    const hash = crypto.pbkdf2Sync(apiKey, salt, 10000, 64, 'sha256').toString('hex');
    return { hash, salt };
  }
  
  static async verifyApiKey(apiKey, hash, salt) {
    const computedHash = crypto.pbkdf2Sync(apiKey, salt, 10000, 64, 'sha256').toString('hex');
    return crypto.timingSafeEqual(Buffer.from(hash), Buffer.from(computedHash));
  }
}

// API key authentication middleware
async function authenticateApiKey(req, res, next) {
  const apiKey = req.headers['x-api-key'];
  
  if (!apiKey) {
    return res.status(401).json({ error: 'API key required' });
  }
  
  try {
    const keyRecord = await ApiKey.findByKeyPrefix(apiKey.substring(0, 8));
    
    if (!keyRecord || !keyRecord.isActive) {
      return res.status(401).json({ error: 'Invalid API key' });
    }
    
    const isValid = await ApiKeyService.verifyApiKey(
      apiKey, 
      keyRecord.hash, 
      keyRecord.salt
    );
    
    if (!isValid) {
      return res.status(401).json({ error: 'Invalid API key' });
    }
    
    // Update last used timestamp
    await ApiKey.updateLastUsed(keyRecord.id);
    
    req.apiKey = keyRecord;
    next();
  } catch (error) {
    res.status(500).json({ error: 'Authentication failed' });
  }
}
```

## Security Monitoring and Logging

```javascript
const winston = require('winston');

// Security-focused logging
const securityLogger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'logs/security.log' }),
    new winston.transports.Console()
  ]
});

// Security event logging middleware
function logSecurityEvent(eventType) {
  return (req, res, next) => {
    const logData = {
      event: eventType,
      ip: req.ip,
      userAgent: req.get('User-Agent'),
      timestamp: new Date().toISOString(),
      path: req.path,
      method: req.method,
      userId: req.user?.id || 'anonymous'
    };
    
    securityLogger.info('Security event', logData);
    next();
  };
}

// Usage
app.post('/login', logSecurityEvent('LOGIN_ATTEMPT'), loginHandler);
app.post('/admin/*', logSecurityEvent('ADMIN_ACCESS'), adminHandler);
app.use('/api/sensitive', logSecurityEvent('SENSITIVE_DATA_ACCESS'));

// Failed authentication logging
app.use((err, req, res, next) => {
  if (err.name === 'UnauthorizedError') {
    securityLogger.warn('Unauthorized access attempt', {
      ip: req.ip,
      path: req.path,
      userAgent: req.get('User-Agent'),
      error: err.message
    });
  }
  next(err);
});
```

## Security Testing

```javascript
// Security-focused unit tests
const request = require('supertest');
const app = require('../app');

describe('Security Tests', () => {
  describe('XSS Protection', () => {
    test('should sanitize script tags in comments', async () => {
      const maliciousComment = '<script>alert("XSS")</script>Hello';
      
      const response = await request(app)
        .post('/api/comments')
        .set('Authorization', `Bearer ${validToken}`)
        .send({ text: maliciousComment });
      
      expect(response.status).toBe(201);
      expect(response.body.comment.text).not.toContain('<script>');
      expect(response.body.comment.text).toContain('Hello');
    });
  });
  
  describe('SQL Injection Protection', () => {
    test('should not be vulnerable to SQL injection', async () => {
      const maliciousId = "1'; DROP TABLE users; --";
      
      const response = await request(app)
        .get(`/api/users/${maliciousId}`)
        .set('Authorization', `Bearer ${validToken}`);
      
      expect(response.status).toBe(400);
      expect(response.body.error).toContain('Invalid input');
    });
  });
  
  describe('Rate Limiting', () => {
    test('should enforce rate limits', async () => {
      // Make multiple requests rapidly
      const promises = Array(10).fill().map(() =>
        request(app).post('/api/auth/login').send({
          email: 'test@example.com',
          password: 'wrongpassword'
        })
      );
      
      const responses = await Promise.all(promises);
      const tooManyRequests = responses.some(res => res.status === 429);
      expect(tooManyRequests).toBe(true);
    });
  });
});
```

## Security Checklist

### Development Phase
- [ ] Input validation on all endpoints
- [ ] Output encoding/escaping
- [ ] Parameterized queries for database access
- [ ] Secure authentication implementation
- [ ] Proper error handling (no information leakage)
- [ ] Security headers implementation
- [ ] File upload restrictions
- [ ] Rate limiting configuration

### Deployment Phase
- [ ] HTTPS enforcement
- [ ] Secure cookie configuration
- [ ] Environment variables for secrets
- [ ] Security monitoring setup
- [ ] Log analysis configuration
- [ ] Backup and recovery procedures
- [ ] Dependency vulnerability scanning

### Ongoing Maintenance
- [ ] Regular security updates
- [ ] Penetration testing
- [ ] Security audit logs review
- [ ] Incident response plan
- [ ] Team security training

Remember: Security is not a one-time implementation but an ongoing process. Stay updated with the latest security threats and best practices, and always assume that your application will be targeted by attackers.